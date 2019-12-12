# -*- coding:utf-8 -*-
'''
@project: '__dbreport__.py'
@modules: report.cli
@description:
    
@author: abelit
@email: ychenid@live.com
@created:Mar 14, 2018

@licence: GPL
'''


import sys, getopt, os
import argparse
import time

from utils.rundaemon import Daemon
from config import settings
from utils import rptlogging

logger = rptlogging.rptlogger(settings.ReportSetting().getPackageSetting()['logfile'])


# Daemon name. It's only used in messages.
DAEMON_NAME = 'DBReport Service'
# Cleanstop wait time before to kill the process.
DAEMON_STOP_TIMEOUT = 10
# Daemon pid file.
PIDFILE = '/tmp/dbreport_service.pid'
# Deamon run file. "stop" request deletes this file to inform the process and
# waits DAEMON_STOP_TIMEOUT seconds before to send SIGTERM. The process has a
# change to stop cleanly if it's written appropriately.
RUNFILE = '/tmp/dbreport_service.run'
# Sleep time.
LOOP_SLEEP = 300
# Debug mode.
DEBUG = 0

class DBDaemon(Daemon):
    def __init__(self, conf, **kwargs):
        Daemon.__init__(self, **kwargs) #继承父类构造方法

        self.conf = conf #传入方法
          
    def run(self):
        import datetime,calendar
        '''
        Daemon start to run here.
        '''
        
        icount = 0
        jcount = 0
        days = settings.ReportSetting().getReportSetting()['report_interval']
        # Run while there is no stop request.
        while os.path.exists(self.runfile):
            try:
                if icount==0 and calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1] == datetime.datetime.now().day:
                    genPDF(mode=self.conf['mode'], conf=self.conf['conf'], filename=self.conf['filename'])
                    icount += 1
                    
                genMonitor(mode='alert')
                
                if jcount == 0 and datetime.datetime.now().hour in days:
                    genMonitor(conf=None, mode='daily')
                    jcount += 1
                           
            except Exception as err:
                if self.debug:
                    raise
                else:
                    sys.stderr.write('%s\n' % (err))
            finally:
                #print("hello")
                if calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1] != datetime.datetime.now().day:
                    icount = 0
                  
                if datetime.datetime.now().hour not in days:  
                    jcount = 0
                    
                    
                self.wait(timeout=self.looptimeout)
         
         
class DBDaemonNT(object):
    def __init__(self,conf):
        self.conf = conf
        
    def run(self):
        import datetime,calendar
        '''
        Daemon start to run here.
        '''
        
        icount = 0
        jcount = 0
        days = settings.ReportSetting().getReportSetting()['report_interval']
        # Run while there is no stop request.
        while True:
            try:
                if icount==0 and calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1] == datetime.datetime.now().day:
                    genPDF(mode=self.conf['mode'], conf=self.conf['conf'], filename=self.conf['filename'])
                    icount += 1
                    
                genMonitor(mode='alert')
                
                if jcount == 0 and datetime.datetime.now().hour in days:
                    genMonitor(conf=None, mode='daily')
                    jcount += 1
                           
            except Exception as err:
                    sys.stderr.write('%s\n' % (err))
            finally:
                #print("hello")
                if calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1] != datetime.datetime.now().day:
                    icount = 0
                  
                if datetime.datetime.now().hour not in days:  
                    jcount = 0
                
            time.sleep(LOOP_SLEEP)

def genMonitor(conf=None,mode='alert'): 
    from report import monitoring  
    
    from utils import wechat, mail

    rptsettings = settings.ReportSetting(conf).getReportSetting()

    # 邮件设置信息
    mail_host = rptsettings['mail_host']
    mail_user = rptsettings['mail_user']
    mail_pass = rptsettings['mail_pass']
    mail_sender = rptsettings['mail_sender']
    mail_receiver = rptsettings['mail_receiver']
    mail_subject = '数据库监控'
    mail_content = ''


    # 微信企业号文件共享
    corpid = rptsettings['corpid']
    corpsecret = rptsettings['corpsecret']
#     token = wechat.get_token(corpid, corpsecret)
    tag = rptsettings['tag']
    touser = rptsettings['touser']
    toparty = rptsettings['toparty']
    agentid = rptsettings['agentid']
    subject = rptsettings['subject']
    content = ''

    content_error = ''

    status = 0

    om = monitoring.OracleMonitor().test_connect_oracle()
    for oralist in om:
        content = content + '***********************\n' + '主机名：' + oralist['host'] + '\n' + '实例名称：' +  oralist['instance'][0] + '\n' + '实例状态：' +oralist['instance'][3] + '\n' + '数据库名：' + oralist['database'][0] + '\n' + '数据状态：' +  oralist['database'][2] + '\n' + '可连接性：' +  str(oralist['connectability']) + '\n'
        if oralist['instance'][3] != 'OPEN' or oralist['database'][2] != 'READ WRITE' or oralist['connectability'] != 1:
            status = 1
            content_error = content_error + '***********************\n' + '主机名：' + oralist['host'] + '\n' + '实例名称：' +  oralist['instance'][0] + '\n' + '实例状态：' +oralist['instance'][3] + '\n' + '数据库名：' + oralist['database'][0] + '\n' + '数据状态：' +  oralist['database'][2] + '\n' + '可连接性：' +  str(oralist['connectability']) + '\n'
    
    # 发送信息及附件
    try:
        if mode == 'alert' and status == 1:
            wechat.send_msg(corpid, corpsecret, tag, touser, toparty, agentid, subject, content_error)   
            
        if mode == 'daily':
            wechat.send_msg(corpid, corpsecret, tag, touser, toparty, agentid, subject, content)
    except Exception as e:
        print(e)
        print('微信消息及附件发送失败，您可能现在无法连接到互联网！')


    try:
        if mode == 'alert' and status == 1:
            mail.sendMail(mail_host,mail_user,mail_pass,mail_sender,mail_receiver, mail_subject, content_error)
            
            
        if mode == 'daily':
            mail.sendMail(mail_host,mail_user,mail_pass,mail_sender,mail_receiver, mail_subject, content)
    except Exception as e:
        print(e)
        print('邮件消息及附件发送失败，您可能现在无法连接到互联网！')
                
    

def genPDF(mode=None,conf=None,filename=None):
    #from config import settings
    from report import oraclerpt
    from utils import wechat, mail

    rptsettings = settings.ReportSetting(conf).getReportSetting()
    
    # 附件文件
    if filename is not None:
        report_filename = filename
    else:
        report_filename = rptsettings['report_filename']

    # 邮件设置信息
    mail_host = rptsettings['mail_host']
    mail_user = rptsettings['mail_user']
    mail_pass = rptsettings['mail_pass']
    mail_sender = rptsettings['mail_sender']
    mail_receiver = rptsettings['mail_receiver']
    mail_subject = rptsettings['mail_subject']
    mail_content = rptsettings['mail_content']


    # 微信企业号文件共享
    corpid = rptsettings['corpid']
    corpsecret = rptsettings['corpsecret']
#     token = wechat.get_token(corpid, corpsecret)
    tag = rptsettings['tag']
    touser = rptsettings['touser']
    toparty = rptsettings['toparty']
    agentid = rptsettings['agentid']
    subject = rptsettings['subject']
    content = rptsettings['content']

    content_error = rptsettings['content_error']

    status = 0

    try:
        rpt = oraclerpt.OracleReport(settings.ReportSetting(conf),report_filename)
        if mode is not None:
            rpt.run(mode)
        else:
            rpt.run()
    except Exception as e:
        status = 1
        print(e)
        print('生成PDF巡检报告失败！')

    # 发送信息及附件
    try:
        if status == 1:
            wechat.send_msg(corpid, corpsecret, tag, touser, toparty, agentid, subject, content_error)
        else:
            wechat.send_msg(corpid, corpsecret, tag, touser, toparty, agentid, subject, content)
            wechat.send_file(corpid, corpsecret, tag, touser, toparty, agentid, report_filename)
    except Exception as e:
        print(e)
        print('微信消息及附件发送失败，您可能现在无法连接到互联网！')

    print(status)

    try:
        if status == 1:
            mail.sendMail(mail_host,mail_user,mail_pass,mail_sender,mail_receiver, mail_subject, content_error, report_filename)
        else: 
            mail.sendMail(mail_host,mail_user,mail_pass,mail_sender,mail_receiver, mail_subject, mail_content, report_filename)
    except Exception as e:
        print(e)
        print('邮件消息及附件发送失败，您可能现在无法连接到互联网！')
        
    
def getConfiguration(value):  
    #from config import settings
    example_conf = settings.path_settings['config'] + 'dbreport.json'  
    if value == 'configuration':
        example_conf = settings.path_settings['config'] + 'dbreport.json'
    elif value == 'example':
        example_conf = settings.path_settings['config'] + 'dbreport_example.json'
    else:
        print('Usage like --show|-s example/configuarion')
        sys.exit(0)
    f = open(file=example_conf , mode='r', encoding='utf-8')
    print(f.read())
    sys.exit(0)
    
def setConfiguration(userconf):
    #from config import settings
    
    conf = settings.path_settings['config'] + 'dbreport.json'
    f = open(file=conf , mode='r+', encoding='utf-8')
    
    tempf = open(file=userconf , mode='r', encoding='utf-8')
    content = tempf.read()
    
    f.truncate()
    f.write(content)
    f.close()
    nf = open(file=conf , mode='r+', encoding='utf-8')
    
    print('Configuration has been set, and its contents lists as belowing:')
    print(nf.read())
    
    nf.close()
    tempf.close()
    
    sys.exit(0)

def getVersion():
    #from config import settings
    __VERSION__ = settings.project_settings['version']
    
    print(__VERSION__)
    sys.exit(0)
    
def usage():
    print('DBReport: usage of this procedure.')
    print('-h | --help, get help information of dbreport.')
    print('-v | --version, get version of dbreport.')
    print('-c | --conf, assign the configuration to dbreport, eg. dbreport -c "{your path}/dbreport.json" \n or dbreport --conf="{your path}/dbreport.json"')
    print('-o | --outfile, assign the path of pdf report which is generated by dbreport.')
    print('-m | --mode, assign the content of pdf report which is generated by dbreport.')   
    print('-s | --show, {example|configuration} show the (example) settings of document.')
    print('--set-config, set configuration for oracle report pdf.')
    print('--service, {start|restart|stop|status}, to run DBReport as a background service.')
    print('Now you can use dbreport_daemon {start|restart|stop|status} based on posix system and you can use \n dbreport_daemon.bat {start|restart|install|stop|remove} based on nt system, \n to run DBReport as a background service.')
    print('Usage Example:')     
    print('dbreport')
    print('dbreport -v|--version')
    print('dbreport -o {your path}/myoracle.pdf ,---- will generate pdf to {your path}/myreport')
    print('dbreport -c {your path}/dbreport_gs.json  ,---- will generate pdf based on dbreport_gs.json settings.')
    print('dbreport -o {your path}/myoracle.pdf -c {your path}/dbreport_gs.json')
    sys.exit(0)
        
opts, args = getopt.getopt(sys.argv[1:], "hvc:o:m:s:f:",["help", "version", "mode=", "outfile=", "conf=","show=","set-config=", "service="])
optconf = {'mode':'month','conf':None, 'filename':None, 'service': None}

def reportopt(var,value):
    opts = {
        '-c': lambda value: optconf.update({'conf':value}),
        '--conf': lambda value: optconf.update({'conf':value}),
        '-o': lambda value: optconf.update({'filename':value}),
        '--outfile': lambda value: optconf.update({'filename':value}), 
        '-m': lambda value: optconf.update({'mode':value}),
        '--mode': lambda value: optconf.update({'mode':value}), 
        
        '--service': lambda value: optconf.update({'service':value}),
        
        '--set-config': lambda value: setConfiguration(value),
        '-s': lambda value: getConfiguration(value),
        '--show': lambda value: getConfiguration(value),
        '-h': lambda value: usage(), 
        '--help': lambda value: usage(), 
        '-v': lambda value: getVersion(), 
        '--version': lambda value: getVersion(),
    }[var](value) 

    return opts

def get_args():
    '''
    >>> get_args()
    ('start',)
    >>> get_args()
    ('stop',)
    '''

    try:
        parser =  argparse.ArgumentParser()
        parser.add_argument('action', help='action',
                            choices=['start', 'status', 'stop', 'restart'])
        args = parser.parse_args()

        result = (args.action, )
    except Exception as err:
        if DEBUG:
            raise
        else:
            sys.stderr.write('%s\n' % (err))

        result = (None, )

    return result 
        
def main():  
    
    if len(opts) != 0:
        for op, value in opts:
            reportopt(op,value)

    if os.name == 'posix':
        try:
            d = DBDaemon(conf=optconf,name=DAEMON_NAME, pidfile=PIDFILE, runfile=RUNFILE, looptimeout=LOOP_SLEEP,stoptimeout=DAEMON_STOP_TIMEOUT, debug=DEBUG)
            if optconf['service'] is None:
                genPDF(mode=optconf['mode'], conf=optconf['conf'], filename=optconf['filename'])
            elif optconf['service'] == 'start':
                d.start()
            elif optconf['service'] == 'stop':
                d.stop()
            elif optconf['service'] == 'status':
                d.status()
            elif optconf['service'] == 'restart':
                d.restart()
            else:
                raise NameError('Unknown Parameter for --service !')
            
            sys.exit(0)
        except Exception as err:
            if DEBUG:
                raise
            else:
                sys.stderr.write('%s\n' % err)
                logger.error(err)
            sys.exit(1)
    elif os.name == 'nt':
#         if optconf['service'] is not None:
#             logger.info("Unsupported system about this parameter.")
#             sys.exit(0)
#         genPDF(mode=optconf['mode'], conf=optconf['conf'], filename=optconf['filename'])
        d = DBDaemonNT(conf=optconf)
        if optconf['service'] is None:
            genPDF(mode=optconf['mode'], conf=optconf['conf'], filename=optconf['filename'])
        
        elif optconf['service'] == 'start':  
            d.run()
        else:
            print('Unsupport parameters')
    else:
        logger.error('Unknown Operating System?')
    
def run_daemon():
    if os.name == 'posix':
        # Get arguments.
        (action, ) = get_args()
        try:
            # Create daemon object.
            d = DBDaemon(conf=optconf,name=DAEMON_NAME, pidfile=PIDFILE, runfile=RUNFILE, looptimeout=LOOP_SLEEP,stoptimeout=DAEMON_STOP_TIMEOUT, debug=DEBUG)
            # Action requested.
            if action == 'start':
                d.start()
            elif action == 'status':
                d.status()
            elif action == 'stop':
                d.stop()
            elif action == 'restart':
                d.restart()
            else:
                raise NameError('Unknown action')
    
            sys.exit(0)
        except Exception as err:
            if DEBUG:
                raise
            else:
                sys.stderr.write('%s\n' % err)
    
            sys.exit(1)
    elif os.name == 'nt':
        #while True:
            #genPDF(mode=optconf['mode'], conf=optconf['conf'], filename=optconf['filename'])
            #time.sleep(10)
        d = DBDaemonNT(conf=optconf)
        d.run()
            
    else:
        logger.error('Unknown Operating System?')

if __name__ == '__main__':
    genMonitor(conf=None, mode='daily')
    

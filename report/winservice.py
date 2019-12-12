# -*- coding:utf-8 -*-
'''
@project: '__dbreport__.py'
@modules: report.winservice
@description:

@author: abelit
@email: ychenid@live.com
@created: Apr 2, 2018

@licence: GPL
'''

# Service running backgound based windows         
try:     
    import win32serviceutil
    import win32service
    import win32event
    import servicemanager
    import socket
    import time
    import sys
except ImportError as e:
    print(e)
    
from config import settings


# Sleep time.
LOOP_SLEEP = 300
    
    

def genMonitor(conf=None,mode='error'): 
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
        if oralist['instance'][3] != 'OPEN' and oralist['database'][2] != 'READ WRITE' and oralist['connectability'] != 1:
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


class DBReportService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'DBReportService'
    _svc_display_name_ = 'DBReportService'
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        
        socket.setdefaulttimeout(60)
        self.isAlive = True
        
    def SvcStop(self):
        self.isAlive = False
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        
    def SvcDoRun(self):
        self.isAlive = True
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, 
                              servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
        self.main()
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
        
    def main(self):
        #i = 0
        import datetime,calendar
        '''
        Daemon start to run here.
        '''
        
        icount = 0
        jcount = 0
        days = settings.ReportSetting().getReportSetting()['report_interval']
        
        while self.isAlive: 
            # Run while there is no stop request.
            try:
                if icount==0 and calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1] == datetime.datetime.now().day:
                    genPDF()
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



if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(DBReportService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(DBReportService)

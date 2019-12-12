# -*- coding:utf-8 -*-
'''
@project: '__dbreport__.py'
@modules: genReport
@description:
    
@author: abelit
@email: ychenid@live.com
@created:Mar 14, 2018

@licence: GPL
'''



import sys, getopt


def genPDF(mode=None,conf=None,filename=None):
    from config import settings
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
    from config import settings
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
    from config import settings
    
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
    from config import settings
    __VERSION__ = settings.project_settings['version']
    
    print(__VERSION__)
    sys.exit(0)
    
def usage():
    print('DBReport: usage of this procedure.')
    print('-h | --help, get help information of dbreport.')
    print('-v | --version, get version of dbreport.')
    print('-c | --conf, assign the configuration to dbreport, eg. dbreport -c "/home/oracle/dbreport.json" or dbreport --conf="/home/oracle/dbreport.json"')
    print('-o | --outfile, assign the path of pdf report which is generated by dbrepor.')
    print('-m | --mode, assign the content of pdf report which is generated by dbrepor.')   
    print('-s | --show, show the (example) settings of document.')
    print('--set-config, set configuration for oracle report pdf.')
    print('Usage Example:')     
    print('dbreport')
    print('dbreport -v|--version')
    print('dbreport -o Downloads/myreport/myoracle.pdf ,---- will generate pdf to Downloads/myreport')
    print('dbreport -c Downloads/myreport/dbreport_gs.json  ,---- will generate pdf based on dbreport_gs.json settings.')
    print('dbreport -o Downloads/myreport/myoracle.pdf -c Downloads/myreport/dbreport_gs.json')
    sys.exit(0)
        
opts, args = getopt.getopt(sys.argv[1:], "hvc:o:m:s:f:",["help", "version", "mode=", "outfile=", "conf=","show=","set-config="])
optconf = {'mode':'month','conf':None, 'filename':None}

def reportopt(var,value):
    opts = {
        '-c': lambda value: optconf.update({'conf':value}),
        '--conf': lambda value: optconf.update({'conf':value}),
        '-o': lambda value: optconf.update({'filename':value}),
        '--outfile': lambda value: optconf.update({'filename':value}), 
        '-m': lambda value: optconf.update({'mode':value}),
        '--mode': lambda value: optconf.update({'mode':value}), 
        
        '--set-config': lambda value: setConfiguration(value),
        '-s': lambda value: getConfiguration(value),
        '--show': lambda value: getConfiguration(value),
        '-h': lambda value: usage(), 
        '--help': lambda value: usage(), 
        '-v': lambda value: getVersion(), 
        '--version': lambda value: getVersion(),
    }[var](value) 

    return opts
        
def main():
    if len(opts) != 0:
        for op, value in opts:
            reportopt(op,value)

    genPDF(mode=optconf['mode'], conf=optconf['conf'], filename=optconf['filename'])

if __name__ == '__main__':
    main()
    
# -*- coding:utf-8 -*-
'''
@project: '__dbreport__.py'
@modules: config.settings
@description:

@author: abelit
@email: ychenid@live.com
@created:Feb 9, 2018

@licence: GPL
'''


import os
import sys
import json

sys.path.append('/Users/abelit/Downloads/Workspace/Code/DBReport')

from utils import filepath


project_settings = {
    # 项目信息配置
    'package': 'dev',
    'version':'3.1415',
    'name':'__dbreport__.py',
    'author':'abelit',
    'email':'ychenid@live.com',
    'description':'',
}

path_settings = {
    'root_path': filepath.get_root_path(project_settings['name']),
    'image': filepath.get_root_path(project_settings['name']) + os.sep + 'images' + os.sep,
    'log': filepath.get_root_path(project_settings['name']) + os.sep + 'logs' + os.sep,
    'font': filepath.get_root_path(project_settings['name']) + os.sep + 'fonts' + os.sep,
    'resource': filepath.get_root_path(project_settings['name']) + os.sep + 'resource' + os.sep,
    'config': filepath.get_root_path(project_settings['name']) + os.sep + 'config' + os.sep,
}


class ReportSetting:
    def __init__(self,userconf= None):
        if userconf is not None:
            self.USERCONF = userconf
        else:
            self.USERCONF = path_settings['config'] + 'dbreport.json'
            
    def getPackageSetting(self):
        
        return {
             # 软件日志设置
             'logfile': path_settings['log'] + 'dbreport.log',
             'syslogin': path_settings['log'] + 'syslogin.log'
        }
       
    def getDatabaseSetting(self):
        conf = open(self.USERCONF, encoding='utf-8')
        base_settings = json.load(conf)
        return base_settings['DATABASE']

    def getReportSetting(self):
        conf = open(self.USERCONF, encoding='utf-8')
        base_settings = json.load(conf)

        ORGANIZATION_NAME = base_settings['ORGANIZATION_NAME']
        ORGANIZATION_SHORTNAME = base_settings['ORGANIZATION_SHORTNAME']
        ORGANIZATION_OBJECT = base_settings['ORGANIZATION_OBJECT']
        DATE_DISPLAY = base_settings['DATE_DISPLAY']

        AUTHOR = base_settings['AUTHOR']
        
        REPORT_INTERVAL = base_settings['REPORT_INTERVAL']

        return {
            'report_version': project_settings['version'],
            # 服务方和客户方基本信息配置
            'report_title': ORGANIZATION_NAME,
            'report_title1': ORGANIZATION_OBJECT+'巡检报告',
            'report_title2':DATE_DISPLAY,
            'report_copy': 2,
            'cover_logo': path_settings['image'] + 'db_logo.jpg',
            'company_logo': path_settings['image'] + 'vision_logo.jpg',
            'company_name':'贵州维讯信息技术有限公司',
            'company_name_short':'贵州维讯',
            'company_name_short_en':'Vision-IT',
            'company_address':'贵阳市观山湖诚信南路绿地集团大厦',
            'company_telephone':'（0851）85835058',
            'company_website':'www.vision-it.com.cn',
            'copyright': ['''1. 本版权声明是贵州维讯信息技术有限公司关于“{0}{1}”技术文档的全部版本 (包括已有版本及未来更新版本)及与该文档全部版本有关的源代码、目标代码、相关文档资料以及任何由贵 州维讯信息技术有限公司关于“{0}{1}”维护或支持服务所提供的数据库及查询方式、数 据、资料等(以下统称:{2}数据库技术文档)做出的法律声明。'''.format(ORGANIZATION_NAME,ORGANIZATION_OBJECT,ORGANIZATION_SHORTNAME),
                          '''2. {0}数据库技术文档的著作权、商标权等知识产权属于贵州维讯信息技术有限公司及文档作者所 有， 受《中华人民共和国著作权法》、《知识产权保护条例》和相关国际版权条约、法律、法规，以及其它 知识产权法律和条约的保护。'''.format(ORGANIZATION_SHORTNAME),
                          '''3. 任何单位和个人未经贵州维讯信息技术有限公司与作者书面授权，不得以任何目的(包 括但不限于学 习、研究等非商业用途)修改、使用、复制、截取、编纂、编译、上传、下载等或以任何方式和媒介复制、转 载和传播{0}数据库技术文档的任何部分，否则将视为侵权，贵州维讯信息技术有限公司及作者保留依法追 究其法律责任的权利。'''.format(ORGANIZATION_SHORTNAME),
                          '''4. 本文档包含{0}数据重要信息，仅限于内部传播阅览，请文档使用者谨慎传播，注意保密。'''.format(ORGANIZATION_SHORTNAME), ],

            # 文档基本信息配置
            'report_filename': path_settings['resource'] + 'oracle_report.pdf',
            'report_font':'msyh',
            'content_name':'目 录',
            'content_level':3,

            # 文档作者、版本、版权信息
            'flowshape': path_settings['image'] + 'response.png',

            # 邮件信息配置
            'mail_host':'smtp.126.com',  # 发送邮件使用的邮件服务器
            'mail_user':'ychenid@126.com',  # 发送邮件使用的用户
            'mail_pass':'test',
            'mail_subject':'{0}{1}巡检报告'.format(ORGANIZATION_SHORTNAME,ORGANIZATION_OBJECT),
            'mail_content':'请注意查收！',
            'mail_sender':'ychenid@126.com',
            'mail_receiver':['948640709@qq.com', 'ychenid@163.com'],

            # 微信信息配置
            'corpid': 'wweaa126f843984b84',  # 微信企业号id
            'corpsecret': 's5u8dfFWsfH0nV0VHmhcKNUFUmmDs0ZeYJk2z-NGIFk',  # 微信企业号应用密码密钥
            'tag': '1',  # 标签
            'touser': '@all',  # 接收微信信息的用户，@all表示所有组下的成员，如果是单独指定用户，使用“ChenYing|Ableit”进行发送
            'toparty': '1',  # 部门id号
            'agentid': '1000002',  # 应用id号
            'subject': '{0}巡检报告'.format(ORGANIZATION_SHORTNAME),  # 发送文本消息的主题
            'content': '{0}巡检报告已生成，电子文档已经发送到微信企业号和您的邮箱，请查收！'.format(ORGANIZATION_SHORTNAME),  # 发送文本消息时的内容
            'content_error' : '{0}巡检报告生成失败,请查看原因！'.format(ORGANIZATION_SHORTNAME),
            'path': path_settings['log'] + 'oracle_report.pdf',  # 发送文件、语音、视频、图片等媒体文件的文件所在位置

            #author
            'author': AUTHOR,
            
            #monitoring interval
            'report_interval': REPORT_INTERVAL,
        }


if __name__ == '__main__':
    myset = ReportSetting(path_settings['config']+os.sep+'dbreport_gs.json')

    print(myset.getReportSetting())

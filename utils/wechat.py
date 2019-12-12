#! /usr/bin/env python3
# -*- coding:utf-8 -*-
'''
@project: '__dbreport__.py'
@modules: utils.wechat
@description:
    
@author: abelit
@email: ychenid@live.com
@created:Feb 7, 2018

@licence: GPL
'''
 
import requests
import json
import os

 
def get_token(corpid, corpsecret):
 
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    values = {'corpid' : corpid,
      'corpsecret':corpsecret,
       }
    try:
        req = requests.post(url, params=values)  
    except Exception as err:
        print(err)
    
    data = json.loads(req.text)
    return data["access_token"]

def upload_file(token, path, filetype):
#     token = get_token(corpid, corpsecret)
    url = "https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s" % (token, filetype)
    files = {'filename': (os.path.basename(path), open(path, 'rb'))}  # 显式的设置文件名
    req = requests.post(url, files=files)
    data = json.loads(req.text)
    media_id = data['media_id']
    print("***已获取素材所需id.")
    return media_id
 
 
def send_msg(corpid, corpsecret, tag, touser, toparty, agentid, subject, content):
    token = get_token(corpid, corpsecret)
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + token
    values = {
       'touser' : touser,  # 通讯录用户ID
       'toparty' :toparty,  # 通讯录组ID
       'totag' : tag,  # 通讯录标签ID
       'msgtype' : 'text',
       'agentid' :agentid,  # 企业号应用的agentid
       'text' : {
           'content' : content
       },
       'safe':0
    }
    
    requests.post(url, data=json.dumps(values)) 
    
    
def send_file(corpid, corpsecret, tag, touser, toparty, agentid, path):  # 发送图片
    token = get_token(corpid, corpsecret)
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + token
    media_id = upload_file(token, path, 'file')
    values = {
        "touser": touser,
        "toparty": toparty,  # ***************部门******************
        "totag": tag,
        "msgtype": "file",
        "agentid": agentid,
        "file": {
            "media_id": media_id
        },
        "safe": 0
    }
    data = json.dumps(values)
    req = requests.post(url, data)
#     print("返回结果:", req.text)
    return req

def send_image(corpid, corpsecret, tag, touser, toparty, agentid, path):  # 发送图片
    token = get_token(corpid, corpsecret)
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + token
    media_id = upload_file(token, path, 'image')
    values = {
        "touser": touser,
        "toparty": toparty,  # ***************部门******************
        "totag": tag,
        "msgtype": "image",
        "agentid": agentid,
        "image": {
            "media_id": media_id
        },
        "safe": 0
    }
    data = json.dumps(values)
    req = requests.post(url, data)
#     print("返回结果:", req.text)
    return req
  
if __name__ == '__main__':
    corpid = 'wweaa126f843984b84'
    corpsecret = 's5u8dfFWsfH0nV0VHmhcKNUFUmmDs0ZeYJk2z-NGIFk'
#     token = get_token(corpid, corpsecret)
    tag = '1'
    touser = '@all'
    toparty = '1'
    agentid = '1000002'
    subject = u'报警日志'
    content = u'工商局系统监管数据库异机备份开始了'
    path = '../resource/oracle_report.pdf'
    
    send_msg(corpid, corpsecret, tag, touser, toparty, agentid, subject, 'daf\n dfaf \n 烦死了 \n')

#     text = send_file(corpid, corpsecret, tag, touser, toparty, agentid, path)
    

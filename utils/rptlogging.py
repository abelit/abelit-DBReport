# -*- coding:utf-8 -*-
'''
@project: '__dbreport__.py'
@modules: utils.rptlogging
@description:
    
@author: abelit
@email: ychenid@live.com
@created:Feb 6, 2018

@licence: GPL
'''
import logging,os

def rptlogger(logpath):
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler(logpath)
    if not logger.handlers:
        # 设置日志格式、记录方式及日志文件位置
        
        logger.setLevel(level=logging.INFO)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        
        logger.addHandler(handler)
        logger.addHandler(console)
    
    
    return logger


if __name__ == '__main__':
    pass
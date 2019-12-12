'''
Created on Mar 13, 2018

@author: abelit
'''


import os
import json

from utils import filepath


project_settings = {
    # 项目信息配置
    'package': 'dev',
    'version':'3.14',
    'name':'__dbreport__.py',
    'author':'abelit',
    'email':'ychenid@live.com',
    'description':'',
}

path_settings = {
    'image': filepath.get_root_path(project_settings['name']) + os.sep + 'images' + os.sep,
    'log': filepath.get_root_path(project_settings['name']) + os.sep + 'logs' + os.sep,
    'font': filepath.get_root_path(project_settings['name']) + os.sep + 'fonts' + os.sep,
    'resource': filepath.get_root_path(project_settings['name']) + os.sep + 'resource' + os.sep,
    'config': filepath.get_root_path(project_settings['name']) + os.sep + 'config' + os.sep,
}

USERCONF = path_settings['config']+'dbreport.json'



if __name__ == '__main__':
    print(USERCONF)

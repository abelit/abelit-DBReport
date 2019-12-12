# encoding: utf-8
'''
@project: '__dbreport__.py'
@modules: utils.getpath
@description:
    
@author: abelit
@email: ychenid@live.com
@created:Feb 6, 2018

@licence: GPL
'''

import os
import sys
from genericpath import isfile
    
def get_full_path(filename):
    # Get the separator sign of the os, such as '/' in linux/unix or '\' in windows
    separator = os.sep
    path = os.getcwd()
    path = path.split(separator)
    while len(path) > 0:
        filepath = separator.join(path) + separator + filename
        leng = len(path)
        if os.path.exists(filepath):
            return os.path.dirname(filepath)
        path.remove(path[leng - 1])
        
def get_real_path():
    path = os.path.split(os.path.realpath(__file__))[0]
    
    return path
  
def work_all_path(path):
    allpath = []
    # os.walk to search all path under the file or dir you want.
    for dirpath, dirnames, _filenames in os.walk(path):
        for file in dirnames:
            fullpath = os.path.join(dirpath, file)
            allpath.append(fullpath)
    return allpath

def add_env_path(path):
    # Add package folder to searching path
    # Search the dir that contains file '__dbreport__.py'
    for dirname in work_all_path(path):
        if isfile(dirname + os.sep + '__dbreport__.py') and dirname not in sys.path:
            sys.path.append(dirname) 
            
def get_root_path(filename):
    separator = os.sep
    path = get_real_path()
    path = path.split(os.sep)
    while len(path) > 0:
        filepath = separator.join(path) + separator + filename
        leng = len(path)
        if os.path.exists(filepath):
            return os.path.dirname(filepath)
        path.remove(path[leng - 1])
        
        
if __name__ == '__main__':
    
    print(get_full_path('__dbreport__.py'))
    print(get_real_path())
    
    print(get_root_path('__dbreport__.py'))

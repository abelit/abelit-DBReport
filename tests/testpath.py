'''
Created on Mar 13, 2018

@author: abelit
'''


import sys,os
sys.path.append('/Users/abelit/Downloads/Workspace/Code/DBReport')
from utils import filepath


print("=============sys.path======================")
print(sys.path)

print("=============sys.path[0]======================")

print(sys.path[0])

print("=============sys.argv[0]======================")

print(sys.argv[0])

print("=============os.path.realpath(__file__)======================")

print(os.path.realpath(__file__))


print("=============os.path.split(os.path.realpath(__file__))[0]======================")

print(os.path.split(os.path.realpath(__file__))[0])

print("=============filepath======================")

print(filepath.get_full_path('__dbreport__.py'))
print(filepath.get_root_path('__dbreport__.py'))
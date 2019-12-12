'''
Created on Mar 14, 2018

@author: abelit
'''

from config import settings
example_conf = settings.path_settings['config'] + 'dbreport_example.json'
conf = settings.path_settings['config'] + 'dbreport.json'
f = open(file=example_conf , mode='r', encoding='utf-8')

f1 = open(file=conf , mode='r+', encoding='utf-8')

content = f.read()

f1.truncate()
f1.write(content)

f.close()
f1.close()

print(content)
'''
Created on Mar 29, 2018

@author: abelit
'''

import subprocess
import threading
import time

try:
    import cx_Oracle
except ImportError:
    cx_oracle_exists = False
else:
    cx_oracle_exists = True
    
def mydemo():
    while True:
        print('hahha')
        time.sleep(5)
        
timeout = 0

username='sys'
password='gzgsoracle'
mode="sysdba"
host="172.230.0.40"
port=1521
instance='orcl'

dsn = cx_Oracle.makedsn(host=host, port=port, service_name=instance)


conn=cx_Oracle.connect(username, password, dsn, mode=cx_Oracle.SYSDBA)

t = threading.Timer(timeout,conn.cancel())


t.start()
print('hello')
t.cancel()    
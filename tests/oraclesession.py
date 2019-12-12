'''
Created on Mar 29, 2018

@author: abelit
'''


import cx_Oracle
import threading

poolConn = cx_Oracle.SessionPool("doron_tomp", "doron1234~", "192.168.102.37/tomp", 2, 5, 1,threaded = True)

print(poolConn.timeout())


def query_data1():
    conn = poolConn.acquire()
    cursor = conn.cursor()
    print("query_data1(): beginning execute...")
    cursor.execute('select * from test')
    print("query_data1(): done execute...")
    while True:
        rows = cursor.fetchmany()
        if not rows:
            break
        print(rows)
    print("TheLongQuery(): all done!")
    
    
def query_data2():
    conn = poolConn.acquire()
    cursor = conn.cursor()
    print("query_data2(): beginning execute...")
    cursor.execute('select * from test')
    print("query_data2(): done execute...")
    while True:
        rows = cursor.fetchmany()
        if not rows:
            break
        print(rows)
    print("TheLongQuery(): all done!")
    
    
thread1 = threading.Thread(None, query_data1)
thread1.start()
thread2 = threading.Thread(None, query_data2)
thread2.start()
thread1.join()
thread2.join()
print("All done!")

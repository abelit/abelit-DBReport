# -*- coding:utf-8 -*-
'''
@project: '__dbreport__.py'
@modules: tests.testtime
@description:

@author: abelit
@email: ychenid@live.com
@created: Apr 2, 2018

@licence: GPL
'''
LOOP_SLEEP = 5


def main():
    #i = 0
    import datetime,time,sys
    '''
    Daemon start to run here.
    '''
    icount = 0
    jcount = 0
    days = [12,13,14]
    
    while True: 
        # Run while there is no stop request.
        try:
            if icount==0 and datetime.datetime.now().day == 2:
                print('the first line')
                icount = icount+1
                #print(icount)
            
            #print(icount)   
            print('the alert line')
            
            if jcount == 0 and datetime.datetime.now().hour in days:
                print('the daily line')
                print(jcount)
                jcount += 1
                       
                       
            print(jcount)
        except Exception as err:
                sys.stderr.write('%s\n' % (err))
        finally:
            #print("hello")
            if datetime.datetime.now().day != 2:
                icount = 0
              
            if datetime.datetime.now().hour not in days:  
                jcount = 0

        time.sleep(LOOP_SLEEP)
        
        
def mycount():
    import time
    i = 0
    while True:
        i += 1
        
        print(i)
        
        time.sleep(3)
        
        
def mydemo():
    import datetime
    jcount = 0
    days = [12,13,14]
    for i in days:
        if i != datetime.datetime.now().hour:  
            jcount = 0
            print(jcount)
        
if __name__ == '__main__':
    main()
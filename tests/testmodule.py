'''
Created on Mar 30, 2018

@author: abelit
'''

def runServiceBaseNT():
    # Service running backgound based windows         
    try:     
        import win32serviceutil
        import win32service
        import win32event
        import servicemanager
        import socket
        import time
        import sys
    except ImportError as e:
        print(e)


    class DBReportService(win32serviceutil.ServiceFramework):
        _svc_name_ = 'DBReportService'
        _svc_display_name_ = 'DBReportService'
        
        def __init__(self, args):
            win32serviceutil.ServiceFramework.__init__(self, args)
            self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
            
            socket.setdefaulttimeout(60)
            self.isAlive = True
            
        def SvcStop(self):
            self.isAlive = False
            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
            win32event.SetEvent(self.hWaitStop)
            
        def SvcDoRun(self):
            self.isAlive = True
            servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, 
                                  servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
            while self.isAlive: 
                wfile()
                time.sleep(3)

            win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
            
        def main(self):
            #i = 0
            while self.isAlive: 
                wfile()
                time.sleep(3)


    return DBReportService


def wfile():
    f = open('C:\\Users\\Abelit\\Desktop\\demo.txt','a')

    f.write('hello abelit \n')

    f.close()


if __name__ == '__main__':
    print(runServiceBaseNT())
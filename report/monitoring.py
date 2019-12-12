# -*- coding:utf-8 -*-
'''
@project: '__dbreport__.py'
@modules: report.monitoring
@description:
    
@author: abelit
@email: ychenid@live.com
@created:Mar 12, 2018

@licence: GPL
'''

from report.database import Oracle
from config import settings

from utils import rptlogging

logger = rptlogging.rptlogger(settings.ReportSetting().getPackageSetting()['logfile'])


class OracleMonitor():
    
    def __init__(self,conf=settings.ReportSetting()):
        self.dbsettings = conf.getDatabaseSetting()
    
    
    def test_connect_oracle(self):
        results = []
        for db in self.dbsettings.values():
            oracle = Oracle(username=db['username'], password=db['password'], mode=db['mode'], host=db['host'], port=db['port'], instance=db['service_name'])
            
            
            try:
                instance_status = oracle.instance_status()[0]
            except Exception as e:
                print(e)
                instance_status = ('Unknown?', 'Unknown?', 'Unknown?', 'Unknown?', 'Unknown?')
             
            try:
                database_status = oracle.database_status()[0]
            except Exception as e:
                print(e)
                database_status = ('Unknown?', 'Unknown?', 'Unknown?', 'Unknown?')
                
            try:
                test_connect_status = oracle.test_connect()[0][0]
            except Exception as e:
                print(e)
                test_connect_status = 'Not Available!'
            
            
            results.append({'host':db['host'],'instance':instance_status,'database':database_status,'connectability':test_connect_status})
        
        return results
      
        
if __name__ == '__main__':
    om = OracleMonitor()
    ret = om.test_connect_oracle()
    
    print(ret)
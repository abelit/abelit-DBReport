'''
Created on Mar 29, 2018

@author: abelit
'''

from config import settings

days = settings.ReportSetting().getReportSetting()['report_interval']

print(days)
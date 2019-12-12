'''
Created on Mar 15, 2018

@author: abelit
'''

import datetime
import calendar

date_range = calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)

print(date_range[1]==31)
print(datetime.datetime.now().day == 15)

print(datetime.datetime.now().hour)
print(datetime.datetime.now().minute)
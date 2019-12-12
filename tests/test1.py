'''
Created on Mar 15, 2018

@author: abelit
'''

import sys,os

def configWindowsBat():
    from report import cli
    
    print("Configging execute bat for System based on NT.")
    
    win_scripts = """@ECHO OFF 
        REM Runs DBReport on Windows
        if "%1" == "h" goto begin 
        mshta vbscript:createobject("wscript.shell").run("%~nx0 h",0)(window.close)&&exit 
        :BEGIN
        {0}
        PAUSE"""
        
    print(os.path.realpath(cli.__file__))
    print(win_scripts.format('pythonw '+os.path.realpath(cli.__file__)))
        
    f = open(file=sys.exec_prefix+os.sep+'Scripts/dbreport_daemon.bat', mode='a', encoding='utf-8')
    
    f.truncate()

    f.write(win_scripts.format('pythonw '+os.path.realpath(cli.__file__)))
  
if os.name == 'nt':  
    configWindowsBat()
    configWindowsBat()
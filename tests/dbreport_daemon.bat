@ECHO OFF 

REM Runs DBReport on Windows

if "%1" == "h" goto begin 
mshta vbscript:createobject("wscript.shell").run("%~nx0 h",0)(window.close)&&exit 
:BEGIN

pythonw ./testtime.py

PAUSE
# -*- coding:utf-8 -*-
'''
@project: '__dbreport__.py'
@modules: setup
@description:

@author: abelit
@email: ychenid@live.com
@created:Mar 6, 2018

@licence: GPL
'''

import io
import re
from setuptools import setup,find_packages

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

with io.open('__dbreport__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)
    
project_name='DBReport'

setup(
    name=project_name,
    version=version,
    url='http://www.dataforum.org/',
    license='BSD',
    author='Abelit/ChenYing',
    author_email='ychenid@live.com',
    maintainer='Dataforum Group/Abelit',
    maintainer_email='ychenid@live.com',
    description='Generate a report of database for Oracle DBA.',
    long_description=readme,
    packages=find_packages(exclude=["tests"]),
    package_data={'': ['*.*','../*.py']},
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'cx-Oracle>=6.1',
        'matplotlib>=2.1.0',
        'paramiko>=2.4.0',
        'reportlab>=3.4.0',
        'requests>=2.18.1',
    ],
    extras_require={
        "bcrypt": ["bcrypt"],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Application Environment',
        'Framework :: DBReport',
        'Intended Audience :: Developers&DBA',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    entry_points={
        'console_scripts': [
            'dbreport = report.cli:main',
            'dbreport_daemon = report.cli:run_daemon',
        ],
    },
)

import os,sys
from distutils.sysconfig import get_python_lib
def configWindowsBat():
    
    print("Configging execute bat for System based on NT.")
    
#     win_scripts = """@ECHO OFF 
#         REM Runs DBReport on Windows
#         choice /t 5 /d y /n >nul
#         if "%1" == "h" goto begin 
#         mshta vbscript:createobject("wscript.shell").run("%~nx0 h",0)(window.close)&&exit 
#         :BEGIN
#         {0}
#         PAUSE"""
        
    win_scripts = """@ECHO OFF \nREM Runs DBReport on Windows \n{0} %1"""
    #print(os.path.realpath(cli.__file__))
    #print(win_scripts.format('pythonw '+os.path.realpath(cli.__file__)))
        
    f = open(file=sys.exec_prefix+os.sep+'Scripts/dbreport_daemon.bat', mode='w', encoding='utf-8')
    
    f.truncate()

#     f.write(win_scripts.format('pythonw '+os.path.realpath(cli.__file__)))'DBReport-3.14-py3.6.egg'
    f.write(win_scripts.format('python '+get_python_lib()+os.sep+project_name+'-'+str(version)+'-'+'py'+str(sys.version_info.major)+'.'+str(sys.version_info.minor)+'.egg'+os.sep+'report'+os.sep+'winservice.py'))

    
    print('dbreport_daemon.bat is generate on nt this system successfully \n and if want to run this procedure as as windows server, do it using "dbreport_daemon.bat"')
  
if os.name == 'nt':  
    configWindowsBat()


# -*- coding:utf-8 -*-
'''
@project: '__dbreport__.py'
@modules: report.host
@description:
    
@author: abelit
@email: ychenid@live.com
@created:Feb 28, 2018

@licence: GPL
'''


import paramiko
import re
import time
 
class HostMetric:
    def __init__(self, hostname, username, password, port, logpath=None):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.logpath = logpath
        
    def execute(self, command):
        if self.logpath is not None:
            paramiko.util.log_to_file(self.logpath)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_system_host_keys()
     
        ssh.connect(hostname=self.hostname, username=self.username, password=self.password, port=self.port, allow_agent=False,look_for_keys=False)
     
        stdin, stdout, stderr = ssh.exec_command("source .bash_profile;" + command)
        
        if stdin != "":  
            print(stdin) 
         
        if stderr != "":  
            print(stderr)   
        
        results = stdout.readlines()
        ssh.close()
        return results
    
    def get_disk_metric(self):
        results = self.execute('df -h')
  
        data = []
        for i in results:
            data.append(i.split())
             
        return data
    
    def get_net_metric(self):
        results = self.execute('cat /proc/net/dev')
    
        data = []
        
        for i in results[1:]:
            data.append([i.split()[0], i.split()[1], i.split()[4]])
            
        return data
    
    def get_mem_metric(self):
        results = self.execute('cat /proc/meminfo')
        str_total = results[0]
        str_free = results[1]
        
        totalmem = re.search('\d+', str_total).group()  
        freemem = re.search('\d+', str_free).group()  
        freepct = round(float(freemem) / float(totalmem), 2) 
        # print('当前内存使用率为： '+str(1-freepct)) 
        
        return {'MemTotal':totalmem, 'MemFree':freemem, 'MemUsedRate':1 - freepct}
    
    def get_cpu_metric(self):
        results1 = self.execute('cat /proc/stat | grep "cpu "')
        time.sleep(2)
        results2 = self.execute('cat /proc/stat | grep "cpu "')
        
        cpu_time_list1 = re.findall('\d+', results1[0])
        cpu_time_list2 = re.findall('\d+', results2[0])   
         
        cpu_idle1 = cpu_time_list1[3]  
        cpu_idle2 = cpu_time_list2[3] 
        total_cpu_time1 = 0  
        total_cpu_time2 = 0  
        
        for t1 in cpu_time_list1:  
            total_cpu_time1 = total_cpu_time1 + int(t1) 
            
        for t2 in cpu_time_list2:  
            total_cpu_time2 = total_cpu_time2 + int(t2) 
            
        cpu_usage = round(1 - (float(cpu_idle2) - float(cpu_idle1)) / (total_cpu_time2 - total_cpu_time1), 2)  
                
        return cpu_usage
    
    def get_load_metric(self):
        results = self.execute('cat /proc/loadavg')
    
        data = []
        for i in results:
            data.append(i.split())
             
        return data
    
    
if __name__ == '__main__':
    hostmetric = HostMetric('172.28.1.222', 'oracle', 'oracle', 22)

    # 获取网卡使用信息
    data = [['Face', 'Bytes', 'Drop']]
    try:
        results = hostmetric.get_net_metric()
        results = results[1:]
        note = ''
    except Exception:
        results = ['', '', '']  
        note = '注释：服务器连接异常，请检查服务器运行是否正常。'
      
    data.extend(results)

    
    
    print(data)
    
    
    

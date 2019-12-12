# -*- coding:utf-8 -*-
'''
@project: '__dbreport__.py'
@modules: report.database
@description:
    
@author: abelit
@email: ychenid@live.com
@created:Feb 6, 2018

@licence: GPL
'''
# import os

from report import sqlscript
from utils import rptlogging
from config import settings

logger = rptlogging.rptlogger(settings.ReportSetting().getPackageSetting()['logfile'])

# Import module cx_Oracle to connect oracle using python
try:
    import cx_Oracle
except ImportError:
    cx_oracle_exists = False
else:
    cx_oracle_exists = True

class Oracle:
    def __init__(self, username, password, host, port, instance, mode):
        """
        Function: __init__
        Summary: InsertHere
        Examples: InsertHere
        Attributes:
            @param (self):InsertHere
            @param (*args):InsertHere
            username: oracle user,
            password: oracle user's password,
            mod:  "normal, sysdba, sysoper",defaut is normal,
            host: the oracle database locates
            port: the port listen oracle database service, config is 1521
            insrance: the service name of the oracle database instance
        Returns: InsertHere
        """
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.instance = instance
        self.mode = mode

    def __connect(self):
        """
        Function: __connect
        Summary: InsertHere
        Examples: self.__connect()
        Attributes:
            @param (self):Call __connect metod Oracle.__connect()
        Returns: connection
        """
        if not cx_oracle_exists:
            msg = """The cx_Oracle module is required. 'pip install cx_Oracle' \
                should do the trick. If cx_Oracle is installed, make sure ORACLE_HOME \
                & LD_LIBRARY_PATH is set"""
            logger.warn(msg)

        dsn = cx_Oracle.makedsn(host=self.host, port=self.port, service_name=self.instance)

        try:
            if self.mode == 'sysdba' or self.username == 'sys':
                self.connection = cx_Oracle.connect(self.username, self.password, dsn, \
                                                    mode=cx_Oracle.SYSDBA)
            else:
                self.connection = cx_Oracle.connect(self.username, self.password, dsn)
            logger.info("Connect database " + str(self.connection) + " successfully.")
        except cx_Oracle.DatabaseError as cx_msg:
            msg = 'Could not connect to database: %s, dsn: %s ' % (cx_msg, dsn)
            logger.error (msg) 
        return self.connection

    def __disconnect(self):
        try:
            self.cursor.close()
            self.connection.close()
            logger.info("Disconnect from oracle.")
        except cx_Oracle.DatabaseError as cx_msg:
            logger.error(cx_msg)
            print(cx_msg)

    def select(self, sql, bindvars=''):
        """
        Given a valid SELECT statement, return the results from the database
        """
        
        results = None

        try:
            self.__connect()
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql, bindvars)
            results = self.cursor.fetchall()
            logger.info("The sql executing from database successfully and the sql is " + '"' + sql + '".')
        except cx_Oracle.DatabaseError as cx_msg:
            logger.error(cx_msg)
            print(cx_msg)
        finally:
            self.__disconnect()
        return results

    def execute(self, sql, bindvars='', commit=True):
        """
        Function: execute
        Summary: Execute whatever SQL statements are passed to the method;
            commit if specified. Do not specify fetchall() in here as
            the SQL statement may not be a select.
            bindvars is a dictionary of variables you pass to execute.
        Examples: Oracle().execute(...)
        Attributes:
            @param (self):class method
            @param (sql):The sql that will be excuted
            @param (bindvars) config='': The bind variables of sql
            @param (many) config=False: If set many is True, multiple sql will be excuted at the same time
            @param (commit) config=False: False is not needed commit after excuting sql, but True is needed commit, gernerally DML sql
        Returns: NO value will be returned
        """

        try:
            self.__connect()
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql, bindvars)
            logger.info("The sql executing from database successfully and the sql is " + '"' + sql + '".')
        except cx_Oracle.DatabaseError as cx_msg:
            logger.error(cx_msg)
        finally:
            # Only commit if it-s necessary.
            if commit:
                self.connection.commit()
            else:
                pass
            self.__disconnect()
            
    def test_connect(self):
        sql = sqlscript.sqlpool['test_connect']
        results = self.select(sql)
        
        return results
            
    def instance_status(self):
        sql = sqlscript.sqlpool['instance_status']
        results = self.select(sql)
        
        return results
    
    def database_status(self):
        sql = sqlscript.sqlpool['database_status']
        results = self.select(sql)
        
        return results
    
    def register(self):
        sql = sqlscript.sqlpool['register']
        results = self.select(sql)
        
        return results
    
    def datafile(self):
        sql = sqlscript.sqlpool['datafile']
        results = self.select(sql)
        
        return results
    
    def tablespace(self):
        sql = sqlscript.sqlpool['tablespace']
        results = self.select(sql)
        
        return results
    
    def controlfile(self):
        sql = sqlscript.sqlpool['controlfile']
        results = self.select(sql)
        
        return results
    
    def logcount(self):
        sql = sqlscript.sqlpool['logcount']
        results = self.select(sql)
        
        return results
        
    def logfile(self):
        sql = sqlscript.sqlpool['logfile']
        results = self.select(sql)
        
        return results
    
    def invalid_objects(self):
        sql = sqlscript.sqlpool['invalid_objects']
        results = self.select(sql)
        
        return results
    
    def disabled_constraints(self):
        sql = sqlscript.sqlpool['disabled_constraints']
        results = self.select(sql)
        
        return results
    
    def disabled_triggers(self):
        sql = sqlscript.sqlpool['disabled_triggers']
        results = self.select(sql)
        
        return results
    
    def invalid_indexes(self):
        sql = sqlscript.sqlpool['invalid_indexes']
        results = self.select(sql)
        
        return results
    
    def rollback_segments(self):
        sql = sqlscript.sqlpool['rollback_segments']
        results = self.select(sql)
        
        return results
    
    
    def zombie_process(self):
        sql = sqlscript.sqlpool['zombie_process']
        results = self.select(sql)
        
        return results
    
    def data_buffer_cache(self):
        sql = sqlscript.sqlpool['data_buffer_cache']
        results = self.select(sql)
        
        return results
    
    def library_cache(self):
        sql = sqlscript.sqlpool['library_cache']
        results = self.select(sql)
        
        return results
    
    
    def log_buffer(self):
        sql = sqlscript.sqlpool['log_buffer']
        results = self.select(sql)
        
        return results
    
    def sort_area(self):
        sql = sqlscript.sqlpool['sort_area']
        results = self.select(sql)
        
        return results
    
    def dead_lock(self):
        sql = sqlscript.sqlpool['dead_lock']
        results = self.select(sql)
        
        return results
    
    
    def table_fragment(self):
        sql = sqlscript.sqlpool['table_fragment']
        results = self.select(sql)
        
        return results
    
    def wait(self):
        sql = sqlscript.sqlpool['wait']
        results = self.select(sql)
        
        return results
    
    def sql_wait(self):
        sql = sqlscript.sqlpool['sql_wait']
        results = self.select(sql)
        
        return results
    
    def sql_performance(self):
        sql = sqlscript.sqlpool['sql_performance']
        results = self.select(sql)
        
        return results
    
    
    def sql_disk(self):
        sql = sqlscript.sqlpool['sql_disk']
        results = self.select(sql)
        
        return results
    
    def sql_cpu(self):
        sql = sqlscript.sqlpool['sql_cpu']
        results = self.select(sql)
        
        return results
    
    def sql_cpu_top_hist(self):
        sql = sqlscript.sqlpool['sql_cpu_top_hist']
        results = self.select(sql)
        
        return results
    
    def sql_disk_top_hist(self):
        sql = sqlscript.sqlpool['sql_disk_top_hist']
        results = self.select(sql)
        
        return results
    
    def sql_buffer_top_hist(self):
        sql = sqlscript.sqlpool['sql_buffer_top_hist']
        results = self.select(sql)
        
        return results
    
    def sql_executions_top_hist(self):
        sql = sqlscript.sqlpool['sql_executions_top_hist']
        results = self.select(sql)
        
        return results
    
    def sql_sorts_top_hist(self):
        sql = sqlscript.sqlpool['sql_sorts_top_hist']
        results = self.select(sql)
        
        return results
    
    def alert(self):
        sql = sqlscript.sqlpool['alert']
        results = self.select(sql, ('2018-01-01', '2018-01-02', 'ora-'))
        
        return results
    
    def session(self):
        sql = sqlscript.sqlpool['session']
        results = self.select(sql)
        
        return results
    
    def active_session(self):
        sql = sqlscript.sqlpool['active_session']
        results = self.select(sql)
        
        return results
    
    def rman_backup(self):
        sql = sqlscript.sqlpool['rman_backup']
        results = self.select(sql)
        
        return results
    
    def rman_backupset(self):
        sql = sqlscript.sqlpool['rman_backupset']
        results = self.select(sql)
        
        return results
    
    def log_switch(self):
        sql = sqlscript.sqlpool['log_switch']
        results = self.select(sql)
        
        return results
    
    def log_increase(self):
        sql = sqlscript.sqlpool['log_increase']
        results = self.select(sql)
        
        return results
    
    def undo_usage_hist(self):
        sql = sqlscript.sqlpool['undo_usage_hist']
        results = self.select(sql)
        
        return results
    
    def db_load_hist(self):
        sql = sqlscript.sqlpool['db_load_hist']
        results = self.select(sql)
        
        return results
    
    def event_top_hist(self):
        sql = sqlscript.sqlpool['event_top_hist']
        results = self.select(sql)
        
        return results
    
    def wait_class_hist(self):
        sql = sqlscript.sqlpool['wait_class_hist']
        results = self.select(sql)
        
        return results
    
    def soft_parse_hist(self):
        sql = sqlscript.sqlpool['soft_parse_hist']
        results = self.select(sql)
        
        return results
    
    def libraycache_hit_hist(self):
        sql = sqlscript.sqlpool['libraycache_hit_hist']
        results = self.select(sql)
        
        return results
    
    def buffer_hit_hist(self):
        sql = sqlscript.sqlpool['buffer_hit_hist']
        results = self.select(sql)
        
        return results
    
    def memory_sort_hist(self):
        sql = sqlscript.sqlpool['memory_sort_hist']
        results = self.select(sql)
        
        return results
    
    def cpu_usage_hist(self):
        sql = sqlscript.sqlpool['cpu_usage_hist']
        results = self.select(sql)
        
        return results
    
    
    
if __name__ == '__main__':
#     oracle = Oracle(username='sys',password='oracle',mode="sysdba",host="192.168.56.201",port=1521,instance='orcl.org')
#     results = oracle.select("select file_id,file_name from dba_data_files")
#     print(results)
#     oracle = Oracle(username='sys',password='oracle',mode="sysdba",host="192.168.56.201",port=1521,instance='orcl.org')
    
    oracle = Oracle(username='sys', password='gzgsoracle', mode="sysdba", host="172.230.0.40", port=1521, instance='orcl')
#     try:
#         oracle.select("slect 'ok' from dual")
#     except Exception as e:
#         print(e) 

    print(oracle.test_connect()[0][0])
    

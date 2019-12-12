# -*- coding:utf-8 -*-
'''
@project: '__dbreport__.py'
@modules: report.sqlscript
@description:

@author: abelit
@email: ychenid@live.com
@created:Feb 10, 2018

@licence: GPL
'''

sqlpool = {
    "test_connect": """select 1 from dual""",
    "instance_status": """select instance_name,host_name,startup_time,status,database_status from v$instance""",
    "database_status": """select name,log_mode,open_mode,supplemental_log_data_min from v$database""",
    "register": """select comp_id,comp_name,version,status from dba_registry""",
    "datafile": """select file_id, file_name,online_status, round(bytes/1024/1024,2) size_mb, round(maxbytes/1024/1024,2) maxsize_mb, autoextensible from dba_data_files order by file_id""",
    "tablespace": """select tbsz.tablespace_name,tbsn.status,tbsz.total_mb,use_mb,free_mb,use_pct from (
        Select a.tablespace_name,
        round(a.bytes/1024/1024,2) total_mb,
        round(b.bytes/1024/1024,2) free_mb,
        round(a.bytes/1024/1024 - b.bytes/1024/1024,2) use_mb,
        round((1 - b.bytes/a.bytes)*100,2) || '%' use_pct
        from (select tablespace_name,
        sum(bytes) bytes
        from dba_data_files
        group by tablespace_name) a,
        (select tablespace_name,
        sum(bytes) bytes
        from dba_free_space
        group by tablespace_name) b
        where a.tablespace_name = b.tablespace_name
        union all
        select c.tablespace_name,
        round(c.bytes/1024/1024,2) total_mb,
        round( (c.bytes-d.bytes_used)/1024/1024,2) free_mb,
        round(d.bytes_used/1024/1024,2) use_mb,
        round(d.bytes_used*100/c.bytes,2) || '%' use_pct
        from
        (select tablespace_name,sum(bytes) bytes
        from dba_temp_files group by tablespace_name) c,
        (select tablespace_name,sum(bytes_cached) bytes_used
        from v$temp_extent_pool group by tablespace_name) d
        where c.tablespace_name = d.tablespace_name
        ) tbsz, dba_tablespaces tbsn where tbsz.tablespace_name=tbsn.tablespace_name""",
    "controlfile": """select status,name,block_size from v$controlfile""",
    "logfile": """select group#,status,type,member from v$logfile""",
    "log":"""select group#,sequence#,bytes/1024/1024,archived,status from v$log""",
    "logcount":"""select count(1) from v$log""",

    "invalid_objects": """SELECT owner, object_name, object_type,status FROM dba_objects WHERE status = 'INVALID' and (OBJECT_TYPE != 'TYPE' or (OBJECT_TYPE='TYPE' and SUBOBJECT_NAME is null)) and owner not in ('SYS','SYSTEM')""",
    "disabled_constraints": """SELECT owner, constraint_name, table_name, constraint_type, status FROM dba_constraints WHERE status = 'DISABLED' and owner not in ('SYS','SYSTEM')""",
    "disabled_triggers": """SELECT owner, trigger_name, table_name, status FROM dba_triggers WHERE status = 'DISABLED' and owner not in ('SYS','SYSTEM')""",
    "invalid_indexes": """select owner,index_name,table_name,tablespace_name,status from dba_indexes where status<>'VALID' and owner not in ('SYS','SYSTEM')""",

    "rollback_segments": """select segment_name, tablespace_name,file_id,status from dba_rollback_segs""",
    "zombie_process": """select spid from v$process where addr not in (select paddr from v$session)""",
    "data_buffer_cache": """SSELECT a.VALUE + b.VALUE logical_reads,
        c.VALUE phys_reads,
        round(100*(1-c.value/(a.value+b.value)),4) hit_ratio
        FROM v$sysstat a,v$sysstat b,v$sysstat c
        WHERE a.NAME='db block gets'
        AND b.NAME='consistent gets'
        AND c.NAME='physical reads'""",
    "library_cache": """select sum(pinhits)/sum(pins)*100 from v$librarycache""",
    "log_buffer": """select name,value from v$sysstat where name in ('redo entries','redo buffer allocation retries')""",
    "sort_area": """select name,value from v$sysstat where name like '%sort%'""",

    "dead_lock": """select sid,serial#,username,SCHEMANAME,osuser,MACHINE,
        terminal,PROGRAM,owner,object_name,object_type,o.object_id
        from dba_objects o,v$locked_object l,v$session s
        where o.object_id=l.object_id and s.sid=l.session_id""",

    "table_fragment": """SELECT segment_name table_name,COUNT(*) extents FROM dba_segments WHERE owner NOT IN ('SYS', 'SYSTEM')
        GROUP BY segment_name HAVING COUNT(*)=(SELECT MAX(COUNT(*)) FROM dba_segments GROUP BY segment_name)""",

    "wait": """select sid,event,p1,p2,p3,WAIT_TIME,SECONDS_IN_WAIT from v$session_wait where event not like 'SQL%' and event not like 'rdbms%'""",
    "sql_performance": """SELECT * FROM (SELECT PARSING_USER_ID EXECUTIONS,SORTS,COMMAND_TYPE,DISK_READS,SQL_TEXT FROM V$SQLAREA ORDER BY DISK_READS DESC) WHERE ROWNUM<10""",

    "sql_disk": """select * from (select substr(sql_text,1,500) "SQL",
                                      (cpu_time/1000000) "CPU_Seconds",
                                      disk_reads "Disk_Reads",
                                      buffer_gets "Buffer_Gets",
                                      executions "Executions",
                                      case when rows_processed = 0 then null
                                           else round((buffer_gets/nvl(replace(rows_processed,0,1),1)))
                                           end "Buffer_gets/rows_proc",
                                      round((buffer_gets/nvl(replace(executions,0,1),1))) "Buffer_gets/executions",
                                      (elapsed_time/1000000) "Elapsed_Seconds",
                                      module "Module"
                                 from gv$sql s
                                order by disk_reads desc nulls last) where rownum<=10""",
    "sql_cpu": """select * from (select substr(sql_text,1,500) "SQL",
                                      (cpu_time/1000000) "CPU_Seconds",
                                      disk_reads "Disk_Reads",
                                      buffer_gets "Buffer_Gets",
                                      executions "Executions",
                                      case when rows_processed = 0 then null
                                           else round((buffer_gets/nvl(replace(rows_processed,0,1),1)))
                                           end "Buffer_gets/rows_proc",
                                      round((buffer_gets/nvl(replace(executions,0,1),1))) "Buffer_gets/executions",
                                      (elapsed_time/1000000) "Elapsed_Seconds",
                                      module "Module"
                                 from gv$sql s
                                order by cpu_time desc nulls last) where rownum <=10""",
    "sql_cpu_top_hist":"""select t1.sql_id, dbms_lob.substr(substr(t2.sql_text,0,100))||'......',t1.cpu_time,t1.disk_reads_time,t1.counts from (select * from 
        (select
          s.SQL_ID,
          sum(s.CPU_TIME_DELTA) cpu_time,
          sum(s.DISK_READS_DELTA) disk_reads_time,
          count(*) counts
        from DBA_HIST_SQLSTAT s, DBA_HIST_SNAPSHOT p
        where 1=1
         and s.SNAP_ID = p.SNAP_ID
         and EXTRACT(HOUR FROM p.END_INTERVAL_TIME) between 0 and  23
         and p.END_INTERVAL_TIME between SYSDATE-7 and SYSDATE
        group by s.SQL_ID
        order by sum(s.CPU_TIME_DELTA) desc
        )
        where rownum <=10) t1,DBA_HIST_SQLTEXT t2 where t1.sql_id=t2.sql_id""",

    "sql_disk_top_hist":"""select t1.sql_id,dbms_lob.substr(substr(t2.sql_text,0,100))||'......',t1.disk_reads_time,t1.cpu_time,t1.counts from (select * from 
       (select
          s.SQL_ID,
          sum(s.CPU_TIME_DELTA) cpu_time,
          sum(s.DISK_READS_DELTA) disk_reads_time,
          count(*) counts
        from DBA_HIST_SQLSTAT s, DBA_HIST_SNAPSHOT p
        where 1=1
         and s.SNAP_ID = p.SNAP_ID
         and EXTRACT(HOUR FROM p.END_INTERVAL_TIME) between 0 and  23
         and p.END_INTERVAL_TIME between SYSDATE-7 and SYSDATE
        group by s.SQL_ID
        order by sum(s.DISK_READS_DELTA) desc
       )
    where rownum <=10) t1,DBA_HIST_SQLTEXT t2 where t1.sql_id=t2.sql_id""",

    "sql_buffer_top_hist":"""select t1.sql_id,dbms_lob.substr(substr(t2.sql_text,0,100))||'......',t1.buffer_reads_time,t1.cpu_time,t1.counts from (select * from 
       (select
          s.SQL_ID,
          sum(s.CPU_TIME_DELTA) cpu_time,
          sum(s.BUFFER_GETS_DELTA) buffer_reads_time,
          count(*) counts
        from DBA_HIST_SQLSTAT s, DBA_HIST_SNAPSHOT p
        where 1=1
         and s.SNAP_ID = p.SNAP_ID
         and EXTRACT(HOUR FROM p.END_INTERVAL_TIME) between 0 and  23
         and p.END_INTERVAL_TIME between SYSDATE-7 and SYSDATE
        group by s.SQL_ID
        order by sum(s.BUFFER_GETS_DELTA) desc
       )
    where rownum <=10) t1,DBA_HIST_SQLTEXT t2 where t1.sql_id=t2.sql_id""",

    "sql_executions_top_hist":"""select t1.sql_id,dbms_lob.substr(substr(t2.sql_text,0,100))||'......',t1.executions,t1.cpu_time,t1.counts from (select * from 
       (select
          s.SQL_ID,
          sum(s.CPU_TIME_DELTA) cpu_time,
          sum(s.EXECUTIONS_DELTA) executions,
          count(*) counts
        from DBA_HIST_SQLSTAT s, DBA_HIST_SNAPSHOT p
        where 1=1
         and s.SNAP_ID = p.SNAP_ID
         and EXTRACT(HOUR FROM p.END_INTERVAL_TIME) between 0 and  23
         and p.END_INTERVAL_TIME between SYSDATE-7 and SYSDATE
        group by s.SQL_ID
        order by sum(s.EXECUTIONS_DELTA) desc
       )
    where rownum <=10) t1,DBA_HIST_SQLTEXT t2 where t1.sql_id=t2.sql_id""",

    "sql_sorts_top_hist":"""select t1.sql_id,dbms_lob.substr(substr(t2.sql_text,0,100))||'......',t1.sorts,t1.cpu_time,t1.counts from (select * from 
       (select
          s.SQL_ID,
          sum(s.CPU_TIME_DELTA) cpu_time,
          sum(s.SORTS_DELTA) sorts,
          count(*) counts
        from DBA_HIST_SQLSTAT s, DBA_HIST_SNAPSHOT p
        where 1=1
         and s.SNAP_ID = p.SNAP_ID
         and EXTRACT(HOUR FROM p.END_INTERVAL_TIME) between 0 and  23
         and p.END_INTERVAL_TIME between SYSDATE-7 and SYSDATE
        group by s.SQL_ID
        order by sum(s.SORTS_DELTA) desc
       )
    where rownum <=10) t1,DBA_HIST_SQLTEXT t2 where t1.sql_id=t2.sql_id""",

    "alert": """SELECT
        record_id "Id",
        created "Created on",
        message_text "Message Text"
        FROM
            (
                SELECT
                    record_id,
                    originating_timestamp created,
                    message_text
                FROM
                    x$dbgalertext
                WHERE TO_CHAR(originating_timestamp,'yyyy-mm-dd') BETWEEN :start_date AND :end_date
                ORDER BY record_id DESC
            )
        WHERE lower(message_text) LIKE lower(DECODE(
                    :filter,
                    '',
                    '%',
                    '%' ||:filter || '%'
                ) )
        ORDER BY record_id ASC""",
    "active_session": """select inst_id,program,module,event,SQL_ID,machine,
        lpad(
                        to_char(
                                trunc(24*(sysdate-s.logon_time))
                        ) ||
                        to_char(trunc(sysdate) + (sysdate-s.logon_time)
                        ,       ':MI:SS'
                        )
                , 10, ' ') AS UP_time from gv$session s where type!='BACKGROUND'
        and status='ACTIVE' and sql_id is not null""",

    "session": """
        with vs as (select rownum rnum,
                          inst_id,
                          sid,
                          serial#,
                          status,
                          username,
                          last_call_et,
                          command,
                          machine,
                          osuser,
                          module,
                          action,
                          resource_consumer_group,
                          client_info,
                          client_identifier,
                          type,
                          terminal,
                          sql_id,
                          sql_child_number
                     from gv$session)
         select vs.inst_id, vs.sid ,serial# serial, vs.sql_id, vs.sql_child_number,
                vs.username "Username",
                case when vs.status = 'ACTIVE'
                          then last_call_et
                     else null end "Seconds in Wait",
                (select command_name from v$sqlcommand where command_type = vs.command ) "Command",
                vs.machine "Machine",
                vs.osuser "OS User",
                lower(vs.status) "Status",
                vs.module "Module",
                vs.action "Action",
                vs.resource_consumer_group,
                vs.client_info,
                vs.client_identifier
           from vs
          where vs.USERNAME is not null
            and nvl(vs.osuser,'x') <> 'SYSTEM'
            and vs.type <> 'BACKGROUND'
            order by 1,2,3""",
    "rman_backup": """select (select NAME from v$database) Instance,
        object_type,status,
        round((end_time - start_time) * 24 * 60, 2) Elapsed_Time,
        to_char(start_time, 'yyyy-mm-dd') start_time,
        round((input_bytes/(1024*1024*1024)),2) input_gb,
        round((output_bytes/(1024*1024*1024)),2) output_gb
        from v$rman_status
        where start_time > trunc(sysdate-31) and operation = 'BACKUP' order by start_time""",
    "rman_backupset":"""SELECT A.RECID "BACKUP SET",
                DECODE (B.INCREMENTAL_LEVEL,
                        '', DECODE (BACKUP_TYPE, 'L', 'Archivelog', 'Full'),
                        2, 'Incr-2',
                        1, 'Incr-1',
                        0, 'Incr-0',
                        B.INCREMENTAL_LEVEL)
                   "Type LV",
                DECODE (A.STATUS,
                        'A', 'AVAILABLE',
                        'D', 'DELETED',
                        'X', 'EXPIRED',
                        'ERROR')
                   "STATUS",
                A.START_TIME "Start Time",
                round(A.ELAPSED_SECONDS,2) "Elapsed Seconds",
                round(A.BYTES/1024/1024/1024,2) "Size(G)",
                A.HANDLE "Path"
           FROM GV$BACKUP_PIECE A, GV$BACKUP_SET B
          WHERE A.SET_STAMP = B.SET_STAMP AND A.DELETED = 'NO'
          AND A.START_TIME > trunc(sysdate-31)
        ORDER BY A.COMPLETION_TIME""",
    
    "log_switch": """SELECT
            *
        FROM
            (
                SELECT
                    b.recid,
                    b.first_time,
                    a.first_time last_time,
                    round(
                        (a.first_time - b.first_time) * 24 * 60,
                        2
                    ) minites
                FROM
                    v$log_history a,
                    v$log_history b
                WHERE
                    a.recid = b.recid + 1
                ORDER BY a.first_time DESC
            )
        WHERE
            ROWNUM < 120""",
            
    "log_increase":"""SELECT TO_CHAR (TRUNC (COMPLETION_TIME), 'yyyy-mm-dd') collect_time,
         round(SUM (blocks * BLOCK_SIZE) / 1024 / 1024 / 1024,2)  log_size
        FROM V$ARCHIVED_LOG
           WHERE dest_id = 1
        GROUP BY TRUNC (COMPLETION_TIME)
        ORDER BY TRUNC (COMPLETION_TIME)""",
    "undo_usage_hist":"""select to_char(begin_time,'yyyy-mm-dd HH24:MI:SS') collect_time,activeblks,unexpiredblks,expiredblks 
        from dba_hist_undostat where instance_number=(select instance_number from v$instance) order by 1""",
    "db_load_hist":"""select to_char(sn.end_interval_time,'yyyy-mm-dd HH24:MI:SS') collect_time,os.value from dba_hist_osstat os, dba_hist_snapshot sn 
        where os.stat_name='LOAD' and os.snap_id=sn.snap_id and os.instance_number=(select instance_number from v$instance) order by 1""",
    "wait_class_hist":"""select  wait_class,sum(total_waits) from dba_hist_system_event group by wait_class""",
    "event_top_hist":"""select * from (select  event_name,sum(wait_time_milli) from dba_hist_event_histogram group by event_name order by 2 desc) where rownum<=20""",
    "soft_parse_hist":"""select to_char(begin_time,'yyyy-mm-dd HH24:MI:SS') collect_time, metric_name,round(maxval,2),round(average,2) from dba_hist_sysmetric_summary 
        where metric_name='Soft Parse Ratio' and instance_number=(select instance_number from v$instance) order by 1""",
    "libraycache_hit_hist":"""select to_char(begin_time,'yyyy-mm-dd HH24:MI:SS') collect_time, metric_name,round(maxval,2),round(average,2) 
        from dba_hist_sysmetric_summary where metric_name='Library Cache Hit Ratio' and instance_number=(select instance_number from v$instance) order by 1""",
    "buffer_hit_hist":"""select to_char(begin_time,'yyyy-mm-dd HH24:MI:SS') collect_time, metric_name,round(maxval,2),round(average,2) from dba_hist_sysmetric_summary 
        where metric_name='Buffer Cache Hit Ratio' and instance_number=(select instance_number from v$instance) order by 1""",
    "memory_sort_hist":"""select to_char(begin_time,'yyyy-mm-dd HH24:MI:SS') collect_time, metric_name,round(maxval,2),round(average,2) from dba_hist_sysmetric_summary 
        where metric_name='Memory Sorts Ratio' and instance_number=(select instance_number from v$instance) order by 1""",
    "cpu_usage_hist":"""SELECT sn.instance_number,
               sn.snap_id,
               to_char(sn.end_interval_time, 'YYYY-MM-DD HH24:MI') AS snaptime,
               newread.value - oldread.value "physical reads",
               newwrite.value - oldwrite.value "physical writes",
               round((newdbtime.value - olddbtime.value) / 1000000 / 60, 2) "DB time(min)",
               round((newbusy.value - oldbusy.value) /
                     ((newidle.value - oldidle.value) +
                     (newbusy.value - oldbusy.value)) * 100,
                     2) "CPU(%)"
          FROM dba_hist_sysstat        oldread,
               dba_hist_sysstat        newread,
               dba_hist_sysstat        oldwrite,
               dba_hist_sysstat        newwrite,
               dba_hist_sys_time_model olddbtime,
               dba_hist_sys_time_model newdbtime,
               dba_hist_osstat         oldidle,
               dba_hist_osstat         newidle,
               dba_hist_osstat         oldbusy,
               dba_hist_osstat         newbusy,
               dba_hist_snapshot       sn
         WHERE newread.stat_name = 'physical reads'
           AND oldread.stat_name = 'physical reads'
           AND newread.snap_id = sn.snap_id
           AND oldread.snap_id = sn.snap_id - 1
           AND newread.instance_number = sn.instance_number
           AND oldread.instance_number = sn.instance_number
           AND newread.dbid = sn.dbid
           AND oldread.dbid = sn.dbid
           AND newwrite.stat_name = 'physical writes'
           AND oldwrite.stat_name = 'physical writes'
           AND newwrite.snap_id = sn.snap_id
           AND oldwrite.snap_id = sn.snap_id - 1
           AND newwrite.instance_number = sn.instance_number
           AND oldwrite.instance_number = sn.instance_number
           AND newwrite.dbid = sn.dbid
           AND oldwrite.dbid = sn.dbid
           AND newdbtime.stat_name = 'DB time'
           AND olddbtime.stat_name = 'DB time'
           AND newdbtime.snap_id = sn.snap_id
           AND olddbtime.snap_id = sn.snap_id - 1
           AND newdbtime.instance_number = sn.instance_number
           AND olddbtime.instance_number = sn.instance_number
           AND newdbtime.dbid = sn.dbid
           AND olddbtime.dbid = sn.dbid
           AND newidle.stat_name = 'IDLE_TIME'
           AND oldidle.stat_name = 'IDLE_TIME'
           AND newidle.snap_id = sn.snap_id
           AND oldidle.snap_id = sn.snap_id - 1
           AND newidle.instance_number = sn.instance_number
           AND oldidle.instance_number = sn.instance_number
           AND newidle.dbid = sn.dbid
           AND oldidle.dbid = sn.dbid
           AND newbusy.stat_name = 'BUSY_TIME'
           AND oldbusy.stat_name = 'BUSY_TIME'
           AND newbusy.snap_id = sn.snap_id
           AND oldbusy.snap_id = sn.snap_id - 1
           AND newbusy.instance_number = sn.instance_number
           AND oldbusy.instance_number = sn.instance_number
           AND newbusy.dbid = sn.dbid
           AND oldbusy.dbid = sn.dbid
           AND sn.instance_number =  (select instance_number from v$instance)
         ORDER BY sn.instance_number, sn.snap_id""",
}

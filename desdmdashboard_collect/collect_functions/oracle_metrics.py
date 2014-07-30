"""


This file contains routines that collect metrics from the ORACLE system 

-- GB read, written -- for all node in the cluster for a given schema. typcally
   this number grows.  the simplest plot is an integarl.

-- the number of GB allocaed to MyDB tables for that schema.


:: Author :: Donald Petravick
"""

import os
from desdmdashboard_remote.senddata.decorators import Monitor
from desdmdashboard_collect.collect_utils import log, database

logger = log.get_logger('desdmdashboard_collect')

def main():
   print read_GB('db-desoper')
   print read_GB('db-dessci')
   print write_GB('db-desoper')
   print write_GB('db-dessci')
   print mydb_GB('db-desoper')
   print mydb_GB('db-dessci')


#
# Collect total reads from a database
#
def create_read_GB_metric_name(section):
   db_name = database.get_db_name(section)
   metric_name = "{db_name}_read_GB".format(db_name=db_name)
   return metric_name

@Monitor(create_read_GB_metric_name,value_type="int", logger=logger)
def read_GB(section):
   """ return the GB read from disk  for all queries """
   q = """SELECT 
             sys_context('userenv','db_name'), 
             SUM(SMALL_read_megabytes), 
             SUM(LARGE_read_megabytes)
           FROM 
             GV$IOSTAT_FILE
           """
   (dbname, small_reads, large_reads) = database.query_one_row(q,
           section=section)
   reads  = (small_reads  + large_reads)/1024
   return reads 

#
# Collect total writes to a database
#
def create_write_GB_metric_name(section):
   db_name = database.get_db_name(section)
   metric_name = "{db_name}_write_GB".format(db_name=db_name)
   return metric_name

@Monitor(create_write_GB_metric_name,value_type="int", logger=logger)
def write_GB(section):
   """ return the GB read from disk  for all queries """
   q = """SELECT 
             sys_context('userenv','db_name'), 
             SUM(SMALL_WRITE_megabytes), 
             SUM(LARGE_WRITE_megabytes) 
           FROM 
             GV$IOSTAT_FILE
           """
   (dbname, small_writes, large_writes) = database.query_one_row(q,  section)
   writes = (small_writes + large_writes)/1024
   return writes

#
# Collect total size of "mydb" for a database
#
def create_mydb_GB_metric_name(section):
   db_name = database.get_db_name(section)
   metric_name = "{db_name}_mydb_GB".format(db_name=db_name)
   return metric_name

@Monitor(create_mydb_GB_metric_name,value_type="int", logger=logger)
def mydb_GB(section):
   "return the total GB of allocated mydb data table space for a schema"
   q = """SELECT  
           sys_context('userenv','db_name'), 
           sum(BYTES)/1024/1024/1024  
          from 
            DBA_SEGMENTS 
         where 
            tablespace_name = 'USERS_BIG'"""
   (dbname, mytablespace) = database.query_one_row(q,  section)
   # can be none if no space used.
   if not mytablespace :  mytablespace = 0  
   return mytablespace

if __name__ == "__main__":

   main()

"""
This file contains routines that collect metrics from the 
ORACLE system 

-- GB read, written -- for all node in the cluster
   for a given schema. typcally this number grows.
   the simplest plot is an integarl.

-- the number of GB allocaed to MyDB tables for that
   schema.

"""

import os
import coreutils
import cx_Oracle #needed to catch execptions
from desdmdashboard_remote.senddata.decorators import Monitor


def main():
   print read_requests('db-desoper')
   print read_requests('db-dessci')
   print write_requests('db-desoper')
   print write_requests('db-dessci')
   print mydb_GB('db-desoper')
   print mydb_GB('db-dessci')

class X(Exception):
    pass


def _query_one_row(query, section):
   """ open session, eecute  query returning one line

       Throw an exeception of if in None or multi-row.
   """
   dbh = coreutils.DesDbi(os.path.join(os.getenv("HOME"),".desservices.ini"),section)
   cur = dbh.cursor()
   cur.execute(query)
   row = cur.fetchall()
   print row
   if len(row) != 1:
      errtxt = "expected one row,  got %s rows : query : %s" % (len(row), query)
      raise X(errtxt)
   dbh.close()
   return row[0]

#
#@Monitor('desar_httpd_cpu', value_type='int')
#
def read_requests(section):
   """ return the GB read from disk  for all queries """
   q = """SELECT 
             sys_context('userenv','db_name'), 
             SUM(SMALL_read_megabytes), 
             SUM(LARGE_read_megabytes)
           FROM 
             GV$IOSTAT_FILE
           """
   (dbname, small_reads, 
    large_reads) =_query_one_row(q,  section)
   reads  = (small_reads  + large_reads)/1024
   return reads 

def write_requests(section):
   """ return the GB read from disk  for all queries """
   q = """SELECT 
             sys_context('userenv','db_name'), 
             SUM(SMALL_WRITE_megabytes), 
             SUM(LARGE_WRITE_megabytes) 
           FROM 
             GV$IOSTAT_FILE
           """
   (dbname, small_writes, 
    large_writes) =_query_one_row(q,  section)
   writes = (small_writes + large_writes)/1024
   return writes


def mydb_GB(section):
   "return the total GB of allocated mydb data table space for a schema"
   q = """SELECT  
           sys_context('userenv','db_name'), 
           sum(BYTES)/1024/1024/1024  
          from 
            DBA_SEGMENTS 
         where 
            tablespace_name = 'USERS_BIG'"""
   (dbname, mytablespace) = _query_one_row(q,  section)
   # can be none if no space used.
   if not mytablespace :  mytablespace = 0  
   return mytablespace

if __name__ == "__main__":

   main()

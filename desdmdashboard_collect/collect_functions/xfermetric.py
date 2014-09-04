"""
file transfer metrics.

For each site, a metric related to to
the average transfer rates to/ftom
that site in the last 24 hours.
"""



def getTransferSummary(exec_host_pattern, dbh, args):
   cur = dbh.cursor()
   query = """select
            /* this  computes durations there's no interval arithmetic in ORACLE */
            numtodsinterval(
               sum (
                      extract (day    from (t.end_time - t.start_time)) * 86400
                    + extract (hour   from (t.end_time - t.start_time)) *  3600
                    + extract (minute from (t.end_time - t.start_time)) *    60
                    + extract (second from (t.end_time - t.start_time))
            ), 'SECOND') tota_second,
            sum(b.total_num_bytes) total_bytes,
            sum(b.total_num_files) total_files,
            b.transfer_class
         from
            prod.task t, prod.transfer_batch b
          where
              t.info_table = 'transfer_batch'
            and
              t.id = b.task_id
            and
              t.status = 0
            and
              t.start_time > sysdate-1
            and
             t.exec_host like '%s'
            group by
              b.transfer_class

        """  % exec_host_pattern
   q=rc.Q(dbh, query, args)
   rows = q.query_via_cache().fetchall()
   for duration, bytes, files, method in rows:
      print (bytes/1000./1000)/duration.total_seconds(), method
   return rows


import os
import sys
import time
import argparse
import coreutils
import cx_Oracle #needed to catch execptions
import reportcommon as rc
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('--section','-s',default='db-desoper',
             help='section in the .desservices file w/ DB connection information')
parser.add_argument('--debug','-d',help='print debug info', default=False, action='store_true')
args = parser.parse_args()
dbh = coreutils.DesDbi(os.path.join(os.getenv("HOME"),".desservices.ini"),'db-desoper')
cur = dbh.cursor()
data = getTransferSummary("%fnal.gov", dbh, args)
data = getTransferSummary("%cosmology%", dbh, args)
data = getTransferSummary("%nersc%", dbh, args)
for d in data :
   print d


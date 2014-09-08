"""
file transfer metrics.

For each site, a metric related to to
the average transfer rates to/ftom
that site in the last 24 hours.
"""

from desdmdashboard_collect.collect_utils.database import make_db_query



def getTransferSummary(exec_host_pattern):
    '''
    '''
    
    QUERY = """
                SELECT
                /* this  computes durations there's no interval arithmetic */
                /* in ORACLE */
                    NUMTODSINTERVAL(
                        SUM (
                               EXTRACT(day FROM (t.end_time - t.start_time))*86400
                             + EXTRACT(hour FROM(t.end_time - t.start_time))*3600
                             + EXTRACT(minute FROM(t.end_time - t.start_time))*60
                             + extract (second from (t.end_time - t.start_time))
                        ), 'SECOND') total_second,
                        SUM(b.total_num_bytes) total_bytes,
                        SUM(b.total_num_files) total_files,
                        b.transfer_class
                FROM
                    prod.task t, prod.transfer_batch b
                WHERE 
                    t.info_table = 'transfer_batch'
                AND
                    t.id = b.task_id
                AND
                    t.status = 0
                AND
                    t.start_time > sysdate-1
                AND
                    t.exec_host LIKE '%{exec_host_pattern}%'
                GROUP BY
                    b.transfer_class
            """

    recs = make_db_query(QUERY.format(exec_host_pattern=exec_host_pattern),
            section='db-desoper')

    for duration, bytes, files, method in recs:
        print 'duration: ', duration, 'bytes: ', bytes, 'files: ', files
        print (bytes/1000./1000)/duration.total_seconds(), method
	# rate 43.678792696   bytes:  175367191553 files:  3402

    return recs


if __name__ == '__main__':

    getTransferSummary('fnal.gov')

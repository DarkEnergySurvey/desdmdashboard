"""
file transfer metrics.

For each site, a metric related to to
the average transfer rates to/ftom
that site in the last 24 hours.
"""

import json

from desdmdashboard_remote import http_requests
from desdmdashboard_remote.senddata.functions import send_metric_data

from desdmdashboard_collect.collect_utils import log, database

logger = log.get_logger('desdmdashboard_collect')

BASE_NAME = 'TransferSummary'
NAME_PATTERN = BASE_NAME+'_{site}_{met}_{metric}'


def transfer_summary(exec_host_pattern):
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

    data_to_send = {}

    logger.info('getting existing metrics from database.')

    tsmetricnames = get_transfer_summary_metricnames_from_desdmdashboard(
            exec_host_pattern)
    logger.info('{n} metrics do already exist.'.format(n=len(tsmetricnames)))

    # we have to send at least an empty value for the ones that do exist
    # already for this site 
    for metr in tsmetricnames:
        data_to_send[metr] = {
                'name' : metr, 
                'value' : '',
                'value_type' : '',
                'logger' : logger,
                }

    logger.info('executing db query.')

    recs = database.make_db_query(
            QUERY.format(exec_host_pattern=exec_host_pattern),
            section='db-desoper')

    logger.info('{n} row returned. now sending rows to db.'.format(
        n=len(recs)))


    for duration, bytes, files, method in recs:

        for metric_type in ['rate', 'Mbytes', 'files', ]:
            metric_name = NAME_PATTERN.format(
                site=exec_host_pattern,
                met=method.rsplit('_')[-1],
                metric=metric_type)

            if metric_type == 'rate':
                val = (bytes/1000./1000.)/duration.total_seconds()
            elif metric_type == 'Mbytes':
                val = bytes/1000./1000.
            elif metric_type == 'files':
                val = files

            data_to_send.update(
                    { metric_name : {
                        'name': metric_name,
                        'value': val,
                        'value_type': 'float',
                        'logger': logger,
                        },
                        })

    # now that we aggregated all data we want to send, we do it!
    for data in data_to_send.values():
        print data
        #_ = send_metric_data(**data)


def get_transfer_summary_metricnames_from_desdmdashboard(exec_host_pattern):
    '''
    '''
    search_pattern = BASE_NAME+'_{e_h_p}'

    req = http_requests.Request()
    req.GET(url=http_requests.POST_URL,
        params={
            'name': search_pattern.format(e_h_p=exec_host_pattern),
            'format': 'json',
            'owner': 'gdaues'
            }
        )
    
    tsmetrics = json.loads(req.response.read())
    tsmetricnames = [d['name'] for d in tsmetrics]

    return tsmetricnames



if __name__ == '__main__':

    transfer_summary('fnal.gov')

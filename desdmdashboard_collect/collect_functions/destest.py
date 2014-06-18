'''
DESDMDASHBOARD DATA COLLECTION FUNCTIONS


:: Author :: michael.graber@fhnw.ch
'''

from desdmdashboard_remote.senddata.functions import send_metric_value 
from desdmdashboard_collect.collect_utils.database import make_db_query

from desdmdashboard_collect.collect_utils import log 
logger = log.get_logger('desdmdashboard_collect')

def file_archive_info__sum_filesize__archive_name():
    '''
    '''

    QUERY = '''
        SELECT archive_name, SUM(filesize)
        FROM file_archive_info
        GROUP BY archive_name
        '''

    logger.debug('executing db query')
    try:
        records = make_db_query(QUERY, section='db-destest')
    except:
        logger.debug('db query not successfull')

    for record in records:

        archive_name = record[0]
        archive_size = record[1]

        metric_name = 'size '+archive_name

        logger.debug('sending value for metric %s to db' % metric_name)
        req = send_metric_value(metric_name, archive_size, value_type='int')
        if req.error_status[0]:
            logger.debug(req.error_status[1])
        
    return


if __name__ == '__main__':
    file_archive_info__sum_filesize__archive_name()


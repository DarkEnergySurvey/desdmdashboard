'''
DESDMDASHBOARD DATA COLLECTION FUNCTIONS


:: Author :: michael.graber@fhnw.ch
'''

from coreutils import DesDbi

from desdmdashboard_remote.senddata.functions import send_metric_value 
from desdmdashboard_collect.collect_utils.database import make_db_query


def file_archive_info__sum_filesize__archive_name():
    '''
    '''

    QUERY = '''
        SELECT archive_name, SUM(filesize)
        FROM file_archive_info
        GROUP BY archive_name
        '''

    records = make_db_query(QUERY, section='db-destest')

    for record in records:

        archive_name = record[0]
        archive_size = record[1]

        metric_name = 'size '+archive_name

        req = send_metric_value(metric_name, archive_size, value_type='int')
        
    return


if __name__ == '__main__':
    file_archive_info__sum_filesize__archive_name()

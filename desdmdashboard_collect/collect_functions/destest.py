'''
DESDMDASHBOARD DATA COLLECTION FUNCTIONS


:: Author :: michael.graber@fhnw.ch
'''

from coreutils import DesDbi

from desdmdashboard_remote.senddata.decorators import Monitor

from ..collect_utils.database import make_db_query


#@Monitor('file_archive_info__file_size__archive_name')
def file_archive_info__sum_filesize__archive_name():
    '''
    '''

    QUERY = '''
        SELECT archive_name, SUM(filesize)
        FROM file_archive_info
        GROUP BY archive_name
        '''

    records = make_db_query(QUERY, section='db-destest')

    return records


if __name__ == '__main__':
    file_archive_info__sum_filesize__archive_name()


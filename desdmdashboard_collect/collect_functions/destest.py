'''
DESDMDASHBOARD DATA COLLECTION FUNCTIONS


:: Author :: michael.graber@fhnw.ch
'''

from ..collect_utils import database

from desdmdashboard_remote.senddata.decorators import Monitor


#@Monitor('file_archive_info__file_size__archive_name')
def file_archive_info__sum_filesize__archive_name():
    '''
    '''
    QUERY = '''
            SELECT archive_name, SUM(filesize)
                FROM file_archive_info
                GROUP BY archive_name
            '''
    
    records = database.make_db_query(QUERY, section='db-destest')




'''
'''
import os
import coreutils

from collect_utils import log
logger = log.get_logger('desdmdashboard_collect')

def make_db_query(QUERY,
        desfile=os.path.join(os.environ['HOME'], '.desservices.ini'),
        section=None):
    '''
    Funtion opens a DB connection, gets a cursor, executes the QUERY,
    and return all records.
    
    '''
    with coreutils.DesDbi(desfile=desfile, section=section) as dbh:
        cursor = dbh.cursor()
        records = cursor.execute(QUERY).fetchall()

    if not records:
        logger.warning('empty record set returned: %s' % records)

    return records

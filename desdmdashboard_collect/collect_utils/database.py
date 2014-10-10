'''
DESDMDashboard data collection utility database functions

'''

import os
import coreutils
from coreutils import serviceaccess

from desdmdashboard_collect.collect_utils import log

try:
    logger = log.get_logger('desdmdashboard_collect')
except:
    logger = None


class DataCollectionErrorDB(Exception):
    pass


def make_db_query(QUERY,
        desfile=os.path.join(os.environ['HOME'], '.desservices.ini'),
        section=None):
    '''
    Funtion opens a DB connection, gets a cursor, executes the QUERY,
    and return all records.
    '''
    with coreutils.DesDbi(desfile=desfile, section=section) as dbh:
        logger.debug('DesDbi database handler intantiated.')
        cursor = dbh.cursor()
        records = cursor.execute(QUERY).fetchall()
        logger.debug('Query executed.')

    if logger and not records:
        logger.warning('empty record set returned: %s' % records)
        logger.debug('.desservices.ini section %s' % section)
        logger.debug('QUERY : %s' % QUERY )

    return records


def query_one_row(QUERY, 
        desfile=os.path.join(os.environ['HOME'], '.desservices.ini'),
        section=None):
    '''
    Funtion opens a DB connection, gets a cursor, executes the QUERY, 
    expects exactly one row to be returned, raises Exception otherwise.
    '''
    recs = make_db_query(QUERY, desfile=desfile, section=section)
    
    if len(recs) != 1:
        err = 'Exactly one row expected, got {nr} rows instead!\nQUERY:{Q}'
        if logger:
            logger.error(err.format(nr=len(recs), Q=QUERY))
        else:
            raise DataCollectionErrorDB(err.format(nr=len(recs), Q=QUERY))

    return recs[0]


def get_db_name(section, desfile=os.path.join(os.getenv("HOME"),".desservices.ini")):
   db_name = serviceaccess.parse(desfile, section)["name"]
   return db_name

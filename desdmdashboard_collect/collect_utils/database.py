'''
'''
import os

import coreutils

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
    return records

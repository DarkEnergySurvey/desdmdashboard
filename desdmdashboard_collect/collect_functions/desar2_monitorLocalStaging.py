'''
DESDMDASHBOARD DATA COLLECTION FUNCTION example : monitor local staging area disk usage 

:: Author :: daues@illinois.edu
'''

from desdmdashboard_remote.senddata import decorators 

from desdmdashboard_collect.collect_utils.commandline import du_dir_Mb

from desdmdashboard_collect.collect_utils import log 

logger = log.get_logger('desdmdashboard_collect')


def create_local_staging_name(path):
    return 'desar2 : du ' + path

@decorators.Monitor(create_local_staging_name, value_type='int', logger=logger)
def monitor_local_staging_via_du(path):
    '''
    '''
    logger.info('monitor_local_staging_via_du entered.')
    logger.info('executing du on '+path)

    try:
        du_return = du_dir_Mb(path=path)
        logger.info('du_dir_Mb successfully executed.')
    except Exception, err:
        logger.error('du_dir_Mb failed: '+err)

    return du_return


if __name__ == '__main__':
    monitor_local_staging_via_du('~/')

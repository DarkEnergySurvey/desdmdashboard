'''
DESDMDASHBOARD DATA COLLECTION FUNCTION example : monitor local staging area disk usage 

:: Author :: daues@illinois.edu
'''

from desdmdashboard_remote.senddata.functions import send_metric_value 

from collect_utils.commandline import shell_command
from collect_utils.commandline import du_dir_Mb

from collect_utils import log 

logger = log.get_logger('desdmdashboard_collect')

def monitor_local_staging_via_du():
    '''
    '''
    logger.info('monitor_local_staging_via_du entered.')

    logger.info('executing du')

    try:
        records = du_dir_Mb(path='/local/Staging')
        logger.info('du_dir_Mb successfully executed.')
    except:
        logger.error('du_dir_Mb not successfull.')
	return

    for record in records:

        logger.info("write records:")
        logger.info(str(records))

        # archive_name = record[0]
        # archive_size = record[1]

        # metric_name = 'size '+archive_name

        # logger.info('sending value for metric %s to db' % metric_name)

        # req = send_metric_value(metric_name, archive_size, value_type='int')

        # if req.error_status[0]:
        #     logger.error(req.error_status[1])
        
    return


if __name__ == '__main__':
    monitor_local_staging_via_du()


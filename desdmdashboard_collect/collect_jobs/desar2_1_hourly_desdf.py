'''
DESDMDASHBOARD DATA COLLECTION JOB SCRIPT

A python script to be executed on a regular basis for the collection of
timestamped data in the DESDMDASHBOARD.

All functions that are supposed to be executed when this file is run have to be
called in main().

$ crontab -e
07 0,4,8,12,16,20 * * * /desdmdashboard_collect/desdmdashboard_collect/collect_cron_job /desdmdashboard_collect/desdmdashboard_collect/collect_jobs/4_hourly.py

general crontab syntax:

 +---------------- minute (0 - 59)
 |  +------------- hour (0 - 23)
 |  |  +---------- day of month (1 - 31)
 |  |  |  +------- month (1 - 12)
 |  |  |  |  +---- day of week (0 - 6) (Sunday=0 or 7)
 |  |  |  |  |
 *  *  *  *  *  command to be executed

:: Author :: michael.graber@fhnw.ch
'''

from desdmdashboard_collect.collect_utils import log 
logger = log.get_logger('desdmdashboard_collect')

from desdmdashboard_collect.collect_functions.desar2_desdf_metrics\
        import measure_desdf


def main():
    measure_desdf() 
    

if __name__ == '__main__':
    logger.info('Start 1 hourly measure_desdf data collection script.')
    main()
    logger.info('1 hourly measure_desdf data collection script finished.')

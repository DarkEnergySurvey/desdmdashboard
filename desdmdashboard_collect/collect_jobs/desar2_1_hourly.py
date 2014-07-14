

from collect_utils import log 
logger = log.get_logger('desdmdashboard_collect')


from collect_functions.system_metrics import sick_httpd


def main():
    sick_httpd()
    

if __name__ == '__main__':
    logger.info('Start 1 hourly data collection script.')
    main()
    logger.info('1 hourly data collection script finished.')

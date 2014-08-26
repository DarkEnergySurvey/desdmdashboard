

from desdmdashboard_collect.collect_utils import log
logger = log.get_logger('desdmdashboard_collect')


# from desdmdashboard_collect.collect_functions.system_metrics import sick_httpd
# from desdmdashboard_collect.collect_functions.desar2_iosystem import stken_connections
# from desdmdashboard_collect.collect_functions.desar2_iosystem import fermigrid_connections
# from desdmdashboard_collect.collect_functions.desar2_iosystem import noao_connections
# from desdmdashboard_collect.collect_functions.desar2_iosystem import gpfs_connections
from desdmdashboard_collect.collect_functions.desar2_iosystem import any_connections

def main():
    any_connections()
    

if __name__ == '__main__':
    logger.info('Start 1 hourly data collection script. (any-connections) ')
    main()
    logger.info('1 hourly data collection script finished. (any-connections)')

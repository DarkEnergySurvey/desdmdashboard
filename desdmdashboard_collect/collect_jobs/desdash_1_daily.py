

from desdmdashboard_collect.collect_utils import log
logger = log.get_logger('desdmdashboard_collect')


from desdmdashboard_collect.collect_functions.xfermetric import transfer_summary


def main():
    transfer_summary('fnpc', 'fermigrid')
    transfer_summary('fermicloud', 'fermicloud')
    transfer_summary('cosmology.illinois.edu', 'cosmology')
    transfer_summary('128.55', 'nersc')
    transfer_summary('iforge', 'iforge')


if __name__ == '__main__':
    logger.info('Start 1 daily data collection script.')
    main()
    logger.info('1 daily data collection script finished.')

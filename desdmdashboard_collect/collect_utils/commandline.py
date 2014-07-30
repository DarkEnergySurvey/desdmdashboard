'''
DESDMDashboard data collection utility database functions

'''

import subprocess

try:
    from desdmdashboard_collect.collect_utils import log
    logger = log.get_logger('desdmdashboard_collect')
except:
    logger = None


class DataCollectionCommandLineError(Exception):
    pass


def shell_command(cmd):
    if logger:
        logger.info('Executing shell command through subprocess module.')
        logger.debug('command: ' + ' '.join(cmd))
    p = subprocess.Popen(cmd, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if logger and err:
        logger.error(err)
    elif err:
        raise DataCollectionCommandLineError(err)
    return out, err


def du_dir_Mb(path):
    out, err = shell_command('du -s -m ' + path)
    if err:
        raise DataCollectionCommandLineError(err)
    out = out.rsplit('\n')
    return out[0].rsplit('\t')[0]

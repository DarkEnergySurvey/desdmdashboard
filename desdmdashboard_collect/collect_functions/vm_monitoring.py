'''

# load average, ie 2nd line in top
Load Avg: 1.50, 1.33, 1.39 # number of process waiting to be computed
# with number of processes indicator for cpu load
# threshold at 2x num processors
uptime

# num processors: 
/proc/cpuinfo

# memory:
/proc/meminfo
# amount of available memory, point of excessive swaping detection
# threshold

# filesystem:
df with filter negative type via mount

# network load 

# open ports
netstat

# disk usage
iostat

'''

import sys
import socket
import multiprocessing

from desdmdashboard_remote.senddata.decorators import Monitor
from desdmdashboard_remote.senddata.functions import send_metric_data

from desdmdashboard_collect.collect_utils import log, commandline


logger = log.get_logger('desdmdashboard_collect')

BASE_NAME = 'VM'

HOSTNAME = socket.gethostname()
METRIC_NAME_PATTERN = '_'.join([BASE_NAME, HOSTNAME, '{measure}'])

PLATFORM = sys.platform


class PlatformError(Exception):
    pass


def is_valid_platform():
    '''
    VMs to be monitored are supposed to be linux machines.
    '''
    if 'linux' in PLATFORM:
        return True
    else:
        return False

# -----------------------------------------------------------------------------
# AVG LOAD
# -----------------------------------------------------------------------------

def avg_load(logger=logger):
    '''
    The 15min average load.
    '''
    try:
        out, err = commandline.shell_command('uptime', logger=logger)
    except:
        raise
    if err:
        return

    fifteen_min_average = float(out.replace('\n', '').rsplit(' ')[-1])
    return fifteen_min_average


@Monitor(METRIC_NAME_PATTERN.format(measure='avg-load-per-cpu'), value_type='float', logger=logger)
def avg_load_per_cpu(logger=logger):
    '''
    The 15min average load divided by the number of processors.
    '''
    return avg_load(logger=logger)/multiprocessing.cpu_count()


# -----------------------------------------------------------------------------
# PROC MEMINFO 
# -----------------------------------------------------------------------------

PROC_MEMINFO_FIELDS = (
            
            # info on /proc/meminfo:
            # http://superuser.com/questions/521551/cat-proc-meminfo-what-do-all-those-numbers-mean

            'MemTotal', # Total amount of physical RAM, in kilobytes.
            'MemFree', # The amount of physical RAM, in kilobytes, left unused by the system.
            'Buffers', # The amount of physical RAM, in kilobytes, used for file buffers.
            'Cached', # The amount of physical RAM, in kilobytes, used as cache memory.
            'SwapCached', # The amount of swap, in kilobytes, used as cache memory.
            'Active', # The total amount of buffer or page cache memory, in kilobytes, that is in active use. This is memory that has been recently used and is usually not reclaimed for other purposes.
            'Inactive', # The total amount of buffer or page cache memory, in kilobytes, that are free and available. This is memory that has not been recently used and can be reclaimed for other purposes.
          # 'Active(anon)',
          # 'Inactive(anon)',
          # 'Active(file)',
          # 'Inactive(file)',
          # 'Unevictable',
          # 'Mlocked', 
            'SwapTotal', # The total amount of swap available, in kilobytes.
            'SwapFree', #  The total amount of swap free, in kilobytes.
          # 'Dirty',
          # 'Writeback',
          # 'AnonPages',
          # 'Mapped',
          # 'Shmem',
          # 'Slab',
          # 'SReclaimable',
          # 'SUnreclaim',
          # 'KernelStack',
          # 'PageTables',
          # 'NFS_Unstable',
          # 'Bounce',
          # 'WritebackTmp',
          # 'CommitLimit',
          # 'Committed_AS',
          # 'VmallocTotal',
          # 'VmallocUsed',
          # 'VmallocChunk',
          # 'HardwareCorrupted',
          # 'AnonHugePages',
          # 'HugePages_Total',
          # 'HugePages_Free',
          # 'HugePages_Rsvd',
          # 'HugePages_Surp',
          # 'Hugepagesize',
          # 'DirectMap4k',
          # 'DirectMap2M',
        )


def proc_meminfo(logger=logger):

    logger.info('reading /proc/meminfo')
    with open('/proc/meminfo', 'r') as fid:
        meminfo = fid.readlines()

    meminfo = [[el for el in l.replace('\n', '').replace(':', '').rsplit(' ') if el]\
            for l in meminfo if l]
    meminfo = { m[0]: int(m[1]) for m in meminfo }

    for metric in PROC_MEMINFO_FIELDS:

        data = {
                'name' : METRIC_NAME_PATTERN.format(measure=metric), 
                'value' : meminfo[metric],
                'value_type' : 'int',
                'logger' : logger,
                }

        _ send_metric_data(**data)

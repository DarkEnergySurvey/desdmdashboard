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

import re
import os
import sys
import socket
import multiprocessing
import json

from desdmdashboard_remote.senddata.decorators import Monitor
from desdmdashboard_remote.senddata.functions import send_metric_data

from desdmdashboard_collect.collect_utils import log, commandline, tmp


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

            # Total amount of physical RAM, in kilobytes.
            'MemTotal', 

            # The amount of physical RAM, in kilobytes, left unused by the
            # system.
            'MemFree',

            # The amount of physical RAM, in kilobytes, used for file buffers.
            'Buffers',

            # The amount of physical RAM, in kilobytes, used as cache memory.
            'Cached',

            # The amount of swap, in kilobytes, used as cache memory.
            'SwapCached',

            # The total amount of buffer or page cache memory, in kilobytes,
            # that is in active use. This is memory that has been recently used
            # and is usually not reclaimed for other purposes.
            'Active',
            
            # The total amount of buffer or page cache memory, in
            # kilobytes, that are free and available. This is memory that has
            # not been recently used and can be reclaimed for other purposes.
            'Inactive', 

          # 'Active(anon)', 'Inactive(anon)', 'Active(file)', 'Inactive(file)',
          # 'Unevictable', 'Mlocked', 

            # The total amount of swap available, in kilobytes.
            'SwapTotal', 

            #  The total amount of swap free, in kilobytes.
            'SwapFree', 

          # 'Dirty', 'Writeback', 'AnonPages', 'Mapped', 'Shmem', 'Slab',
          # 'SReclaimable', 'SUnreclaim', 'KernelStack', 'PageTables',
          # 'NFS_Unstable', 'Bounce', 'WritebackTmp', 'CommitLimit',
          # 'Committed_AS', 'VmallocTotal', 'VmallocUsed', 'VmallocChunk',
          # 'HardwareCorrupted', 'AnonHugePages', 'HugePages_Total',
          # 'HugePages_Free', 'HugePages_Rsvd', 'HugePages_Surp',
          # 'Hugepagesize', 'DirectMap4k', 'DirectMap2M',
        )


def proc_meminfo(logger=logger, platform=PLATFORM):

    if not is_valid_platform():
        logger.info('cannot read /proc/meminfo on this platform: ' + PLATFORM)
        return

    logger.info('reading /proc/meminfo')
    with open('/proc/meminfo', 'r') as fid:
        meminfo = fid.readlines()

    meminfo = [[el for el in l.replace('\n', '').replace(':', '').rsplit(' ') if el]\
            for l in meminfo if l]
    meminfo = { m[0]: int(m[1]) for m in meminfo }

    for metric in PROC_MEMINFO_FIELDS:

        data = {
                'name' : METRIC_NAME_PATTERN.format(measure='meminfo-'+metric), 
                'value' : meminfo[metric],
                'value_type' : 'int',
                'logger' : logger,
                }

        _ = send_metric_data(**data)


# -----------------------------------------------------------------------------
# DISK SPACE
# -----------------------------------------------------------------------------

def disk_space(logger=logger):

    logger.info('evaluating disk space')

#   try:
#       mounts, err = commandline.shell_command('mount', logger=logger)
#   except:
#       raise
#   if err:
#       return

#   mounts = [line for line in mounts.rsplit('\n') if line]
#   mounts = [[el for el in line.rsplit(' ') if el] for line in mounts]

#   mounts = [{'name': line[0], 'path': line[2], 'type': line[4]} for line in mounts]

    try:
        # discard (-x) fs of type iso9660 (cd) and tmpfs
        df, err = commandline.shell_command('df -T -x iso9660 -x tmpfs --block-size 1000', logger=logger)

        '''
	    $ df -T -x iso9660 -x tmpfs --block-size 1000
	    Filesystem           Type 1kB-blocks     Used Available Use% Mounted on
	    /dev/mapper/vg_michael-lv_root
                     	     ext4   12623987 10258822   2236945  83% /
	    /dev/sda1            ext4     507745   113087    368444  24% /boot
        '''

    except:
        raise
    if err:
        return

    df = [[el for el in line.rsplit(' ') if el] for line in df.rsplit('\n') if line]

    # the first line is the header, see above
    header = df[0]
    # 'Mounted on' is split in two elements
    header[-2] = ' '.join(header[-2:])
    header = header[:-1]

    i = 1
    dfs = []
    while i < len(df):
        els = df[i]
        while len(els) < len(header):
            els.extend(df[i+1])
            i += 1
        dfs.append(dict(zip(header, els)))
        i += 1

    for fs in dfs:

        for m in ['1kB-blocks', 'Used', 'Available', ]:
            mname = METRIC_NAME_PATTERN.format(measure='df-'+fs['Filesystem']+'-'+m)
            data = {
                    'name' : mname, 
                    'value' : int(fs[m]),
                    'value_type' : 'int',
                    'logger' : logger,
                    }

            _ = send_metric_data(**data)


# -----------------------------------------------------------------------------
# NETWORK LOAD 
# -----------------------------------------------------------------------------
@Monitor(METRIC_NAME_PATTERN.format(measure='tcp-connections'), value_type='int', logger=logger)
def established_tcp_connections():
    ''' the number of currently established tcp connections '''
    try:
        netstat, err = commandline.shell_command(
                'netstat --tcp | grep ESTABLISHED', logger=logger)
    except:
        raise
    if err:
        return

    # split lines
    netstat = [l for l in netstat.rsplit('\n') if l]
    return len(netstat)


def network_io():
    '''network io summary'''

    DISCARD_NETWORK_INTERFACES_REGEXP = [
            'docker', # do not monitor the docker host
            'virbr', # do not monitor the virtual bridge interface
            'lo', # do not monitor loopback interfaces
            ]

    # check the platform
    if not is_valid_platform():
        logger.info('cannot read /proc/net/dev on this platform: ' + PLATFORM)
        return

    # setup the tmp directory where we store older states
    TMP_FILE = '~/.desdmdashboard_collect/tmp/network_io.json'
    if not os.path.exists(os.path.dirname(TMP_FILE)):
        os.makedirs(os.path.dirname(TMP_FILE))

    # read the /proc file
    logger.info('reading /proc/meminfo')
    with open('/proc/net/dev', 'r') as fid:
        netdev = fid.readlines()

    '''
    -bash-4.1$ cat /proc/net/dev
    Inter-|   Receive                                                |  Transmit
     face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed
        lo:52492637  399164    0    0    0     0          0         0 52492637  399164    0    0    0     0       0          0
      eth1:26403780235 24842946    0    0    0     0          0    774878 10839841500 19304623    0    0    0     0       0          0
    docker0:       0       0    0    0    0     0          0         0      468       6    0    0    0     0       0          0
    virbr0:       0       0    0    0    0     0          0         0        0       0    0    0    0     0       0          0
    virbr0-nic:       0       0    0    0    0     0          0         0        0       0    0    0    0     0       0          0
    '''

    header = [
            'rec-bytes', 'rec-packets', 'rec-errs', 'rec-drop', 'rec-fifo',
            'rec-frame', 'rec-compressed', 'rec-multicast',
            'trans-bytes', 'trans-packets', 'trans-errs', 'trans-drop',
            'trans-fifo', 'trans-colls', 'trans-carrier', 'trans-compressed',
            ]

    interfaces = {}

    for line in netdev[2:]:
        lineels = [el for el in line.replace('\n', '').rsplit(' ') if el]
        interfaces[lineels[0].replace(':', '')] = dict(zip(header, [int(el) for el in lineels[1:]]))

    # try to find data in an existing tmpfile
    if os.path.exists(TMP_FILE):
        with open(TMP_FILE, 'r') as tmpfile:
            olddata = json.loads(tmpfile.read())
    else:
        olddata = None

    # write data to tmp file
    json_data = json.dumps(interfaces) 
    with open(TMP_FILE, 'w') as tmpfile:
        tmpfile.write(json_data)

    # now calculate and send the diff values of new - old 
    for name, ifdata in interfaces.items():
        diss = []
        for dis in DISCARD_NETWORK_INTERFACES_REGEXP:
            diss.append(re.match(dis, name))
        if any(diss):
            continue

        for measure in ['trans-bytes', 'rec-bytes', ]:
            datapoint = ifdata[measure] - olddata[name][measure]
            if datapoint < 0:
                message = 'negative diff value new-old for interface {interf}, {dp}'
                logger.info(message.format(interf=name, dp=datapoint))
                continue

            mname = METRIC_NAME_PATTERN.format(measure='networkIO:_'+name+'_'+measure)
            data = {
                    'name' : mname, 
                    'value' : int(datapoint),
                    'value_type' : 'bytes',
                    'logger' : logger,
                    }

            _ = send_metric_data(**data)


# -----------------------------------------------------------------------------
# CPU STATS
# -----------------------------------------------------------------------------
def iostat_cpu():
    '''
    '''
    try:
        # discard (-x) fs of type iso9660 (cd) and tmpfs
        iostatc, err = commandline.shell_command('iostat -c', logger=logger)
    except:
        raise
    if err:
        return

    iostatc = [l for l in iostatc.rsplit('\n') if l][1:]
    header = [el for el in iostatc[0].rsplit(' ') if el][1:]
    data = [el for el in iostatc[1].rsplit(' ') if el]

    iostatc = dict(zip(header, data))

    for stat in iostatc:

        mname = METRIC_NAME_PATTERN.format(measure='iostatc-'+stat)
        data = {
                'name' : mname, 
                'value' : float(iostatc[stat]),
                'value_type' : 'float',
                'logger' : logger,
                }

        _ = send_metric_data(**data)




# -----------------------------------------------------------------------------
# MAIN 
# -----------------------------------------------------------------------------

if __name__ == '__main__':

    print 'nothing done here'

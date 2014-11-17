'''
DESDMDASHBOARD DATA COLLECTION FUNCTIONS


:: Author :: michael.graber@fhnw.ch
'''

from desdmdashboard_remote.senddata import functions

from desdmdashboard_collect.collect_utils import log 
logger = log.get_logger('desdmdashboard_collect')

STATS = [
            'total memory',
            'used memory',
            'active memory',
            'inactive memory',
            'free memory',
            'buffer memory',
            'swap cache',
            'total swap',
            'used swap',
            'free swap',
            'non-nice user cpu ticks',
            'nice user cpu ticks',
            'system cpu ticks',
            'idle cpu ticks',
            'IO-wait cpu ticks',
            'IRQ cpu ticks',
            'softirq cpu ticks',
            'stolen cpu ticks',
            'pages paged in',
            'pages paged out',
            'pages swapped in',
            'pages swapped out',
            'interrupts',
            'CPU context switches',
            'boot time',
            'forks',
        ]

if __name__ == '__main__':
    pass

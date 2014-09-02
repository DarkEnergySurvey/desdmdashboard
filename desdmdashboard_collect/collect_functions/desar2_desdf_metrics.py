"""
feeding the output of the desdf cluster command into the desdmdashboard

"""

import os
from desdmdashboard_remote.senddata.functions import send_metric_data
from desdmdashboard_collect.collect_utils import log, database

from desdmdashboard_collect.collect_utils import commandline

logger = log.get_logger('desdmdashboard_collect')


def measure_desdf():

    logger.info('Measuring desdf')
    desdfoutput, err = commandline.shell_command(['desdf', ])
    
    if err:
        logger.error(err)

    for desdfline in desdfoutput.rsplit('\n')[1:]:
        if not desdfline:
            continue
        linels = [el for el in desdfline.rsplit(' ') if el]

        name = linels[0].rsplit('/')[-1]
        size = 1024*float(linels[1])/10.**12 
        used = 1024*float(linels[2])/10.**12 
        avail = 1024*float(linels[3])/10.**12 

#       print 
#       print 'NAME: ', name
#       print 'size: ', size
#       print 'used: ', used
#       print 'avail: ', avail

        _ = send_metric_data(name='desdf_'+name+'_size', value=size,
                value_type='float', logger=logger)
        _ = send_metric_data(name='desdf_'+name+'_avail', value=avail,
                value_type='float', logger=logger)
        _ = send_metric_data(name='desdf_'+name+'_used', value=used,
                value_type='float', logger=logger)


if __name__ == '__main__':

    measure_desdf()



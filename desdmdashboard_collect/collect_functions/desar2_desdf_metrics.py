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
    desdfoutput, err = commandline.shell_command(['/usr/local/bin/desdf', ])
    
    if err:
        logger.error(err)

    for desdfline in desdfoutput.rsplit('\n')[1:]:
        if not desdfline:
            continue
        linels = [el for el in desdfline.rsplit(' ') if el]

        name = linels[0].rsplit('/')[-1]
        if linels[1][-1] == 'T': linels[1] = linels[1][:-1]
        if linels[2][-1] == 'T': linels[2] = linels[2][:-1]
        if linels[3][-1] == 'T': linels[3] = linels[3][:-1]
        size = float(linels[1])
        used = float(linels[2]) 
        avail = float(linels[3]) 

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



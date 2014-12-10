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

        measures = {
                'size': None,
                'avail': None,
                'used': None,
                }

        for elidx, meas in ((1, 'size'), (2, 'used'), (3, 'avail'), ):

            if linels[elidx][-1] == 'T':
                measures[meas] = float(linels[elidx][:-1])
            elif linels[elidx][-1] == 'G':
                measures[meas] = 0.001*float(linels[elidx][:-1])
            else:
                logger.error('cannot handle disk space specified in ' + linels[elidx][-1])
                logger.debug(desdfline)
                continue

#       print 
#       print 'NAME: ', name
#       print 'size: ', size
#       print 'used: ', used
#       print 'avail: ', avail

        _ = send_metric_data(name='desdf_'+name+'_size', value=measures['size'],
                value_type='float', logger=logger)
        _ = send_metric_data(name='desdf_'+name+'_avail', value=measures['avail'],
                value_type='float', logger=logger)
        _ = send_metric_data(name='desdf_'+name+'_used', value=measures['used'],
                value_type='float', logger=logger)


if __name__ == '__main__':

    measure_desdf()



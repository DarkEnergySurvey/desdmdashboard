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
        if not desfline:
            continue
        linels = [el for el in desdfline.rsplit(' ') if el]

        name = linels[0].rsplit('/')[-1]
        size = lineels[1] # TODO : conversion
        used = linels[2] # TODO : conversion
        avail = lineels[3] # TODO : conversion
        use_percents = int(linels[4][:-1])
        mounts = linels[5:]

        _ = send_metric_data(name='desdf_'+name+'_size', value=size,
                logger=logger)
        _ = send_metric_data(name='desdf_'+name+'_avail', value=avail,
                logger=logger)
        _ = send_metric_data(name='desdf_'+name+'_used', value=used,
                logger=logger)

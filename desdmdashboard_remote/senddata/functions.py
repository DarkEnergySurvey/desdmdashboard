'''
'''

from utils import DATA_TEMPLATE
from ..http_requests import Request


def send_metric_data(**kwargs):
    '''
    Send any of the possible arguments to the DESDMDASHBOARD db as kwargs of
    this function.

    Returns a request object.
    '''

    logger = kwargs.pop('logger', None)

    data = DATA_TEMPLATE.copy()
    data.update(kwargs)

    if self.logger:
        mess = 'Sending value {val} to metric {met}'
        self.logger.info(mess.format(
            val=data['value'], met=data['name'])
            )

    request = Request()
    request.POST(data=data)

    if request.error_status[0]:
        logger.error('sending data failed: ' + request.error_status[1])
    else:
        logger.info('data successfully sent.')

    return request


def send_metric_value(metric_name, value, **kwargs):
    '''
    Function sends value to metric on the DESDMDASHBOARD.

    Returns a request object.
    '''
    request = send_metric_data(name=metric, value=value, **kwargs)
    return request



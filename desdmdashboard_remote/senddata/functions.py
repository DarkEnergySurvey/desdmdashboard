'''
'''

from .utils import DATA_TEMPLATE
from ..http_requests import Request


def send_metric_data(**kwargs):
    '''
    Send any of the possible arguments to the DESDMDASHBOARD db as kwargs of
    this function.

    Returns a request object.
    '''

    logger = kwargs.pop('logger', None)
    verbose = kwargs.pop('verbose', False)

    # we need to read them out here due to added underscore
    # this is not very nice but it works
    # it originates from the serializer variable type expectation
    time_ = kwargs.pop('time', None)
    value_type_ = kwargs.pop('value_type', None)

    _data = DATA_TEMPLATE.copy()
    _data.update(kwargs)
    if time_:
        _data['time_'] = time_
    if value_type_:
        _data['value_type_'] = value_type_

    mess = 'Sending value {val} to metric {met}'
    if logger:
        logger.info(mess.format(
            val=_data['value'], met=_data['name'])
            )
    if verbose:
        print mess.format(
            val=_data['value'], met=_data['name'])

    request = Request()
    request.POST(data=_data)

    if request.error_status[0]:
        mess = 'sending data failed: ' + request.error_status[1]
        if logger:
            logger.error(mess)
        if verbose:
            print mess
    else:
        mess = 'data successfully sent.'
        if logger:
            logger.info('data successfully sent.')
        if verbose:
            print mess

    return request


def send_metric_value(metric_name, val, **kwargs):
    '''
    Function sends value to metric on the DESDMDASHBOARD.

    Returns a request object.
    '''
    request = send_metric_data(name=metric_name, value=val, **kwargs)
    return request



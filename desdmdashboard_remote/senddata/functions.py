'''
'''

from utils import DATA_TEMPLATE
from ..http_requests import Request


def send_metric_value(metric_name, value, **kwargs):
    '''
    Function sends value to metric on the DESDMDASHBOARD.

    Returns a request object.
    '''
    data = DATA_TEMPLATE.copy()

    data['name'] = metric_name
    data['value'] = value 
    data.update(kwargs)

    request = Request()
    request.POST(data=data)

    return request


def send_metric_data(**kwargs):
    '''
    Send any of the possible arguments to the DESDMDASHBOARD db as kwargs of
    this function.

    Returns a request object.
    '''
    data = DATA_TEMPLATE.copy()
    data.update(kwargs)

    request = Request()
    request.POST(data=data)

    return request

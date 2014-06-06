'''
'''

from ..http_requests import Request


def send_metric_value(metric_name, value, **kwargs):
    '''
    Function sends value to metric on the DESDMDASHBOARD.

    Returns a request object.
    '''
    data = {}

    data['name'] = metric_name
    data['value'] = value 
    data['tags'] = kwargs.get('tags', u'')
    data['value_type_'] = kwargs.get('value_type_', u'')
    data['has_error'] kwargs.get('has_error', u'')
    data['error_message'] kwargs.get('error_message', u'')

    request = Request()

    request.POST(data=data)

    return request

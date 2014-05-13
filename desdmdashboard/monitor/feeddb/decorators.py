'''
'''

import requests
import time

# import the credentials via coreutils from the local .desservices file if
# possible
try:
    from coreutils import serviceaccess
    creds = serviceaccess.parse(None, 'desdmdashboard')
    USERNAME = creds['user']
    PASSWORD = creds['passwd']
    API_URL = creds['api_url']
except:
    USERNAME = 'michael'
    PASSWORD = 'dummypwd'
    API_URL = 'http://127.0.0.1:8000/monitor/api/'



DATA_TEMPLATE = {
    'name': u'',
    'has_error': False, 
    'error_message': u'',
    'value_type_': u'',
    'value': u'',
    'tags': u''
    }



class WebAPIFeeder(object):
    '''
    '''

    def __init__(self, api_url=API_URL, auth=(USERNAME, PASSWORD),
            data=DATA_TEMPLATE, ):
        self.api_url = api_url
        self.auth = auth
        self.data = data
        self.request = None

    def dispatch_request(self, data=None):
        if type(data)==dict:
            self.data.update(data)
        self.request = requests.post(self.api_url, self.data, auth=self.auth)


class Monitor(object):
    '''
    A function decorator class to feed function output into the monitoring
    database via its web api.

    USAGE:
    1. specify your desdmdashboard credentials in your .desservices like this

        [desdmdashboard]
        user = michael
        passwd = dummypassword

    2. decorate a any function producing a value you would like to feed to the
    dashboard with the decorator like this: 

        @Monitor('MyMetric')
        def metric_measurement_function(*args, **kwargs):
            
            x = ...

            return x

    whenever `metric_measurement_function` will be executed, x will be fed into
    the metric 'MyMetric' in the database.


    '''
    
    def __init__(self, metric_name, auth=(USERNAME, PASSWORD), api_url=API_URL,
            **kwargs):
        self.feeder = WebAPIFeeder(api_url=api_url, auth=auth)
        self.data = {} 
        self.data['name'] = metric_name
        self.data['tags'] = kwargs.get('tags', '')
        self.data['value_type_'] = kwargs.get('value_type_', '')

    def __call__(self, func):
        decorator_self = self

        def wrappee(*args, **kwargs):
            # stuff before func execution
            started_at = time.time()
            # func execution
            # TODO : enable tags, catching errors & error messages
            value = func(*args, **kwargs)
            # stuff after func execution
            exectime = time.time() - started_at
            try:
                self.data['value'] = value
                decorator_self.feeder.dispatch_request(
                        data=self.data)
                if not decorator_self.feeder.request.ok:
                    raise APIFeedError()
            except:
                raise

        return wrappee

class APIFeedError(Exception):
    pass

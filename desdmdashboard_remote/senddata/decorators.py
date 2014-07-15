'''
'''

#import requests
import time

import urllib2
import urllib
from base64 import b64encode

from ..http_requests import Request


DATA_TEMPLATE = {
    'name': u'',
    'has_error': False, 
    'error_message': u'',
    'value_type_': u'',
    'value': u'',
    'tags': u'',
    'time_': u'',
    }


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

    3. set up a cron job executing a python file in which monitor function
    executions follow after if __name__ == '__main__':, like here:

    if __name__ == '__main__':
        metric_measurement_function()

    '''
    
    def __init__(self, metric_name, **kwargs):
        self.request = Request()
        self.data = DATA_TEMPLATE
        self.logger = kwargs.get('logger', None)
        if type(metric_name) == str:
            self.data['name'] = metric_name
            self.metric_name_generator = None
        elif hasattr(metric_name, '__call__'):
            self.metric_name_generator = metric_name
        else:
            mess = 'metric_name has to be either a string or a callable.'
            if self.logger:
                self.logger.error(mess)
            raise ValueError(mess)
        self.data['tags'] = kwargs.get('tags', u'')
        self.data['value_type_'] = kwargs.get('value_type', u'')

    def __call__(self, func):
        decorator_self = self

        def wrappee(*args, **kwargs):
            # stuff before func execution
            # started_at = time.time()

            if self.metric_name_generator:
                self.data['name'] = self.metric_name_generator(*args, **kwargs)

            if self.logger:
                self.logger.info('function execution in Monitor decorator: ' + func.func_name)
                self.logger.debug('args: ' + str(args) + ' kwargs: ' + str(kwargs) )
            # func execution
            try:
                self.data['value'] = func(*args, **kwargs)
                if self.logger:
                    self.logger.info('function successfully executed.')
            except Exception, err:
                value = ''
                self.data['has_error'] = True
                self.data['error_message'] = err
                if self.logger:
                    self.logger.error(err)
                
            # stuff after func execution
            # exectime = time.time() - started_at
            if self.logger:
                mess = 'sending value {val} to metric {met}'
                self.logger.info(mess.format(
                    val=self.data['value'], met=self.data['name'])
                    )
            try:
                decorator_self.request.POST(data=self.data)
                if self.logger:
                    if decorator_self.request.error_status[0]:
                        self.logger.error(decorator_self.request.error_status[1])
                    else:
                        self.logger.info('metric value successfully sent.')
            except Exception, err:
                if self.logger:
                    self.logger.error(err)

        return wrappee

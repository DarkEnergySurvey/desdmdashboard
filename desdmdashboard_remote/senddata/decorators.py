'''
'''

import sys
import time

import urllib2
import urllib
from base64 import b64encode

from utils import DATA_TEMPLATE

from ..http_requests import Request


class Monitor(object):
    '''
    A function decorator class to feed function output into the monitoring
    database via its web api.

    USAGE:
    1. specify your desdmdashboard credentials in your .desservices like this

        [desdmdashboard]
        user = my_desdmdashboard_username 
        passwd = my_desdmdashboard_password
        # web api url of the desdmdashboard (current dev version below)
        api_url = http://desdash.cosmology.illinois.edu/dev/desdmdashboard/monitor/api

    2. decorate a any function producing a value you would like to feed to the
    dashboard with the decorator like this: 

        @Monitor('MyMetric')
        def metric_measurement_function(*args, **kwargs):
            
            x = ...

            return x

    whenever `metric_measurement_function` will be executed, x will be fed into
    the metric 'MyMetric' in the database.

    Instead of specifying a fixed metric name by a string, you can also pass a
    metric name generator function. This function will be fed with the same
    args and kwargs as the metric_measurement_function at function execution
    time. It has to return a string.

    If your metric does not exist yet in the beginning you do also have to
    indicate which data table to use, using the value_type keyword. Possible
    options are 'int', 'float', 'char', 'datetime', 'json'. Once set, the
    value_type cannot be overwritten by passing the value_type keyword.

    3. set up a (cron) job executing a python file in which monitor function
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
        self.send_docstring = kwargs.get('send_docstring', True)

    def __call__(self, func):
        decorator_self = self

        def wrappee(*args, **kwargs):
            # stuff before func execution
            # started_at = time.time()

            if self.metric_name_generator:
                self.data['name'] = self.metric_name_generator(*args, **kwargs)
                if not type(self.data['name']) == str:
                    mess = ('The output of the metric_name_generator function '
                            'has to be of type str, %s was returned.' % type(self.data['name']))
                    raise ValueError(mess)

            if self.logger:
                self.logger.info('Function execution in Monitor decorator: ' + func.func_name)
                self.logger.debug('args: ' + str(args) + ' kwargs: ' + str(kwargs) )
            # func execution
            try:
                self.data['value'] = func(*args, **kwargs)
                if self.logger:
                    self.logger.info('Function successfully executed.')
            except Exception, err:
                value = ''
                self.data['has_error'] = True
                self.data['error_message'] = err
                if self.logger:
                    self.logger.exception('Function execution failed:')

            if self.send_docstring:
                if func.__doc__:
                    self.data['doc'] = trim_docstring(func.__doc__)
                
            # stuff after func execution
            # exectime = time.time() - started_at
            if self.logger:
                mess = 'Sending value {val} to metric {met}'
                self.logger.info(mess.format(
                    val=self.data['value'], met=self.data['name'])
                    )
            try:
                decorator_self.request.POST(data=self.data)
                if self.logger:
                    if decorator_self.request.error_status[0]:
                        self.logger.error(decorator_self.request.error_status[1])
                    else:
                        self.logger.info('Metric value successfully sent.')
            except Exception, err:
                if self.logger:
                    self.logger.error(err)

        return wrappee


def trim_docstring(docstring):
    '''code from http://legacy.python.org/dev/peps/pep-0257/
    '''
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)

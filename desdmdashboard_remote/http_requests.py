'''
Library module providing an easy-to-use API for http requests to the
desdmdashboard web application api.

Loads credentials and WebAPI settings from a .desservices file in the users
home directory.

:author: michael h graber, michael.graber@fhnw.ch
'''

import urllib, urllib2
from base64 import b64encode


# -----------------------------------------------------------------------------

# THIS IS DESDMDASHBOARD Web API SPECIFIC STUFF 

# import the credentials via coreutils from the local .desservices file if
# possible, otherwise I assume I am locally developing on my machine ..
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

POST_URL = API_URL
GET_URL = API_URL + 'data/' if API_URL[-1] == '/' else API_URL + '/data/' 

# -----------------------------------------------------------------------------


class Request(object):
    '''
    '''

    def __init__(self, auth=(USERNAME, PASSWORD)):
        self.auth = auth
        self.url = None 
        self.response = None
        self.error_status = (False, '')

    def POST(self, url=POST_URL, data=None):
        ''' '''
        if not type(data)==dict:
            raise ValueError(('The data kwarg needs to be set and of type '
                'dictionary.'))
        else:
            self.data = data
        if not url:
            raise ValueError('You need to provide an ulr kwarg.')
        else:
            self.url = url

        urllib_req = urllib2.Request(self.url)
        urllib_req.add_header('Authorization',
                'Basic ' + b64encode(self.auth[0]+':'+self.auth[1]))
        try:
            self.response = urllib2.urlopen(urllib_req,
                    urllib.urlencode(self.data))
        except Exception, e:
            self.error_status = (True, str(e))

    def GET(self, url=GET_URL, params={}):
        ''' '''
        if not url:
            raise ValueError('You need to provide an ulr kwarg.')
        else:
            self.url = url

        url_params = '?'+'&'.join([k+'='+v for k, v in params.iteritems()])
        urllib_req = urllib2.Request(self.url+url_params)
        urllib_req.add_header('Authorization',
                'Basic ' + b64encode(self.auth[0]+':'+self.auth[1]))
        try:
            self.response = urllib2.urlopen(urllib_req)
        except Exception, e:
            self.error_status = (True, str(e))

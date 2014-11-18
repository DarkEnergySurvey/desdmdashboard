
# settings for the development of the desdmdashboard on 
# michaels dude macbook

from common_settings import *


# Application definition - EXTENSIONS
# =============================================================================
'''
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', ]
'''

INSTALLED_APPS += (
    # testing the following two packages
    'debug_toolbar',
    #'django_extensions',
    # 'south',
    )

MIDDLEWARE_CLASSES += (
    'desdmdashboard.middleware.ProfileMiddleware',
    )


# this is a bit cheap but in order to be able to send emails containing the
# entire url, incl. domain, i need to store the domain root someplace
DOMAIN_ROOT = 'http://127.0.0.1:8000'

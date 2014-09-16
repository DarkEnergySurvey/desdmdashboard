
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
    # 'debug_toolbar',
    'monitor_cache',
    'django_extensions',
    'south',
    )

MIDDLEWARE_CLASSES += (
    'desdmdashboard.middleware.ProfileMiddleware',
    )

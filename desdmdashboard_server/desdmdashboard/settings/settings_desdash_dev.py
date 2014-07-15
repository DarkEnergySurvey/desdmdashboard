
# settings for the deployment of the desdmdashboard on 
# desdash.cosmology.illinois.edu 

from common_settings import *


# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = False
DEBUG = True

TEMPLATE_DEBUG = False



# https://docs.djangoproject.com/en/1.5/ref/settings/#std:setting-ALLOWED_HOSTS

ALLOWED_HOSTS = ['desdash.cosmology.illinois.edu',]


#SESSION_COOKIE_PATH = '/dev/desdmdashboard'


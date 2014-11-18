
# settings for the deployment of the desdmdashboard on
# desdash.cosmology.illinois.edu

from common_settings import *


# SECURITY WARNING: don't run with debug turned on in production!
### FIXME
DEBUG = True

TEMPLATE_DEBUG = False

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.oracle',
       'NAME': 'DESOPER',
       'USER': 'dashboard',
       'PASSWORD': 'XXX',
       'HOST': '',
       'PORT': '',
   }
}



# https://docs.djangoproject.com/en/1.5/ref/settings/#std:setting-ALLOWED_HOSTS
ALLOWED_HOSTS = ['desdash.cosmology.illinois.edu',]


# this is a bit cheap but in order to be able to send emails containing the
# entire url, incl. domain, i need to store the domain root someplace
DOMAIN_ROOT = 'http://desdash.cosmology.illinois.edu/desdmdashboard'

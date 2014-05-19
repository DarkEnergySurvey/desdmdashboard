
# settings for the development of the desdmdashboard on 
# michaels dude macbook

from common_settings import *


# Application definition - EXTENSIONS
# =============================================================================

INSTALLED_APPS += (

    # testing the following two packages
    'debug_toolbar',
    'django_extensions',

    )

MIDDLEWARE_CLASSES += (

    'desdmdashboard.middleware.ProfileMiddleware',

    )

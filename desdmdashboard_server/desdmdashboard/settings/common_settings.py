"""
Django settings for desdmdashboard project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.split(os.path.dirname(os.path.dirname(__file__)))[0]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ohp-j_n1-@5^if!#a*%ha40&#dujs%7ushfca@^9ed19ka37u*'

# SECURITY WARNING: don't run with debug turned on in production!
### FIXME
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []



# ERROR NOTIFICATION HANDLING
# =============================================================================

'''
A tuple that lists people who get code error notifications. When DEBUG=False and
a view raises an exception, Django will e-mail these people with the full
exception information. Each member of the tuple should be a tuple of
(Full name, e-mail address).
'''
ADMINS = (
    ('Michael Graber', 'michael.graber@fhnw.ch'),
    ('Gregory Daues', 'daues@ncsa.uiuc.edu'),
)

'''
A tuple in the same format as ADMINS that specifies who should get broken-link
notifications when SEND_BROKEN_LINK_EMAILS=True.
'''
MANAGERS = ADMINS

'''
Whether to send an e-mail to the MANAGERS each time somebody visits a
Django-powered page that is 404ed with a non-empty referer (i.e., a broken link).
This is only used if CommonMiddleware is installed (see Middleware. See also
IGNORABLE_404_STARTS, IGNORABLE_404_ENDS and Error reporting via e-mail.
'''
SEND_BROKEN_LINK_EMAILS = True


# EMAIL 
# =============================================================================

EMAIL_HOST = 'smtp.ncsa.illinois.edu'
EMAIL_PORT = 25
EMAIL_SUBJECT_PREFIX = '[desdmdashboard_server] '
DEFAULT_FROM_EMAIL = 'admin@desdash.cosmology.illinois.edu'


# Templates
# =============================================================================

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'desdmdashboard', 'templates'),
    os.path.join(BASE_DIR, 'monitor', 'templates'),
    os.path.join(BASE_DIR, 'dashboard', 'templates'),
)


# Application definition
# =============================================================================

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'monitor',

    ### FIXME
    # testing the following two packages
#   'debug_toolbar',
#   'django_extensions',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'desdmdashboard.urls'

WSGI_APPLICATION = 'desdmdashboard.wsgi.application'


# Database
# =============================================================================
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# =============================================================================
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'GMT'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# =============================================================================
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static', ),
    )

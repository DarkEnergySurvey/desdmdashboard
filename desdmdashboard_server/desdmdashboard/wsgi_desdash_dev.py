"""
WSGI config for desdmdashboard project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import sys
import os

sys.path.append('/webapps/dev/desdmdashboard_server')

# necessary to allow multiple django projects to be run in same wsgi process
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "desdmdashboard.settings.settings_desdash_dev")
os.environ["DJANGO_SETTINGS_MODULE"] = "desdmdashboard.settings.settings_desdash_dev"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

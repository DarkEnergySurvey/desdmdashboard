"""
WSGI config for desdmdashboard project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import sys
import os

sys.path.append('/webapps/releases/current/desdmdashboard_server')

os.environ["DJANGO_SETTINGS_MODULE"] = "desdmdashboard.settings.settings_desdash_production"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

"""
WSGI config for desdmdashboard project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import sys

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "desdmdashboard.settings.settings_desdash")

sys.path.append('/webapps/dev/desdmdashboard_server') #parent directory of project
sys.path.append('/webapps/dev/desdmdashboard_server/desdmdashboard')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

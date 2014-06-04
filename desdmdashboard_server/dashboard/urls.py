from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from monitor.views import api
from monitor.views.users import UserList, UserDetail


urlpatterns = patterns('dashboard.views',
#   url('^$', RedirectView.as_view(
#       url='home/', permanent=False), name='dashboard_home'),
    url(r'^$', 'generator.dashboard_home', name='dashboard_home'),
    url(r'^(?P<section>\w+)/*$', 'generator.dashboard_section', 
        name='dashboard_section'),
    )

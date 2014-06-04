from django.conf.urls import patterns, include, url

from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

     url('^$', RedirectView.as_view(
         url='dashboard/', permanent=False), name='index'),
#   url('^dashboard/*$', 'desdmdashboard.views.dashboard.entrance', {},
#       name='dashboard_entrance'),

    url(r'^monitor/', include('monitor.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^admin/', include(admin.site.urls)),

)

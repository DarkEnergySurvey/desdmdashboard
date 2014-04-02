from django.conf.urls import patterns, include, url

from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url('^$', RedirectView.as_view(
        url='monitor/dashboard/', permanent=False), name='index'),
    url(r'^monitor/', include('monitor.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

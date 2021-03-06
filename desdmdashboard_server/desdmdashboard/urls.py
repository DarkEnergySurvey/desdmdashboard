from django.conf.urls import patterns, include, url

from django.shortcuts import render_to_response

from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()


def template_test(request):
    '''
    A utility view function to test templates.
    '''
    ctx = {
            'navsection': 'dashboard',
            'sections': {'bla': 'bla', 'blu': 'blu'},
            'section_name': 'VMs',
            'virtualmachines': ['desdash.cosmology', 'desbuild.cosmology', 'tre', ],
            }
    return render_to_response('dashboard.html', ctx)


urlpatterns = patterns('',

#   url('^$', template_test, {}, name='home'),
    url('^$', RedirectView.as_view(
         url='dashboard/', permanent=False), name='home'),

    url('^doc/*$', 'desdmdashboard.views.main.doc', {},
        name='doc_home'),

    url(r'^monitor/', include('monitor.urls')),
    url(r'^dashboard/', include('dashboard.urls'), name='dashboard_home'),
    url(r'^admin/', include(admin.site.urls), name='admin_home'),

)

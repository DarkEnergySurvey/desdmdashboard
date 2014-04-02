from django.conf.urls import patterns, include, url


urlpatterns = patterns('monitor.views.main',
    url(r'^dashboard/$', 'dashboard', {}, 'dashboard'),
    #url(r'^api/$', api_view.CreateMetricView.as_view()),
)
'''
urlpatterns += patterns('monitor.views.api',
    url(r'^api/$', CreateMetricView.as_view()),
)
'''

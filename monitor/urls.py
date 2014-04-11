from django.conf.urls import patterns, include, url

from monitor.views.api import CreateMetricView
from monitor.views.users import UserList, UserDetail


urlpatterns = patterns('monitor.views.main',
    url(r'^dashboard/$', 'dashboard', {}, 'dashboard'),
    #url(r'^api/$', api_view.CreateMetricView.as_view()),
)

urlpatterns += patterns('monitor.views.api',
    url(r'^api/$', CreateMetricView.as_view()),
)

urlpatterns += patterns('monitor.views.users',
    url(r'^users/$', UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
)

urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
)

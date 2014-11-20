from django.conf.urls import patterns, include, url

from monitor.views import api
from monitor.views.users import UserList, UserDetail


urlpatterns = patterns('monitor.views',
    url(r'^$', 'main.dashboard', {}, name='metrics_home'),
    url(r'^api/*$', api.ListCreateMetricView.as_view(), {},
        name='api'),
    url(r'^api/data/*$', api.ListMetricDataView.as_view(), {},
        name='api_data'),
    url(r'^api-auth/', include('rest_framework.urls',
        namespace='rest_framework')),
    )

urlpatterns += patterns('monitor.views.main',
    url(r'^(?P<owner>\w+)/*$', 'dashboard', {}, name='owner_dashboard',),
    url(r'^(?P<owner>\w+)/(?P<nameslug>[\w-]+)/*$', 'metric_detail', {},
        name='metric_detail',),
    )

'''
urlpatterns += patterns('monitor.views.users',
    url(r'^users/$', UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
)
'''

from rest_framework.generics import CreateAPIView
from rest_framework.authentication import SessionAuthentication

from desdmdashboard import authentication, permissions
from . import models, serializers


class CreateMetricView(CreateAPIView):
    """Saves a new metric value (or values)"""
    authentication_classes = (authentication.SettingsAuthentication,
                              SessionAuthentication)
    permission_classes = (permissions.DESDMDashboardPermission,)
    model = models.Metric
    serializer_class = serializers.MetricSerializer

    def get_serializer(self, instance=None, data=None, files=None,
                       many=False, partial=False):
        if isinstance(data, list):
            many = True
        return super(CreateMetricView, self).get_serializer(instance, data,
                                                            files, many,
                                                            partial)

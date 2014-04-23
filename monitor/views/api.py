from rest_framework.generics import CreateAPIView
from rest_framework import permissions

from monitor import models, serializers
from monitor.permissions import IsOwnerOrReadOnly


class CreateMetricView(CreateAPIView):
    """Saves a new metric value (or values)"""
    permission_classes = (permissions.IsAuthenticated,
            IsOwnerOrReadOnly, )

    model = models.Metric
    serializer_class = serializers.MetricSerializer

    def get_serializer(self, instance=None, data=None, files=None,
                       many=False, partial=False):
        if isinstance(data, list):
            many = True
        return super(CreateMetricView, self).get_serializer(instance, data,
                                                            files, many,
                                                            partial)
    def pre_save(self, obj):
        obj.owner = self.request.user

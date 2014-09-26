from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework import permissions

from monitor import models, serializers
from monitor.permissions import IsOwnerOrReadOnly


class ListCreateMetricView(ListCreateAPIView):
    ''' '''
    permission_classes = (permissions.IsAuthenticated,
            IsOwnerOrReadOnly, )

    model = models.Metric
    serializer_class = serializers.MetricSerializer

    def get_serializer(self, instance=None, data=None, files=None,
                       many=False, partial=False):
        if isinstance(data, list):
            many = True
        return super(ListCreateMetricView, self).get_serializer(
                instance, data, files, many, partial)

    def pre_save(self, obj):
        obj.owner = self.request.user

    def get_queryset(self):
        """ """
        name = self.request.QUERY_PARAMS.get('name', None)
        owner = self.request.QUERY_PARAMS.get('owner', None)
        if owner is None:
            owner = self.request.user.username
        if name == None:
            return models.Metric.objects.filter(owner__username=owner,
                    name=name)
        else:
            return models.Metric.objects.filter(owner__username=owner,
                    name__regex=name)


class ListMetricDataView(ListAPIView):
    ''' '''
    permission_classes = (permissions.IsAuthenticated, )

    #model = models.MetricDataJSON
    #serializer_class = serializers.MetricDataSerializer

    def get_serializer_class(self):
        value_type = self.request.QUERY_PARAMS.get('value_type', None)
        if value_type == 'metricdatajson':
            return serializers.MetricDataJSONSerializer
        elif value_type == 'metricdataint':
            return serializers.MetricDataIntSerializer
        elif value_type == 'metricdatachar':
            return serializers.MetricDataCharSerializer
        elif value_type == 'metricdatafloat':
            return serializers.MetricDataFloatSerializer
        elif value_type == 'metricdatadatetime':
            return serializers.MetricDataDatetimeSerializer
        else:
            raise ValueError(('No valid value_type provided to select '
                                'serializer.'))

    def get_queryset(self):
        """ """
        metric_pk = self.request.QUERY_PARAMS.get('metric_pk', None)
        value_type = self.request.QUERY_PARAMS.get('value_type', None)
        if not value_type and metric_pk:
            return ['error: you have to provide value_type and metric_pk!']
        if value_type == 'metricdatajson':
            qs = models.MetricDataJSON.objects.filter(
                    metric__pk=int(metric_pk))
        elif value_type == 'metricdataint':
            qs = models.MetricDataInt.objects.filter(
                    metric__pk=int(metric_pk))
        elif value_type == 'metricdatafloat':
            qs = models.MetricDataFloat.objects.filter(
                    metric__pk=int(metric_pk))
        elif value_type == 'metricdatadatetime':
            qs = models.MetricDataDatetime.objects.filter(
                    metric__pk=int(metric_pk))
        elif value_type == 'metricdatachar':
            qs = models.MetricDataChar.objects.filter(
                    metric__pk=int(metric_pk))
        else:
            return ['error: no valid value_type was provided']
        return qs

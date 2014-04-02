from django.utils.timezone import now
from rest_framework import serializers

from . import models


class MetricDataSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=255)
    source_name = serializers.CharField(max_length=255, required=False)
    instrument_name = serializers.CharField(max_length=255, required=False)

    valueinput = serializers.CharField(max_length=1024)

    def restore_object(self, attrs, instance=None):
        # get the metric
        metric, metric_created = models.Metric.objects.get_or_create(
                name=attrs['name'])
        metric_name = attrs['name']
        newdatakwargs = { 'metric_name' : attrs['name']}
        if 'source_name' in attrs:

        




class DepMetricDataSerializer(serializers.ModelSerializer):
    source = serializers.CharField(source='source.name', required=False)
    value = serializers.FloatField(source='latest_value')
    timestamp = serializers.DateTimeField(source='last_updated',
                                          required=False)

    class Meta:
        model = models.Metric
        fields = ('source', 'name', 'value', 'timestamp')

    def restore_object(self, attrs, instance=None):
        kwargs = {'name': attrs['name']}
        if 'source.name' in attrs:
            source, created = models.Source.objects.get_or_create(
                name=attrs['source.name'])
            if created:
                logger.debug('Created source: %s', source.name)
            kwargs['source_id'] = source.pk
        try:
            instance = self.opts.model.objects.get(**kwargs)
        except self.opts.model.DoesNotExist:
            instance = self.opts.model(**kwargs)
        instance.latest_value = attrs['latest_value']
        instance.last_updated = attrs.get('timestamp', now())
        return instance

    def save_object(self, obj, **kwargs):
        if 'force_insert' in kwargs:
            del(kwargs['force_insert'])
        super(MetricSerializer, self).save_object(obj, **kwargs)
        obj.add_latest_to_archive()



# DEV STUFF
# -----------------------------------------------------------------------------

import cStringIO
from rest_framework.parsers import JSONParser

jsonstr = '''
            { 
                "name": "capacity",
                "source_name": "deslogin",
                "instrument_name": "desdf",
                "valueinput": "3212243" 
            }
          '''

jsonparsed = JSONParser().parse(cStringIO.StringIO(jsonstr))



'''
 583     def save(self, **kwargs):
 584         """
 585         Save the deserialized object and return it.
 586         """
 587         # Clear cached _data, which may be invalidated by `save()`
 588         self._data = None
 589
 590         if isinstance(self.object, list):
 591             [self.save_object(item, **kwargs) for item in self.object]
 592
 593             if self.object._deleted:
 594                 [self.delete_object(item) for item in self.object._deleted]
 595         else:
 596             self.save_object(self.object, **kwargs)
 597
 598         return self.object

 '''

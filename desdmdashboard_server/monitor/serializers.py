
from datetime import datetime

from django import db 

from django.utils.timezone import now
from django.utils.text import slugify

from django.contrib import contenttypes
from django.contrib.auth.models import User


from rest_framework import serializers

from monitor import models
from monitor_cache.models import MetricCache


class UserSerializer(serializers.ModelSerializer):
    metrics = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'metrics', )



class MetricSerializer(serializers.ModelSerializer):

    pk = serializers.Field()
    value_type_ = serializers.CharField(source='value_type', required=False) 
    tags = serializers.CharField(source='latest_tags', required=False) 
    value = serializers.CharField(source='latest_value', required=False) 
    owner = serializers.Field(source='owner.username')
    time_ = serializers.CharField(source='latest_time', required=False) 

    class Meta:
        model = models.Metric
        fields = ('pk', 'name', 'has_error', 'error_message', 'value_type_',
                'value', 'time_', 'tags', 'owner', 'doc', )

    def restore_object(self, attrs, instance=None):

        try:
            request = self.context['request']
            instance = self.opts.model.objects.get_by_natural_key(
                    owner=request.user.pk, name=attrs['name'])

        except:
            if not attrs['value_type']:
                raise ValueError(('The Metric %s does not exist yet, therefore'
                    ' you have to provide a value type.') % attrs['name'])
            instance = self.opts.model.create(attrs['name'],
                    attrs['value_type'])
            instance.slug = slugify(instance.name)

        if attrs['latest_time']:
            t = datetime.strptime(attrs['latest_time'].rstrip(),
                    '%Y-%m-%d %H:%M:%S')
        else:
            t = now()

        if attrs['doc']:
            instance.doc = attrs['doc']

        instance.set_latest_measurements(
                value=attrs['latest_value'],
                tags=attrs['latest_tags'],
                has_error=attrs['has_error'],
                error_message=attrs['error_message'],
                time=t)

        return instance

    def save_object(self, obj, **kwargs):
        if 'force_insert' in kwargs:
            del(kwargs['force_insert'])
        super(MetricSerializer, self).save_object(obj, **kwargs)
        obj._save_latest_values_to_data_table()
        # we simply save here again to update the alert_triggered variable
        super(MetricSerializer, self).save_object(obj, **kwargs)
        _ = MetricCache.create_or_update(obj)


class MetricDataJSONSerializer(serializers.ModelSerializer):

    def transform_value(self, obj, value):
        return obj.value

    class Meta:
        model = models.MetricDataJSON

class MetricDataIntSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MetricDataInt

class MetricDataFloatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MetricDataFloat

class MetricDataDatetimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MetricDataDatetime

class MetricDataCharSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MetricDataDatetime

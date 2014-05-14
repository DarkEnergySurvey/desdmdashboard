from django import db 
from django.utils.timezone import now
from django.contrib import contenttypes
from django.contrib.auth.models import User

from rest_framework import serializers

from monitor import models


class UserSerializer(serializers.ModelSerializer):
    metrics = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'metrics', )



class MetricSerializer(serializers.ModelSerializer):

    value_type_ = serializers.CharField(source='value_type', required=False) 
    tags = serializers.CharField(source='latest_tags', required=False) 
    value = serializers.CharField(source='latest_value', required=False) 
    owner = serializers.Field(source='owner.username')

    class Meta:
        model = models.Metric
        fields = ('name', 'has_error', 'error_message', 'value_type_',
                'value', 'tags', 'owner', )

    def restore_object(self, attrs, instance=None):

        try:
            request = self.context['request']
            instance = self.opts.model.objects.get_by_natural_key(
                    name=attrs['name'], owner=request.user.pk)

        except:
            if not attrs['value_type']:
                raise ValueError(('The Metric %s does not exist yet, therefore'
                    ' you have to provide a value type.') % attrs['name'])
            instance = self.opts.model.create(attrs['name'],
                    attrs['value_type'])

        instance.set_latest_measurements(
                value=attrs['latest_value'],
                tags=attrs['latest_tags'],
                has_error=attrs['has_error'],
                error_message=attrs['error_message'],
                time=now())

        return instance

    def save_object(self, obj, **kwargs):
        if 'force_insert' in kwargs:
            del(kwargs['force_insert'])
        super(MetricSerializer, self).save_object(obj, **kwargs)
        obj._save_latest_values_to_data_table()
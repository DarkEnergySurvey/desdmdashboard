'''
DESDM DASHBOARD

Django data model for saving system snapshot data for monitoring purposes.


'''
import operator
import json

from datetime import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.timezone import now
from django.core.urlresolvers import reverse

from jsonfield.fields import JSONField

from .managers import MetricManager, MetricDataManager



class Metric(models.Model):
    '''
    The time series measured.
    '''
    objects = MetricManager()
    data = MetricDataManager()

    name = models.CharField(max_length=512)
    slug = models.SlugField(max_length=512)

    owner = models.ForeignKey('auth.User', related_name='metrics')

    warning_if_no_value_after_seconds = models.PositiveIntegerField(
            default=60*60*24*7, null=True, blank=True)

    latest_value = models.CharField(max_length=1024, null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)

    latest_tags = models.CharField(max_length=256, blank=True, default='')

    has_error = models.BooleanField(default=False)
    error_message = models.CharField(null=True, blank=True, max_length=256)

    #source = models.ForeignKey(Source, blank=True, null=True)
    #source = models.CharField(max_length=512)
    #instrument  = models.ForeignKey(Instrument, blank=True, null=True)
    #instrument = models.CharField(max_length=512)

    UNIT_BYTES = 1
    UNIT_SECONDS = 2

    UNIT_CHOICES = (
            (UNIT_BYTES, 'bytes'),
            (UNIT_SECONDS, 'seconds'),
            )
    unit = models.PositiveSmallIntegerField(choices=UNIT_CHOICES, null=True,
            blank=True)

    VALUE_TYPE_CHOICES = models.Q(app_label='monitor', model='metricdataint') |\
            models.Q(app_label='monitor', model='metricdatafloat') |\
            models.Q(app_label='monitor', model='metricdatachar') |\
            models.Q(app_label='monitor', model='metricdatajson') |\
            models.Q(app_label='monitor', model='metricdatadatetime')
    value_type = models.ForeignKey(generic.ContentType, 
            limit_choices_to=VALUE_TYPE_CHOICES)

    show_on_dashboard = models.BooleanField(default=True)

    OPERATOR_CHOICES = (
        ('lt', 'value < alert'),
        ('le', 'value <= alert'),
        ('eq', 'value == alert'),
        ('ne', 'value != alert'),
        ('ge', 'value >= alert'),
        ('gt', 'value > alert'),
    )
    alert_operator = models.CharField(max_length=2, choices=OPERATOR_CHOICES,
            blank=True)
    alert_value = models.FloatField(null=True, blank=True)
    alert_triggered = models.BooleanField(default=False)

    doc = models.TextField(blank=True, null=True)

    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('name', 'owner'), )

    def natural_key(self):
        return (self.name, self.owner.username)

    def __unicode__(self):
        return u'{n} ({u})'.format(n=self.name, u=self.owner.username)

    def get_absolute_url(self):
        return reverse('monitor.views.main.metric_detail',
                kwargs={'name': self.name, 'owner': self.owner.username})

    @property
    def has_no_value_warning(self):
        '''
        '''
        dp = self.get_last_datapoint_from_table()
        delta_t = now() - dp.time
        if self.warning_if_no_value_after_seconds:
            return delta_t.total_seconds() >= self.warning_if_no_value_after_seconds
        else:
            return False
        
    @property
    def is_in_trouble_status(self):
        '''
        either has an error or an alert was triggered or both
        '''
        err = bool(self.has_error)
        alert = bool(self.alert_triggered)
        warn = bool(self.has_no_value_warning)
        return (err or alert or warn)

    @classmethod
    def create(cls, name, value_type):
        obj = cls(name=name)
        if value_type.lower() == 'int':
            obj.value_type = ContentType.objects.get(model='metricdataint')
        elif value_type.lower() == 'float':
            obj.value_type = ContentType.objects.get(model='metricdatafloat')
        elif value_type.lower() == 'char':
            obj.value_type = ContentType.objects.get(model='metricdatachar')
        elif value_type.lower() == 'datetime':
            obj.value_type = ContentType.objects.get(model='metricdatadatetime')
        else:
            raise ValueError(("Cannot create Metric object with value_type %s . "
                "It has to from ('int', 'char', 'float', 'datetime')") %
                value_type )
        return obj
    
    def create_value_obj(self):
        return self.value_type.model_class()(metric=self)

    def check_alert(self):
        if not self.alert_operator:
            return
        oper = getattr(operator, self.alert_operator)
        latest_value = self.get_last_datapoint_from_table().value
        return oper(latest_value, self.alert_value)

    def set_latest_measurements(self, value=None, tags='', has_error=False,
            error_message='', time=None):
        ''' '''

        if has_error and value:
            raise ValueError('You cannot provide a value and an error')
        elif has_error and not error_message:
            raise ValueError(('You need to provide an error message if you '
                    'want to set has_error to true'))
        elif value and error_message:
            raise ValueError(('You cannot provide a value and an error '
                ' message'))
        elif type(time) != datetime:
            raise ValueError(('You have to provide a "time" keyword argument '
                'of type datetime.'))
        else:
            self.latest_value = value
            self.latest_tags = tags
            self.has_error = has_error
            self.error_message = error_message
            self.last_updated = time

    def _save_latest_values_to_data_table(self):
        ''' '''
        dobj = self.create_value_obj()
        dobj.time = self.last_updated
        dobj.has_error = self.has_error
        dobj.error_message = self.error_message
        if not dobj.has_error:    
            dobj.value_from_string(self.latest_value)
        dobj.save()

    def get_data_queryset(self):
        vtclass = self.value_type.model_class()
        return vtclass.objects.filter(metric=self)

    def get_last_datapoint_from_table(self):
        data = self.get_data_queryset().order_by('-time')
        if any(data):
            return data[0] 
        else:
            return None

    def save(self, *args, **kwargs):
        self.alert_triggered = bool(self.check_alert())
        obj = super(Metric, self).save(*args, **kwargs)
        return obj

        
class MetricDataBase(models.Model):

    metric = models.ForeignKey(Metric)
    time = models.DateTimeField()
    
    has_error = models.BooleanField(default=False)
    error_message = models.CharField(null=True, blank=True, max_length=512)

    tags = models.CharField(max_length=256, default='', blank=True,
            help_text='Comma separated tags.')

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'{m} : {v} / {t}'.format(
                v=self.value,
                m=self.metric,
                t=self.time.isoformat(sep=' ').rsplit('.')[0])

    def value_from_string(self, value):
        raise NotImplementedError()

    def get_tags(self):
        return self.tags.rsplit(',')

    def has_tag(self, tag):
        return tag in self.get_tags()


class MetricDataInt(MetricDataBase):
    value = models.PositiveIntegerField(null=True, blank=True)

    def value_from_string(self, value):
        try:
            self.value = int(value.rstrip())
        except:
            raise


class MetricDataFloat(MetricDataBase):
    value = models.FloatField(null=True, blank=True)

    def value_from_string(self, value):
        try:
            self.value = float(value.rstrip())
        except:
            raise


class MetricDataChar(MetricDataBase):
    value = models.CharField(null=True, blank=True, max_length=1024)

    def value_from_string(self, value):
        try:
            self.value = value.rstrip()
        except:
            raise


class MetricDataDatetime(MetricDataBase):
    value = models.DateTimeField(null=True, blank=True)

    def value_from_string(self, value):
        try:
            self.value = datetime.strptime(value.rstrip(), '%Y-%m-%dT%H:%M:%S')
        except:
            raise


class MetricDataJSON(MetricDataBase):
    value = JSONField()

    def value_from_string(self, value):
        try:
            json_obj = json.loads(value)
            self.value = json_obj
        except:
            raise


'''
DESDM DASHBOARD

Django data model for saving system snapshot data for monitoring purposes.


'''

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class Instrument(models.Model):
    '''
    A tool to measure a Metric.
    '''
    name = models.CharField(max_length=31, unique=True)
    script = models.TextField()


class Source(models.Model):
    '''
    The source which is to be monitored.
    '''
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255, unique=True)

    TYPE_DATABASE = 'DB'
    TYPE_FILESYSTEM = 'FS'
    TYPE_OTHER = 'OT'

    TYPE_CHOICES =   (
            (TYPE_DATABASE, 'database'),
            (TYPE_FILESYSTEM, 'filesystem'),
            (TYPE_OTHER, 'other type'),
                        )

    stype = models.CharField(max_length=2, choices=TYPE_CHOICES)
    do_monitor = models.BooleanField(default=True)
    log = models.TextField(blank = True, null = True)

'''
class MetricManager(models.Manager):
    def get_by_natural_key(self, name, source, instrument):
        return self.get(name=name, source__name=source,
                instrument__name=instrument)
'''

class Metric(models.Model):
    '''
    The time series measured.
    '''
    name = models.CharField(max_length=255)
    source = models.ForeignKey(Source, blank=True, null=True)
    instrument  = models.ForeignKey(Instrument, blank=True, null=True)

    UNIT_BYTES = 'bytes'
    UNIT_SECONDS = 'seconds'

    UNIT_CHOICES = (
            (UNIT_BYTES, 'bytes'),
            (UNIT_SECONDS, 'seconds'),
            )
    unit = models.CharField(max_length=31, choices=UNIT_CHOICES)

    VALUE_TYPE_CHOICES = models.Q(app_label='monitor', model='metricdataint') |\
            models.Q(app_label='monitor', model='metricdatafloat') |\
            models.Q(app_label='monitor', model='metricdatachar') |\
            models.Q(app_label='monitor', model='metricdatadatetimegmt') |\
            models.Q(app_label='monitor', model='metricdatatimedelta')
    value_type = models.ForeignKey(generic.ContentType, 
            limit_choices_to=VALUE_TYPE_CHOICES)

    is_measured = models.BooleanField(default=True)

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

    doc = models.TextField()

    timestamp_created_gmt = models.DateTimeField(auto_now_add=True)
    timestamp_modified_gmt = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('name', 'source', 'instrument', ),)

    def __unicode__(self):
        if self.source:
            return u'{n} on {t}'.format(n=self.name, t=self.source.name)
        else:
            return u'{n}'.format(n=self.name)

    '''
    def natural_key(self):
        return (self.name, self.source.name, self.instrument.name)
    '''

    def add_value(self, value=None, has_error=False,
                    error_message='unspecified default error message'):
        '''
        Method to add a value to the corresponding table defined by value_type.
        '''
        if value is not None:
            vt_obj = self.value_type.model_class()(value=value, metric=self)
        elif value is None and has_error:
            vt_obj = self.value_type.model_class()(has_error=True,
                    error_message=error_message)
        else:
            err = ('You cannot provide a value and at '
                    'the same time set has_error to True.')
            raise ValueError(err)
        vt_obj.save()

    def get_data_queryset(self):
        vtclass = self.value_type.model_class()
        return vtclass.objects.filter(metric=self)

        


class MetricDataBase(models.Model):

    metric = models.ForeignKey(Metric)

    timepoint_gmt = models.DateTimeField(auto_now_add=True)
    
    has_error = models.BooleanField(default=False)
    error_message = models.CharField(null=True, blank=True, max_length=255)

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'{v} : {m} at {t}'.format(
                v=self.value,
                m=self.metric,
                t=self.timepoint_gmt.isoformat(sep=' ').rsplit('.')[0])


class MetricDataInt(MetricDataBase):
    value = models.PositiveIntegerField(null=True, blank=True)

class MetricDataFloat(MetricDataBase):
    value = models.FloatField(null=True, blank=True)

class MetricDataChar(MetricDataBase):
    value = models.CharField(null=True, blank=True, max_length=511)

class MetricDataDatetimeGMT(MetricDataBase):
    value = models.DateTimeField(null=True, blank=True)

class MetricDataTimeDelta(MetricDataBase):
    value = models.DateTimeField(null=True, blank=True)

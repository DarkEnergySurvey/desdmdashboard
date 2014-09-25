'''
DESDM DASHBOARD

Django data model for saving system snapshot data for monitoring purposes.


'''
import operator
import json

from datetime import datetime

from docutils.core import publish_parts

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.timezone import now
from django.utils.functional import cached_property
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

    DEFAULT_STALENESS_WARNING_AFTER_SECONDS = 60*60*24*2

    warning_if_no_value_after_seconds = models.PositiveIntegerField(
            default=DEFAULT_STALENESS_WARNING_AFTER_SECONDS, null=True,
            blank=True)

    latest_value = models.CharField(max_length=1024, null=True, blank=True)
    latest_time = models.DateTimeField(null=True, blank=True)

    latest_tags = models.CharField(max_length=256, blank=True, default='')

    has_error = models.BooleanField(default=False)
    error_message = models.CharField(null=True, blank=True, max_length=256)

    #source = models.ForeignKey(Source, blank=True, null=True)
    #source = models.CharField(max_length=512)
    #instrument  = models.ForeignKey(Instrument, blank=True, null=True)
    #instrument = models.CharField(max_length=512)

    UNIT_BYTES = 0 # 1000^0
    UNIT_KILOBYTES= 1
    UNIT_MEGABYTES = 2
    UNIT_GIGABYTES = 3
    UNIT_TERABYTES = 4
    UNIT_PETABYTES = 5
    UNIT_EXABYTES = 6

    UNIT_SECONDS = 10
    UNIT_MINUTES = 11
    UNIT_HOURS = 12

    UNIT_MB_PER_SECOND = 15

    UNIT_NUMCONNECTION = 20
    UNIT_NUMFILES = 21

    UNIT_CHOICES = (
            (UNIT_BYTES, 'Bytes'),
            (UNIT_KILOBYTES, 'KB'),
            (UNIT_MEGABYTES, 'MB'),
            (UNIT_GIGABYTES, 'GB'),
            (UNIT_TERABYTES, 'TB'),
            (UNIT_PETABYTES, 'PB'),
            (UNIT_SECONDS, 'seconds'),
            (UNIT_MINUTES, 'minutes'),
            (UNIT_HOURS, 'hours'),
            (UNIT_MB_PER_SECOND, 'MB/s'),
            (UNIT_NUMCONNECTION, '# Connections'),
            (UNIT_NUMFILES, '# Files'),
            )
    unit = models.PositiveSmallIntegerField(choices=UNIT_CHOICES, null=True,
            blank=True)

    VALUE_TYPE_CHOICES = models.Q(app_label='monitor', model='metricdataint') |\
            models.Q(app_label='monitor', model='metricdatafloat') |\
            models.Q(app_label='monitor', model='metricdatachar') |\
            models.Q(app_label='monitor', model='metricdatajson') |\
            models.Q(app_label='monitor', model='metricdataboolean') |\
            models.Q(app_label='monitor', model='metricdatadatetime')
    value_type = models.ForeignKey(generic.ContentType, 
            limit_choices_to=VALUE_TYPE_CHOICES)

    DASHBOARD_DISPLAY_OPTION_NOSHOW = 0
    DASHBOARD_DISPLAY_OPTION_TABLE = 1
    DASHBOARD_DISPLAY_OPTION_PLOT = 2

    DASHBOARD_DISPLAY_OPTION_CHOICES = (
            (DASHBOARD_DISPLAY_OPTION_NOSHOW, "don't show"),
            (DASHBOARD_DISPLAY_OPTION_TABLE, "table"),
            (DASHBOARD_DISPLAY_OPTION_PLOT, "plot"),
            )

    dashboard_display_option = models.PositiveSmallIntegerField(
            choices=DASHBOARD_DISPLAY_OPTION_CHOICES,
            default=DASHBOARD_DISPLAY_OPTION_PLOT)

    dashboard_display_window_length_days = models.PositiveSmallIntegerField(
            default=7)

    OPERATOR_CHOICES = (
        ('lt', 'latest value < alert value'),
        ('le', 'latest value <= alert value'),
        ('eq', 'latest value == alert value'),
        ('ne', 'latest value != alert value'),
        ('ge', 'latest value >= alert value'),
        ('gt', 'latest value > alert value'),
    )
    alert_operator = models.CharField(max_length=2, choices=OPERATOR_CHOICES,
            blank=True)
    alert_value = models.FloatField(null=True, blank=True)
    alert_triggered = models.BooleanField(default=False)

    expression_string = models.CharField(null=True, blank=True, max_length=512)

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
                kwargs={'nameslug': self.slug, 'owner': self.owner.username})

    @property
    def doc_rst_as_html(self):
        '''
        returns the doc string as rendered html under assumption that it is
        restructerd text.  '''
        try:
            doc_html = publish_parts(self.doc, writer_name='html', 
                    settings_overrides={'doctitle_xform':False,
                        'initial_header_level': 4, 'report_level': 'quiet'}
                    )['html_body']
            return doc_html
        except Exception, err:
            return err

    @property
    def has_no_value_warning(self):
        '''
        '''
        #dp = self.get_last_datapoint_from_table()
        #delta_t = now() - dp.time
        delta_t = now() - self.latest_time
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

    @property
    def expression_evaluation(self):
        try:
            df = self.get_data_dataframe()
            r = eval(self.expression_string, {}, { 'data': df })
            return r
        except Exception, err:
            return err

    def get_trouble_statements(self):
        troubles = []
        if self.has_error:
            troubles.append('ERROR MESSAGE: ' + self.error_message)
        if self.alert_triggered:
            alert_str = ('ALERT TRIGGERED: {op} !').format(
                    op=self.get_alert_operator_display())
            troubles.append(alert_str)
        if self.has_no_value_warning:
            troubles.append('NO VALUE UPDATE!! within %s seconds' %\
                    self.warning_if_no_value_after_seconds)
        return troubles

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
        elif value_type.lower() == 'json':
            obj.value_type = ContentType.objects.get(model='metricdatajson')
        elif value_type.lower() == 'boolean':
            obj.value_type = ContentType.objects.get(model='metricdataboolean')
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
            self.latest_time = time

    def _save_latest_values_to_data_table(self):
        ''' '''
        dobj = self.create_value_obj()
        dobj.time = self.latest_time
        dobj.has_error = self.has_error
        dobj.error_message = self.error_message
        if not dobj.has_error:    
            dobj.value_from_string(self.latest_value)
        dobj.save()

    def get_data_queryset(self):
        vtclass = self.value_type.model_class()
        return vtclass.objects.filter(metric=self)

    @cached_property
    def data_queryset(self):
        vtclass = self.value_type.model_class()
        return vtclass.objects.filter(metric=self)

    @cached_property
    def data_records(self):
        return list(self.data_queryset)

    @cached_property
    def data_dataframe(self):
        return self.get_data_dataframe()

    def get_data_dataframe(self, fields=('time', 'value'), index='time',
            filter=None):
        try:
            import pandas
            if filter:
                qs = self.data_queryset.filter(**filter)
            else:
                qs = self.data_queryset
            return pandas.DataFrame.from_records(qs.values(*fields),
                    index=index)
        except:
            raise

    def get_last_datapoint_from_table(self):
        data = self.data_queryset.order_by('-time')
        if any(data):
            return data.first()
        else:
            return None

    def save(self, *args, **kwargs):
        self.alert_triggered = bool(self.check_alert())
        try:
            self.metriccache_set.first().update_cache()
        except Exception, e:
            pass
        obj = super(Metric, self).save(*args, **kwargs)
        return obj

        
class MetricDataBase(models.Model):

    metric = models.ForeignKey(Metric)
    time = models.DateTimeField()
    
    has_error = models.BooleanField(default=False)
    error_message = models.CharField(null=True, blank=True, max_length=512)

    tags = models.CharField(max_length=256, default='', blank=True,
            help_text='Comma separated tags.')

    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_modified = models.DateTimeField(auto_now=True)

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
    value = models.BigIntegerField(null=True, blank=True)

    def value_from_string(self, value):
        try:
            if value:
                self.value = int(value.rstrip())
            else:
                self.value = None
        except:
            raise


class MetricDataFloat(MetricDataBase):
    value = models.FloatField(null=True, blank=True)

    def value_from_string(self, value):
        try:
            if value:
                self.value = float(value.rstrip())
            else:
                self.value = None
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
            if value:
                self.value = datetime.strptime(value.rstrip(), '%Y-%m-%d %H:%M:%S')
            else:
                self.value = None
        except:
            raise


class MetricDataJSON(MetricDataBase):
    value = JSONField()

    def value_from_string(self, value):
        try:
            if value:
                json_obj = json.loads(value)
                self.value = json_obj
            else:
                self.value = None
        except:
            raise


class MetricDataBoolean(MetricDataBase):
    value = models.BooleanField(default=False)

    def value_from_string(self, value):
        try:
            if value.lower() in ['1', 'true', ]:
                self.value = True
            elif value == '':
                self.value = None
            elif value.lower() in ['0', 'false', ]:
                self.value = False
            else:
                raise ValueError("Value has to be from ['1', 'True', '', 'False', '0', ]")
        except:
            raise


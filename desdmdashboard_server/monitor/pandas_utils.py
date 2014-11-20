
from datetime import timedelta 

import pandas

from django.conf import settings
from django.utils.timezone import now

from .models import Metric
from .serializers import MetricDataJSONSerializer


DEFAULT_PERIOD_LENGTH = timedelta(10)


def get_metric_dataframe(owner, name, fields=('time','value', ),
        index='time', period_from=None, period_to=None):
    '''
    Possible fields:
    fields = ('time', 'value', 'has_error', 'error_message', 'tags', )

    MetricDataJSON value fields are automatically expanded if 'value' is in
    fields.

    With the period_from and period_to keywords arguments you can specify the
    period your data should originate from. If these arguments are None there
    are simply no restrictions with respect to the boundary.
    '''
    metric = Metric.objects.get_by_natural_key(owner, name)
    df = get_dataframe(metric, fields=fields, index=index,
            period_from=period_from, period_to=period_to)
    return df, metric
    

def get_dataframe(metric, fields=('time','value', ), index='time',
        period_from=now()-DEFAULT_PERIOD_LENGTH, period_to=None):
    '''
    '''
    if metric.value_type.model == 'metricdatajson':
        
        mdata = metric.get_data_queryset()
        if period_from:
            mdata = mdata.filter(time__gte=period_from)
        if period_to:
            mdata = mdata.filter(time__lte=period_to)

        ser = MetricDataJSONSerializer(
                instance=mdata, many=True)

        if 'value' in fields:
            value = True
            fields = list(fields)
            fields.remove('value')
        else:
            value = False

        data = [{k: v for k, v in el.iteritems() if k in fields } for el in
                ser.data ]

        if value:
            for i, datrow in enumerate(data):
                datrow.update(ser.data[i]['value'])

        df = pandas.DataFrame(data)
        
    else:
        mdata = metric.get_data_queryset().values(*fields)

        if period_from:
            mdata = mdata.filter(time__gte=period_from)
        if period_to:
            mdata = mdata.filter(time__lte=period_to)

        df = pandas.DataFrame(list(mdata))

    if index:
        try:
            df = df.set_index(index)
        except:
            print 'could not set dataframe index to ', index

        if index == 'time':
            df.index = df.index.tz_convert(settings.TIME_ZONE)

    if 'value' in df:
        columns = df.columns.tolist()
        columns[columns.index('value')] = metric.name
        df.columns = columns

    return df


def get_multimetric_dataframe(owner_name_pairs, resample='D', period_from=None,
        period_to=None):
    '''
    Returns a timeseries dataframe for multiple Metrics specified by 
    an iterable consisting of (owner__username, name) tuples.
    '''

    dfs = {}
    metrics = {}

    for i, metricspec in enumerate(owner_name_pairs):
        dfs[metricspec[1]], metrics[metricspec[1]] = get_metric_dataframe(
                metricspec[0], metricspec[1])

    df = pandas.concat(dfs.values(), join='outer', axis=0,)

    if resample:
        df = df.resample(resample)

    return df, metrics

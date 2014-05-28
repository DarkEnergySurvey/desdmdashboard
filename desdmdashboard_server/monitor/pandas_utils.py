
import pandas
from .models import Metric
from .serializers import MetricDataJSONSerializer


def get_metric_dataframe(name, owner, fields=('time','value', ),
        index='time'):
    '''
    possible fields:
    fields = ('time', 'value', 'has_error', 'error_message', 'tags', )

    MetricDataJSON value fields are automatically expanded if 'value' is in
    fields.
    '''
    metric = Metric.objects.get_by_natural_key(name, owner)
    
    if metric.value_type.model == 'metricdatajson':
        ser = MetricDataJSONSerializer(
                instance=metric.get_data_queryset(), many=True)

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
        df = pandas.DataFrame(list(mdata))

    if index:
        try:
            df = df.set_index(index)
        except:
            print 'could not set dataframe index to ', index

    if 'value' in df:
        columns = df.columns.tolist()
        columns[columns.index('value')] = name
        df.columns = columns

    return df


def get_multimetric_dataframe(name_owner_pairs, resample='D'):
    '''
    Returns a timeseries dataframe for multiple Metrics specified by 
    an iterable consisting of (name, owner__username) tuples.
    '''

    dfs = {}

    for i, metricspec in enumerate(name_owner_pairs):
        dfs[metricspec[0]] = get_metric_dataframe(metricspec[0], metricspec[1])

    df = pandas.concat(dfs.values(), join='outer', axis=0,)

    if resample:
        df = df.resample(resample)

    return df

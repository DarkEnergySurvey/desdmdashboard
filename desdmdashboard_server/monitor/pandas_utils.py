
import pandas
from monitor.models import Metric

def get_dataframe(name_owner_pairs):
    '''
    Returns a timeseries dataframe for multiple Metrics specified by 
    an iterable consisting of (name, owner__username) tuples.
    '''

    dfs = {}

    for i, metricspec in enumerate(name_owner_pairs):
        metric = Metric.objects.get(name=metricspec[0],
                owner__username=metricspec[1])
        mdata = Metric.data.get_queryset(metric.name, metric.owner)
        if metric.value_type.model == 'metricdatajson':
            pass
        else:
            dfs[metric.name] = mdata.to_timeseries(
                    index='time', fieldnames=('value',))

    df = pandas.concat(dfs.values(), join='outer', axis=1,).resample('D')
    df.columns = dfs.keys()

    return df

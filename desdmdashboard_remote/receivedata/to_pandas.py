'''
'''

import json
import pandas

from ..http_requests import Request, API_URL 


def get_metric_dataframe(name, owner=None, fields=('time', 'value'),
        index='time'):
    '''
    '''

    # GET META INFORMATION ABOUT METRIC FIRST
    # we have to do that to get the pk of the metric
    meta_request = Request()
    if owner is None:
        meta_request.GET(url=API_URL, params={'name': name, 'format': 'json', })
    else:
        meta_request.GET(url=API_URL, params={'name': name, 'format': 'json',
            'owner': owner })
    meta_response = json.loads(meta_request.response.read())

    if len(meta_response) == 0:
        raise ValueError(('The metric "{n}" does not exist in your '
                'namespace.').format(n=name))

    if len(meta_response) > 1:
        print meta_response
        raise IOError('Received too many metrics. This should not happen!')

    meta_response = meta_response[0]

    # GET THE METRIC DATA
    md_getparams = {
            'metric_pk': meta_response['pk'],
            'value_type': meta_response['value_type_'].replace(' ', ''),
            'format': 'json',
            }

    data_request = Request()
    data_request.GET(params=md_getparams)

    if md_getparams['value_type'] == 'metricdatajson':
        data = json.loads(data_request.response.read())

        if 'value' in fields:
            value = True
            fields = list(fields)
            fields.remove('value')
        else:
            value = False

        dfdata = [{k: v for k, v in el.iteritems() if k in fields } for el in
                data ]

        if value:
            for i, datrow in enumerate(data):
                dfdata[i].update(datrow['value'])

        df = pandas.DataFrame(dfdata)

    else:
        df = pandas.io.api.read_json(data_request.response.read())
        for col in df.columns.tolist():
            if col not in fields:
                del(df[col])

        if md_getparams['value_type'] == 'metricdatadatetime':
            df['value'] = pandas.to_datetime(df['value'])

        if 'value' in df.columns.tolist():
            columns = df.columns.tolist()
            columns[columns.index('value')] = name
            df.columns = columns

    if 'time' in df.columns.tolist():
        df['time'] = pandas.to_datetime(df['time'])

    if index:
        try:
            df = df.set_index(index)
        except:
            print 'could not set dataframe index to ', index

    return df 


def get_multimetric_dataframe(name_owner_pairs, resample='D'):
    '''
    Returns a timeseries dataframe for multiple Metrics specified by 
    an iterable consisting of (name, owner__username) tuples.
    '''

    dfs = {}

    for i, metricspec in enumerate(name_owner_pairs):
        dfs[metricspec[0]] = get_metric_dataframe(metricspec[0], owner=metricspec[1])

    df = pandas.concat(dfs.values(), join='outer', axis=0,)

    if resample:
        df = df.resample(resample)

    return df

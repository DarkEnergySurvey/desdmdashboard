from monitor import pandas_utils


def deshist():
    '''
    '''
    df = pandas_utils.get_metric_dataframe('deshist', 'don', index=None)
    return df.to_html(index=False, classes='sortable') 


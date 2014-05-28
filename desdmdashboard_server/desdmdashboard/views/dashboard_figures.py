
from monitor import pandas_utils

from . import plotutils


def deshist():
    '''
    '''
    df = pandas_utils.get_metric_dataframe('deshist', 'don')
    return df.to_html(index=False, classes='sortable') 


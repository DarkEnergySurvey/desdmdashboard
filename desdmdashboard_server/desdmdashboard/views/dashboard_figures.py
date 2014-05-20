
import json
import pandas

from monitor.pandas_utils import get_dataframe
from monitor import models

from . import plotutils


def deshist():
    '''
    '''

    mquery = models.Metric.data.get_queryset('deshist', 'don')
    recs = [r[0] for r in list(mquery.values_list('value'))]
    ddicts = [json.loads(json.loads(r)) for r in recs]
    df = pandas.io.json.json_normalize(ddicts)

    return df.to_html(index=False, classes='sortable') 


"""
def iforge_overview():
    '''
    '''

    metrices = (('iforge_total', 'don'), ('iforge_nothomed', 'don'),
            ('iforge_run', 'don'), ('iforge_src', 'don'),
            ('iforge_cal', 'don'),)
    df = get_dataframe(metrices)
    figstring = plotutils.plot_df_to_svg_string(df, style='.-', y_label='Bytes')

    return figstring 


def Write_HTML_String():
    return '<h4>Header 4</h4>What else?'
"""

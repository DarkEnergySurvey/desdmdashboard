
from monitor.pandas_utils import get_dataframe

from . import plotutils


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

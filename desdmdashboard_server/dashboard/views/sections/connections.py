from datetime import timedelta
from django.utils.timezone import now

from monitor import pandas_utils
from dashboard.views.plotutils import plot_df_to_svg_string

# SHOW, ie is ACTIVE?
ACTIVE = False 

PERIOD_SHOWN = 8 # days
PERIOD_FROM = now()-timedelta(PERIOD_SHOWN)

def connections2D_summary():
    '''
    :View Author: Michael Graber
    '''

    df, metrics = pandas_utils.get_multimetric_dataframe(
            (('gdaues', 'desar_conn_to_any', ),
                ('gdaues', 'connections_to_fermigrid', ),
                ('gdaues', 'desar_conn_to_noao', ),
                ('gdaues', 'desar_conn_to_gpfs', ),
                ('gdaues', 'connections_to_stken', ),),
            resample='20Min',
            period_from=PERIOD_FROM,
            )
    # do anything with panda you want

    # do the plotting
    figstring = plot_df_to_svg_string(df.last('2D'), 
            metrics=metrics,
            style='.-', y_label='# Connections',
            legend_loc='upper left',
            ylim=(0, 'auto'), colormap='spectral')

    sectiondict = {
            'title': 'Network connections 2 Days',
            'content_html': figstring, 
            }

    return sectiondict

def connections_summary():
    '''
    :View Author: Michael Graber
    '''
    df, metrics = pandas_utils.get_multimetric_dataframe(
            (('gdaues', 'desar_conn_to_any', ),
                ('gdaues', 'connections_to_fermigrid', ),
                ('gdaues', 'desar_conn_to_noao', ),
                ('gdaues', 'desar_conn_to_gpfs', ),
                ('gdaues', 'connections_to_stken', ),),
            resample='H',
            period_from=PERIOD_FROM,
            )
    # do anything with panda you want

    # do the plotting
    figstring = plot_df_to_svg_string(df.last('7D'), 
            metrics=metrics,
            style='-', y_label='# Connections',
            legend_loc='upper left',
            ylim=(0, 'auto'), colormap='spectral')

    sectiondict = {
            'title': 'Network connections 7 Days',
            'content_html': figstring, 
            }

    return sectiondict


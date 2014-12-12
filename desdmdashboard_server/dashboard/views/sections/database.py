from datetime import timedelta
from django.utils.timezone import now

from monitor import pandas_utils
from dashboard.views.plotutils import plot_df_to_svg_string

# SHOW, ie is ACTIVE?
ACTIVE = True 

PERIOD_SHOWN = 31 # days
PERIOD_FROM = now()-timedelta(PERIOD_SHOWN)

def desoper():
    '''
    Read, write and mydb operations on desoper.

    :View Author: Michael Graber
    '''
    df, metrics = pandas_utils.get_multimetric_dataframe(
            (('gdaues', 'desoper_write_GB', ),
                ('gdaues', 'desoper_read_GB', ),
                ('gdaues', 'desoper_mydb_GB', ), ),
            resample='D',
            period_from=PERIOD_FROM,
            )
    # do anything with panda you want

    # do the plotting
    figstring = plot_df_to_svg_string(df.last('30D'),
            metrics=metrics,
            style='.-', colormap='jet',
            logy=True, y_label='GB')

    sectiondict = {
            'title': 'desoper operations',
            'content_html': figstring, 
            }

    return sectiondict


def dessci():
    '''
    Read, write and mydb operations on dessci.

    :View Author: Michael Graber
    '''
    df, metrics = pandas_utils.get_multimetric_dataframe(
            (('gdaues', 'dessci_write_GB', ),
                ('gdaues', 'dessci_read_GB', ),
                ('gdaues', 'dessci_mydb_GB', ),),
            resample='D',
            period_from=PERIOD_FROM,
            )
    # do anything with panda you want

    # do the plotting
    figstring = plot_df_to_svg_string(df.last('30D'),
            metrics=metrics,
            style='.-', y_label='GB')

    sectiondict = {
            'title': 'dessci operations',
            'content_html': figstring, 
            }

    return sectiondict


from monitor import pandas_utils
from dashboard.views.plotutils import plot_df_to_svg_string

# SHOW, ie is ACTIVE?
ACTIVE = True 

def desoper():
    df, metrics = pandas_utils.get_multimetric_dataframe(
            (('gdaues', 'desoper_write_GB', ),
                ('gdaues', 'desoper_read_GB', ),
                ('gdaues', 'desoper_mydb_GB', ), ),
            resample='D',
            )
    # do anything with panda you want

    #get serillizes plot
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
    Read, write and **MyDB** operations ..

    - list item 1
    - list item 2
    - list item 3

    .. sourcecode:: python

        def say_hi():
            print 'hi!'

    :Author: Michael Graber
    '''
    df, metrics = pandas_utils.get_multimetric_dataframe(
            (('gdaues', 'dessci_write_GB', ),
                ('gdaues', 'dessci_read_GB', ),
                ('gdaues', 'dessci_mydb_GB', ),),
            resample='D',
            )
    # do anything with panda you want

    #get serillizes plot
    figstring = plot_df_to_svg_string(df.last('30D'),
            metrics=metrics,
            style='.-', y_label='GB')

    sectiondict = {
            'title': 'dessci operations',
            'content_html': figstring, 
            }

    return sectiondict

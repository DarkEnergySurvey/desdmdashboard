from monitor import pandas_utils
from dashboard.views.plotutils import plot_df_to_svg_string

def desoper():
    df = pandas_utils.get_multimetric_dataframe(
            (('desoper_write_GB', 'gdaues',),
                ('desoper_read_GB', 'gdaues',),
                ('desoper_mydb_GB', 'gdaues',),),
            resample='D',
            )
    # do anything with panda you want

    #get serillizes plot
    figstring = plot_df_to_svg_string(df, style='.-', logy=True, y_label='GB')

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
    df = pandas_utils.get_multimetric_dataframe(
            (('dessci_write_GB', 'gdaues',),
                ('dessci_read_GB', 'gdaues',),
                ('dessci_mydb_GB', 'gdaues',),),
            resample='D',
            )
    # do anything with panda you want

    #get serillizes plot
    figstring = plot_df_to_svg_string(df, style='.-', y_label='GB')

    sectiondict = {
            'title': 'dessci operations',
            'content_html': figstring, 
            }

    return sectiondict

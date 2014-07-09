from monitor import pandas_utils
from dashboard.views.plotutils import plot_df_to_svg_string

def size():
    '''
    '''
    df = pandas_utils.get_multimetric_dataframe(
            (('toy_metric_0', 'donaldp',),),
            resample='D',
            )
    # do anything with panda you want

    #get serillizes plot
    figstring = plot_df_to_svg_string(df, style='.-', logy=True)
    return figstring


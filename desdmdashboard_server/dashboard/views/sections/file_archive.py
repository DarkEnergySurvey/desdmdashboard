from monitor import pandas_utils
from dashboard.views.plotutils import plot_df_to_svg_string

def size():
    '''
    '''
    df = pandas_utils.get_multimetric_dataframe(
            (('size desar2home', 'mgraber',),),
            resample='D',
            )
    figstring = plot_df_to_svg_string(df, style='.-', logy=True)
    return figstring


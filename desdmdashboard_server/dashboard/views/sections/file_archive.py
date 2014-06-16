from monitor import pandas_utils
from dashboard.views.plotutils import plot_df_to_svg_string

def archive_sizes():
    '''
    '''
    df = pandas_utils.get_multimetric_dataframe(
            (('size desar2home', 'mgraber',),
            ('size archive_home_mjohns44', 'mgraber',),
            ('size archive_target_mjohns44', 'mgraber',),
            ('size desdev1_mmg', 'mgraber',),),
            resample='20Min',
            )
    figstring = plot_df_to_svg_string(df, style='.-')
    return figstring


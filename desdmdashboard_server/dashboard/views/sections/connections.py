from monitor import pandas_utils
from dashboard.views.plotutils import plot_df_to_svg_string

def connections_summary():
    df, metrics = pandas_utils.get_multimetric_dataframe(
            (('gdaues', 'desar_conn_to_any', ),
                ('gdaues', 'connections_to_fermigrid', ),
                ('gdaues', 'desar_conn_to_noao', ),
                ('gdaues', 'desar_conn_to_gpfs', ),
                ('gdaues', 'connections_to_stken', ),),
            resample='H',
            )
    # do anything with panda you want

    #get serillizes plot
    figstring = plot_df_to_svg_string(df.last('7D'), 
            metrics=metrics,
            style='.-', y_label='# Connections',
            ylim=(0, 100), colormap='spectral')

    sectiondict = {
            'title': 'Network connections',
            'content_html': figstring, 
            }

    return sectiondict


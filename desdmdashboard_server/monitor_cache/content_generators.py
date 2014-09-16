'''
A library of functions that are used to create the content that is cached.

'''


import StringIO
from datetime import timedelta

import matplotlib.pyplot as plt

from django.utils.timezone import now



def create_svg_plot_for_metric(metric, kind='detail'):

    plot_after = now() - timedelta(
            metric.dashboard_display_window_length_days)

    # get the data for the metric
    df = metric.data_dataframe

    imgdata = StringIO.StringIO()

    if kind == 'detail':
        ax = df.plot(
                style='.-',
                fontsize=2,
                figsize=(8,4),
                lw=1.5,
                color=(0, 0, 0.6),
                xlim=(plot_after, now()),
                )
        ax.legend((metric.name,), loc='best')

    elif kind == 'dashboard':
        ax = df.plot(
                fontsize=1,
                figsize=(4.7,2.7),
                lw=1.5,
                color=(0, 0, 0.6),
                legend=False,
                xlim=(plot_after, now()),
                )

    if metric.value_type.model in ['metricdataint', 'metricdatafloat', ]:
        if metric.alert_value:
            yav = [metric.alert_value, metric.alert_value, ]
            xlim = ax.get_xlim()
            xav = [xlim[0], xlim[1],]
            ax.plot(xav,yav, 'r--')


    if metric.unit:
        ax.set_ylabel(metric.get_unit_display())
    fig = ax.get_figure()
    fig.tight_layout()

    fig.savefig(imgdata, format='svg')
    plt.close(fig)
    imgdata.seek(0)
    
    return imgdata.buf



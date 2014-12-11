import StringIO
from datetime import timedelta

from matplotlib import pyplot as plt
import numpy as np

from django.utils.timezone import now

from monitor import pandas_utils, models
from dashboard.views.plotutils import plot_df_to_svg_string


# SHOW, ie is ACTIVE?
ACTIVE = True 

# some constants
SHOW_NUMBER_OF_DAYS = 10


# reading the desdf metrics from the db and grouping them
desdf_metrics = models.Metric.objects.filter(name__startswith='desdf_')
desdf_names = [nd['name'] for nd in desdf_metrics.values('name')]
name_groups = { name.rsplit('_')[1]: [] for name in desdf_names }
for name in desdf_names:
    name_groups[name.rsplit('_')[1]].append(name)


def desdf_overview(name_groups=name_groups):
    '''
    Evolution of disk space over time.
    '''

    # setting up the figure for all subplots
    fig, ax = plt.subplots(nrows=len(name_groups), ncols=1,
            figsize=(8, len(name_groups)*2.5))
    plot_after = now() - timedelta(SHOW_NUMBER_OF_DAYS)

    # create all subplots
    for i, namegroup in enumerate(sorted(name_groups.keys())):

        # create (owner, name) tuples
        ontups = tuple(('gdaues', name) for name in name_groups[namegroup])

        df, metrics = pandas_utils.get_multimetric_dataframe(ontups,
                resample='D', period_from=plot_after)

        # plotting
        df.last(str(SHOW_NUMBER_OF_DAYS)+'D').plot(
                style='.-', colormap='jet', ax=ax[i], legend=False,
                xlim=(plot_after, now()))

        # tweaking the plot
        ax[i].set_ylim(0,ax[i].get_ylim()[1])
        ax[i].set_ylabel('TB')
        ax[i].legend(sorted(name_groups[namegroup]), loc='best')

    fig.tight_layout()

    # getting the svg string
    imgdata = StringIO.StringIO()
    fig.savefig(imgdata, format='svg')
    plt.close(fig)
    imgdata.seek(0)
    figstring = imgdata.buf

    sectiondict = {
            'title': 'DESDF overview',
            'content_html': figstring, 
            }

    return sectiondict


import StringIO

from datetime import timedelta

from matplotlib import pyplot as plt

from django.shortcuts import render, render_to_response, get_object_or_404
from django.utils.timezone import now

from monitor.models import Metric
from monitor.pandas_utils import get_multimetric_dataframe

from dashboard.views.plotutils import plot_df_to_svg_string

PERIOD_SHOWN = 2 # days
PERIOD_FROM = now()-timedelta(PERIOD_SHOWN)


def get_vm_section_dict(vm_name):
    if not Metric.objects.filter(name__startswith='VM_'+vm_name):
        return []
    content_generators = (
            memory_overview, 
            df_overview,
            cpu_load, 
            tcp_connections,
            )
    section_dicts = []
    for gen in content_generators:
        section_dicts.append(gen(vm_name))
    return section_dicts 


# content generators
# -----------------------------------------------------------------------------

def cpu_load(vmname):
    metric = Metric.objects.get(name='VM_'+vmname+'_avg-load-per-cpu')
    figstring = metric.cache.first().current_detail_figure
    section_dict = {
            'title' : 'Average Load per CPU',
            'content_html' : figstring,
            }
    return section_dict 


def tcp_connections(vmname):
    metric = Metric.objects.get(name='VM_'+vmname+'_tcp-connections')
    figstring = metric.cache.first().current_detail_figure
    section_dict = {
            'title' : 'tcp Connections',
            'content_html' : figstring,
            }
    return section_dict 


def memory_overview(vmname):
    '''
    A plot about the development of the system memory.
    '''
    metrics = Metric.objects.filter(name__startswith='VM_'+vmname+'_meminfo')
    owner_name_list = [(vm['owner__username'], vm['name'])
            for vm in metrics.values('name', 'owner__username')]

    df, metrics = get_multimetric_dataframe(owner_name_list, resample='30Min',
            period_from=PERIOD_FROM)

    # convert to MB, we have bytes
    df = df / 1000000
    df.columns = [col.rsplit('-')[-1] for col in df.columns]

    figstring = plot_df_to_svg_string(df, 
            metrics=metrics,
            style='-', y_label='GB',
            ylim=(.1, 'auto'), logy=True, legend_loc='lower left',
            figsize=(8, 4), colormap='spectral', )

    section_dict = {
            'title' : 'Memory Overview',
            'content_html' : figstring,
            }

    return section_dict 


def df_overview(vmname, show_num_days=10):

    plot_after = now()-timedelta(show_num_days)

    metrics = Metric.objects.filter(name__startswith='VM_'+vmname+'_df-')
    owner_name_list = [(vm['owner__username'], vm['name'])
            for vm in metrics.values('name', 'owner__username')]

    filesystems = set([name.rsplit('_')[-1].rsplit('-')[1]
        for _, name in owner_name_list])

    fig, ax = plt.subplots(nrows=len(filesystems), ncols=1,
            figsize=(8, len(filesystems)*3))

    for i, fs in enumerate(filesystems):
        metrics = Metric.objects.filter(
                name__startswith='VM_'+vmname+'_df-'+fs+'-')
        owner_name_list = [(vm['owner__username'], vm['name'])
                for vm in metrics.values('name', 'owner__username')]

        df, metrics = get_multimetric_dataframe(owner_name_list,
                resample='6H', period_from=plot_after)

        # shorten the metric names
        df.columns = [col.rsplit('_')[-1].rsplit('-')[-1] for col in df.columns]
        # rename 'blocks' to 'Size'
        df.colums = [n for n in df.columns]

        # convert to GB, we have KB so far
        df = df / 1000000.

        df.plot(style='-', colormap='jet', ax=ax[i], legend=False,
                xlim=(plot_after, now()),)

        # tweaking the plot
        maxy = ax[i].get_ylim()[1]
        ax[i].set_ylim(0,maxy+0.1*maxy)
        ax[i].set_ylabel('GB')
        ax[i].legend(df.columns, loc='best')
        ax[i].set_title(fs)

    fig.tight_layout()

    # getting the svg string
    imgdata = StringIO.StringIO()
    fig.savefig(imgdata, format='svg')
    plt.close(fig)
    imgdata.seek(0)
    figstring = imgdata.buf

    section_dict = {
            'title': 'Filesystems overview',
            'content_html': figstring, 
            }

    return section_dict



# utilities
# -----------------------------------------------------------------------------

def get_vm_dict():
    vmmetrics = Metric.objects.filter(name__startswith='VM_')
    namelist = [vm['name'].rsplit('_')[1] for vm in vmmetrics.values('name')]
    vm_dict = { vm:vm.replace('.', '_') for vm in set(namelist)}
    return vm_dict



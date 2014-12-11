
from datetime import timedelta

from django.shortcuts import render, render_to_response, get_object_or_404
from django.utils.timezone import now

from monitor.models import Metric
from monitor.pandas_utils import get_multimetric_dataframe

from dashboard.views.plotutils import plot_df_to_svg_string

PERIOD_SHOWN = 2 # days
PERIOD_FROM = now()-timedelta(PERIOD_SHOWN)


def get_vm_section_dict(vm):
    content_generators = (
            memory_overview, 
            cpu_load, 
            tcp_connections,
            )
    section_dicts = []
    for gen in content_generators:
        section_dicts.append(gen(vm))
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

    df.columns = [col.rsplit('-')[-1] for col in df.columns]

    figstring = plot_df_to_svg_string(df, 
            metrics=metrics,
            style='.-', y_label='GB',
            ylim=(0, 'auto'), logy=True, legend_loc='lower left',
            figsize=(8, 4), colormap='spectral', )

    section_dict = {
            'title' : 'Memory Overview',
            'content_html' : figstring,
            }

    return section_dict 



# utilities
# -----------------------------------------------------------------------------

def get_vm_dict():
    vmmetrics = Metric.objects.filter(name__startswith='VM_')
    namelist = [vm['name'].rsplit('_')[1] for vm in vmmetrics.values('name')]
    vm_dict = { vm:vm.replace('.', '_') for vm in set(namelist)}
    return vm_dict



import StringIO

import pandas
import matplotlib.pyplot as plt

from django.shortcuts import render, render_to_response, get_object_or_404

from monitor.models import Metric
from monitor_cache.models import MetricCache

from django.utils.timezone import now
from datetime import timedelta

font = {
    'family' : 'sans-serif',
#   'weight' : 'bold',
    'size'   : 8,
    }

plt.rc('font', **font)


def dashboard(request, owner=None):

    if owner:
        ms = Metric.objects.filter(owner__username=owner).extra(select={'lower_name': 'lower(name)'}).order_by('lower_name')
    else:
        ms = Metric.objects.all().extra(select={'lower_name': 'lower(name)'}).order_by('lower_name')

    metrices = []
    for metric in ms:

        mc = metric.metriccache_set.first()
        if not mc:
            MetricCache.create_or_update(metric)

        if metric.dashboard_display_option == metric.DASHBOARD_DISPLAY_OPTION_PLOT:
            try:
                #data_display = plot_svgbuf_for_metric(metric, size='small')
                data_display = mc.current_dashboard_figure
            except Exception, e:
                data_display = e
        elif metric.dashboard_display_option == metric.DASHBOARD_DISPLAY_OPTION_TABLE:
            try:
                df = metric.get_data_dataframe()
                df = df[['value', 'has_error', 'error_message']]
                data_display = df.to_html()
            except Exception, e:
                data_display = e
        else:
            continue
        m = {
            'name': metric.name,
            'is_in_trouble_status': metric.is_in_trouble_status,
            'data_display': data_display,
            'owner': metric.owner.username,
            'get_absolute_url': metric.get_absolute_url(),
            'last_updated': metric.latest_time,
            }
        metrices.append(m)

    return render_to_response('monitor_dashboard.html',\
            { 'metrices': metrices, 'owner': owner, })


def metric_detail(request, owner=None, nameslug=None):

    metric = get_object_or_404(Metric, slug=nameslug, owner__username=owner)

    try:
        imdata = plot_svgbuf_for_metric(metric) 
    except Exception, e:
        imdata = e

    return render_to_response('metric_detail.html',\
            { 'metric': metric, 'figure': imdata })


def plot_svgbuf_for_metric(metric, size='big'):

    plot_after = now() - timedelta(
            metric.dashboard_display_window_length_days)

    # get the data for the metric
    df = metric.data_dataframe

    imgdata = StringIO.StringIO()

    if size == 'big':
        ax = df.plot(
                style='.-',
                fontsize=2,
                figsize=(8,4),
                lw=1.5,
                color=(0, 0, 0.6),
                xlim=(plot_after, now()),
                )
        ax.legend((metric.name,), loc='best')

    elif size == 'small':
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

    # give some space to the graph on the y axis
    ylim = ax.get_ylim()
    ylen = ylim[1]-ylim[0]
    ax.set_ylim(ylim[0]-0.05*ylen, ylim[1]+0.05*ylen)

    if metric.unit:
        ax.set_ylabel(metric.get_unit_display())
    fig = ax.get_figure()
    fig.tight_layout()

    fig.savefig(imgdata, format='svg')
    plt.close(fig)
    imgdata.seek(0)
    
    return imgdata.buf

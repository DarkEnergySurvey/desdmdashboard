import StringIO

import matplotlib.pyplot as plt

from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext

from monitor.models import Metric


def dashboard(request, owner=None):

    if owner:
        ms = Metric.objects.filter(owner__username=owner)
    else:
        ms = Metric.objects.all()

    metrices = []
    for metric in ms:
        m = {
            'name': metric.name.upper(),
            'has_error': metric.has_error,
            'doc' : metric.doc,
            'svgplot': plot_svgbuf_for_metric(metric),
            'owner': metric.owner.username,
            'get_absolute_url': metric.get_absolute_url()
            }

        metrices.append(m)

    return render_to_response('dashboard.html',\
            { 'metrices': metrices })


def metric_detail(request, owner=None, name=None):

    metric = get_object_or_404(Metric, name=name, owner__username=owner)
    imdata = plot_svgbuf_for_metric(metric)

    return render_to_response('metric.html',\
            { 'metric': metric, 'figure': imdata })


font = {'family' : 'normal',
#        'weight' : 'bold',
        'size'   : 8, }

plt.rc('font', **font)


def plot_svgbuf_for_metric(metric):
    # get the data for the metric
    mdata = Metric.data.get_queryset(metric.name, metric.owner)
    # get the pandas timeseries
    df = mdata.to_timeseries(index='time', fieldnames=('value', ))
    #df = df.resample('h')

    imgdata = StringIO.StringIO()

    ax = df.plot(
            fontsize=2,
            figsize=(9,4),
            )
    ax.legend((metric.name,))

    if metric.unit:
        ax.set_ylabel(metric.get_unit_display())
    fig = ax.get_figure()

    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    return imgdata.buf

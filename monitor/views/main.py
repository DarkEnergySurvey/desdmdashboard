import StringIO

import pandas
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

        if metric.show_on_dashboard:
            m = {
                'name': metric.name,
                'is_in_trouble_status': metric.is_in_trouble_status,
                'doc' : metric.doc,
                'svgplot': plot_svgbuf_for_metric(metric),
                'owner': metric.owner.username,
                'get_absolute_url': metric.get_absolute_url()
                }
            metrices.append(m)

    return render_to_response('dashboard.html',\
            { 'metrices': metrices })


def metric_detail(request, owner=None, name=None):

    ms = name.rsplit('&')

    if len(ms) == 1:
        metric = get_object_or_404(Metric, name=name, owner__username=owner)
        imdata = plot_svgbuf_for_metric(metric)

        return render_to_response('metric.html',\
                { 'metric': metric, 'figure': imdata })

    else:
        dfs = {}
        unit = None
        for i, m in enumerate(ms):
            metric = get_object_or_404(Metric, name=m, owner__username=owner)
            if metric.get_unit_display() != None:
                unit = metric.get_unit_display()
            mdata = Metric.data.get_queryset(metric.name, metric.owner)
            dfs[metric.name] = mdata.to_timeseries(
                    index='time', fieldnames=('value',))

        df = pandas.concat(dfs.values(), join='outer', axis=1,).resample('D')
        df.columns = dfs.keys()

        imgdata = StringIO.StringIO()
        ax = df.plot(
                fontsize=2,
                figsize=(8,4),
                lw=1.5,
                )
        #ax.legend(dfs.keys())
        ax.set_ylabel(unit)

        fig = ax.get_figure()

        fig.savefig(imgdata, format='svg')
        imgdata.seek(0)
    
        return render_to_response('multimetric.html',\
                { 'figure': imgdata.buf, })


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
            figsize=(8,4),
            lw=1.5,
            color=(0, 0, 0.6),
            )

    if metric.value_type.model in ['metricdataint', 'metricdatafloat', ]:
        if metric.alert_value:
            yav = [metric.alert_value, metric.alert_value, ]
            xav = [min(df.index), max(df.index),]
            ax.plot(xav,yav, 'r--')

    ax.legend((metric.name,))

    if metric.unit:
        ax.set_ylabel(metric.get_unit_display())
    fig = ax.get_figure()

    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    return imgdata.buf

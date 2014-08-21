import StringIO

import pandas
import matplotlib.pyplot as plt

from django.shortcuts import render, render_to_response, get_object_or_404

from monitor.models import Metric

from datetime import datetime

font = {
    'family' : 'sans-serif',
#   'weight' : 'bold',
    'size'   : 8,
    }

plt.rc('font', **font)


def dashboard(request, owner=None):

    #print '\n\nDASHBOARD CALLED!!'
    initime = datetime.now()

    if owner:
        ms = Metric.objects.filter(owner__username=owner)
    else:
        ms = Metric.objects.all()

    metrices = []
    for metric in ms:

        if metric.dashboard_display_option == metric.DASHBOARD_DISPLAY_OPTION_PLOT:
            try:
                data_display = plot_svgbuf_for_metric(metric, size='small')
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
            'get_absolute_url': metric.get_absolute_url()
            }
        metrices.append(m)


    #print 'DASHBOARD BEFORE RETURN:'
    #offtime = datetime.now()
    #print 'time spent : ', offtime - initime

    return render_to_response('monitor_dashboard.html',\
            { 'metrices': metrices, })


def metric_detail(request, owner=None, nameslug=None):

    ms = nameslug.rsplit('&')

    if len(ms) == 1:
        metric = get_object_or_404(Metric, slug=nameslug, owner__username=owner)
        try:
            imdata = plot_svgbuf_for_metric(metric)
        except Exception, e:
            imdata = e

        return render_to_response('metric_detail.html',\
                { 'metric': metric, 'figure': imdata })

    else:
        dfs = {}
        unit = None
        for i, m in enumerate(ms):
            metric = get_object_or_404(Metric, nameslug=m, owner__username=owner)
            if metric.get_unit_display() != None:
                unit = metric.get_unit_display()
            mdata = Metric.data.get_dataframe_queryset(metric.name, metric.owner)
            dfs[metric.name] = mdata.to_timeseries(
                    index='time', fieldnames=('value',))

        df = pandas.concat(dfs.values(), join='outer', axis=1,).resample('D')
        df.columns = dfs.keys()

        ax = df.plot(
                fontsize=2,
                figsize=(8,4),
                lw=1.5,
                )
        #ax.legend(dfs.keys())
        ax.set_ylabel(unit)
        fig = ax.get_figure()

        imgdata = StringIO.StringIO()
        fig.savefig(imgdata, format='svg')
        imgdata.seek(0)
    
        return render_to_response('multimetric.html',\
                { 'figure': imgdata.buf, })


def plot_svgbuf_for_metric(metric, size='big'):

    init = datetime.now()

    # get the data for the metric
    mdata = Metric.data.get_dataframe_queryset(metric.owner, metric.name)
    # get the pandas timeseries
    df = mdata.to_timeseries(index='time', fieldnames=('value', ))
    #df = df.resample('h')

    imgdata = StringIO.StringIO()

    if size == 'big':
        ax = df.plot(
                fontsize=2,
                figsize=(8,4),
                lw=1.5,
                color=(0, 0, 0.6),
                )
        ax.legend((metric.name,), loc='best')

    elif size == 'small':
        ax = df.plot(
                fontsize=1,
                figsize=(4.7,2.7),
                lw=1.5,
                color=(0, 0, 0.6),
                legend=False,
                )

    if metric.value_type.model in ['metricdataint', 'metricdatafloat', ]:
        if metric.alert_value:
            yav = [metric.alert_value, metric.alert_value, ]
            xav = [min(df.index), max(df.index),]
            ax.plot(xav,yav, 'r--')


    if metric.unit:
        ax.set_ylabel(metric.get_unit_display())
    fig = ax.get_figure()
    fig.tight_layout()

    fig.savefig(imgdata, format='svg')
    plt.close(fig)
    imgdata.seek(0)
    
    endt = datetime.now()
    #print 'create metric plot in (s): ', endt - init

    return imgdata.buf


import StringIO

import matplotlib.pyplot as plt

font = {'family' : 'normal',
#        'weight' : 'bold',
        'size'   : 8, }

plt.rc('font', **font)


def plot_df_to_svg_string(df, **kwargs):
    '''
    '''

    fonts = kwargs.pop('fontsize', 2)
    figs = kwargs.pop('figsize', (8,4))
    metrics = kwargs.pop('metrics', None)
    line_width = kwargs.pop('lw', 1.5)
    y_label = kwargs.pop('y_label', None)
    ylim = kwargs.pop('ylim', None)
    legend_loc = kwargs.pop('legend_loc', 'best')

    if ylim and (ylim[0]=='auto' or ylim[1]=='auto'):
        autoylim=True
    else:
        autoylim=False
        if ylim:
            kwargs['ylim'] == ylim

    # FIXME !!
#   if metrics:
#       labels = [] 
#       for k, metric in metrics.iteritems():
#           l_str = "<a href='{url}'>{label}</a>"
#           label = l_str.format(url=metric.get_absolute_url(), label=k)
#           labels.append(label)
#       kwargs['labels'] = labels

    ax = df.plot(fontsize=fonts, figsize=figs, lw=line_width, legend=False, **kwargs)
    columns = df.columns
    ax.legend(columns, loc=legend_loc)

    if autoylim:
        if ylim[0] == 'auto' and not ylim[1] == 'auto':
            ax.set_ylim(ax.get_ylim()[0], ylim[1])
        if ylim[1] == 'auto' and not ylim[0] == 'auto':
            ax.set_ylim(ylim[0], ax.get_ylim()[1])

    if y_label:
        ax.set_ylabel(y_label)

    fig = ax.get_figure()
    fig.tight_layout()

    imgdata = StringIO.StringIO()
    fig.savefig(imgdata, format='svg')
    plt.close(fig)
    imgdata.seek(0)

    return imgdata.buf

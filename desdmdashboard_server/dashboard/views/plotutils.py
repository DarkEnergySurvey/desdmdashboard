
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
    ax.legend(columns, loc='best')


    if y_label:
        ax.set_ylabel(y_label)

    fig = ax.get_figure()

    imgdata = StringIO.StringIO()
    fig.savefig(imgdata, format='svg')
    plt.close(fig)
    imgdata.seek(0)

    return imgdata.buf

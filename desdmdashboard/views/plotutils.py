
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
    line_width = kwargs.pop('lw', 1.5)
    y_label = kwargs.pop('y_label', None)

    ax = df.plot(fontsize=fonts, figsize=figs, lw=line_width, **kwargs)

    if y_label:
        ax.set_ylabel(y_label)

    fig = ax.get_figure()

    imgdata = StringIO.StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    return imgdata.buf

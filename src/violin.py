import numpy as np
import matplotlib.pylab as plt

def violin(data,
        ax=None,
        COLORS=None,
        title='',
        fig_args=dict(bottom=0.3, left=0.7, top=1.),
        axes_args={},
        legend=None):

    """
    return fig, ax
    """

    # getting or creating the axis
    if ax is None:
        if legend is not None:
            fig, ax = plt.subplots(1, figsize=(2,1.5))
            plt.subplots_adjust(right=.7)
        else:
            fig, ax = plt.subplots(1, figsize=(1.5,1))
            plt.subplots_adjust(left=.3, right=.8)
    else:
        fig = plt.gcf()

    ax.plot(1+np.arange(data.shape[1]), data.mean(axis=0), 'ko', ms=1)
    violin_parts = ax.violinplot(data,
                                 quantiles=[[0.25,0.5,0.75] for i in range(data.shape[1])],
                                 showextrema=False)

    if COLORS is not None:
        for pc, color in zip(violin_parts['bodies'], COLORS):
            pc.set_facecolor(color)
            pc.set_edgecolor('black')

    violin_parts['cquantiles'].set_linewidth(0.5)

    """
    if COLORS is None:
        COLORS = [plt.cm.tab10(i) for i in range(len(data))]
    if (explodes is None):
        explodes = np.zeros(len(data))
    if (ext_labels is None):
        ext_labels = np.zeros(len(data), dtype=str)

    if pie_labels is not None:
        pie_labels_map = {}
        for pl, val in zip(pie_labels, data):
            pie_labels_map[str(np.round(100.*val/np.sum(data),pie_labels_digits))] = pl
        def func(pct):
            return pie_labels_map[str(np.round(pct,pie_labels_digits))]
    else:
        def func(pct):
            return ''


    wedges, ext_texts, pie_texts = ax.pie(data,
                                          labels=ext_labels,
                                          autopct=func,
                                          explode=explodes,
                                          pctdistance=pie_labels_distance,
                                          labeldistance=ext_labels_distance,
                                          colors=COLORS, **pie_args)

    if 'fontsize' not in pie_text_settings:
        pie_text_settings['fontsize'] = 8
    if 'fontsize' not in ext_text_settings:
        ext_text_settings['fontsize'] = 8

    plt.setp(pie_texts, **pie_text_settings)
    plt.setp(ext_texts, **ext_text_settings)

    Centre_Circle = plt.Circle((0,0), center_circle, fc='white')
    ax.add_artist(Centre_Circle)

    if legend is not None:
        if 'loc' not in legend:
            legend['loc']=(1.21,.2)
        ax.legend(**legend)

    if title!='':
        ax.set_title(title)

    """
    return fig, ax


if __name__=='__main__':

    import sys
    sys.path.append('./')

    data = np.random.randn(100, 4)

    #plotting
    fig, ax = violin(data, COLORS=[plt.cm.tab10(i) for i in range(4)])
    plt.show()

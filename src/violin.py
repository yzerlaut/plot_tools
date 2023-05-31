import numpy as np
import matplotlib.pylab as plt

def violin(data,
        ax=None,
        COLORS=None,
        title='',
        figsize=(1.5, 1),
        legend=None):

    """
    return fig, ax
    """

    # getting or creating the axis
    if ax is None:
        fig, ax = plt.subplots(1, figsize=figsize)
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

    if title!='':
        ax.set_title(title)

    return fig, ax


if __name__=='__main__':

    import sys
    sys.path.append('./')

    data = np.random.randn(100, 4)

    #plotting
    fig, ax = violin(data, COLORS=[plt.cm.tab10(i) for i in range(4)])
    plt.show()

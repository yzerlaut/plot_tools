import numpy as np
import matplotlib.pylab as plt

def violin(data,
           X=None,
           ax=None,
           COLORS=None,
           showmeans=True,
           showextrema=False,
           showmedians=False,
           quantiles=[0.25, 0.5, 0.75],
           points=100,
           title='',
           figsize=(1.5, 1),
           legend=None):

    """
    return fig, ax
    """

    data = np.array(data)
    if (X is None) and (len(data.shape)>1):
        X = np.arange(data.shape[1])
    elif (X is None):
        X = [0]

    # getting or creating the axis
    if ax is None:
        fig, ax = plt.subplots(1, figsize=figsize)
    else:
        fig = plt.gcf()

    if showmeans:
        ax.plot(X, np.array(data.mean(axis=0)), 'ko', ms=1)
    violin_parts = ax.violinplot(data,
                                 positions=X,
                                 quantiles=[quantiles for i in range(len(X))],
                                 showextrema=False,
                                 showmedians=showmedians,
                                 points=points)

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

    data = np.random.randn(100)#, 4)
    #plotting
    fig, ax = violin(data, COLORS=[plt.cm.tab10(i) for i in range(4)])
    data = np.random.randn(100)#, 4)
    violin(data, X=[1], COLORS=[plt.cm.tab10(2)], ax=ax, points=1000)
    plt.show()

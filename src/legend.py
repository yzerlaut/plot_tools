import matplotlib.pylab as plt
import matplotlib as mpl
import numpy as np

from .inset import inset

def bar_legend(stuff,
               X = None, continuous=False,
               ax_colorbar=None,
               colorbar_inset=dict(rect=[.72,.3,.03,.5], facecolor=None),
               colormap=plt.cm.copper,
               bar_legend_args={},
               label='',
               bounds=None,
               ticks = None,
               ticks_labels=None,
               no_ticks=False,
               orientation='vertical',
               scale='linear',\
               labelpad=2., size='', fontsize=None, alpha=1.,
               color_discretization=None):
    """
    
    """
    if X is None:
        continuous = True

    if ax_colorbar is None:
        ax_colorbar = inset(stuff, **colorbar_inset)

    if continuous:
        cb = build_bar_legend_continuous(ax_colorbar, colormap,
                                         bounds=bounds,
                                         ticks=ticks,
                                         ticks_labels=ticks_labels,
                                         orientation=orientation,
                                         alpha=alpha,
                                         scale=scale)
    else:
        cb = build_bar_legend(ax_colorbar, X,
                              colormap,
                              scale=scale,
                              bounds=bounds,
                              orientation=orientation,
                              color_discretization=color_discretization,
                              no_ticks=no_ticks,
                              ticks_labels=ticks_labels)


    bar_legend_args['orientation'] = orientation
    bar_legend_args['label'] = label
    bar_legend_args['labelpad'] = labelpad
    bar_legend_args['size'] = size
        
    set_bar_legend(ax_colorbar, cb, **bar_legend_args)
    
    return cb, ax_colorbar 



def set_bar_legend(ax_cb, cb,
                   label='',
                   orientation='vertical',
                   label_position='right',
                   color='k',
                   labelpad=1.,
                   size='', 
                   fontsize=None):
    """
    Just for labels and fontsize
    """
        
    cb.set_label(label, labelpad=labelpad, fontsize=fontsize, color=color)
    
    if orientation=='vertical':
        ax_cb.tick_params(axis='y', labelsize=fontsize, color=color)
        ax_cb.yaxis.set_label_position(label_position)
    elif (orientation=='horizontal') and label_position=='right':
        ax_cb.tick_params(axis='x', labelsize=fontsize, color=color)
        ax_cb.xaxis.set_label_position('top') # top by default
    elif orientation=='horizontal':
        ax_cb.tick_params(axis='x', labelsize=fontsize, color=color)
        ax_cb.xaxis.set_label_position(label_position)

    plt.setp(ax_cb.get_xticklabels(), color=color)
    plt.setp(ax_cb.get_yticklabels(), color=color)
    ax_cb.tick_params(axis='x', which='both', colors=color)
    ax_cb.tick_params(axis='y', which='both', colors=color)


    
def build_bar_legend(ax_cb, X, mymap,
                     bounds=None,
                     ticks_labels=None,
                     no_ticks=False,
                     orientation='vertical',
                     alpha=1.,
                     scale='linear',\
                     font_color='k',
                     color_discretization=None):
    
    """ X -> ticks """
    if color_discretization is None:
        color_discretization = len(X)
        
    # scale : 'linear' / 'log' / 'custom'
    if scale=='linear':
        if bounds is None:
            try:
                bounds = [X[0]+(X[1]-X[0])/2., X[-1]+(X[1]-X[0])/2.]
            except IndexError:
                bounds = [X[0], X[0]+1]
                
        bounds = np.linspace(bounds[0], bounds[1], color_discretization)
    elif scale=='log10':
        if bounds is None:
            bounds = [int(np.log(X[0])/np.log(10))-.1*int(np.log(X[0])/np.log(10)),\
                      int(np.log(X[-1])/np.log(10))+1+.1*int(np.log(X[-1])/np.log(10))]
        else:
            bounds = [np.log(bounds[0])/np.log(10), np.log(bounds[1])/np.log(10)]
        bounds = np.logspace(bounds[0], bounds[1], color_discretization)
    elif scale=='custom':
        bounds = np.linspace(X[0]+(X[1]-X[0])/2., X[-1]+(X[1]-X[0])/2., color_discretization)
    norm = mpl.colors.BoundaryNorm(bounds, mymap.N)
    cb = mpl.colorbar.ColorbarBase(ax_cb, cmap=mymap, norm=norm,\
                                   orientation=orientation, alpha=alpha)
    if no_ticks:
        cb.set_ticks([])
    else:
        cb.set_ticks(X)
        if ticks_labels is not None:
            cb.set_ticklabels(ticks_labels)
        
    return cb

def build_bar_legend_continuous(ax_cb, mymap,
                                bounds=[0,1],
                                ticks=None,
                                ticks_labels=None,
                                orientation='vertical',
                                alpha=1.,
                                scale='linear'):

    cb = mpl.colorbar.ColorbarBase(ax_cb,
                                   cmap=mymap,
                                   orientation=orientation,
                                   alpha=alpha)
    
    if (bounds is None):
        cb.set_ticks([])
        
    else:
        
        if scale=='log':
            
            if bounds[0]<=0.:
                print('need to set a positive lower bound for the data')
                print('set to 0.01')
                bounds[0] = 0.01
                
            if orientation=='vertical':
                set_ticks_to_log10_axis(cb.ax.yaxis, bounds, normed_to_unit=True)
                # if ticks_labels is not None:
                #     cb.ax.yaxis.set_ticklabels(ticks_labels)
            elif orientation=='horizontal':
                set_ticks_to_log10_axis(cb.ax.xaxis, bounds, normed_to_unit=True)
                # if ticks_labels is not None:
                #     cb.ax.xaxis.set_ticklabels(ticks_labels)
            
        else:
            
            if ticks is None:
                ticks = np.linspace(bounds[0]+.1*(bounds[1]-bounds[0]), bounds[1]-.1*(bounds[1]-bounds[0]), 3)
                
            if ticks_labels is None:
                ticks_labels = ['%.1f' % t for t in ticks]

            cb.set_ticks((np.array(ticks)-bounds[0])/(bounds[1]-bounds[0]))
            cb.set_ticklabels(ticks_labels)
        
    return cb


def legend(ax,
           size='', fontsize=None,
           frameon=False,
           handletextpad=0.3,
           handlelength=1.,
           labelspacing=0.5,
           ncol=1,
           title='',
           columnspacing=1.,
           color=None,
           loc='best'):
    """
    """
    leg = ax.legend(loc=loc,
                    frameon=frameon,
                    ncol=ncol,
                    numpoints=1,
                    scatterpoints=1,
                    columnspacing=columnspacing,
                    handletextpad=handletextpad,
                    handlelength=handlelength,
                    labelspacing=labelspacing,
                    title=title,
                    fontsize=fontsize)

    plt.setp(leg.get_texts(), color=color)

    

if __name__=='__main__':

    import sys
    sys.path.append('./')
    from datavyz import graph_env_manuscript as ge
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir))
    from datavyz import graph_env_manuscript as ge

    Y = [np.exp(np.random.randn(100)) for i in range(4)]
    
    fig, ax = ge.figure(right=5.) # with extended right space
    
    for i in range(2):
        ax.plot(np.arange(10)*10, np.exp(np.random.randn(10)), 'o', ms=2, label='line'+str(i+1))
    for i in range(2):
        ax.plot(np.arange(10)*10, np.exp(np.random.randn(10)), '-', label='line'+str(i+1))
        
    ge.legend(ax, ncol=2)
        
    ge.plot(Y=Y,
            xlabel='time', ylabel='y-value',
            colormap=ge.copper,
            lw=1., ax=ax)

    
    ge.bar_legend(fig,
                  X = np.arange(5),
                  # inset={'rect':[.3,.8,.3,.05]},
                  colormap=ge.copper,
                  orientation='horizontal',
                  label='Trial ID', no_ticks=True)
    
    ge.bar_legend(fig,
                  bounds = [1e-3, 10],
                  scale='log',
                  label='scale')
    ge.show()

# %%
import sys

sys.path.append('..')
import plot_tools as pt
pt.set_style('dark')
import matplotlib.pylab as plt
import numpy as np

# %%

def gen_fig():

    fig, AX = pt.figure((2,1),
            figsize=('1-column', 0.3))

    pt.scatter(np.random.randn(100), ax=AX[0], ms=5)
    pt.scatter(np.random.randn(100), ax=AX[0], ms=5)
    pt.set_plot(AX[0], xlabel='obs #', 
                ylabel='value')
    pt.annotate(AX[0], 'A', (-0.4, 1.05), 
                fontsize=8, bold=True)
    AX[1].hist(np.random.randn(100))
    AX[1].hist(np.random.randn(100))
    pt.set_plot(AX[1], ylabel='hist', xlabel='value')
    pt.annotate(AX[1], 'some\nlabel', (1,1), 
                va='top', ha='right', fontsize=6)
    pt.annotate(AX[1], 'B', (-0.25, 1.05), 
                fontsize=8, bold=True)
    return fig

fig = gen_fig()
pt.save(fig, on='temp', fig_name='fig.png')
    
# %%
# CHECK THAT THE FIGURE NICELY FITS
import tempfile
from IPython.display import Image
Image(os.path.join(tempfile.tempdir, 'fig.png'))

# %%
# now the same with the manuscript style
pt.set_style('manuscript')
fig = gen_fig()
pt.save(fig, on='Desktop', fig_name='fig.png', dpi=300)
Image(os.path.join(os.path.expanduser('~'), 'Desktop', 'fig.png'))
# %%

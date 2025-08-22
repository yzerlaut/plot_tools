import os, sys, pathlib


import matplotlib.pylab as plt
sys.path.append('../')
import plot_tools as pt

import numpy as np

pt.set_style('dark-notebook')

if False:
    # fig, ax = plt.subplots(1)
    fig, ax = pt.figure()
    ax.hist(np.random.randn(200),bins=40)
    pt.set_plot(ax, xlabel='value', ylabel='hist', 
                title='title')

if True:
    fig, AX = pt.figure(axes=(4,1), figsize=("1-column",0.33))
    fig, AX = pt.figure(axes=(3,1), figsize=("1-column",0.33),wspace=1.4)
    pt.scatter(np.random.randn(100), ax=AX[0])
    pt.set_plot(AX[0], xlabel='obs. #', ylabel='value')
    AX[1].hist(np.random.randn(100))
    pt.set_plot(AX[1], xlabel='value', ylabel='hist')

if False:
    fig, ax = plt.subplots(1, figsize=(1.2,1.2))
    pt.matrix(np.random.randn(20,20), ax=ax)

plt.show()


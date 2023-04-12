import os, pathlib
from matplotlib import pylab 

from .src.inset import *
from .src.adjust_plots import *

pylab.style.use(os.path.join(pathlib.Path(__file__).resolve().parent,
                             'style_sheets', 'manuscript_style.py'))


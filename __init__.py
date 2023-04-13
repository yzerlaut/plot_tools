import os, pathlib
from matplotlib import pylab 

from .src.inset import *
from .src.adjust_plots import *
from .src.legend import *
from .src.export import *
from .src.annotations import *

pylab.style.use(os.path.join(pathlib.Path(__file__).resolve().parent,
                             'style-sheets', 'manuscript_style.py'))


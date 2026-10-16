import string, datetime, os
from tempfile import gettempdir
import matplotlib.pylab as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.figure import Figure

# SPECIAL PYTHON PACKAGES FOR:
try:
    import svgutils.compose as sg # SVG
except ModuleNotFoundError:
    pass

# import fpdf # PDF
from PIL import Image # BITMAP (png, jpg, ...)
### [!!] need to have the inkscape 

def mm2inch(x):
    return x/25.4
    
def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)    

def inch2cm(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i*inch for i in tupl[0])
    else:
        return tuple(i*inch for i in tupl)    


def put_list_of_figs_to_svg_fig(FIGS,
                                fig_name="fig.svg",
                                initial_guess=True,
                                visualize=False,
                                export_as_png=False,
                                Props = None,
                                figsize = None,
                                fontsize=9,
                                SCALING_FACTOR=1.34, # needed to get the right cm size ...
                                with_top_left_letter=False,
                                transparent=True):
    """ take a list of figures and make a multi panel plot"""
    
    label = list(string.ascii_uppercase)[:len(FIGS)]

    SIZE = []
    for fig in FIGS:
        if type(fig)==str:
            SIZE.append([1.,1.])
        else:
            SIZE.append(fig.get_size_inches())
            
    width = np.max([s[0] for s in SIZE])
    height = np.max([s[1] for s in SIZE])
    
    if Props is None:
        LABELS, XCOORD, YCOORD = [], [], []

        # saving as svg
        for i in range(len(FIGS)):
            LABELS.append(label[i])
            XCOORD.append((i%3)*width*100)
            YCOORD.append(int(i/3)*height*100)
        XCOORD_LABELS,\
            YCOORD_LABELS = XCOORD, YCOORD

    else:
        XCOORD, YCOORD = Props['XCOORD'],\
                Props['YCOORD'], 
        if 'LABELS' in Props:
            LABELS = Props['LABELS']
        else:
            LABELS = ['' for x in XCOORD]
        if 'XCOORD_LABELS' in Props:
            XCOORD_LABELS,\
                YCOORD_LABELS = Props['XCOORD_LABELS'],\
                                Props['YCOORD_LABELS']
        else:
            XCOORD_LABELS,\
                YCOORD_LABELS = XCOORD, YCOORD

    LOCATIONS = []
    for i in range(len(FIGS)):
        if type(FIGS[i]) is str:
            LOCATIONS.append(FIGS[i])
        else:
            LOCATIONS.append(os.path.join(gettempdir(), str(i)+'.svg'))
            FIGS[i].savefig(LOCATIONS[-1], format='svg',
                            transparent=transparent)
        
    PANELS = []
    for i in range(len(FIGS)):
        PANELS.append(sg.Panel(\
            sg.SVG(LOCATIONS[i]).move(XCOORD[i],YCOORD[i])))
                      
    for i in range(len(LABELS)):
        PANELS.append(sg.Panel(\
            sg.Text(LABELS[i], 15, 10,
                    size=fontsize, weight='bold').move(\
                                                       XCOORD_LABELS[i],YCOORD_LABELS[i]))\
        )

    sg.Figure("21cm", "29.7cm", *PANELS).scale(SCALING_FACTOR).save(fig_name)
    # if figsize is None:
    #     sg.Figure("21cm", "29.7cm", *PANELS).save(fig_name)
    # else:
    #     sg.Figure(str(inch2cm(figsize[0]*A0_format['width'])[0])+"cm",\
    #               str(inch2cm(figsize[1]*A0_format['height'])[0])+"cm",\
    #               *PANELS).scale(SCALING_FACTOR).save(fig_name)

    if visualize:
        os.system('open '+fig_name) # works well with 'Gapplin' on OS-X
        ## KEEP -> previous version
        # os.system('convert '+fig_name+' '+fig_name.replace('.svg', '.png'))
        # plt.close('all')
        # z = plt.imread(fig_name.replace('.svg', '.png'))
        # plt.imshow(z)
        # fig = plt.gcf()
        # # if figsize is not None:
        # #     fig.set_size_inches(fig.get_size_inches()[0]*3,
        # #                         fig.get_size_inches()[1]*3,
        # #                         forward=True)
        # if not no_show:
        #     from datavyz..graphs import show
        #     show()

def _flatten_artists(item):
    """ artists from an artist, a container (ax.bar, ax.errorbar, ...),
    or a (nested) list / tuple of those """
    from matplotlib.artist import Artist
    from matplotlib.container import Container
    if item is None:
        return []
    if isinstance(item, Container):
        return [a for child in item.get_children()
                for a in _flatten_artists(child)]
    if isinstance(item, Artist):
        return [item]
    if isinstance(item, (list, tuple)):
        return [a for child in item for a in _flatten_artists(child)]
    raise TypeError('save_layers: cannot export %s as a layer element' % type(item))


def save_layers(fig, fig_name, layers,
                labels=None,
                base_label='base',
                **savefig_kwargs):
    """
    save the figure as an SVG where groups of elements are on separate
    Inkscape layers, e.g. to make them appear one by one in a presentation
    (talk template: each layer after the first appears on the next click)

    fig:     the matplotlib figure
    layers:  list of layers, each a list of elements (lines, scatter,
             ax.bar(...) / ax.errorbar(...) results, texts, legend, axes...)
             -> layer 1, layer 2, ...;  everything else is on a first
                "base" layer (axes, ticks, labels, ...)
    labels:  optional names of the layers (default: "layer 1", ...)

    e.g.
        l1, = ax.plot(t, x)
        l2, = ax.plot(t, y)
        bars = ax.bar(...)
        pt.save_layers(fig, 'fig.svg', [[l1], [l2], [bars, ax.legend()]])

    [!!] a layer is drawn on top of the previous ones (whatever the zorder)
    """
    import io
    import xml.etree.ElementTree as ET

    SVG, INK = 'http://www.w3.org/2000/svg', 'http://www.inkscape.org/namespaces/inkscape'
    for prefix, uri in [('', SVG), ('inkscape', INK),
                        ('xlink', 'http://www.w3.org/1999/xlink'),
                        ('dc', 'http://purl.org/dc/elements/1.1/'),
                        ('cc', 'http://creativecommons.org/ns#'),
                        ('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')]:
        ET.register_namespace(prefix, uri)

    if labels is None:
        labels = ['layer %i' % (k+1) for k in range(len(layers))]

    # tag the elements of each layer (unique svg ids), keeping their gids
    artists = [_flatten_artists(layer) for layer in layers]
    previous_gids = {}
    for k, layer in enumerate(artists):
        for i, a in enumerate(layer):
            previous_gids.setdefault(a, a.get_gid())
            a.set_gid('pt-layer%i-%i' % (k+1, i))
    try:
        buffer = io.StringIO()
        fig.savefig(buffer, format='svg', **savefig_kwargs)
    finally:
        for a, gid in previous_gids.items():
            a.set_gid(gid)
    buffer.seek(0)
    root = ET.parse(buffer).getroot()

    def layer_group(label, k):
        return ET.SubElement(root, '{%s}g' % SVG,
                             {'{%s}groupmode' % INK: 'layer',
                              '{%s}label' % INK: label,
                              'id': 'layer%i' % k})

    # base layer: the whole figure
    figure_group = root.find('{%s}g' % SVG)
    root.remove(figure_group)
    layer_group(base_label, 0).append(figure_group)

    # one layer per group of elements (in document order)
    for k, label in enumerate(labels[:len(layers)]):
        group = layer_group(label, k+1)
        prefix = 'pt-layer%i-' % (k+1)
        for element in [e for e in figure_group.iter()
                        if e.get('id', '').startswith(prefix)]:
            parent = {c: p for p in root.iter() for c in p}[element]
            parent.remove(element)
            group.append(element)
        if len(group)==0:
            print('[!!] layer "%s" is empty (elements not drawn?)' % label)

    ET.ElementTree(root).write(fig_name, xml_declaration=True, encoding='utf-8')
    return fig_name


def export_as_png(fig_name,
                  dpi=300, background='white'):
    instruction = 'inkscape %s --export-area-page --export-background="%s" --export-type=png --export-filename="%s" --export-dpi=%i' % (fig_name, background, fig_name.replace('.svg', '.png'), dpi)
    print('RUNNING:', instruction)
    os.system(instruction)
    if os.path.isfile(fig_name.replace('.svg', '.png')):
        print('[ok] figure successfully exported as: %s' % fig_name.replace('.svg', '.png'))
    else:
        print('[!!] %s not exported as png' % fig_name)
        
def put_list_of_figs_to_multipage_pdf(FIGS,
                                      pdf_name='figures.pdf',
                                      pdf_title=''):
    """
    adapted from:
    http://matplotlib.org/examples/pylab_examples/multipage_pdf.html
    """
    
    # Create the PdfPages object to which we will save the pages:
    # The with statement makes sure that the PdfPages object is closed properly at
    # the end of the block, even if an Exception occurs.
    with PdfPages(pdf_name) as pdf:
        
        for fig in FIGS:
            pdf.savefig(fig)  # saves the current figure into a pdf page

        # We can also set the file's metadata via the PdfPages object:
        d = pdf.infodict()
        d['Title'] = pdf_title
        d['Author'] = u'Y. Zerlaut'
        # d['Keywords'] = 'PdfPages multipage keywords author title subject'
        d['CreationDate'] = datetime.datetime(2009, 11, 13)
        d['ModDate'] = datetime.datetime.today()


def concatenate_pngs(PNG_LIST, ordering='vertically', figname='fig.png'):
    
    images = map(Image.open, PNG_LIST)
    widths, heights = zip(*(i.size for i in images))

    if ordering=='vertically':
        total_height = sum(heights)
        max_width = max(widths)
        new_im = Image.new('RGB', (max_width, total_height))
        y_offset = 0
        for fig in PNG_LIST:
            im = Image.open(fig)
            new_im.paste(im, (0, y_offset))
            y_offset += im.size[1]

    new_im.save(figname)


def multipanel_figure(FIGS,
                      X = None, Y = None, Labels=None,
                      LABELS = None, X_LABELS = None, Y_LABELS = None,
                      width=85.,# mm
                      height=None, # mm
                      grid=False,
                      autoposition=False,
                      SCALING_FACTOR = 1.34, fontsize=9, fontweight='bold',
                      export_to_png=False, bg='white',
                      fig_name='fig.svg'):
    """
    
    """
    # building the figure matrix if not explicited
    if type(FIGS) is Figure:
        FIGS = [[FIGS]]
    elif type(FIGS) is list:
        if (len(FIGS)>0) and (type(FIGS[0]) is Figure):
            FIGS = [FIGS]
        elif (len(FIGS)>0) and (type(FIGS[0]) is str):
            FIGS = [FIGS]
    # else should be list of list

    if autoposition:
        X, Y = [], []
        y = [0]
        for i, lfig in enumerate(FIGS):
            Y.append([np.max(y) for fig in lfig])
            x = []
            for fig in lfig:
                if type(fig) is not str:
                    x.append(72.*fig.get_size_inches()[0])
                    y.append(72.*fig.get_size_inches()[1])
                else:
                    x.append(120)
                    y.append(80)
            X.append([0]+list(np.cumsum(x)))
            y = [dy+Y[-1][0] for dy in y]
        Y.append([np.max(y)])
        print('X = ', X)
        print('Y = ', Y)
    
    if X is None:
        X = [[0 for fig in lfig] for lfig in FIGS]
    if Y is None:
        Y = [[0 for fig in lfig] for lfig in FIGS]
    if LABELS is None:
        LABELS = [['' for fig in lfig] for lfig in FIGS]
    if X_LABELS is None:
       X_LABELS = X 
    if Y_LABELS is None:
       Y_LABELS = Y
    
    if height is None:
        try:
            height = np.max([50, Y[-1][-1]])*0.27 # TO BE SET UP
        except IndexError:
            height = 50
    
    # size
    if width=='single-column':
        width = 85.
    elif width=='one-and-a-half-column':
        width = 114.
    elif width=='one-column-and-a-half':
        width = 114.
    elif width=='double-column':
        width = 174.

    LOCATIONS, PANELS = [], []
    for i, lfig in enumerate(FIGS):
        LOCATIONS.append([])
        for j, fig in enumerate(lfig):
            if type(FIGS[i][j]) is str:
                LOCATIONS[i].append(FIGS[i][j])
                # 1.26625 -- NEW SCALING FACTOR
            else:
                LOCATIONS[i].append(os.path.join(gettempdir(), '%i_%i.svg' % (i,j)))
                FIGS[i][j].savefig(LOCATIONS[i][j], format='svg',
                                   transparent=True)
            PANELS.append(sg.Panel(sg.SVG(LOCATIONS[i][j]).move(X[i][j], Y[i][j])))

    for i, labels in enumerate(LABELS):
        for j, label in enumerate(labels):
            if label!='':
                PANELS.append(sg.Panel(sg.Text(label, 3, 10, 
                                               size=fontsize, weight=fontweight).move(\
                                                        X_LABELS[i][j],Y_LABELS[i][j])))

    if grid:
        sg.Figure("%.1fcm" % (width/10.), "%.1fcm" % (height/10.),
                  *PANELS, sg.Grid(40,40)).scale(SCALING_FACTOR).save(fig_name.replace('.png', '.svg'))
    else:
        sg.Figure("%.1fcm" % (width/10.), "%.1fcm" % (height/10.),
                  *PANELS).scale(SCALING_FACTOR).save(fig_name.replace('.png', '.svg'))

    if fig_name.endswith('.png'):
        export_as_png(fig_name.replace('.png', '.svg'), dpi=300, background=bg)
        os.remove(fig_name.replace('.png', '.svg'))
        print('[ok] removed %s' % fig_name.replace('.png', '.svg'))

    elif export_to_png:
        export_as_png(fig_name, dpi=300, background=bg)
        
    
if __name__=='__main__':

    import sys, os, pathlib
    sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))
    import plot_tools as pt

    import sys
    sys.path.append('./')

    """
    fig, ax = ge.figure()
    ge.multipanel_figure([],
                         # LABELS=[['a'],['b','c']], X_LABELS=[[0],[0,130]], Y_LABELS=[[0],[70,70]],
                         width='single-column', height=60.,                         
                         fig_name='fig1.png', bg='gray', grid=True)
    ge.multipanel_figure([],
                         width='double-column', # can also be "single-column" or "one-and-a-half-column"
                         fig_name='fig2.png', bg='gray', grid=True)
    ge.multipanel_figure([],
                         width='one-and-a-half-column', # can also be "single-column" or "one-and-a-half-column"
                         fig_name='fig3.png', bg='gray', grid=True)

    """
    # generate some random data
    t = np.linspace(0, 10, 1000)
    y = np.cos(5*t)+np.random.randn(len(t))

    # Panel 'a' - schematic
    fig11 = 'docs/schematic.svg'

    # Panel 'b' - time series plot
    fig12, ax12 = ge.figure(axes_extents=(3,1)) # i.e. a wide plot
    ax12.plot(t, y)
    ge.set_plot(ax12, xlabel='xlabel (xunit)', ylabel='ylabel (yunit)')
    
    # Panel 'c' - more time series plot
    fig21, ax21 = ge.figure(axes_extents=(4,1)) # i.e. a very wide plot
    ax21.plot(t[t>9], y[t>9], label='raw')
    ax21.plot(t[t>9][1:], np.diff(y[t>9]), label='deriv.')
    ax21.plot(t[t>9][1:-1], np.diff(np.diff(y[t>9])), label='2nd deriv.')
    ge.set_plot(ax21, xlabel='xlabel (xunit)', ylabel='ylabel (yunit)')
    ge.legend(ax21, ncol=3, loc=(.3,1.)) # put a legend

    # Panel 'd' - scatter plot
    fig31, ax31 = ge.scatter(t[::10], t[::10]+np.random.randn(100),
                             xlabel='ylabel (yunit)')
    
    # Panel 'e' - bar plot
    fig32, ax32 = ge.bar(np.random.randn(8),
                         COLORS=[ge.viridis(i/7) for i in range(8)],
                         xlabel='ylabel (yunit)')

    # Panel 'f' - bar plot
    fig33, ax33 = ge.pie([0.25,0.4,0.35], ext_labels=['Set 1', 'Set 2', 'Set 3'])

    # Panel 'g' - bar plot
    fig34, ax34 = ge.hist(np.random.randn(200))
    
    ge.multipanel_figure([[fig11, fig12],
                          [fig21],
                          [fig31,fig32,fig33,fig34]],
                         LABELS=[['a','b'],
                                 ['c'],
                                 ['d', 'e', 'f', 'g']],
                         width='double-column', # can also be "single-column" or "one-and-a-half-column"
                         # bg='gray',
                         fig_name='docs/multipanel.png',
                         grid=False, # switch to True to get the Grid position and pricesely place labels if necesary
                         autoposition=True)




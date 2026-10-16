## Matched to the 16:9 Quarto/reveal.js talk template (presentations repo,
## slides/Talks/): the default figure is the full content area of a slide,
## i.e. the 1180x570 px frame used by `![](figure.svg){.frame}`.
## Units: 1 slide px = 1/96 inch = 0.75 pt  ->  1180x570 px = 12.29 x 5.94 in,
## slide body text 32 px = 24 pt, so figure text here is slightly smaller.
## Use:  pt.set_style('slides-dark')  then  fig.savefig('figure.svg')

### FIGURE
figure.figsize: 12.29, 5.94  # = 1180x570 slide px (full frame)
figure.dpi: 96               # on screen: 1 figure px = 1 slide px
figure.facecolor: 1f1f1f
figure.titlesize: 22
figure.subplot.left: 0.09
figure.subplot.right: 0.97
figure.subplot.bottom: 0.14
figure.subplot.top: 0.94
figure.subplot.wspace: 0.3
figure.subplot.hspace: 0.4
figure.autolayout: False

### SAVING
savefig.dpi: 192             # png: 2x the slide resolution (sharp on retina / projectors)
savefig.transparent: True    # sits directly on the slide background
savefig.facecolor: 1f1f1f
svg.fonttype: none           # keep text as text (editable in Inkscape, same font as slides)

### FONTS (cross-platform: Arial on macOS / Windows, Liberation Sans (same metrics) on Linux,
###        DejaVu Sans (shipped with matplotlib) as last resort)
font.family: sans-serif
font.sans-serif: Arial, Liberation Sans, DejaVu Sans
font.size: 20                # pt  (~27 px on the slide, body text = 32 px)

### TEXT
text.color: e4e5ee

### AXES
axes.grid: False
axes.facecolor: 1f1f1f
axes.edgecolor: e4e5ee
axes.labelcolor: e4e5ee
axes.titlecolor: e4e5ee
axes.linewidth: 1.5
axes.titlesize: 22
axes.labelsize: 20
axes.labelpad: 8
axes.spines.top: False
axes.spines.right: False
axes.prop_cycle: cycler('color', ['e4e5ee', '56B4E9', '009E73', 'D55E00', 'CC79A7', 'F0E442', '0072B2'])

### TICKS
xtick.direction: out
ytick.direction: out
xtick.color: e4e5ee
ytick.color: e4e5ee
xtick.labelsize: 18
ytick.labelsize: 18
xtick.major.size: 7
ytick.major.size: 7
xtick.major.width: 1.5
ytick.major.width: 1.5
xtick.minor.size: 4
ytick.minor.size: 4
xtick.minor.width: 1.2
ytick.minor.width: 1.2

### LINES
lines.linewidth: 2.5
lines.markersize: 7
lines.color: e4e5ee

### PATCHES
patch.facecolor: 0072B2

### LEGEND
legend.fontsize: 18
legend.frameon: False

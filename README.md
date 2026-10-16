# plot_tools

> A set of data visualization functions based on `matplotlib` for scientific communications

## Install & Usage

```
pip install git+https://github.com/yzerlaut/plot_tools
```

### tests

```
python -m plot_tools.src.time_freq
```

## Matplotlib style sheets

All available style sheets are in [./style-sheets](./style-sheets), set with `pt.set_style(...)`:

- `'manuscript'` (default), `'dark'`
- `'slides-light'`, `'slides-dark'`: matched to the 16:9 talk template of the [presentations](https://github.com/yzerlaut/presentations) repo: the default figure fills the free area of a slide (1180x570 px), with text slightly smaller than the slide text. Show it with `![](figure.svg){.frame}`

## Layered SVG export (build-up animations in slides)

`pt.save_layers` saves an SVG where groups of elements are on separate Inkscape layers. Everything not listed (axes, ticks, labels, ...) is on a first "base" layer. In the talk template, each layer after the first appears on the next click.

```python
pt.set_style('slides-dark')
fig, ax = plt.subplots()
l1, = ax.plot(t, x, label='control')
l2, = ax.plot(t, y, label='treated')
bars = ax.bar(...)

pt.save_layers(fig, 'figure.svg',
               [[l1], [l2], [bars, ax.legend()]],         # layer 1, layer 2, layer 3
               labels=['control', 'treated', 'summary'])  # optional layer names
```

Layer elements can be lines, scatters, `ax.bar(...)` / `ax.hist(...)` / `ax.errorbar(...)` results, texts, legends or whole axes. A layer is drawn on top of the previous ones, whatever the `zorder`.

## Figure size

```

```

## Multipanel figures

## Documentation



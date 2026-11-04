"""Draw the neural network figures of lecture 7 in the style of the course.

    uv run python scripts/draw_neural_networks.py

They replace the figures of Prince's Understanding Deep Learning that the deck used for shallow and deep
networks, in the deck's notation: units, inputs and outputs counted from 0, a hidden unit
h_j = ReLU(w_j x + b_j), an output y = sum_j v_j h_j + c. The networks are drawn with the helpers of
`draw_bn_diagrams.py` (circles, KaTeX labels, arrow tips on the outlines); the plots with matplotlib,
text in Roboto and math in Computer Modern, the hidden units in the colors of the shallow network demo
(`demo/lec7/shallow.html`), whose default parameters the one-dimensional examples share. Writes to
`figures/lec7/`:

- `nn-terminology.svg`, a network with three inputs, four hidden units and two outputs;
- `nn-shallow.svg`, the single-input single-output network with its parameters, and in compact form;
- `nn-functions.svg`, three functions of the family it defines;
- `nn-approximate.svg`, a target approximated with 5, 10 and 20 linear regions;
- `nn-two-outputs-net.svg` and `nn-two-outputs-plot.svg`, the network with two outputs and the two
  functions it computes, and `nn-two-inputs.svg`, the network with two inputs;
- `nn-buildup-2d.svg`, the units and output of a network with two inputs, over the plane;
- `nn-concat-net.svg` and `nn-concat.svg`, two shallow networks in series, and the functions they
  compute (the same f and g as the folding animation `demo/lec7/fold.html`);
- `nn-two-layer-2d-net.svg` and `nn-two-layer-2d-plot.svg`, a network with two inputs composed with a
  shallow network, and its output over the plane, the joints dashed (first network) or dotted (second);
- `nn-deep.svg` and `nn-deep-buildup.svg`, a network with two hidden layers and how its second layer
  builds its output;
- `nn-regions.svg`, the number of linear regions against the number of parameters;
- `nn-activations.svg`, the sigmoid, tanh and ReLU activation functions;
- `lr-gaussian-model.svg` and `lr-residuals.svg`, linear regression as a linear Gaussian model, and its
  squared residuals;
- `nn-conv-pattern.svg`, the deck's cat through two 7x7 kernels, a ReLU and a 2x2 max-pooling, computed
  here, with the receptive field of one pooled value boxed back to the input;
- `nn-conv1d.svg`, `nn-conv2d.svg`, `nn-conv-channels.svg` and `nn-pooling.svg`, a 1d and a 2d
  convolution at two positions of the window, a 3x3x3 kernel on the cat's three channels, and
  subsampling, max-pooling and average-pooling of a 4x4 input, cell by cell, every value computed;
- `nn-next-token.svg`, a language model predicting the next token twice on a sentence about Pacman,
  with illustrative probabilities (no model is run).
"""

import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

sys.path.insert(0, str(Path(__file__).resolve().parent))
from draw_bn_diagrams import R, caption, label, math, svg   # noqa: E402
from draw_bn_diagrams import link as bn_link   # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
INK = "#2a2a2a"
GREY = "#8a8a8a"
LIGHT = "#d0d0d0"
BLUE = "#356aaf"
ORANGE = "#d9822b"
UNITS = [ORANGE, "#3f8f5a", "#8a5fb5", "#c2577f"]   # the hidden units, as in the demo; blue is kept for outputs
OUT = BLUE                 # the output of the single-output networks, node and curve
OUTPUTS = [BLUE, ORANGE]   # the two outputs of the network with two outputs (its hidden units are in ink)
STROKE = 2.6   # nodes and edges a little thicker than lecture 5's networks, at this smaller scale
# Every network diagram of the deck, and the network of y given x of `draw_bn_diagrams.py`, has its
# width and height scaled by SCALE, and the deck shows them at their natural size, without a width
# class: nodes, labels and strokes then have one size on every slide (one unit shows as about 0.78 px).
SCALE = 0.55
DIV = LinearSegmentedColormap.from_list("div", ["#a5561a", "#d9822b", "#f3d2b1", "#ffffff", "#bcd0ea", "#356aaf", "#1f3f6b"])

plt.rcParams.update({
    "font.family": "Roboto",
    "font.size": 15,
    "mathtext.fontset": "cm",
    "svg.fonttype": "path",
    "svg.hashsalt": "lec7",
    "axes.edgecolor": INK,
    "axes.labelcolor": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 1.0,
    "lines.linewidth": 2.2,
    "figure.facecolor": "none",
    "axes.facecolor": "none",
})

relu = lambda z: np.maximum(0, z)


def link(p, q):
    """An arrow from node to node, its tip on the outline, with the thicker stroke of these figures."""
    return bn_link(p, q).replace('stroke-width="2"', f'stroke-width="{STROKE:g}"')

# The shallow network of the demo: three units (w_j, b_j, v_j) and the offset c, on [0, 1].
SHALLOW = [(1.0, -0.2, 1.2), (-1.5, 0.75, 0.8), (2.0, -1.6, -1.5)]
C = 0.1
X = np.linspace(0, 1, 801)



# Every plot of the deck has its width and height scaled by PLOT_SCALE and is shown at that natural size,
# without a width class, so that text and lines have one size on every slide (the fonts are the same in
# points in every figure); the plots that are then wider than a slide are shown with `.width-100`.
# (The network diagrams use SCALE, for the same reason.)
PLOT_SCALE = 0.8


def rescale(path):
    svg_text = path.read_text(encoding="utf-8")
    def fix(m):
        return f'{m.group(1)}="{float(m.group(2)) * PLOT_SCALE:.2f}pt"'
    i = svg_text.index("<svg")
    j = svg_text.index(">", i)
    tag = re.sub(r'(width|height)="([\d.]+)pt"', fix, svg_text[i:j])
    path.write_text(svg_text[:i] + tag + svg_text[j:], encoding="utf-8")

def save(fig, name):
    out = ROOT / "figures" / "lec7" / f"{name}.svg"
    fig.savefig(out, bbox_inches="tight", transparent=True, metadata={"Date": None})
    rescale(out)
    plt.close(fig)
    print(out.relative_to(ROOT))


# ---- network diagrams

def primed(x, y, name, sub=None, size=28):
    """h' or h'_0 as LaTeX sets them: the prime raised and smaller, the subscript under it."""
    head = f'<tspan font-family="KaTeX_Math">{name}</tspan>'
    prime = f'<tspan font-family="KaTeX_Main" font-size="{0.75 * size:g}" dy="{-0.38 * size:g}">′</tspan>'
    tail = ""
    if sub:
        tail = (f'<tspan font-family="KaTeX_Main" font-size="{0.7 * size:g}" dx="{-0.28 * size:g}" '
                f'dy="{0.63 * size:g}">{sub}</tspan>')
    return (f'<text x="{x:g}" y="{y + 0.3 * size:.1f}" font-size="{size:g}" fill="{INK}" '
            f'text-anchor="middle">{head}{prime}{tail}</text>')


def unit_node(x, y, name, sub=None, color=INK):
    circle = f'<circle cx="{x:g}" cy="{y:g}" r="{R}" fill="white" stroke="{color}" stroke-width="{STROKE:g}"/>'
    if name.endswith("′"):
        return circle + primed(x, y, name[:-1], sub)
    return circle + label(x, y, name, sub)


def halo(s):
    """A label with a white halo, readable over the edges it sits on."""
    return s.replace("<text ", '<text stroke="white" stroke-width="6" paint-order="stroke" stroke-linejoin="round" ', 1)


def dots(x, y):
    return math(x, y, [("⋮", "")], size=28, fill=GREY)


def network(columns, edges=None, colors=None):
    """Columns of nodes as lists of (x, y, name, sub); consecutive columns fully connected by default."""
    colors = {("y", None): OUT, ("y′", None): OUT, **(colors or {})}
    parts = []
    if edges is None:
        edges = [(a, b) for i in range(len(columns) - 1) for a in columns[i] for b in columns[i + 1]]
    parts += [link(a[:2], b[:2]) for a, b in edges]
    for col in columns:
        for (x, y, name, sub) in col:
            parts.append(unit_node(x, y, name, sub, colors.get((name, sub), INK)))
    return parts


def column(x, names, top, step, sub=None):
    return [(x, top + i * step, n, s) for i, (n, s) in enumerate(names)]


def terminology():
    xs = column(70, [("x", "0"), ("x", "1"), ("x", "2")], 130, 110)
    hs = column(330, [("h", str(j)) for j in range(4)], 75, 110)
    ys = column(590, [("y", "0"), ("y", "1")], 185, 110)
    colors = {("h", str(j)): UNITS[j] for j in range(4)}
    return network([xs, hs, ys], colors=colors) + [
        caption(70, 26, "input layer"), caption(330, 26, "hidden layer"), caption(590, 26, "output layer"),
    ]


def shallow_net():
    # a) every parameter on its edge, with the constant input 1 for the biases; b) the compact form
    parts = []
    # the network of b) node for node, with the constant inputs 1 as auxiliary nodes above x and the hidden units
    x, one, hs, y, one2 = (70, 310), (70, 150), [(260, 170), (260, 310), (260, 450)], (450, 310), (260, 40)
    for j, h in enumerate(hs):
        parts += [link(x, h), link(one, h), link(h, y)]
    parts.append(link(one2, y))
    parts += [unit_node(*x, "x"), unit_node(*y, "y", None, OUT)]
    parts += [f'<circle cx="{one[0]}" cy="{one[1]}" r="{R}" fill="white" stroke="{GREY}" stroke-width="{STROKE:g}"/>',
              math(one[0], one[1], [("1", "")], size=28, fill=GREY),
              f'<circle cx="{one2[0]}" cy="{one2[1]}" r="{R}" fill="white" stroke="{GREY}" stroke-width="{STROKE:g}"/>',
              math(one2[0], one2[1], [("1", "")], size=28, fill=GREY)]
    for j, h in enumerate(hs):
        parts.append(unit_node(*h, "h", str(j), UNITS[j]))
    # edge labels, near the middle of each edge, in the color of the unit
    def mid(p, q, t=0.5, dx=0, dy=0):
        return p[0] + t * (q[0] - p[0]) + dx, p[1] + t * (q[1] - p[1]) + dy
    for j, h in enumerate(hs):
        parts.append(halo(math(*mid(x, h, 0.45), [("w", "i"), (str(j), "s")], size=26, fill=UNITS[j])))
        parts.append(halo(math(*mid(one, h, (0.5, 0.72, 0.72)[j]), [("b", "i"), (str(j), "s")], size=26, fill=UNITS[j])))
        parts.append(halo(math(*mid(h, y, 0.5), [("v", "i"), (str(j), "s")], size=26, fill=UNITS[j])))
    parts.append(halo(math(*mid(one2, y, 0.5), [("c", "i")], size=26, fill=GREY)))
    parts += [caption(10, 30, "a)", anchor="start")]
    # b) compact
    ox = 620
    xb, hb, yb = (ox + x[0], x[1]), [(ox + h[0], h[1]) for h in hs], (ox + y[0], y[1])
    for h in hb:
        parts += [link(xb, h), link(h, yb)]
    parts += [unit_node(*xb, "x"), unit_node(*yb, "y", None, OUT)] + [unit_node(*h, "h", str(j), UNITS[j]) for j, h in enumerate(hb)]
    parts += [caption(ox + 10, 30, "b)", anchor="start")]
    return parts


def data_split():
    """The dataset d split into a training and a test set, then into training, validation and test sets."""
    width, h = 900, 64
    fills = {"train": "#e9e9e9", "valid": "#f3d2b1", "test": "#bcd0ea"}
    roles = {"train": None, "valid": "hyperparameters", "test": "final estimate"}

    def name(x, y, sub):
        return (f'<text x="{x:g}" y="{y + 10:g}" font-size="28" fill="{INK}" text-anchor="middle">'
                f'<tspan font-family="KaTeX_Main" font-weight="700">d</tspan>'
                f'<tspan font-family="KaTeX_Main" font-size="19.6" dy="6">{sub}</tspan></text>')

    parts = []
    for y0, split in [(30, [("train", 0.8), ("test", 0.2)]), (210, [("train", 0.6), ("valid", 0.2), ("test", 0.2)])]:
        x = 10
        for key, frac in split:
            w = frac * width
            parts.append(f'<rect x="{x:g}" y="{y0}" width="{w:g}" height="{h}" fill="{fills[key]}" '
                         f'stroke="white" stroke-width="4"/>')
            parts.append(name(x + w / 2, y0 + h / 2, key))
            if roles[key]:
                parts.append(caption(x + w / 2, y0 + h + 28, roles[key]))
            else:   # "fit θ", with θ in KaTeX_Math as on the slides
                parts.append(f'<text x="{x + w / 2:g}" y="{y0 + h + 35:g}" font-size="20" fill="#555555" text-anchor="middle">'
                             f'<tspan font-family="Roboto, sans-serif">fit </tspan>'
                             f'<tspan font-family="KaTeX_Math" font-size="21">θ</tspan></text>')
            x += w
        parts.append(f'<rect x="10" y="{y0}" width="{width}" height="{h}" fill="none" stroke="{INK}" stroke-width="{STROKE:g}"/>')
    return parts


def two_outputs_net():
    xs = [(70, 230, "x", None)]
    hs = column(300, [("h", str(j)) for j in range(4)], 65, 110)
    ys = column(530, [("y", "0"), ("y", "1")], 175, 110)
    # the two outputs are color coded, their nodes and curves; the edges and hidden units in ink
    parts = [link(xs[0][:2], h[:2]) for h in hs]
    parts += [link(h[:2], yk[:2]) for yk in ys for h in hs]
    parts += [unit_node(*n[:2], n[2], n[3]) for n in xs + hs]
    parts += [unit_node(*yk[:2], yk[2], yk[3], OUTPUTS[k]) for k, yk in enumerate(ys)]
    return parts


def two_inputs_net():
    xs = column(70, [("x", "0"), ("x", "1")], 120, 120)
    hs = column(310, [("h", str(j)) for j in range(3)], 60, 120)
    ys = [(550, 180, "y", None)]
    return network([xs, hs, ys], colors={("h", str(j)): UNITS[j] for j in range(3)})


def concat_net():
    x = [(60, 160, "x", None)]
    h = column(230, [("h", str(j)) for j in range(3)], 50, 110)
    y = [(400, 160, "y", None)]
    h2 = column(570, [("h′", str(j)) for j in range(3)], 50, 110)
    y2 = [(740, 160, "y′", None)]
    return network([x, h, y, h2, y2])


def two_layer_2d_net():
    xs = column(60, [("x", "0"), ("x", "1")], 100, 120)
    h = column(230, [("h", str(j)) for j in range(3)], 40, 120)
    y = [(400, 160, "y", None)]
    h2 = column(570, [("h′", str(j)) for j in range(2)], 100, 120)
    y2 = [(740, 160, "y′", None)]
    return network([xs, h, y, h2, y2])


def deep_net():
    x = [(60, 160, "x", None)]
    h = column(260, [("h", str(j)) for j in range(3)], 50, 110)
    h2 = column(460, [("h′", str(j)) for j in range(3)], 50, 110)
    y = [(660, 160, "y", None)]
    return network([x, h, h2, y])


# ---- one-dimensional plots

def axes_1d(ax, ylim=(-1, 1), xlabel=True, ylabel=None):
    ax.set_box_aspect(1)   # plots of a function of x are square
    ax.set_xlim(0, 1)
    ax.set_ylim(*ylim)
    if ylim[0] < 0:
        ticks = [-1, -0.5, 0, 0.5, 1] if ylim[1] <= 1 else [-1, 0, 1]
        ax.set_yticks(ticks, [f"{v:g}" for v in ticks])
    ax.axhline(0, color=LIGHT, linewidth=1, zorder=0)
    ax.set_xticks([0, 0.5, 1], ["0", "0.5", "1"])
    if xlabel:
        ax.set_xlabel(r"$x$", fontsize=19)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=19)


def shallow(params, c, x=X):
    return sum(v * relu(w * x + b) for w, b, v in params) + c


def joints(ax, params, color=GREY):
    for w, b, _ in params:
        if w != 0 and 0 < -b / w < 1:
            ax.axvline(-b / w, color=color, linewidth=1, linestyle=":", zorder=0)


def functions():
    rng = np.random.default_rng(3)
    sets = [(SHALLOW, C)]
    while len(sets) < 3:
        w = rng.uniform(-3, 3, 3)
        jts = rng.uniform(0.12, 0.88, 3)
        params = [(wj, -wj * jt, vj) for wj, jt, vj in zip(w, jts, rng.uniform(-3, 3, 3))]
        c = rng.uniform(-0.5, 0.5)
        y = shallow(params, c)
        if np.abs(y).max() < 0.9 and np.ptp(y) > 0.9 and np.diff(np.sort(jts)).min() > 0.12 and np.abs(w).min() > 0.8:
            sets.append((params, c))
    fig, axs = plt.subplots(1, 3, figsize=(11, 4), sharey=True)
    for k, (ax, (params, c)) in enumerate(zip(axs, sets)):
        axes_1d(ax, (-1, 1), ylabel=r"$y$" if k == 0 else None)
        joints(ax, params)
        ax.plot(X, shallow(params, c), color=OUT)
    fig.tight_layout()
    save(fig, "nn-functions")


def approximate():
    target = lambda x: 0.65 * np.cos(2 * np.pi * 1.1 * x) - 0.25 * np.exp(-((x - 0.42) ** 2) / 0.006)
    fig, axs = plt.subplots(1, 3, figsize=(11, 4), sharey=True)
    for k, (ax, regions) in enumerate(zip(axs, [5, 10, 20])):
        q = regions - 1
        jts = (np.arange(q) + 1) / regions
        H = np.stack([relu(X - j) for j in jts] + [np.ones_like(X)], axis=1)
        coef, *_ = np.linalg.lstsq(H, target(X), rcond=None)
        axes_1d(ax, (-1, 1), ylabel=r"$y$" if k == 0 else None)
        for j in jts:
            ax.axvline(j, color=LIGHT, linewidth=1, linestyle=":", zorder=0)
        ax.plot(X, target(X), color=GREY, linewidth=1.6, linestyle="--")
        ax.plot(X, H @ coef, color=OUT)
        ax.set_title(f"{regions} linear regions", fontsize=15, color=INK)
    fig.tight_layout()
    save(fig, "nn-approximate")


def two_outputs():
    units = [(1.6, -0.55), (-2.0, 0.9), (2.5, -1.75), (1.2, -0.25)]
    v0, v1, c0, c1 = [0.9, 0.6, -1.4, -0.3], [-0.7, 0.8, 1.6, 0.4], 0.15, -0.35
    fig, ax = plt.subplots(figsize=(4.8, 4.8))
    axes_1d(ax, (-1, 1), ylabel="outputs")
    for w, b in units:
        if 0 < -b / w < 1:
            ax.axvline(-b / w, color=GREY, linewidth=1, linestyle=":", zorder=0)
    h = [relu(w * X + b) for w, b in units]
    y0 = sum(v * hj for v, hj in zip(v0, h)) + c0
    y1 = sum(v * hj for v, hj in zip(v1, h)) + c1
    ax.plot(X, y0, color=OUTPUTS[0])
    ax.plot(X, y1, color=OUTPUTS[1])
    ax.text(0.02, y0[16] + 0.12, r"$y_0$", fontsize=19, color=OUTPUTS[0])
    ax.text(0.02, y1[16] - 0.28, r"$y_1$", fontsize=19, color=OUTPUTS[1])
    save(fig, "nn-two-outputs-plot")


# The two networks in series of the folding animation, on [0, 1]
A_, B_ = 0.38, 0.62
f_ = lambda x: np.where(x < A_, x / A_, np.where(x < B_, 1 - (x - A_) / (B_ - A_), (x - B_) / (1 - B_)))
piece = lambda x: np.where(x < A_, 0, np.where(x < B_, 1, 2))
G_ = np.array([[0, 0.15], [0.3, 0.9], [0.62, 0.25], [1, 0.75]])
g_ = lambda y: np.interp(y, G_[:, 0], G_[:, 1])


def colored(ax, x, y, pieces):
    for k in range(3):
        m = pieces == k
        ax.plot(x[m], y[m], color=UNITS[k])


def concat():
    fig, axs = plt.subplots(1, 3, figsize=(11, 4.2))
    axes_1d(axs[0], (0, 1), ylabel=r"$y$")
    colored(axs[0], X, f_(X), piece(X))
    axs[0].set_title(r"first network $y = f(x)$", fontsize=15)
    axes_1d(axs[1], (0, 1), xlabel=False, ylabel=r"$y'$")
    axs[1].set_xlabel(r"$y$", fontsize=19)
    axs[1].plot(X, g_(X), color=INK)
    axs[1].set_title(r"second network $y' = g(y)$", fontsize=15)
    axes_1d(axs[2], (0, 1), ylabel=r"$y'$")
    for j in (A_, B_):
        axs[2].axvline(j, color=GREY, linewidth=1, linestyle=":", zorder=0)
    colored(axs[2], X, g_(f_(X)), piece(X))
    axs[2].set_title(r"composition $y' = g(f(x))$", fontsize=15)
    for ax in axs:
        ax.set_yticks([0, 0.5, 1], ["0", "0.5", "1"])
    fig.tight_layout()
    save(fig, "nn-concat")


# Second layer of a deep network on top of the demo's first layer
DEEP = [((0.6, -1.3, 1.2), -0.16), ((-1.5, 0.4, 1.9), 0.34), ((1.3, -0.1, -2.0), 0.01)]   # (w'_j0, w'_j1, w'_j2), b'_j
V2, C2 = [1.0, -1.1, -1.0], -0.1   # found by a search: every panel within [-1.15, 1.15], every weighted unit visible


def deep_buildup():
    h = np.stack([relu(w * X + b) for w, b, _ in SHALLOW])
    pre = [np.dot(ws, h) + b for ws, b in DEEP]
    fig, axs = plt.subplots(3, 4, figsize=(13, 10))
    titles = [[rf"$w'_{{{j}0}}h_0 + w'_{{{j}1}}h_1 + w'_{{{j}2}}h_2 + b'_{j}$" for j in range(3)],
              [rf"$h'_{j} = \mathrm{{ReLU}}(\cdot)$" for j in range(3)],
              [rf"$v_{j} h'_{j}$" for j in range(3)]]
    for j in range(3):
        rows = [pre[j], relu(pre[j]), V2[j] * relu(pre[j])]
        for r in range(3):
            ax = axs[r, j]
            axes_1d(ax, (-1.2, 1.2), xlabel=r == 2)
            ax.plot(X, rows[r], color=UNITS[j])
            ax.set_title(titles[r][j], fontsize=12.5)
    y = sum(V2[j] * relu(pre[j]) for j in range(3)) + C2
    assert np.abs(y).max() < 1.2, np.abs(y).max()
    for r in (0, 2):
        axs[r, 3].axis("off")
    ax = axs[1, 3]
    axes_1d(ax, (-1.2, 1.2))
    ax.plot(X, y, color=OUT)
    ax.set_title(r"$y = v_0 h'_0 + v_1 h'_1 + v_2 h'_2 + c$", fontsize=12.5)
    fig.tight_layout()
    save(fig, "nn-deep-buildup")


def regions():
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    shades = ["#b9b9b9", "#9fbbe0", "#5d8bc8", "#356aaf", "#1f3f6b"]
    for K, color in zip(range(1, 6), shades):
        q = np.unique(np.geomspace(1, 400, 26).astype(int))
        params = 2 * q + (K - 1) * (q ** 2 + q) + q + 1
        m = params <= 1000
        ax.plot(params[m], (q[m] + 1.0) ** K, "-o", color=color, markersize=3.5, linewidth=1.8)
        last = np.flatnonzero(m)[-1]
        ax.text(params[last] + 15, (q[last] + 1.0) ** K, rf"$K = {K}$", fontsize=16, color=color, va="center")
    ax.set_yscale("log")
    ax.set_xlim(0, 1130)
    ax.set_xlabel("number of parameters")
    ax.set_ylabel("linear regions")
    save(fig, "nn-regions")


def activations():
    z = np.linspace(-4, 4, 801)
    fig, ax = plt.subplots(figsize=(4.8, 4.8))
    ax.set_box_aspect(1)
    ax.axhline(0, color=LIGHT, linewidth=1, zorder=0)
    ax.axvline(0, color=LIGHT, linewidth=1, zorder=0)
    ax.plot(z, 1 / (1 + np.exp(-z)), color=BLUE)
    ax.plot(z, np.tanh(z), color=ORANGE)
    ax.plot(z, relu(z), color="#3f8f5a")
    ax.text(2.2, 0.72, "sigmoid", color=BLUE, fontsize=15)
    ax.text(-3.9, -0.82, "tanh", color=ORANGE, fontsize=15)
    ax.text(2.6, 2.1, "ReLU", color="#3f8f5a", fontsize=15)
    ax.set_xlim(-4, 4)
    ax.set_ylim(-1.3, 3)
    ax.set_xlabel(r"$x$", fontsize=19)
    ax.set_ylabel(r"$\sigma(x)$", fontsize=19)
    save(fig, "nn-activations")


# ---- two-dimensional plots

UNITS_2D = [((1.0, 0.9), 0.35), ((2.2, -0.35), -0.55), ((-0.6, 1.4), -0.1)]   # (w_j0, w_j1), b_j
V_2D, C_2D = [0.8, -0.9, 0.7], 0.05
G2 = [((1.6,), -0.25), ((-1.3,), 0.45)]   # second network: one input, two units
V2_2D, C2_2D = [-1.1, 0.9], 0.2
GRID = np.linspace(-1, 1, 401)
X0, X1 = np.meshgrid(GRID, GRID)


def field(ax, z, title, lines=(), lim=None):
    lim = lim or max(1e-6, np.abs(z).max())
    ax.imshow(z, extent=(-1, 1, -1, 1), origin="lower", cmap=DIV, vmin=-lim, vmax=lim, interpolation="bilinear")
    ax.contour(X0, X1, z, levels=np.linspace(-lim, lim, 17), colors=GREY, linewidths=0.5, alpha=0.6)
    for (w, b), color in lines:
        if abs(w[1]) > 1e-9:
            ax.plot(GRID, -(w[0] * GRID + b) / w[1], color=INK, linewidth=1.8, linestyle="--")
        else:
            ax.axvline(-b / w[0], color=INK, linewidth=1.8, linestyle="--")
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    ax.set_title(title, fontsize=15)
    for side in ("top", "right"):
        ax.spines[side].set_visible(True)


def buildup_2d():
    fig, axs = plt.subplots(3, 4, figsize=(12, 9.2))
    pre = [w[0] * X0 + w[1] * X1 + b for w, b in UNITS_2D]
    for j, (w, b) in enumerate(UNITS_2D):
        line = [((w, b), UNITS[j])]
        field(axs[0, j], pre[j], rf"$w_{{{j}0}} x_0 + w_{{{j}1}} x_1 + b_{j}$")
        field(axs[1, j], relu(pre[j]), rf"$h_{j} = \mathrm{{ReLU}}(\cdot)$", line)
        field(axs[2, j], V_2D[j] * relu(pre[j]), rf"$v_{j} h_{j}$", line)
    y = sum(V_2D[j] * relu(pre[j]) for j in range(3)) + C_2D
    for r in (0, 2):
        axs[r, 3].axis("off")
    field(axs[1, 3], y, r"$y = v_0 h_0 + v_1 h_1 + v_2 h_2 + c$", [((w, b), UNITS[j]) for j, (w, b) in enumerate(UNITS_2D)])
    for ax in axs[:, 0]:
        ax.set_ylabel(r"$x_1$", fontsize=18)
    for ax in axs[2, :3]:
        ax.set_xlabel(r"$x_0$", fontsize=18)
    fig.tight_layout()
    save(fig, "nn-buildup-2d")


def two_layer_2d():
    pre = [w[0] * X0 + w[1] * X1 + b for w, b in UNITS_2D]
    y = sum(V_2D[j] * relu(pre[j]) for j in range(3)) + C_2D
    g = lambda t: sum(v * relu(w[0] * t + b) for (w, b), v in zip(G2, V2_2D)) + C2_2D
    fig, axs = plt.subplots(1, 3, figsize=(12, 4.2))
    field(axs[0], y, r"first network: $y$", [((w, b), INK) for w, b in UNITS_2D])
    axs[1].axhline(0, color=LIGHT, linewidth=1, zorder=0)
    t = np.linspace(-1, 1, 401)
    ax = axs[1]
    ax.set_box_aspect(1)
    ax.plot(t, g(t), color=INK)
    for (w, b) in G2:
        ax.axvline(-b / w[0], color=GREY, linewidth=1, linestyle=":")
    ax.set_xlim(-1, 1)
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    ax.set_xlabel(r"$y$", fontsize=18)
    ax.set_title(r"second network: $y' = g(y)$", fontsize=15)
    yy = g(y)
    lines = [((w, b), INK) for w, b in UNITS_2D]
    field(axs[2], yy, r"composition: $y'$", lines)
    # the level sets y = joint of g, where the second network's units switch
    for (w, b) in G2:
        axs[2].contour(X0, X1, y, levels=[-b / w[0]], colors=[INK], linewidths=1.8, linestyles=":")
    for ax in (axs[0], axs[2]):
        ax.set_xlabel(r"$x_0$", fontsize=18)
    axs[0].set_ylabel(r"$x_1$", fontsize=18)
    fig.tight_layout()
    save(fig, "nn-two-layer-2d-plot")


# ---- linear regression

def regression_data():
    rng = np.random.default_rng(7)
    x = np.sort(rng.uniform(0.05, 1.95, 12))
    y = 0.35 * x + 0.75 + rng.normal(0, 0.18, x.size)
    w, b = np.polyfit(x, y, 1)
    return x, y, w, b


def lr_gaussian():
    x, y, w, b = regression_data()
    s = np.std(y - (w * x + b))
    fig, ax = plt.subplots(figsize=(5.2, 5.2))
    ax.set_box_aspect(1)
    t = np.linspace(0, 2, 2)
    ax.plot(t, w * t + b, color=INK)
    ax.plot(x, y, "o", color=ORANGE, markersize=7)
    for x0 in (0.5, 1.45):
        yy = np.linspace(w * x0 + b - 3.5 * s, w * x0 + b + 3.5 * s, 200)
        dens = np.exp(-((yy - (w * x0 + b)) ** 2) / (2 * s ** 2))
        ax.fill_betweenx(yy, x0, x0 + 0.28 * dens, color=BLUE, alpha=0.15, linewidth=0)
        ax.plot(x0 + 0.28 * dens, yy, color=BLUE, linewidth=1.6)
        ax.axvline(x0, color=LIGHT, linewidth=1, zorder=0)
    ax.text(1.55, w * 1.45 + b - 0.5, r"$\mathcal{N}(y \mid w x + b, \sigma^2)$", color=BLUE, fontsize=17)
    ax.set_xlim(0, 2)
    ax.set_xlabel(r"$x$", fontsize=19)
    ax.set_ylabel(r"$y$", fontsize=19)
    save(fig, "lr-gaussian-model")


def lr_residuals():
    x, y, w, b = regression_data()
    fig, ax = plt.subplots(figsize=(5.2, 5.2))
    ax.set_box_aspect(1)
    t = np.linspace(0, 2, 2)
    for xi, yi in zip(x, y):
        ax.plot([xi, xi], [yi, w * xi + b], color=ORANGE, linewidth=1.4, linestyle=":")
    ax.plot(t, w * t + b, color=INK)
    ax.plot(x, y, "o", color=ORANGE, markersize=7)
    sse = np.sum((y - (w * x + b)) ** 2)
    ax.set_title(rf"$\sum_i (y_i - (w x_i + b))^2 = {sse:.2f}$", fontsize=17)
    ax.set_xlim(0, 2)
    ax.set_xlabel(r"$x$", fontsize=19)
    ax.set_ylabel(r"$y$", fontsize=19)
    save(fig, "lr-residuals")



# ---- a convolutional and a pooling layer, computed on the deck's cat

# The convolution figures share one layout in inches, so that a cell, a pixel and a label have the same
# size on every slide: all are shown at their natural size (PLOT_SCALE), none wider than a slide.
CELL = 0.36    # a cell with a value: inputs, kernels, outputs, pooling
PIX = 0.13     # a pixel of the cat and of its feature maps
STK = 0.18     # the offset between stacked slices of an image or of feature maps
KSTK = 0.1     # the offset between the slices of a kernel
F_NUM, F_SYM, F_TITLE, F_OP, F_NOTE = 13, 20, 18, 26, 14   # values in cells, symbols, titles, operators, notes


def conv_pattern():
    """The cat of the opening slides through two 7x7 kernels, a ReLU and a 2x2 max-pooling, computed with
    numpy, with the receptive field of one pooled value boxed back to the input."""
    from PIL import Image
    from matplotlib.patches import ConnectionPatch, Rectangle

    # the photo inside its drawn frame, square, so that no border edge dominates the feature maps
    img = Image.open(ROOT / "figures" / "lec7" / "cat.jpg").convert("L").crop((62, 52, 298, 288)).resize((48, 48), Image.LANCZOS)
    x = np.asarray(img, dtype=float) / 255
    # 7x7 edge detectors, derivatives of a Gaussian: vertical edges, then horizontal ones. A large kernel
    # makes the receptive field visible: 8x8 input pixels after one stage, 22x22 after two
    K = 7
    u = np.arange(K) - K // 2
    gauss = np.exp(-u ** 2 / (2 * 1.4 ** 2))
    d = -u * gauss
    vertical = np.outer(gauss, d) / np.abs(np.outer(gauss, d)).sum() * 8
    kernels = [vertical, vertical.T]
    def conv(a, w):   # valid cross-correlation, as on the slides
        h, v = w.shape
        return np.array([[np.sum(a[j:j + h, i:i + v] * w) for i in range(a.shape[1] - v + 1)] for j in range(a.shape[0] - h + 1)])
    def pool(a):
        n = a.shape[0] // 2
        return a[:2 * n, :2 * n].reshape(n, 2, n, 2).max(axis=(1, 3))
    rows = []
    for w in kernels:
        z = conv(x, w)
        r = relu(z)
        rows.append((w, z, r, pool(r)))

    # a second convolutional layer over both pooled maps: a 2 x 7 x 7 kernel omega', smoothing each map, and a ReLU
    pooled_maps = [o for (_, _, _, o) in rows]
    w2 = np.array([gauss[:, None] * gauss[None, :]] * 2)
    w2 /= w2.sum()
    z2 = sum(conv(o, w) for o, w in zip(pooled_maps, w2))
    r2 = relu(z2 - np.median(z2))

    W, H = 9.6, 5.4   # as wide as a slide at PLOT_SCALE, as the other convolution figures
    fig = plt.figure(figsize=(W, H))
    def panel(cx, cy, size):   # a square panel centred at (cx, cy), all in inches
        return fig.add_axes([(cx - size / 2) / W, (cy - size / 2) / H, size / W, size / H])
    def show(ax, a, lim=None, cmap=None):
        if cmap == "gray":
            ax.imshow(a, cmap="gray", vmin=0, vmax=1, interpolation="nearest")
        else:
            ax.imshow(a, cmap=DIV, vmin=-lim, vmax=lim, interpolation="nearest")
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_visible(True); sp.set_color(INK); sp.set_linewidth(1)
    def arrow(a, b, xa=1, ya=0.5, xb=0, yb=0.5):
        fig.add_artist(ConnectionPatch((xa, ya), (xb, yb), "axes fraction", "axes fraction", axesA=a, axesB=b,
                                       arrowstyle="-|>", mutation_scale=16, color=INK, linewidth=1.4, shrinkA=0, shrinkB=0))

    # columns, in inches: input, kernel, convolution, ReLU, pooling, then the kernel, convolution and ReLU of layer 2
    # every panel at one pixel scale, that of the input: a 7x7 kernel is then as large as a 7x7 patch of the cat,
    # the pooled maps half as large as the convolutions, and the receptive fields compare directly
    px = 0.033
    sz = [px * n for n in (48, K, 42, 42, 21, K, 15, 15)]
    cx, at = [], 0.1
    for k, w_ in enumerate(sz):
        cx.append(at + w_ / 2)
        at += w_ + (0.06 if k == 5 else 0) + (0.6 if k == 6 else 0.3)
    ys, ym = [3.35, 1.45], 2.4
    inp = panel(cx[0], ym, sz[0])
    show(inp, x, cmap="gray")
    convs, maps, pools = [], [], []
    for k, (w, z, r, o) in enumerate(rows):
        lim = np.percentile(np.abs(z), 99)   # a few extreme values would wash out the rest
        kax = panel(cx[1], ys[k], sz[1])
        show(kax, w, np.abs(w).max())
        kax.set_title(rf"$\omega_{k}$", fontsize=F_SYM, pad=4)
        a1, a2, a3 = panel(cx[2], ys[k], sz[2]), panel(cx[3], ys[k], sz[3]), panel(cx[4], ys[k], sz[4])
        show(a1, z, lim); show(a2, r, lim); show(a3, o, lim)
        arrow(inp, kax, ya=0.75 if k == 0 else 0.25)
        arrow(kax, a1); arrow(a1, a2); arrow(a2, a3)
        convs.append(a1); maps.append(a2); pools.append(a3)
    # the kernel of layer 2: one 7 x 7 slice per pooled map, stacked
    k2 = []
    for d in (1, 0):
        a = fig.add_axes([(cx[5] - sz[5] / 2 + 0.06 * d) / W, (ym - sz[5] / 2 + 0.06 * d) / H, sz[5] / W, sz[5] / H])
        show(a, w2[d], np.abs(w2).max())
        k2.append(a)
    k2[-1].set_title(r"$\omega'$", fontsize=F_SYM, pad=8)
    lim2 = np.percentile(np.abs(z2 - np.median(z2)), 99)
    c2, out2 = panel(cx[6], ym, sz[6]), panel(cx[7], ym, sz[7])
    show(c2, z2 - np.median(z2), lim2); show(out2, r2, lim2)
    for k, a3 in enumerate(pools):
        arrow(a3, k2[-1], xb=0, yb=0.75 if k == 0 else 0.25)
    arrow(k2[-1], c2, xa=1 + 0.06 / sz[5])
    arrow(c2, out2)

    # receptive fields, in red: one pooled value of the first map comes from a 2x2 block of its map, which sees
    # an 8x8 patch of the input (7x7 kernel, then 2x2 pooling); one value of layer 2 sees a 7x7 block of both
    # pooled maps, which see a 20x20 patch of the input (8 + 6 x 2, pooled values being 2 pixels apart)
    RF = "#c8463d"
    pj, pi = 7, 10
    vj, vi = pj - 3, pi - 3
    def box(ax, j, i, n, style="-", lw=2.4):
        ax.add_patch(Rectangle((i - 0.5, j - 0.5), n, n, fill=False, edgecolor=RF, linewidth=lw, linestyle=style,
                               zorder=6, clip_on=False))
    def cone(ax_a, ja, ia, na, ax_b, jb, ib, nb, style=(0, (3, 2))):
        # from the left corners of the box on ax_a to the right corners of the box on ax_b, over the panels
        for dy in (0, 1):
            fig.add_artist(ConnectionPatch((ia - 0.5, ja - 0.5 + dy * na), (ib - 0.5 + nb, jb - 0.5 + dy * nb), "data", "data",
                                           axesA=ax_a, axesB=ax_b, color=RF, linewidth=1.1, linestyle=style, zorder=6))
    box(out2, vj, vi, 1)
    box(c2, vj, vi, 1)
    cone(out2, vj, vi, 1, c2, vj, vi, 1, style=(0, (4, 2)))
    for a3 in pools:
        box(a3, vj, vi, 7, style=(0, (4, 2)), lw=1.8)
        cone(c2, vj, vi, 1, a3, vj, vi, 7, style=(0, (4, 2)))
    box(pools[0], pj, pi, 1)
    box(maps[0], 2 * pj, 2 * pi, 2)
    box(convs[0], 2 * pj, 2 * pi, 2)
    box(inp, 2 * pj, 2 * pi, K + 1)
    box(inp, 2 * vj, 2 * vi, 20, style=(0, (4, 2)), lw=1.8)
    cone(pools[0], pj, pi, 1, maps[0], 2 * pj, 2 * pi, 2)
    cone(maps[0], 2 * pj, 2 * pi, 2, convs[0], 2 * pj, 2 * pi, 2)
    cone(convs[0], 2 * pj, 2 * pi, 2, inp, 2 * pj, 2 * pi, K + 1)
    def tag(ax, s):   # under a panel, in red
        ax.text(0.5, -0.06, s, transform=ax.transAxes, ha="center", va="top", fontsize=F_NOTE, color=RF)
    tag(out2, "1 value")
    tag(pools[0], "1 value\n7 × 7")
    tag(pools[1], "7 × 7")
    tag(maps[0], "2 × 2")
    tag(convs[0], "2 × 2")
    tag(inp, "1 pooled value: 8 × 8\n1 value of layer 2: 20 × 20")

    # column labels and layer brackets
    top = ys[0] + sz[2] / 2 + 0.55
    for c, s_ in [(cx[0], "input\n" + r"$\mathbf{x}$"), (cx[2], "convolution\n" + r"$\mathbf{x} \circledast \omega_k$"),
                  (cx[3], "ReLU\n"), (cx[4], "max-pooling\n" + r"$\mathbf{o}_k$"),
                  (cx[6], "convolution\n" + r"$\mathbf{o} \circledast \omega'$"), (cx[7], "ReLU\n")]:
        fig.text(c / W, top / H, s_, ha="center", va="center", fontsize=F_TITLE, color=INK)
    def bracket(x0, x1, text):
        y = 0.25
        fig.add_artist(matplotlib.lines.Line2D([x0 / W, x1 / W], [y / H, y / H], color=GREY, linewidth=1.4))
        for xx in (x0, x1):
            fig.add_artist(matplotlib.lines.Line2D([xx / W, xx / W], [y / H, (y + 0.13) / H], color=GREY, linewidth=1.4))
        fig.text((x0 + x1) / 2 / W, (y - 0.07) / H, text, ha="center", va="top", fontsize=F_TITLE, color=GREY)
    bracket(cx[1] - sz[1] / 2, cx[3] + sz[3] / 2, "convolutional layer")
    bracket(cx[4] - sz[4] / 2, cx[4] + sz[4] / 2, "pooling\nlayer")
    bracket(cx[5] - sz[5] / 2, cx[7] + sz[7] / 2, "convolutional\nlayer")
    out = ROOT / "figures" / "lec7" / "nn-conv-pattern.svg"
    fig.savefig(out, bbox_inches="tight", transparent=True, metadata={"Date": None})
    rescale(out)
    plt.close(fig)
    print(out.relative_to(ROOT))


# ---- convolution and pooling, cell by cell, in the style of `nn-conv-pattern.svg`

def cells(ax, a, lim, fmt="{:g}", fontsize=15, cmap=None):
    """A grid of values: each cell colored on the diverging scale (or `cmap`), its value written in it."""
    a = np.atleast_2d(a)
    if cmap is None:
        ax.imshow(a, cmap=DIV, vmin=-lim, vmax=lim)
    else:
        ax.imshow(a, cmap=cmap, vmin=0, vmax=lim)
    for (j, i), v in np.ndenumerate(a):
        if fmt:   # white on the darkest cells, ink elsewhere
            dark = abs(v) / lim > 0.62 if cmap is None else v / lim > 0.62
            ax.text(i, j, fmt.format(v), ha="center", va="center", fontsize=fontsize, color="white" if dark else INK)
    ax.set_xticks(np.arange(-0.5, a.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-0.5, a.shape[0], 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.5)
    ax.tick_params(which="both", length=0)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(True); sp.set_color(INK); sp.set_linewidth(1)


def window(ax, j, i, h, w, style="-"):
    from matplotlib.patches import Rectangle
    ax.add_patch(Rectangle((i - 0.5, j - 0.5), w, h, fill=False, edgecolor=INK, linewidth=2.6, linestyle=style,
                           clip_on=False, zorder=5))


def place(fig, x, y, w, h):
    """Axes from figure fractions of the canvas, so that cells of all grids have one size."""
    return fig.add_axes([x, y, w, h])


def inches(fig):
    W, H = fig.get_size_inches()
    def ax(x, y, w, h):
        return fig.add_axes([x / W, y / H, w / W, h / H])
    def text(x, y, s, **kw):
        return fig.text(x / W, y / H, s, **kw)
    return ax, text


def frame(ax, color, width=2.6):
    for sp in ax.spines.values():
        sp.set_color(color); sp.set_linewidth(width)


def conv_1d():
    xv = np.array([1, 3, 2, 0, -1, 2, 4, 1], float)
    wv = np.array([1, 0, -1], float)
    zv = np.array([np.dot(xv[i:i + 3], wv) for i in range(len(xv) - 2)])
    fig = plt.figure(figsize=(4.6, 3.0))
    ax, text = inches(fig)
    x0, i0, rows = 0.9, 1, [2.3, 1.4, 0.5]
    ax_x = ax(x0, rows[0], 8 * CELL, CELL); cells(ax_x, xv, 5, fontsize=F_NUM)
    ax_w = ax(x0 + i0 * CELL, rows[1], 3 * CELL, CELL); cells(ax_w, wv, 5, fontsize=F_NUM)
    ax_z = ax(x0 + CELL, rows[2], 6 * CELL, CELL); cells(ax_z, zv, 5, fontsize=F_NUM)
    window(ax_x, 0, i0, 1, 3)
    window(ax_z, 0, i0, 1, 1)
    text(x0 - 0.1, rows[0] + CELL / 2, r"$\mathbf{x}$", ha="right", va="center", fontsize=F_SYM)
    text(x0 + i0 * CELL - 0.1, rows[1] + CELL / 2, r"$\omega$", ha="right", va="center", fontsize=F_SYM)
    text(x0 + CELL - 0.1, rows[2] + CELL / 2, r"$\mathbf{x} \circledast \omega$", ha="right", va="center", fontsize=F_SYM)
    terms = " + ".join(f"{xv[i0 + m]:g} \\cdot {wv[m]:g}" for m in range(3)).replace("\\cdot -1", "\\cdot (-1)")
    text(x0 + 4 * CELL, rows[2] - 0.2, rf"$(\mathbf{{x}} \circledast \omega)[{i0}] = {terms} = {zv[i0]:g}$",
         ha="center", va="top", fontsize=F_TITLE, color=INK)
    save(fig, "nn-conv1d")


def conv_2d():
    xv = np.array([[2, 0, 1, 3, 1, 0], [1, 3, 2, 0, 2, 1], [0, 2, 4, 1, 0, 3],
                   [3, 1, 0, 2, 4, 1], [1, 0, 2, 3, 1, 2], [0, 2, 1, 0, 3, 1]], float)
    wv = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]], float)
    zv = np.array([[np.sum(xv[j:j + 3, i:i + 3] * wv) for i in range(4)] for j in range(4)])
    fig = plt.figure(figsize=(6.6, 3.0))
    ax, text = inches(fig)
    lim = np.abs(zv).max()
    y0, cy = 0.2, 0.2 + 3 * CELL
    xx, xw, xz = 0.1, 0.1 + 6 * CELL + 0.6, 0.1 + 9 * CELL + 1.2
    ax_x = ax(xx, y0, 6 * CELL, 6 * CELL); cells(ax_x, xv, lim, fontsize=F_NUM)
    ax_w = ax(xw, cy - 1.5 * CELL, 3 * CELL, 3 * CELL); cells(ax_w, wv, lim, fontsize=F_NUM)
    ax_z = ax(xz, cy - 2 * CELL, 4 * CELL, 4 * CELL); cells(ax_z, zv, lim, fontsize=F_NUM)
    window(ax_x, 0, 0, 3, 3)
    window(ax_z, 0, 0, 1, 1)
    text(xx + 6 * CELL + 0.3, cy, r"$\circledast$", ha="center", va="center", fontsize=F_OP)
    text(xw + 3 * CELL + 0.3, cy, r"$=$", ha="center", va="center", fontsize=F_OP)
    text(xx + 3 * CELL, y0 + 6 * CELL + 0.1, r"$\mathbf{x}$", ha="center", va="bottom", fontsize=F_SYM)
    text(xw + 1.5 * CELL, cy + 1.5 * CELL + 0.1, r"$\omega$", ha="center", va="bottom", fontsize=F_SYM)
    text(xz + 2 * CELL, cy + 2 * CELL + 0.1, r"$\mathbf{x} \circledast \omega$", ha="center", va="bottom", fontsize=F_SYM)
    save(fig, "nn-conv2d")


def the_cat():
    from PIL import Image
    img = Image.open(ROOT / "figures" / "lec7" / "cat.jpg").convert("RGB").crop((62, 52, 298, 288)).resize((16, 16), Image.LANCZOS)
    return np.asarray(img, dtype=float).transpose(2, 0, 1) / 255


def rgb_stack(ax, text, x, j0, i0, y0):
    """The cat as a stack of its R, G and B slices, red at the back, from (0.4, y0) in inches; the name of
    each slice left of it, in the strip where it shows above the slice in front."""
    from matplotlib.colors import LinearSegmentedColormap as LSC
    hues, names = ["#c8463d", "#3f8f5a", "#356aaf"], ["R", "G", "B"]
    n = x.shape[1] * PIX
    for cidx in range(3):
        d = 2 - cidx
        a = ax(0.4 + d * STK, y0 + d * STK, n, n)
        cells(a, x[cidx], 1, fmt=None, cmap=LSC.from_list(names[cidx], ["#ffffff", hues[cidx]]))
        window(a, j0, i0, 3, 3)
        text(0.4 + d * STK - 0.06, y0 + d * STK + n - STK / 2, names[cidx], ha="right", va="center",
             fontsize=F_NOTE, color=hues[cidx])
    text(0.4 + n / 2 + STK, y0 + n + 2 * STK + 0.12, r"input $\mathbf{x} \in \mathbb{R}^{3 \times H \times W}$",
         ha="center", va="bottom", fontsize=F_TITLE)
    return 0.4 + n + 2 * STK   # the right edge of the stack


def kernel_stack(ax, w, x0, y0, color=None, fmt=None):
    """A 3 x 3 x 3 kernel as three slices, at the cell size of every kernel of the deck."""
    lim = np.abs(w).max()
    for cidx in range(3):
        d = 2 - cidx
        a = ax(x0 + d * KSTK, y0 + d * KSTK, 3 * CELL, 3 * CELL)
        cells(a, w[cidx], lim, fmt=fmt, fontsize=F_NUM - 2)
        if color:
            frame(a, color, 2.0)
    return 3 * CELL + 2 * KSTK


def conv_channels():
    """The cat in its three channels, a 3x3x3 kernel, and the map it gives: one value sums over the
    channels and the window."""
    x = the_cat()
    rng = np.random.default_rng(2)
    w = np.round(rng.normal(0, 1, (3, 3, 3)), 1)
    z = np.array([[np.sum(x[:, j:j + 3, i:i + 3] * w) for i in range(14)] for j in range(14)])
    fig = plt.figure(figsize=(9.6, 3.2))
    ax, text = inches(fig)
    j0, i0, y0 = 5, 6, 0.2
    n = 16 * PIX
    cy = y0 + (n + 2 * STK) / 2
    right = rgb_stack(ax, text, x, j0, i0, y0)
    text(right + 0.3, cy, r"$\circledast$", ha="center", va="center", fontsize=F_OP)
    kx = right + 0.6
    size = kernel_stack(ax, w, kx, cy - (3 * CELL + 2 * KSTK) / 2, fmt="{:g}")
    text(kx + size / 2, cy + size / 2 + 0.12, r"kernel $\omega \in \mathbb{R}^{3 \times 3 \times 3}$", ha="center", va="bottom", fontsize=F_TITLE)
    text(kx + size + 0.3, cy, r"$=$", ha="center", va="center", fontsize=F_OP)
    zx, m = kx + size + 0.6, 14 * PIX
    a = ax(zx, cy - m / 2, m, m)
    cells(a, z, np.abs(z).max(), fmt=None)
    window(a, j0, i0, 1, 1)
    text(zx + m / 2, cy + m / 2 + 0.12, r"$\mathbf{x} \circledast \omega$", ha="center", va="bottom", fontsize=F_SYM)
    text(zx + m + 0.2, cy, "one value sums\nover the 3 channels\nof the 3 × 3 window", ha="left", va="center", fontsize=F_NOTE, color=GREY)
    save(fig, "nn-conv-channels")


def conv_layer():
    """A convolutional layer: the cat in its three channels, K = 4 kernels of size 3 x 3 x 3 in parallel,
    and the K feature maps they give, stacked as the output channels; kernel k and map o_k share a color."""
    x = the_cat()
    rng = np.random.default_rng(5)
    K = 4
    ws = rng.normal(0, 1, (K, 3, 3, 3))
    ws = np.round(ws - ws.mean(axis=(1, 2, 3), keepdims=True), 1)   # zero mean: the maps show edges, not brightness
    zs = [np.array([[np.sum(x[:, j:j + 3, i:i + 3] * w) for i in range(14)] for j in range(14)]) for w in ws]
    fig = plt.figure(figsize=(9.6, 3.6))
    ax, text = inches(fig)
    j0, i0, y0 = 5, 6, 0.2
    n = 16 * PIX
    cy = y0 + (n + 2 * STK) / 2
    right = rgb_stack(ax, text, x, j0, i0, y0)
    text(right + 0.3, cy, r"$\circledast$", ha="center", va="center", fontsize=F_OP)
    # the K kernels in a 2 x 2 grid, each named above it
    size, gap = 3 * CELL + 2 * KSTK, 0.35
    kx = right + 0.6
    for k in range(K):
        col, row = k % 2, k // 2
        x0 = kx + col * (size + 0.25)
        yk = cy + gap / 2 if row == 0 else cy - gap / 2 - size
        kernel_stack(ax, ws[k], x0, yk, color=UNITS[k])
        text(x0 + size / 2, yk + size + 0.04, rf"$\omega_{k}$", ha="center", va="bottom", fontsize=F_SYM)
    text(kx + size + 0.125, cy + size + gap / 2 + 0.38, r"$K$ kernels $\omega_k \in \mathbb{R}^{3 \times 3 \times 3}$",
         ha="center", va="bottom", fontsize=F_TITLE)
    ox = kx + 2 * size + 0.25 + 0.3
    text(ox, cy, r"$=$", ha="center", va="center", fontsize=F_OP)
    # the K feature maps, stacked as the K channels of the output, o_0 in front
    m, ostk = 14 * PIX, 0.22
    zx = ox + 0.6
    my = cy - (m + (K - 1) * ostk) / 2
    for k in reversed(range(K)):
        a = ax(zx + k * ostk, my + k * ostk, m, m)
        cells(a, zs[k], np.abs(zs[k]).max(), fmt=None)
        frame(a, UNITS[k])
        window(a, j0, i0, 1, 1)
        text(zx + k * ostk - 0.06, my + k * ostk + m - ostk / 2, rf"$\mathbf{{o}}_{k}$", ha="right", va="center",
             fontsize=F_NOTE + 1, color=UNITS[k])
    text(zx + m / 2 + 1.5 * ostk, my + m + (K - 1) * ostk + 0.12, r"output $\mathbf{o} \in \mathbb{R}^{K \times H' \times W'}$",
         ha="center", va="bottom", fontsize=F_TITLE)
    save(fig, "nn-conv-layer")


def pooling():
    xv = np.array([[1, 3, 5, 3], [6, 2, 0, 8], [4, 6, 1, 4], [2, 8, 0, 3]], float)
    blocks = [(0, 0), (0, 2), (2, 0), (2, 2)]
    sub = np.array([[xv[j, i] for (j, i) in blocks[:2]], [xv[j, i] for (j, i) in blocks[2:]]])
    mx = np.array([[xv[j:j + 2, i:i + 2].max() for (j, i) in blocks[r * 2:r * 2 + 2]] for r in range(2)])
    av = np.array([[xv[j:j + 2, i:i + 2].mean() for (j, i) in blocks[r * 2:r * 2 + 2]] for r in range(2)])
    fig = plt.figure(figsize=(9.6, 2.4))
    ax, text = inches(fig)
    lim = 9
    for k, (title, out, picks, fmt) in enumerate([
            ("subsampling", sub, [(j, i) for (j, i) in blocks], "{:g}"),
            ("max-pooling", mx, [tuple(np.add((j, i), np.unravel_index(np.argmax(xv[j:j + 2, i:i + 2]), (2, 2)))) for (j, i) in blocks], "{:g}"),
            ("average-pooling", av, [], "{:g}")]):
        x0, y0 = 0.1 + k * 3.25, 0.2
        ax_x = ax(x0, y0, 4 * CELL, 4 * CELL); cells(ax_x, xv, lim, fontsize=F_NUM)
        ax_o = ax(x0 + 4 * CELL + 0.6, y0 + CELL, 2 * CELL, 2 * CELL); cells(ax_o, out, lim, fmt=fmt, fontsize=F_NUM)
        ax_x.axhline(1.5, color=INK, linewidth=1.4, linestyle="--"); ax_x.axvline(1.5, color=INK, linewidth=1.4, linestyle="--")
        for (j, i) in picks:
            window(ax_x, j, i, 1, 1)
        text(x0 + 4 * CELL + 0.3, y0 + 2 * CELL, r"$\rightarrow$", ha="center", va="center", fontsize=F_OP)
        text(x0 + (6 * CELL + 0.6) / 2, y0 + 4 * CELL + 0.12, title, ha="center", va="bottom", fontsize=F_TITLE)
    save(fig, "nn-pooling")

def next_token():
    """A language model predicting the next token, twice, on a sentence of the course's world.
    The probabilities are illustrative: no model is run."""
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
    steps = [(["Pacman", "runs", "away", "from", "the"], [("ghost", 0.52), ("ghosts", 0.21), ("wall", 0.08), ("maze", 0.05), ("power pellet", 0.03)], "ghost"),
             (["Pacman", "runs", "away", "from", "the", "ghost"], [(".", 0.38), (",", 0.17), ("and", 0.14), ("Blinky", 0.09), ("who", 0.05)], ".")]
    W, H = 13.4, 6.2
    fig = plt.figure(figsize=(0.92 * W, 0.92 * H))   # drawn a little smaller, to fit the slide at PLOT_SCALE
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    def box(x, y, w, h, fc="white", ec=INK, lw=1.4, r=0.12):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw))
    def arrow(p, q, ls="-", color=INK, conn="arc3"):
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16, lw=1.4, color=color, linestyle=ls,
                                     shrinkA=0, shrinkB=0, connectionstyle=conn))
    width = lambda tok: 0.13 * len(tok) + 0.34
    row_end = 0.5 + sum(width(tok) + 0.1 for tok in steps[1][0])   # the longer sentence sets the layout
    mx = row_end + 0.45
    rows = [3.55, 0.45]
    anchors = {}
    for k, ((tokens, probs, chosen), y) in enumerate(zip(steps, rows)):
        ax.text(0.05, y + 1.0, "ab"[k] + ")", fontsize=16, color=INK, va="center")
        x = 0.5   # the tokens w_1, ..., w_{t-1}
        for m, tok in enumerate(tokens):
            w = width(tok)
            new = k == 1 and m == len(tokens) - 1
            box(x, y + 0.75, w, 0.5, fc="#eef3fa" if new else "white", ec=OUT if new else INK, lw=2 if new else 1.4)
            ax.text(x + w / 2, y + 1.0, tok, ha="center", va="center", fontsize=14, color=INK)
            ax.text(x + w / 2, y + 0.48, rf"$w_{{{m + 1}}}$", ha="center", va="center", fontsize=15, color=GREY)
            if new:
                anchors["new"] = (x + w / 2, y + 1.25)
            x += w + 0.1
        arrow((x, y + 1.0), (mx, y + 1.0))   # into the model
        box(mx, y + 0.45, 2.35, 1.1, fc="#f4f7fb", ec=INK, lw=1.6)
        ax.text(mx + 1.175, y + 1.22, "language model", ha="center", va="center", fontsize=14, color=INK)
        ax.text(mx + 1.175, y + 0.78, rf"$P_\theta(w_{{{len(tokens) + 1}}} \mid w_{{1:{len(tokens)}}})$", ha="center", va="center", fontsize=15, color=INK)
        arrow((mx + 2.35, y + 1.0), (mx + 2.8, y + 1.0))
        bx, top = mx + 4.05, y + 1.72   # the distribution over the vocabulary: a classification
        for n, (tok, pr) in enumerate(probs):
            yy = top - n * 0.34
            ax.text(bx - 0.1, yy, tok, ha="right", va="center", fontsize=13, color=INK)
            ax.add_patch(plt.Rectangle((bx, yy - 0.12), 3.2 * pr, 0.24, color=OUT if tok == chosen else LIGHT))
            ax.text(bx + 3.2 * pr + 0.08, yy, f"{pr:.2f}", ha="left", va="center", fontsize=12, color=GREY)
            if k == 0 and tok == chosen:   # the arrow back starts right of the chosen token's bar and value
                anchors["chosen"] = (bx + 3.2 * pr + 0.6, yy)
        ax.text(bx - 0.1, top - 5 * 0.34, "…", ha="right", va="center", fontsize=13, color=GREY)
    # the chosen token is appended to the sentence, and the model is applied again
    # from the right of the chosen token: right, down into the gap between the rows, left, then down into
    # the appended token, crossing neither bars nor arrows
    from matplotlib.path import Path
    (sx, sy), (nx, ny) = anchors["chosen"], anchors["new"]
    xr, gap = sx + 0.3, (rows[0] + rows[1] + 1.95) / 2
    ax.add_patch(FancyArrowPatch(path=Path([(sx, sy), (xr, sy), (xr, gap), (nx, gap), (nx, ny)]), arrowstyle="-|>",
                                 mutation_scale=16, lw=1.4, color=GREY, linestyle="--", clip_on=False))
    ax.text((xr + nx) / 2, gap + 0.2, "append the chosen token, then predict again", ha="center", va="center",
            fontsize=13, color=GREY)
    out = ROOT / "figures" / "lec7" / "nn-next-token.svg"
    fig.savefig(out, bbox_inches="tight", transparent=True, metadata={"Date": None})
    rescale(out)
    plt.close(fig)
    print(out.relative_to(ROOT))

if __name__ == "__main__":
    svg("nn-terminology", 660, 450, terminology(), folder="lec7", scale=SCALE)
    svg("nn-shallow", 1110, 500, shallow_net(), folder="lec7", scale=SCALE)
    svg("data-split", 920, 330, data_split(), folder="lec7", scale=SCALE)
    svg("nn-two-outputs-net", 600, 460, two_outputs_net(), folder="lec7", scale=SCALE)
    svg("nn-two-inputs", 620, 360, two_inputs_net(), folder="lec7", scale=SCALE)
    svg("nn-concat-net", 800, 320, concat_net(), folder="lec7", scale=SCALE)
    svg("nn-two-layer-2d-net", 800, 320, two_layer_2d_net(), folder="lec7", scale=SCALE)
    svg("nn-deep", 720, 320, deep_net(), folder="lec7", scale=SCALE)
    functions()
    approximate()
    two_outputs()
    concat()
    deep_buildup()
    regions()
    activations()
    buildup_2d()
    two_layer_2d()
    lr_gaussian()
    lr_residuals()
    conv_pattern()
    conv_1d()
    conv_2d()
    conv_channels()
    conv_layer()
    pooling()
    next_token()

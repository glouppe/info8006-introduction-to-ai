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
  here, with the receptive field of one pooled value boxed back to the input.
"""

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


def save(fig, name):
    out = ROOT / "figures" / "lec7" / f"{name}.svg"
    fig.savefig(out, bbox_inches="tight", transparent=True, metadata={"Date": None})
    plt.close(fig)
    print(out.relative_to(ROOT))


# ---- network diagrams

def primed(x, y, name, sub=None, size=28):
    """h' or h'_0 as LaTeX sets them: the prime raised and smaller, the subscript under it."""
    head = f'<tspan font-family="KaTeX_Math" font-style="italic">{name}</tspan>'
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
    x, one, hs, y, one2 = (70, 340), (70, 150), [(330, 170), (330, 310), (330, 450)], (590, 310), (330, 40)
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
        parts.append(halo(math(*mid(x, h, 0.74), [("w", "i"), (str(j), "s")], size=26, fill=UNITS[j])))
        parts.append(halo(math(*mid(one, h, 0.3), [("b", "i"), (str(j), "s")], size=26, fill=UNITS[j])))
        parts.append(halo(math(*mid(h, y, 0.5), [("v", "i"), (str(j), "s")], size=26, fill=UNITS[j])))
    parts.append(halo(math(*mid(one2, y, 0.5), [("c", "i")], size=26, fill=GREY)))
    parts += [caption(10, 30, "a)", anchor="start")]
    # b) compact
    ox = 700
    xb, hb, yb = (ox + 70, 310), [(ox + 260, 170), (ox + 260, 310), (ox + 260, 450)], (ox + 450, 310)
    for h in hb:
        parts += [link(xb, h), link(h, yb)]
    parts += [unit_node(*xb, "x"), unit_node(*yb, "y", None, OUT)] + [unit_node(*h, "h", str(j), UNITS[j]) for j, h in enumerate(hb)]
    parts += [caption(ox + 10, 30, "b)", anchor="start")]
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

    fig = plt.figure(figsize=(13, 5.2))
    S = 0.3   # panel height, in figure fraction; widths follow so that panels are square
    asp = 5.2 / 13
    def panel(cx, cy, size):
        return fig.add_axes([cx - size * asp / 2, cy - size / 2, size * asp, size])
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

    cols = [0.07, 0.235, 0.39, 0.555, 0.715, 0.9]   # input, kernel, convolution, ReLU, pooling, next layer
    ys = [0.66, 0.24]
    inp = panel(cols[0], 0.45, S * 1.05)
    show(inp, x, cmap="gray")
    pooled = []
    for k, (w, z, r, o) in enumerate(rows):
        lim = np.percentile(np.abs(z), 99)   # a few extreme values would wash out the rest
        kax = panel(cols[1], ys[k], S * 0.42)
        show(kax, w, np.abs(w).max())
        kax.set_title(rf"$\omega_{k}$", fontsize=21, pad=4)
        a1, a2, a3 = panel(cols[2], ys[k], S), panel(cols[3], ys[k], S), panel(cols[4], ys[k], S * 0.62)
        show(a1, z, lim); show(a2, r, lim); show(a3, o, lim)
        arrow(inp, kax, ya=0.75 if k == 0 else 0.25)
        arrow(kax, a1); arrow(a1, a2); arrow(a2, a3)
        pooled.append((a2, a3))
    # the next layer: a stack of feature maps, fed by both pooled maps
    stack = fig.add_axes([cols[5] - 0.035, 0.36, 0.07, 0.2]); stack.axis("off")
    for d in range(3):
        stack.add_patch(Rectangle((0.1 + 0.12 * d, 0.1 + 0.12 * d), 0.55, 0.55, facecolor="white", edgecolor=INK, linewidth=1.1))
    stack.set_xlim(0, 1); stack.set_ylim(0, 1)
    for k, (a2, a3) in enumerate(pooled):
        arrow(a3, stack, xb=0.12, yb=0.5)
    stack.text(0.5, -0.12, "next layer", ha="center", va="top", fontsize=18, color=INK)

    # receptive field of one pooled value of the first map: its 2x2 block after the ReLU, its 8x8 patch
    # of the input (7x7 kernel, 2x2 pooling), and the 22x22 patch a second such stage would see
    pj, pi = 7, 10
    a2, a3 = pooled[0]
    box = dict(fill=False, edgecolor=INK, linewidth=2.2)
    a3.add_patch(Rectangle((pi - 0.5, pj - 0.5), 1, 1, **box))
    a2.add_patch(Rectangle((2 * pi - 0.5, 2 * pj - 0.5), 2, 2, **box))
    inp.add_patch(Rectangle((2 * pi - 0.5, 2 * pj - 0.5), K + 1, K + 1, **box))
    inp.add_patch(Rectangle((2 * pi - 6.5, 2 * pj - 6.5), 22, 22, fill=False, edgecolor=INK, linewidth=1.6, linestyle="--"))
    inp.text(2 * pi + 4.5, 2 * pj - 7.5, "receptive field", ha="center", va="bottom", fontsize=15, color=INK,
             bbox=dict(facecolor="white", edgecolor="none", pad=1.5, alpha=0.85))

    # column labels and layer brackets
    labels = [(cols[0], r"input $\mathbf{x}$"), (cols[2], r"convolution $\mathbf{x} \circledast \omega_k$"),
              (cols[3], "ReLU"), (cols[4], r"max-pooling $\mathbf{o}_k$")]
    for cx, s in labels:
        fig.text(cx, ys[0] + S / 2 + 0.07, s, ha="center", va="center", fontsize=20, color=INK)
    def bracket(x0, x1, text):
        y = 0.035
        fig.add_artist(matplotlib.lines.Line2D([x0, x1], [y, y], color=GREY, linewidth=1.4))
        for xx in (x0, x1):
            fig.add_artist(matplotlib.lines.Line2D([xx, xx], [y, y + 0.025], color=GREY, linewidth=1.4))
        fig.text((x0 + x1) / 2, y - 0.012, text, ha="center", va="top", fontsize=18, color=GREY)
    half = S * asp / 2
    bracket(cols[1] - 0.04, cols[3] + half, "convolutional layer")
    bracket(cols[4] - S * 0.62 * asp / 2, cols[4] + S * 0.62 * asp / 2 + 0.02, "pooling layer")
    out = ROOT / "figures" / "lec7" / "nn-conv-pattern.svg"
    fig.savefig(out, bbox_inches="tight", transparent=True, metadata={"Date": None})
    plt.close(fig)
    print(out.relative_to(ROOT))

if __name__ == "__main__":
    svg("nn-terminology", 660, 450, terminology(), folder="lec7", scale=SCALE)
    svg("nn-shallow", 1210, 500, shallow_net(), folder="lec7", scale=SCALE)
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

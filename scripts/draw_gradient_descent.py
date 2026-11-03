"""Draw the logistic regression and gradient descent plots of lecture 7 in the style of the course.

    uv run python scripts/draw_gradient_descent.py

Writes to `figures/lec7/`:

- `sigmoid.svg`, the sigmoid σ(x) = 1 / (1 + exp(-x)) against the Heaviside step it smooths;
- `gd-0.svg` to `gd-7.svg`, eight steps of gradient descent on a one-dimensional loss L(θ) with two
  minima, from θ_0 = -0.5 with the learning rate α = 0.5: each frame shows L, its tangent at θ_t,
  the local approximation L̂(ε; θ_t) = L(θ_t) + ε L'(θ_t) + ε² / (2α), and its minimizer θ_{t+1}.

Text is set in Roboto and math in Computer Modern, as KaTeX on the slides; glyphs are saved as
paths, so the SVGs need no font. The frames share their axes and size, so that the deck can step
through them.
"""

import re
from pathlib import Path

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent

INK = "#2a2a2a"
GREY = "#8a8a8a"
BLUE = "#356aaf"
RED = "#c8463d"

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



# Every plot of the deck is shown at its natural size, without a width class, and has its width and
# height scaled by PLOT_SCALE: text and lines then have one size on every slide, the fonts being the same
# in points in every figure. (The network diagrams use SCALE, for the same reason.)
PLOT_SCALE = 0.6


def rescale(path):
    svg_text = path.read_text(encoding="utf-8")
    def fix(m):
        return f'{m.group(1)}="{float(m.group(2)) * PLOT_SCALE:.2f}pt"'
    i = svg_text.index("<svg")
    j = svg_text.index(">", i)
    tag = re.sub(r'(width|height)="([\d.]+)pt"', fix, svg_text[i:j])
    path.write_text(svg_text[:i] + tag + svg_text[j:], encoding="utf-8")

def save(fig, name, tight=True):
    out = ROOT / "figures" / "lec7" / f"{name}.svg"
    fig.savefig(out, bbox_inches="tight" if tight else None, transparent=True, metadata={"Date": None})
    rescale(out)
    plt.close(fig)
    print(out.relative_to(ROOT))


def sigmoid():
    x = np.linspace(-10, 10, 801)
    fig, ax = plt.subplots(figsize=(4.8, 4.8))
    ax.set_box_aspect(1)
    ax.plot([-10, 0, 0, 10], [0, 0, 1, 1], color=GREY, linewidth=1.6, linestyle="--")
    ax.plot(x, 1 / (1 + np.exp(-x)), color=BLUE)
    ax.text(3.2, 0.8, r"$\sigma(x)$", color=BLUE, fontsize=20)
    ax.text(-9.5, 0.08, "step", color=GREY, fontsize=15)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-0.05, 1.08)
    ax.set_yticks([0, 0.5, 1], ["0", "0.5", "1"])
    ax.set_xticks([-10, -5, 0, 5, 10])
    ax.set_xlabel(r"$x$", fontsize=20)
    save(fig, "sigmoid")


# A loss with a local maximum at 0 and two minima, near -3.36 and 4.4.
A, B, C = 0.0196, -0.0272, -0.58
ALPHA = 0.5


def loss(t):
    return A * t ** 4 + B * t ** 3 + C * t ** 2


def grad(t):
    return 4 * A * t ** 3 + 3 * B * t ** 2 + 2 * C * t


def descent(steps=8, start=-0.5):
    thetas = [start]
    for _ in range(steps - 1):
        thetas.append(thetas[-1] - ALPHA * grad(thetas[-1]))
    return thetas


def frame(t, theta):
    grid = np.linspace(-6, 6, 601)
    eps = np.linspace(-3.5, 3.5, 301)
    nxt = theta - ALPHA * grad(theta)
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    fig.subplots_adjust(left=0.1, right=0.97, bottom=0.14, top=0.88)
    ax.plot(grid, loss(grid), color=INK, label=r"$\mathcal{L}(\theta)$")
    tangent = theta + np.linspace(-3, 3, 2)
    ax.plot(tangent, loss(theta) + (tangent - theta) * grad(theta), color=GREY, linewidth=1.6, linestyle="--")
    ax.plot(theta + eps, loss(theta) + eps * grad(theta) + eps ** 2 / (2 * ALPHA), color=BLUE,
            label=r"$\hat{\mathcal{L}}(\epsilon; \theta_t)$")
    ax.plot([theta], [loss(theta)], "o", color=INK, markersize=8, zorder=3)
    ax.plot([nxt], [loss(theta) - ALPHA * grad(theta) ** 2 / 2], "o", color=RED, markersize=8, zorder=3)
    ax.plot([nxt, nxt], [loss(theta) - ALPHA * grad(theta) ** 2 / 2, loss(nxt)], color=RED, linewidth=1.2,
            linestyle=":")
    ax.set_xlim(-6, 6)
    ax.set_ylim(-8, 5)
    ax.set_xlabel(r"$\theta$", fontsize=20)
    ax.set_title(rf"$\theta_{t} = {theta:.2f}, \quad \alpha = {ALPHA:g}$", fontsize=20, color=INK)
    ax.legend(loc="upper right", frameon=False, fontsize=17)
    save(fig, f"gd-{t}", tight=False)


if __name__ == "__main__":
    sigmoid()
    for t, theta in enumerate(descent()):
        frame(t, theta)

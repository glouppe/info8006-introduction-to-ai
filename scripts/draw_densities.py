"""Draw the density plots of lecture 6 in the style of the course.

    uv run python scripts/draw_densities.py

Writes to `figures/lec6/`: `uniform.svg`, the densities of U(0, 3) and U(-2, 2); `normal.svg`, those
of N(0, 1) and N(1, 4), in the notation N(mu, sigma^2) of the slides; `mvn.svg`, the contours of a
bivariate Gaussian density. Same style and scale as the plots of lecture 5
(`draw_parameter_learning.py`, whose settings are reused): direct labels, math in Computer Modern.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import multivariate_normal, norm

from draw_parameter_learning import BLUE, INK, ROOT

RED = "#c8463d"
x = np.linspace(-5, 5, 1001)


def axes():
    fig, ax = plt.subplots(figsize=(7.5, 3.6))
    ax.set_xlim(-5, 5)
    ax.set_xlabel(r"$x$", fontsize=20)
    ax.set_ylabel(r"$p(x)$", fontsize=20)
    return fig, ax


def save(fig, name):
    out = ROOT / "figures" / "lec6" / f"{name}.svg"
    fig.savefig(out, bbox_inches="tight", transparent=True)
    plt.close(fig)
    print(out.relative_to(ROOT))


def uniform():
    fig, ax = axes()
    for (a, b), colour, (lx, ly, ha) in [((0, 3), RED, (3.15, 1 / 3, "left")), ((-2, 2), BLUE, (-2.15, 0.25, "right"))]:
        y = np.where((x >= a) & (x <= b), 1 / (b - a), 0)
        ax.plot(x, y, color=colour, drawstyle="steps-mid")
        ax.text(lx, ly, rf"$\mathcal{{U}}({a}, {b})$", ha=ha, va="center", color=INK, fontsize=17)
    ax.set_ylim(0, 0.4)
    save(fig, "uniform")


def normal():
    fig, ax = axes()
    for (mu, var), colour, (lx, ly, ha) in [((0, 1), RED, (0.6, 0.385, "left")), ((1, 4), BLUE, (2.9, 0.15, "left"))]:
        ax.plot(x, norm.pdf(x, mu, np.sqrt(var)), color=colour)
        ax.text(lx, ly, rf"$\mathcal{{N}}({mu}, {var})$", ha=ha, va="center", color=INK, fontsize=17)
    ax.set_ylim(0, 0.45)
    save(fig, "normal")


def mvn():
    fig, ax = plt.subplots(figsize=(4.6, 3.6))
    g = np.linspace(-4, 4, 401)
    X1, X2 = np.meshgrid(g, g)
    density = multivariate_normal([0, 0], [[1.0, 0.6], [0.6, 1.5]]).pdf(np.dstack([X1, X2]))
    blues = LinearSegmentedColormap.from_list("blues", ["#ffffff", "#c9d8ee", BLUE, "#1f3f6b"])
    levels = np.linspace(0.02, 1, 10) * density.max()
    ax.contourf(X1, X2, density, levels=levels, cmap=blues, extend="max")
    ax.contour(X1, X2, density, levels=levels, colors=INK, linewidths=0.4, alpha=0.5)
    ax.set_xlabel(r"$x_1$", fontsize=20)
    ax.set_ylabel(r"$x_2$", fontsize=20)
    ax.set_aspect("equal")
    ax.set_xticks([-4, -2, 0, 2, 4])
    ax.set_yticks([-4, -2, 0, 2, 4])
    save(fig, "mvn")


if __name__ == "__main__":
    uniform()
    normal()
    mvn()

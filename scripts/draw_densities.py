"""Draw the density plots of lecture 6 in the style of the course.

    uv run python scripts/draw_densities.py

Writes to `figures/lec6/`: `uniform.svg`, the densities of U(0, 3) and U(-2, 2); `normal.svg`, those
of N(0, 1) and N(1, 4), in the notation N(mu, sigma^2) of the slides; `mvn.svg`, the contours of a
bivariate Gaussian density; `gaussian-conditioning.svg`, a joint Gaussian of (x, y) with its two
marginals and the conditional p(x | y0) of a slice, to illustrate the Gaussian cheat sheet; and
`linear-gaussian.svg`, a Gaussian p(x), the conditionals p(y | x) around the line y = Hx + u, and the
joint and marginal p(y) they make, in the symbols mu, Sigma, H, u, R of the slides. Same style and scale as the plots of lecture 5
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


GREY = "#8a8a8a"
LIGHT = LinearSegmentedColormap.from_list("light", ["#ffffff", "#c9d8ee", "#7ea0cf"])


def joint_axes():
    """A square joint panel with a marginal panel above and one on the right."""
    fig = plt.figure(figsize=(6.4, 5.6))
    gs = fig.add_gridspec(2, 2, width_ratios=(4, 1.1), height_ratios=(1.1, 4), wspace=0.05, hspace=0.05)
    ax = fig.add_subplot(gs[1, 0])
    top = fig.add_subplot(gs[0, 0], sharex=ax)
    right = fig.add_subplot(gs[1, 1], sharey=ax)
    for a in (top, right):
        a.axis("off")
    return fig, ax, top, right


def gaussian_conditioning():
    """x = a + C/B (y - b) + e, with e independent of y: every slice has the same spread, only its centre moves."""
    a, b, A, B, C = 0.0, 0.0, 1.0, 1.0, 0.8
    fig, ax, top, right = joint_axes()
    g = np.linspace(-3.5, 3.5, 401)
    X, Y = np.meshgrid(g, g)
    joint = multivariate_normal([a, b], [[A, C], [C, B]]).pdf(np.dstack([X, Y]))
    levels = np.linspace(0.05, 1, 8) * joint.max()
    ax.contourf(X, Y, joint, levels=levels, cmap=LIGHT, extend="max")
    ax.contour(X, Y, joint, levels=levels, colors=INK, linewidths=0.4, alpha=0.4)
    ax.plot(a + C / B * (g - b), g, color=GREY, linestyle=":", linewidth=1.5)
    ax.text(-0.3, -3.25, r"$a + CB^{-1}(y - b)$", color=GREY, fontsize=15)
    var = A - C * C / B
    for y0 in (-1.6, 0.0, 1.6):
        mean = a + C / B * (y0 - b)
        bump = norm.pdf(g, mean, np.sqrt(var))
        keep = bump > 0.01
        ax.plot(g[keep], y0 + bump[keep], color=RED)
        ax.plot([g[keep][0], g[keep][-1]], [y0, y0], color=RED, linewidth=1)
    ax.text(1.75, 2.25, r"$p(x \mid y)$", color=RED, fontsize=16)
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-3.5, 3.5)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$", fontsize=20)
    ax.set_ylabel(r"$y$", fontsize=20)
    ax.set_xticks([])
    ax.set_yticks([])
    # the marginal of x, wider than every conditional: it adds the spread of the centres
    top.plot(g, norm.pdf(g, a, np.sqrt(A)), color=BLUE)
    top.plot(g, norm.pdf(g, a, np.sqrt(var)) * 0.62, color=RED, linewidth=1.2, linestyle="--")
    top.text(1.3, 0.3, r"$p(x) = \mathcal{N}(a, A)$", color=INK, fontsize=15)
    top.text(-3.4, 0.3, r"$A - CB^{-1}C^T$", color=RED, fontsize=14)
    top.set_ylim(0, 0.45)
    right.plot(norm.pdf(g, b, np.sqrt(B)), g, color=BLUE)
    right.text(0.03, -2.7, r"$p(y)$", color=INK, fontsize=15)
    right.set_xlim(0, 0.45)
    save(fig, "gaussian-conditioning")


def linear_gaussian():
    m, P, H, u, R = 0.0, 1.0, 1.0, 0.3, 1.0
    fig, ax, top, right = joint_axes()
    g = np.linspace(-3.5, 3.5, 401)
    X, Y = np.meshgrid(g, g)
    joint = multivariate_normal([m, H * m + u], [[P, P * H], [H * P, H * P * H + R]]).pdf(np.dstack([X, Y]))
    levels = np.linspace(0.05, 1, 8) * joint.max()
    ax.contourf(X, Y, joint, levels=levels, cmap=LIGHT, extend="max")
    ax.contour(X, Y, joint, levels=levels, colors=INK, linewidths=0.4, alpha=0.4)
    ax.plot(g, H * g + u, color=GREY, linestyle=":", linewidth=1.5)
    ax.text(-3.3, 3.0, r"$y = Hx + u$", color=GREY, fontsize=15)
    for x0 in (-1.5, 0.0, 1.5):
        bump = norm.pdf(g, H * x0 + u, np.sqrt(R))
        keep = bump > 0.05
        ax.plot(x0 + 1.1 * bump[keep], g[keep], color=RED)
        ax.plot([x0, x0], [g[keep][0], g[keep][-1]], color=RED, linewidth=1)
    ax.text(-3.3, 2.4, r"$p(y \mid x) = \mathcal{N}(Hx + u, R)$", color=RED, fontsize=15)
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-3.5, 3.5)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$", fontsize=20)
    ax.set_ylabel(r"$y$", fontsize=20)
    ax.set_xticks([])
    ax.set_yticks([])
    top.plot(g, norm.pdf(g, m, np.sqrt(P)), color=BLUE)
    top.text(1.3, 0.3, r"$p(x) = \mathcal{N}(\mu, \Sigma)$", color=INK, fontsize=15)
    top.set_ylim(0, 0.45)
    # p(x) pushed through the line, then widened by the independent noise
    right.plot(norm.pdf(g, H * m + u, np.sqrt(H * P * H)), g, color=GREY, linestyle="--", linewidth=1.5)
    right.plot(norm.pdf(g, H * m + u, np.sqrt(H * P * H + R)), g, color=BLUE)
    right.text(0.02, 3.0, r"$H\Sigma H^T$", color=GREY, fontsize=14)
    right.text(0.02, -3.2, r"$H\Sigma H^T + R$", color=BLUE, fontsize=14)
    right.set_xlim(0, 0.45)
    save(fig, "linear-gaussian")


if __name__ == "__main__":
    uniform()
    normal()
    mvn()
    gaussian_conditioning()
    linear_gaussian()

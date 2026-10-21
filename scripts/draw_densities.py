"""Draw the density plots of lecture 6 in the style of the course.

    uv run python scripts/draw_densities.py

Writes to `figures/lec6/`: `uniform.svg`, the densities of U(0, 3) and U(-2, 2); `normal.svg`, those
of N(0, 1) and N(1, 4), in the notation N(mu, sigma^2) of the slides; `walk.svg`, one step of the
1d Gaussian random walk (prior, prediction, update on e_1); `mvn.svg`, the contours of a
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
LIGHT = LinearSegmentedColormap.from_list("light", ["#ffffff", "#c9d8ee", "#7ea0cf"])


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


def walk():
    """One step of the 1d Gaussian random walk: prior, prediction, and update on the evidence e_1."""
    mu0, s0, sx, se, e1 = 0.0, 1.0, 2.0, 1.0, 2.0   # variances
    s1 = s0 + sx
    mu, var = (s1 * e1 + se * mu0) / (s1 + se), s1 * se / (s1 + se)
    fig, ax = axes()
    ax.plot(x, norm.pdf(x, mu0, np.sqrt(s0)), color=INK, linewidth=1.6)
    ax.plot(x, norm.pdf(x, mu0, np.sqrt(s1)), color=BLUE, linestyle="--")
    ax.plot(x, norm.pdf(x, mu, np.sqrt(var)), color=RED)
    ax.text(-1.15, 0.33, r"$p(x_0)$", ha="right", va="center", color=INK, fontsize=17)
    ax.text(-2.4, 0.16, r"$p(x_1)$", ha="right", va="center", color=BLUE, fontsize=17)
    ax.text(2.45, 0.33, r"$p(x_1 \mid e_1)$", ha="left", va="center", color=RED, fontsize=17)
    ax.axvline(e1, color=INK, linestyle="--", linewidth=1)   # the observation, as in gaussian_conditioning()
    ax.text(e1 + 0.1, 0.5, r"observed $e_1$", ha="left", va="center", color=GREY, fontsize=13, family="Roboto")
    ax.set_ylim(0, 0.52)
    save(fig, "walk")


def particle_filter():
    """One update cycle of a particle filter on the random walk of walk(): the particles x_0^i, moved by
    the transition model (elapse), weighted by the likelihood of e_1 (weight), and drawn again in
    proportion to their weights (resample). The exact densities of walk() are drawn faintly behind."""
    mu0, s0, sx, se, e1, n = 0.0, 1.0, 2.0, 1.0, 2.0, 20
    s1 = s0 + sx
    mu, var = (s1 * e1 + se * mu0) / (s1 + se), s1 * se / (s1 + se)
    rng = np.random.default_rng(3)
    x0 = rng.normal(mu0, np.sqrt(s0), n)
    x1 = x0 + rng.normal(0, np.sqrt(sx), n)
    w = norm.pdf(e1, x1, np.sqrt(se))
    w /= w.sum()
    picks = np.sort(rng.choice(n, n, p=w))
    rows = {"particles": 3, "elapse": 2, "weight": 1, "resample": 0}
    h, dy = 0.75, 0.09   # height of a density, spacing of stacked copies
    fig, ax = plt.subplots(figsize=(10, 5.6))
    for y in rows.values():
        ax.plot([-5, 5], [y, y], color=GREY, linewidth=0.8)
    def density(y, pdf, colour, **kw):
        ax.plot(x, y + h * pdf / 0.5, color=colour, linewidth=1.4, alpha=0.5, **kw)
    density(3, norm.pdf(x, mu0, np.sqrt(s0)), INK)
    density(2, norm.pdf(x, mu0, np.sqrt(s1)), BLUE, linestyle="--")
    density(1, norm.pdf(x, e1, np.sqrt(se)), GREY)
    density(0, norm.pdf(x, mu, np.sqrt(var)), RED)
    ax.text(-4.9, 3 + 0.45, r"$p(x_0)$", color=INK, fontsize=16)
    ax.text(-4.9, 2 + 0.45, r"$p(x_1)$", color=BLUE, fontsize=16)
    ax.text(-4.9, 1 + 0.45, r"$p(e_1 \mid x_1)$", color=GREY, fontsize=16)
    ax.text(-4.9, 0 + 0.45, r"$p(x_1 \mid e_1)$", color=RED, fontsize=16)
    # elapse: each particle moves by a sample of the transition model
    for a, b in zip(x0, x1):
        ax.plot([a, b], [3, 2], color=GREY, linewidth=0.6, alpha=0.7)
    # weight: the observation, and particles sized by their weights
    ax.plot([e1, e1], [0.9, 1.9], color=INK, linestyle="--", linewidth=1)
    ax.text(e1 + 0.1, 1.85, r"observed $e_1$", color=GREY, fontsize=13, family="Roboto", va="top")
    # resample: copies of the heavy particles, stacked
    count = {}
    for k in picks:
        c = count.get(k, 0)
        count[k] = c + 1
        ax.plot([x1[k], x1[k]], [1, dy * c], color=GREY, linewidth=0.6, alpha=0.7)
        ax.plot([x1[k]], [dy * c], "o", color=BLUE, markersize=6, zorder=3)
    ax.plot(x0, [3] * n, "o", color=BLUE, markersize=6, zorder=3, linestyle="none")
    ax.plot(x1, [2] * n, "o", color=BLUE, markersize=6, zorder=3, linestyle="none")
    ax.scatter(x1, [1] * n, s=1200 * w, color=BLUE, zorder=3)
    for name, y in rows.items():
        ax.text(-5.3, y + 0.05, name, ha="right", va="bottom", color=INK, fontsize=15, family="Roboto")
    ax.set_xlim(-5, 5)
    ax.set_ylim(-0.15, 3.85)
    ax.axis("off")
    save(fig, "particle-filter")


def mvn():
    fig, ax = plt.subplots(figsize=(4.6, 3.6))
    g = np.linspace(-3.5, 3.5, 401)   # the Gaussian of gaussian_conditioning(), drawn the same way
    X1, X2 = np.meshgrid(g, g)
    density = multivariate_normal([0, 0], [[1.0, 0.8], [0.8, 1.0]]).pdf(np.dstack([X1, X2]))
    levels = np.linspace(0.05, 1, 7) * density.max()
    ax.contourf(X1, X2, density, levels=levels, cmap=LIGHT, extend="max", alpha=0.8)
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-3.5, 3.5)
    ax.set_xlabel(r"$x_1$", fontsize=20)
    ax.set_ylabel(r"$x_2$", fontsize=20)
    ax.set_aspect("equal")
    ax.set_xticks([-2, 0, 2])
    ax.set_yticks([-2, 0, 2])
    save(fig, "mvn")


GREY = "#8a8a8a"


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


ORANGE = "#d9822b"   # the surprise, or the noise


def harrow(ax, x0, x1, y, colour, **kw):
    ax.annotate("", xy=(x1, y), xytext=(x0, y), arrowprops=dict(arrowstyle="-|>", color=colour, lw=2.2, shrinkA=0, shrinkB=0), **kw)


def varrow(ax, x, y0, y1, colour):
    ax.annotate("", xy=(x, y1), xytext=(x, y0), arrowprops=dict(arrowstyle="-|>", color=colour, lw=2.2, shrinkA=0, shrinkB=0))


def gaussian_conditioning():
    """Guess a, surprise y - b, correction CB^-1 (y - b); uncertainty A shrinks to A - CB^-1 C^T."""
    a, b, A, B, C, y0 = 0.0, 0.0, 1.0, 1.0, 0.8, 1.8
    xhat, var = a + C / B * (y0 - b), A - C * C / B
    fig, ax, top, right = joint_axes()
    g = np.linspace(-3.5, 3.5, 401)
    X, Y = np.meshgrid(g, g)
    joint = multivariate_normal([a, b], [[A, C], [C, B]]).pdf(np.dstack([X, Y]))
    levels = np.linspace(0.05, 1, 7) * joint.max()
    ax.contourf(X, Y, joint, levels=levels, cmap=LIGHT, extend="max", alpha=0.8)
    ax.plot([a], [b], marker="x", color=INK, markersize=10, mew=2)
    ax.text(a + 0.15, b - 0.45, r"$(a, b)$", color=INK, fontsize=16)
    # the observation and the surprise
    ax.axhline(y0, color=INK, linestyle="--", linewidth=1)
    ax.text(-3.35, y0 + 0.15, r"observed $y$", color=GREY, fontsize=13, family="Roboto")
    ax.plot([-3.5, 3.5], [b, b], color=GREY, linestyle=":", linewidth=1)
    varrow(ax, -2.6, b, y0, ORANGE)
    ax.text(-2.45, (b + y0) / 2, r"$y - b$", color=ORANGE, fontsize=17, va="center")
    # the correction of the guess a, proportional to the surprise
    ax.plot([a, a], [b, y0], color=GREY, linestyle=":", linewidth=1)
    harrow(ax, a, xhat, y0 - 0.05, BLUE)
    ax.text((a + xhat) / 2, y0 - 0.55, r"$CB^{-1}(y - b)$", color=BLUE, fontsize=16, ha="center")
    bump = norm.pdf(g, xhat, np.sqrt(var))
    keep = bump > 0.01
    ax.plot(g[keep], y0 + 0.9 * bump[keep], color=RED)
    ax.text(xhat + 0.5, y0 + 0.7, r"$p(x \mid y)$", color=RED, fontsize=16)
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-3.5, 3.5)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$", fontsize=20)
    ax.set_ylabel(r"$y$", fontsize=20)
    ax.set_xticks([])
    ax.set_yticks([])
    # the uncertainty about x, before and after observing y
    top.plot(g, norm.pdf(g, a, np.sqrt(A)), color=INK, linewidth=1.6)
    top.plot(g, norm.pdf(g, xhat, np.sqrt(var)), color=RED)
    top.text(-3.4, 0.3, r"$\mathcal{N}(a, A)$", color=INK, fontsize=15)
    top.text(xhat + 0.7, 0.5, r"$A - CB^{-1}C^T$", color=RED, fontsize=15)
    top.set_ylim(0, 0.7)
    right.plot(norm.pdf(g, b, np.sqrt(B)), g, color=INK, linewidth=1.6)
    right.text(0.03, -3.0, r"$\mathcal{N}(b, B)$", color=INK, fontsize=14)
    right.set_xlim(0, 0.45)
    save(fig, "gaussian-conditioning")


def linear_gaussian():
    """The mean of x carried through the line, its spread stretched by H, then widened by the noise R."""
    mu, S, H, u, R = 0.0, 0.5, 2.0, 0.3, 1.2
    s = np.sqrt(S)
    fig, ax, top, right = joint_axes()
    g = np.linspace(-3.5, 3.5, 401)
    ax.plot(g, H * g + u, color=GREY, linestyle=":", linewidth=1.5)
    ax.text(0.9, 3.0, r"$y = Hx + u$", color=GREY, fontsize=15, ha="right")
    # the mean, carried through the line
    ym = H * mu + u
    varrow(ax, mu, -3.5, ym, BLUE)
    harrow(ax, mu, 3.5, ym, BLUE)
    ax.text(2.0, ym + 0.2, r"$H\mu + u$", color=BLUE, fontsize=16)
    # one standard deviation of x, stretched by H
    for x0 in (mu - s, mu + s):
        ax.plot([x0, x0], [-3.5, H * x0 + u], color=BLUE, linewidth=0.8, alpha=0.6)
        ax.plot([x0, 3.5], [H * x0 + u] * 2, color=BLUE, linewidth=0.8, alpha=0.6)
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-3.5, 3.5)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$", fontsize=20)
    ax.set_ylabel(r"$y$", fontsize=20)
    ax.set_xticks([])
    ax.set_yticks([])
    top.plot(g, norm.pdf(g, mu, s), color=INK, linewidth=1.6)
    top.text(1.3, 0.3, r"$\mathcal{N}(\mu, \Sigma)$", color=INK, fontsize=15)
    top.set_ylim(0, 0.6)
    # the noise widens the stretched spread
    right.plot(norm.pdf(g, ym, np.sqrt(H * S * H)), g, color=BLUE, linewidth=1.6, linestyle="--")
    right.plot(norm.pdf(g, ym, np.sqrt(H * S * H + R)), g, color=ORANGE)
    right.text(0.12, 2.6, r"$H\Sigma H^T$", color=BLUE, fontsize=14)
    right.text(0.12, -2.8, r"$+\,R$", color=ORANGE, fontsize=16)
    right.set_xlim(0, 0.32)
    save(fig, "linear-gaussian")


if __name__ == "__main__":
    uniform()
    normal()
    walk()
    particle_filter()
    mvn()
    gaussian_conditioning()
    linear_gaussian()

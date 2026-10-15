"""Draw the parameter learning plots of lecture 5 in the style of the course.

    uv run python scripts/draw_parameter_learning.py

Writes three figures to `figures/lec5/`, for the candy example of case (a), where θ is the
fraction of cherry candies:

- `likelihood.svg`, the likelihood θ^c (1 - θ)^l after 1, 4 and 40 candies, rescaled to a maximum
  of 1, with the maximum likelihood estimate c / N;
- `beta-updates.svg`, the uniform prior Beta(θ | 1, 1) and the posteriors Beta(θ | 1 + c, 1 + l) after 1
  cherry, 7 out of 10 and 70 out of 100;
- `map.svg`, one cherry: the prior Beta(θ | 2, 2), the likelihood θ normalized to a density, the
  posterior Beta(θ | 3, 2), with the MLE (1) and the MAP estimate (2/3).

Text is set in Roboto and math in Computer Modern, as KaTeX on the slides; glyphs are saved as
paths, so the SVGs need no font.
"""

from pathlib import Path

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import beta

ROOT = Path(__file__).resolve().parent.parent

INK = "#2a2a2a"
GREY = "#8a8a8a"
BLUE = "#356aaf"
SHADES = ["#9fbbe0", "#5d8bc8", BLUE, "#1f3f6b"]   # light to dark, one hue

plt.rcParams.update({
    "font.family": "Roboto",
    "font.size": 15,
    "mathtext.fontset": "cm",
    "svg.fonttype": "path",
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

theta = np.linspace(0, 1, 501)


def axes(ylabel):
    fig, ax = plt.subplots(figsize=(7.5, 3.6))
    ax.set_xlim(0, 1)
    ax.set_xlabel(r"$\theta$", fontsize=20)
    ax.set_ylabel(ylabel)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1], ["0", "0.25", "0.5", "0.75", "1"])
    return fig, ax


def save(fig, name):
    out = ROOT / "figures" / "lec5" / f"{name}.svg"
    fig.savefig(out, bbox_inches="tight", transparent=True)
    plt.close(fig)
    print(out.relative_to(ROOT))


def likelihood():
    fig, ax = axes("likelihood")
    labels = {1: (0.97, 1.06, "right"), 4: (0.45, 0.55, "right"), 40: (0.6, 0.22, "right")}
    for (c, l), color in zip([(1, 0), (3, 1), (30, 10)], SHADES[:1] + SHADES[2:]):
        n = c + l
        like = theta ** c * (1 - theta) ** l
        ax.plot(theta, like / like.max(), color=color)
        ax.plot([c / n], [1], "o", color=color, markersize=8, zorder=3, clip_on=False)
        x, y, ha = labels[n]
        ax.text(x, y, f"$N = {n}$", ha=ha, color=INK, fontsize=17)
    ax.set_ylim(0, 1.15)
    ax.set_yticks([])   # each curve is rescaled to a maximum of 1: their values are not comparable
    save(fig, "likelihood")


def beta_updates():
    fig, ax = axes("density")
    ax.plot(theta, beta.pdf(theta, 1, 1), color=GREY, linestyle="--")
    ax.text(0.03, 1.3, "prior", ha="left", color=GREY, fontsize=15)
    labels = {1: (0.97, 2.35, "right"), 10: (0.47, 2.6, "right"), 100: (0.64, 7.5, "right")}
    for (c, l), color in zip([(1, 0), (7, 3), (70, 30)], SHADES[:1] + SHADES[2:]):
        n = c + l
        ax.plot(theta, beta.pdf(theta, 1 + c, 1 + l), color=color)
        x, y, ha = labels[n]
        ax.text(x, y, f"$N = {n}$", ha=ha, color=INK, fontsize=17)
    ax.axvline(0.7, color=INK, linewidth=0.8, linestyle=":")
    ax.set_ylim(0, 10)
    ax.set_yticks([])
    save(fig, "beta-updates")


def map_estimate():
    fig, ax = axes("density")
    prior, like, post = beta.pdf(theta, 2, 2), 2 * theta, beta.pdf(theta, 3, 2)
    ax.plot(theta, prior, color=GREY, linestyle="--")
    ax.plot(theta, like, color=SHADES[0])
    ax.plot(theta, post, color=BLUE)
    ax.annotate("prior", (0.2, beta.pdf(0.2, 2, 2)), xytext=(-6, 6), textcoords="offset points", ha="right",
                color=GREY, fontsize=15)
    ax.annotate("likelihood", (0.93, 1.86), xytext=(-8, 0), textcoords="offset points", ha="right", va="center",
                color=INK, fontsize=15)
    ax.text(0.93, 1.25, "posterior", ha="left", color=INK, fontsize=15)
    ax.plot([1], [2], "o", color=SHADES[0], markersize=8, zorder=3, clip_on=False)
    ax.plot([2 / 3], [beta.pdf(2 / 3, 3, 2)], "o", color=BLUE, markersize=8, zorder=3)
    ax.annotate("MLE", (1, 2), xytext=(0, 10), textcoords="offset points", ha="center", color=INK, fontsize=15)
    ax.annotate("MAP", (2 / 3, beta.pdf(2 / 3, 3, 2)), xytext=(0, 10), textcoords="offset points", ha="center",
                color=INK, fontsize=15)
    ax.set_ylim(0, 2.4)
    save(fig, "map")


if __name__ == "__main__":
    likelihood()
    beta_updates()
    map_estimate()

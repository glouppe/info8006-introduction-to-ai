"""Corner plots for the Kalman notebook, with numpy, scipy and matplotlib only.

    from plots import corner, mark_point

`corner` shows the marginals of a sample: the histogram of each variable on the
diagonal, and the credible regions of each pair below it. `mark_point` draws a
point across the panels of such a figure. They replace `lampe.plots`, which the
notebook used to import.
"""

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.patches import Patch
from scipy.ndimage import gaussian_filter

CREDS = (0.6827, 0.9545, 0.9973)  # 1, 2 and 3 standard deviations


def _column(data):
    data = np.asarray(data)
    return data[:, None] if data.ndim == 1 else data


def _levels(hist, creds):
    """The histogram values enclosing the given fractions of the total mass."""
    flat = np.sort(hist.flatten())[::-1]
    cdf = np.cumsum(flat) / flat.sum()
    return [flat[np.searchsorted(cdf, c)] for c in reversed(creds)]


def corner(data, bins=64, smooth=None, labels=None, figsize=(6.4, 6.4), color="C0", creds=CREDS):
    """The marginals of a sample of shape (n, d), as a lower triangular grid of panels."""
    data = _column(data)
    d = data.shape[1]
    bounds = [(x.min(), x.max()) for x in data.T]

    figure, axs = plt.subplots(d, d, figsize=figsize, squeeze=False, sharex="col")
    shades = [(*plt.matplotlib.colors.to_rgb(color), a) for a in (0.2, 0.4, 0.6)]

    for i in range(d):
        for j in range(d):
            ax = axs[i, j]

            if j > i:
                ax.set_axis_off()
                continue

            if i == j:
                hist, edges = np.histogram(data[:, i], bins=bins, range=bounds[i], density=True)
                if smooth:
                    hist = gaussian_filter(hist, smooth)
                ax.plot((edges[:-1] + edges[1:]) / 2, hist, color=color)
                ax.set_ylim(bottom=0)
                ax.set_yticks([])
            else:
                hist, ex, ey = np.histogram2d(data[:, j], data[:, i], bins=bins,
                                              range=[bounds[j], bounds[i]])
                if smooth:
                    hist = gaussian_filter(hist, smooth)
                x, y = (ex[:-1] + ex[1:]) / 2, (ey[:-1] + ey[1:]) / 2
                levels = _levels(hist, creds)
                ax.contourf(x, y, hist.T, levels=[*levels, hist.max()], colors=shades)
                ax.contour(x, y, hist.T, levels=levels, colors=color, linewidths=1)
                ax.set_ylim(*bounds[i])
                if j > 0:
                    ax.sharey(axs[i, 0])
                    ax.tick_params(labelleft=False)

            ax.set_xlim(*bounds[j])
            if i < d - 1:
                ax.tick_params(labelbottom=False)
            else:
                ax.tick_params(axis="x", rotation=45)
                if labels is not None:
                    ax.set_xlabel(labels[j])
            if labels is not None and j == 0 and i > 0:
                ax.set_ylabel(labels[i])

    figure.align_labels()
    figure.tight_layout()

    handles = [Patch(color=str(1 - a)) for a in (0.2, 0.4, 0.6)]
    figure.legend(handles, [f"{100 * c:.1f} %" for c in reversed(creds)],
                  loc="upper right", bbox_to_anchor=(0.98, 0.98), frameon=False)

    return figure


def mark_point(figure, x, color="k", linestyle="dashed"):
    """Draw the point x on every panel of a corner figure, without moving the limits."""
    x = np.asarray(x).flatten()
    d = len(x)
    axs = np.asarray(figure.axes[:d * d]).reshape(d, d)

    for i in range(d):
        for j in range(i + 1):
            ax = axs[i, j]
            xlim, ylim = ax.get_xlim(), ax.get_ylim()
            ax.axvline(x[j], color=color, linestyle=linestyle)
            if i != j:
                ax.axhline(x[i], color=color, linestyle=linestyle)
                ax.plot(x[j], x[i], color=color, marker="s", markersize=4)
            ax.set_xlim(*xlim)
            ax.set_ylim(*ylim)

    return figure

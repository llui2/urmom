"""Finite-size reversible-accessibility transition on random genotype cubes."""

from math import erf
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).with_suffix(".pdf")
SEED = 20261006
BETA = np.linspace(0, 0.8, 121)
SETTINGS = ((6, 400), (8, 300), (10, 200), (12, 120))


def hypercube_edges(L):
    n = 2**L
    i = np.repeat(np.arange(n, dtype=np.int32), L)
    bit = np.tile(1 << np.arange(L, dtype=np.int32), n)
    j = i ^ bit
    keep = i < j
    return i[keep], j[keep]


def component_curves(L, repeats, rng):
    """Largest reversible component for an ensemble of Gaussian landscapes."""
    i, j = hypercube_edges(L)
    n = 2**L
    values = np.zeros((repeats, len(BETA)))

    for r in range(repeats):
        g = rng.normal(size=n)
        threshold = np.abs(g[i] - g[j])
        order = np.argsort(threshold)

        parent = np.arange(n, dtype=np.int32)
        size = np.ones(n, dtype=np.int32)
        largest = 1
        pos = 0

        def root(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        for k, beta in enumerate(BETA):
            while pos < len(order) and threshold[order[pos]] < beta:
                edge = order[pos]
                a = root(int(i[edge]))
                b = root(int(j[edge]))

                if a != b:
                    if size[a] < size[b]:
                        a, b = b, a
                    parent[b] = a
                    size[a] += size[b]
                    largest = max(largest, int(size[a]))

                pos += 1

            values[r, k] = largest / n

    return values


rng = np.random.default_rng(SEED)
data = {}

for L, repeats in SETTINGS:
    values = component_curves(L, repeats, rng)
    c = np.array([L * erf(beta / 2) for beta in BETA])
    data[L] = {
        "c": c,
        "mean": values.mean(axis=0),
        "sem": values.std(axis=0) / np.sqrt(repeats),
        "prob": (values > 0.5).mean(axis=0),
    }

plt.rcParams.update({
    "font.family": "serif",
    "mathtext.fontset": "cm",
    "font.size": 9,
    "axes.labelsize": 10,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
})

fig, axes = plt.subplots(1, 2, figsize=(6.4, 2.5), sharex=True)

for L, _ in SETTINGS:
    curve = data[L]
    line = axes[0].plot(
        curve["c"],
        curve["mean"],
        lw=1.6,
        label=rf"$L={L}$",
    )[0]
    axes[0].fill_between(
        curve["c"],
        curve["mean"] - curve["sem"],
        curve["mean"] + curve["sem"],
        color=line.get_color(),
        alpha=0.12,
        linewidth=0,
    )
    axes[1].plot(
        curve["c"],
        curve["prob"],
        lw=1.6,
        color=line.get_color(),
    )

for ax in axes:
    ax.set_xlim(0, 2.8)
    ax.set_ylim(-0.03, 1.04)
    ax.set_xlabel(r"mean reversible degree $c$")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

axes[0].set_ylabel(r"largest fraction $S$")
axes[1].set_ylabel(r"$P(S>1/2)$")
axes[0].legend(frameon=False, loc="lower right")
axes[0].text(-0.12, 1.03, "(a)", transform=axes[0].transAxes, fontsize=10)
axes[1].text(-0.12, 1.03, "(b)", transform=axes[1].transAxes, fontsize=10)

fig.subplots_adjust(left=0.095, right=0.99, bottom=0.21, top=0.92, wspace=0.28)
fig.savefig(OUT, bbox_inches="tight")
plt.close(fig)

print("L, repeats:", SETTINGS)
print(OUT)

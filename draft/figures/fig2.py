"""Local bridge opening and finite-size reversible-accessibility transition."""

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

# Schematic three-bit landscape. Each square face is internally reversible
# below beta_c = 0.45; the edge 000--100 is the first bridge between them.
g_small = np.array([0.00, 0.10, 0.20, 0.30, 0.45, 0.70, 0.75, 0.82])
i3, j3 = hypercube_edges(3)
threshold3 = np.abs(g_small[i3] - g_small[j3])
cube_xy = np.array([
    [0.00, 0.00],
    [1.00, 0.00],
    [0.00, 1.00],
    [1.00, 1.00],
    [0.38, 0.30],
    [1.38, 0.30],
    [0.38, 1.30],
    [1.38, 1.30],
])
bridge = (0, 4)

assert np.isclose(abs(g_small[0] - g_small[4]), 0.45)
assert all(
    abs(g_small[i] - g_small[j]) < 0.45
    for i, j in [(0, 1), (0, 2), (1, 3), (2, 3)]
)
assert all(
    abs(g_small[i] - g_small[j]) < 0.45
    for i, j in [(4, 5), (4, 6), (5, 7), (6, 7)]
)

plt.rcParams.update({
    "font.family": "serif",
    "mathtext.fontset": "cm",
    "font.size": 9,
    "axes.labelsize": 10,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
})

fig = plt.figure(figsize=(6.4, 2.35))
grid = fig.add_gridspec(1, 3, width_ratios=[1.32, 1, 1], wspace=0.35)
ax0 = fig.add_subplot(grid[0, 0])
ax1 = fig.add_subplot(grid[0, 1])
ax2 = fig.add_subplot(grid[0, 2], sharex=ax1)

for beta, dx in ((0.44, 0.0), (0.46, 1.90)):
    xy = cube_xy.copy()
    xy[:, 0] += dx

    for i, j, threshold in zip(i3, j3, threshold3):
        active = beta > threshold
        is_bridge = (int(i), int(j)) == bridge
        ax0.plot(
            [xy[i, 0], xy[j, 0]],
            [xy[i, 1], xy[j, 1]],
            lw=2.3 if active and is_bridge else (1.45 if active else 0.75),
            color="0.05" if active else "0.84",
            zorder=1,
        )

    ax0.scatter(
        xy[:4, 0],
        xy[:4, 1],
        s=20,
        facecolor="0.15",
        edgecolor="0.15",
        zorder=3,
    )
    ax0.scatter(
        xy[4:, 0],
        xy[4:, 1],
        s=20,
        facecolor="white" if beta < 0.45 else "0.15",
        edgecolor="0.15",
        linewidth=0.8,
        zorder=3,
    )

    relation = "<" if beta < 0.45 else ">"
    ax0.text(
        dx + 0.69,
        -0.33,
        rf"$\beta {relation} \beta_c$",
        ha="center",
    )

ax0.set_xlim(-0.15, 3.40)
ax0.set_ylim(-0.46, 1.48)
ax0.set_aspect("equal")
ax0.axis("off")
ax0.text(-0.03, 1.02, "(a)", transform=ax0.transAxes, fontsize=10)

for L, _ in SETTINGS:
    curve = data[L]
    line = ax1.plot(
        curve["c"],
        curve["mean"],
        lw=1.45,
        label=rf"$L={L}$",
    )[0]
    ax1.fill_between(
        curve["c"],
        curve["mean"] - curve["sem"],
        curve["mean"] + curve["sem"],
        color=line.get_color(),
        alpha=0.12,
        linewidth=0,
    )
    ax2.plot(
        curve["c"],
        curve["prob"],
        lw=1.45,
        color=line.get_color(),
    )

for ax in (ax1, ax2):
    ax.set_xlim(0, 2.8)
    ax.set_ylim(-0.03, 1.04)
    ax.set_xlabel(r"mean reversible degree $c$")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

ax1.set_ylabel(r"largest fraction $S$")
ax2.set_ylabel(r"$P(S>1/2)$")
ax1.legend(frameon=False, loc="lower right", handlelength=1.7)
ax1.text(-0.20, 1.02, "(b)", transform=ax1.transAxes, fontsize=10)
ax2.text(-0.20, 1.02, "(c)", transform=ax2.transAxes, fontsize=10)

fig.subplots_adjust(left=0.03, right=0.99, bottom=0.22, top=0.92, wspace=0.35)
fig.savefig(OUT, bbox_inches="tight")
plt.close(fig)

print("schematic beta_c = 0.450")
print("L, repeats:", SETTINGS)
print(OUT)

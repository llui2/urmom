"""Minimal reversible-accessibility transition on a three-bit genotype cube."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).with_suffix(".pdf")
L = 3
N = 2**L

# Two internally connected four-node components separated by one bridge.
g = np.array([0.00, 0.10, 0.20, 0.30, 0.45, 0.70, 0.75, 0.82])
BETA_C = 0.45

i = np.repeat(np.arange(N, dtype=np.int32), L)
bit = np.tile(1 << np.arange(L, dtype=np.int32), N)
j = i ^ bit
keep = i < j
i = i[keep]
j = j[keep]
threshold = np.abs(g[i] - g[j])

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


def largest_fraction(beta):
    parent = np.arange(N, dtype=np.int32)
    size = np.ones(N, dtype=np.int32)
    largest = 1

    def root(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for u, v, edge_threshold in zip(i, j, threshold):
        if beta <= edge_threshold:
            continue

        a = root(int(u))
        b = root(int(v))

        if a != b:
            if size[a] < size[b]:
                a, b = b, a
            parent[b] = a
            size[a] += size[b]
            largest = max(largest, int(size[a]))

    return largest / N


assert np.isclose(abs(g[0] - g[4]), BETA_C)
assert largest_fraction(0.44) == 0.5
assert largest_fraction(0.46) == 1.0

plt.rcParams.update({
    "font.family": "serif",
    "mathtext.fontset": "cm",
    "font.size": 9,
    "axes.labelsize": 10,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
})

fig, axes = plt.subplots(
    1,
    2,
    figsize=(6.4, 2.45),
    gridspec_kw={"width_ratios": [1.35, 1]},
)

ax = axes[0]

for beta, dx in ((0.44, 0.0), (0.46, 1.95)):
    xy = cube_xy.copy()
    xy[:, 0] += dx

    for u, v, edge_threshold in zip(i, j, threshold):
        active = beta > edge_threshold
        is_bridge = (int(u), int(v)) == bridge

        ax.plot(
            [xy[u, 0], xy[v, 0]],
            [xy[u, 1], xy[v, 1]],
            lw=2.5 if active and is_bridge else (1.6 if active else 0.8),
            color="0.05" if active else "0.84",
            zorder=1,
        )

    ax.scatter(
        xy[:4, 0],
        xy[:4, 1],
        s=22,
        facecolor="0.15",
        edgecolor="0.15",
        zorder=3,
    )
    ax.scatter(
        xy[4:, 0],
        xy[4:, 1],
        s=22,
        facecolor="white" if beta < BETA_C else "0.15",
        edgecolor="0.15",
        linewidth=0.8,
        zorder=3,
    )

    relation = "<" if beta < BETA_C else ">"
    ax.text(
        dx + 0.69,
        -0.34,
        rf"$\beta {relation} \beta_c$",
        ha="center",
    )

ax.set_xlim(-0.15, 3.48)
ax.set_ylim(-0.47, 1.50)
ax.set_aspect("equal")
ax.axis("off")
ax.text(-0.03, 1.02, "(a)", transform=ax.transAxes, fontsize=10)

ax = axes[1]
beta = np.linspace(0, 0.8, 1601)
S = np.array([largest_fraction(value) for value in beta])

ax.step(beta, S, where="post", lw=1.8, color="0.15")
ax.axvline(BETA_C, ls="--", lw=1.0, color="0.45")
ax.text(
    BETA_C + 0.015,
    0.17,
    r"$\beta_c=0.45$",
    rotation=90,
    va="bottom",
)
ax.set_xlim(0, 0.8)
ax.set_ylim(0.08, 1.04)
ax.set_xlabel(r"coupling strength $\beta$")
ax.set_ylabel(r"largest fraction $S$")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.text(-0.16, 1.02, "(b)", transform=ax.transAxes, fontsize=10)

fig.subplots_adjust(left=0.04, right=0.99, bottom=0.22, top=0.92, wspace=0.28)
fig.savefig(OUT, bbox_inches="tight")
plt.close(fig)

print("beta_c = 0.450")
print("S: 0.5 -> 1")
print(OUT)

"""Collective accessibility transition on the three-bit landscape of Fig. 1."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).with_suffix(".pdf")

L = 3
N = 2**L

labels = [format(i, f"0{L}b") for i in range(N)]
sequences = np.array([[int(bit) for bit in label] for label in labels])
distance = np.sum(sequences[:, None, :] != sequences[None, :, :], axis=2)

# Same intrinsic landscape and nearest-neighbor coupling as Fig. 1.
g = np.array([1.00, 0.80, 0.20, 1.05, 0.10, 0.30, 0.60, 1.30])
edges = [
    (i, j)
    for i in range(N)
    for j in range(i + 1, N)
    if distance[i, j] == 1
]
threshold = {(i, j): abs(g[i] - g[j]) for i, j in edges}

# A compact 2D projection of the three-cube.
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


def invasion_matrix(beta):
    """Directed rare-mutant accessibility matrix."""
    adjacency = np.zeros((N, N), dtype=bool)

    for i, j in edges:
        if g[j] - g[i] + beta > 0:
            adjacency[i, j] = True
        if g[i] - g[j] + beta > 0:
            adjacency[j, i] = True

    return adjacency


def largest_scc_size(beta):
    """Largest strongly connected component from Boolean transitive closure."""
    reach = invasion_matrix(beta) | np.eye(N, dtype=bool)

    for k in range(N):
        reach |= reach[:, [k]] & reach[[k], :]

    mutual = reach & reach.T
    return int(mutual.sum(axis=1).max())


def reversible_edge_count(beta):
    return sum(beta > threshold[edge] for edge in edges)


def segmented_xy(xy, selected_edges):
    x, y = [], []

    for i, j in selected_edges:
        x.extend([xy[i, 0], xy[j, 0], np.nan])
        y.extend([xy[i, 1], xy[j, 1], np.nan])

    return x, y


assert largest_scc_size(0.499999) == 4
assert largest_scc_size(0.500001) == 8
assert reversible_edge_count(0.500001) == 7

plt.rcParams.update({
    "font.family": "serif",
    "mathtext.fontset": "cm",
    "font.size": 9,
    "axes.labelsize": 10,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
})

fig, axes = plt.subplots(1, 2, figsize=(6.4, 2.55))

ax = axes[0]
snapshots = (0.0, 0.30, 0.55)
offsets = (0.0, 1.82, 3.64)

for beta, dx in zip(snapshots, offsets):
    ax.set_prop_cycle(None)
    xy = cube_xy.copy()
    xy[:, 0] += dx

    reversible = [edge for edge in edges if beta > threshold[edge]]
    one_way = [edge for edge in edges if edge not in reversible]

    x, y = segmented_xy(xy, one_way)
    ax.plot(x, y, lw=0.8, alpha=0.16)

    x, y = segmented_xy(xy, reversible)
    if reversible:
        ax.plot(x, y, lw=2.0)

    ax.scatter(xy[:, 0], xy[:, 1], s=20, zorder=3)
    ax.text(dx + 0.69, -0.34, rf"$\beta={beta:g}$", ha="center")

ax.set_xlim(-0.20, 5.22)
ax.set_ylim(-0.47, 1.52)
ax.set_aspect("equal")
ax.axis("off")
ax.text(-0.04, 1.04, "(a)", transform=ax.transAxes, fontsize=10)

ax = axes[1]
beta = np.linspace(0, 1.05, 2101)
largest = np.array([largest_scc_size(value) for value in beta])
reversible = np.array([reversible_edge_count(value) for value in beta])

ax.step(beta, largest, where="post", lw=1.8, label="largest SCC")
ax.step(beta, reversible, where="post", lw=1.5, label="reversible edges")
ax.axvline(0.5, ls="--", lw=1.0)
ax.text(0.515, 1.35, r"$\beta_c=0.5$", rotation=90, va="bottom")
ax.set_xlim(0, 1.05)
ax.set_ylim(0, 12.4)
ax.set_xlabel(r"coupling strength $\beta$")
ax.set_ylabel("count")
ax.set_yticks([0, 2, 4, 6, 8, 10, 12])
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(frameon=False, loc="upper left")
ax.text(-0.12, 1.04, "(b)", transform=ax.transAxes, fontsize=10)

fig.subplots_adjust(left=0.035, right=0.99, bottom=0.21, top=0.91, wspace=0.25)
fig.savefig(OUT, bbox_inches="tight")
plt.close(fig)

print("beta_c = 0.500")
print("largest SCC: 4 -> 8")
print("reversible edges at transition: 7 / 12")
print(OUT)

"""Collective accessibility transition on the three-bit landscape of Fig. 1."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).with_suffix(".pdf")

L = 3
N = 2**L

sequences = np.array(
    [[int(bit) for bit in format(i, f"0{L}b")] for i in range(N)]
)
distance = np.sum(
    sequences[:, None, :] != sequences[None, :, :],
    axis=2,
)

# Same intrinsic landscape and nearest-neighbor coupling as Fig. 1.
# g_110 = 0.61 separates two otherwise degenerate edge thresholds.
g = np.array([1.00, 0.80, 0.20, 1.05, 0.10, 0.30, 0.61, 1.30])
edges = [
    (i, j)
    for i in range(N)
    for j in range(i + 1, N)
    if distance[i, j] == 1
]
threshold = {(i, j): abs(g[i] - g[j]) for i, j in edges}

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
        adjacency[i, j] = g[j] - g[i] + beta > 0
        adjacency[j, i] = g[i] - g[j] + beta > 0

    return adjacency


def strong_components(beta):
    """Strongly connected components from Boolean transitive closure."""
    reach = invasion_matrix(beta) | np.eye(N, dtype=bool)

    for k in range(N):
        reach |= reach[:, [k]] & reach[[k], :]

    mutual = reach & reach.T
    unseen = set(range(N))
    components = []

    while unseen:
        i = min(unseen)
        component = set(np.flatnonzero(mutual[i]))
        unseen -= component
        components.append(component)

    return sorted(
        components,
        key=lambda component: (len(component), -min(component)),
        reverse=True,
    )


def largest_scc_size(beta):
    return len(strong_components(beta)[0])


def segmented_xy(xy, selected_edges):
    x, y = [], []

    for i, j in selected_edges:
        x.extend([xy[i, 0], xy[j, 0], np.nan])
        y.extend([xy[i, 1], xy[j, 1], np.nan])

    return x, y


assert [len(component) for component in strong_components(0.49)] == [4, 2, 2]
assert largest_scc_size(0.501) == 8
assert threshold[(1, 5)] == 0.5
assert threshold[(4, 6)] == 0.51

plt.rcParams.update({
    "font.family": "serif",
    "mathtext.fontset": "cm",
    "font.size": 9,
    "axes.labelsize": 10,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
})

fig, axes = plt.subplots(1, 2, figsize=(6.4, 2.45))

ax = axes[0]
snapshots = (0.49, 0.501)
offsets = (0.0, 1.95)
bridge = (1, 5)

for beta, dx in zip(snapshots, offsets):
    xy = cube_xy.copy()
    xy[:, 0] += dx

    reversible = [edge for edge in edges if beta > threshold[edge]]
    one_way = [edge for edge in edges if edge not in reversible]

    x, y = segmented_xy(xy, one_way)
    ax.plot(x, y, lw=0.8, color="0.82", zorder=1)

    x, y = segmented_xy(xy, reversible)
    ax.plot(x, y, lw=1.7, color="0.30", zorder=2)

    if beta > threshold[bridge]:
        x, y = segmented_xy(xy, [bridge])
        ax.plot(x, y, lw=2.6, color="0.08", zorder=3)

    ax.scatter(
        xy[:, 0],
        xy[:, 1],
        s=18,
        facecolor="white",
        edgecolor="0.55",
        linewidth=0.8,
        zorder=4,
    )

    largest = strong_components(beta)[0]
    ids = sorted(largest)
    ax.scatter(
        xy[ids, 0],
        xy[ids, 1],
        s=25,
        facecolor="0.18",
        edgecolor="0.18",
        linewidth=0.8,
        zorder=5,
    )

    relation = "<" if beta < 0.5 else ">"
    ax.text(
        dx + 0.69,
        -0.34,
        rf"$\beta {relation} \beta_c$",
        ha="center",
    )

ax.set_xlim(-0.16, 3.48)
ax.set_ylim(-0.47, 1.50)
ax.set_aspect("equal")
ax.axis("off")
ax.text(-0.04, 1.02, "(a)", transform=ax.transAxes, fontsize=10)

ax = axes[1]
beta = np.linspace(0, 1.05, 2101)
largest = np.array([largest_scc_size(value) for value in beta])

ax.step(beta, largest, where="post", lw=1.8, color="0.15")
ax.axvline(0.5, ls="--", lw=1.0, color="0.45")
ax.text(
    0.515,
    1.30,
    r"$\beta_c=0.5$",
    rotation=90,
    va="bottom",
)
ax.set_xlim(0, 1.05)
ax.set_ylim(0.7, 8.45)
ax.set_xlabel(r"coupling strength $\beta$")
ax.set_ylabel(r"largest component $S_{\max}$")
ax.set_yticks([1, 2, 4, 8])
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.text(-0.13, 1.02, "(b)", transform=ax.transAxes, fontsize=10)

fig.subplots_adjust(
    left=0.04,
    right=0.99,
    bottom=0.22,
    top=0.92,
    wspace=0.30,
)
fig.savefig(OUT, bbox_inches="tight")
plt.close(fig)

print("beta_c = 0.500")
print("S_max: 4 -> 8")
print("next edge threshold = 0.510")
print(OUT)

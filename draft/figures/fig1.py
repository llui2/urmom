"""Illustrative mutation-selection trajectories with frequency-dependent fitness."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).with_suffix(".pdf")

L = 3
N = 2**L
T = 120
MU = 1e-3
ETA = 1.5
BETAS = (0.0, 0.4)

labels = [format(i, f"0{L}b") for i in range(N)]
sequences = np.array([[int(bit) for bit in label] for label in labels])
distance = np.sum(sequences[:, None, :] != sequences[None, :, :], axis=2)

# One fixed illustrative landscape: 000 is a local peak and 111 is the global peak.
g = np.array([1.00, 0.80, 0.20, 1.05, 0.10, 0.30, 0.60, 1.30])

Q = np.zeros((N, N))
for i in range(N):
    Q[i, i] = 1.0 - MU
    Q[i, distance[i] == 1] = MU / L

# Nearest-neighbor fitness coupling: a_0 = 0, a_1 = 1, a_{d>1} = 0.
a = np.array([0.0, 1.0, 0.0, 0.0])
A = a[distance]


def simulate(beta):
    p = np.zeros(N)
    p[0] = 1.0
    history = [p.copy()]

    for _ in range(T):
        f = g + beta * (A @ p)
        weight = p * np.exp(ETA * f)
        p = (weight / weight.sum()) @ Q
        history.append(p.copy())

    return np.asarray(history)


trajectories = [simulate(beta) for beta in BETAS]
assert np.allclose(Q.sum(axis=1), 1.0)
assert all(np.allclose(history.sum(axis=1), 1.0) for history in trajectories)

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.labelsize": 10,
    "legend.fontsize": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
})

fig, axes = plt.subplots(1, 2, figsize=(6.7, 2.7), sharex=True, sharey=True)
path = [0, 1, 3, 7]

for ax, beta, history in zip(axes, BETAS, trajectories):
    for i in path:
        ax.plot(range(T + 1), history[:, i], lw=1.5, label=labels[i])
    ax.set_xlim(0, T)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("generation $t$")
    ax.spines[["top", "right"]].set_visible(False)
    ax.text(0.04, 0.92, rf"$\beta = {beta:g}$", transform=ax.transAxes)

axes[0].set_ylabel("frequency $p_i(t)$")
axes[0].text(
    -0.13, 1.02, "a", transform=axes[0].transAxes,
    fontweight="bold", fontfamily="sans-serif",
)
axes[1].text(
    -0.13, 1.02, "b", transform=axes[1].transAxes,
    fontweight="bold", fontfamily="sans-serif",
)
axes[1].legend(frameon=False, ncol=2, loc="upper right")

fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight")
plt.close(fig)

beta_escape = (g[0] - g[1]) / (a[1] - a[0])
print(f"beta_escape(000 -> 001) = {beta_escape:.3f}")
print(OUT)

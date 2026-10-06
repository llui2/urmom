"""Illustrative mutation-selection trajectories with frequency-dependent fitness."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).with_suffix(".pdf")

L = 3
N = 2**L
T = 140
MU = 1e-3
ETA = 1.5
BETAS = (0.0, 0.4)

labels = [format(i, f"0{L}b") for i in range(N)]
sequences = np.array([[int(bit) for bit in label] for label in labels])
distance = np.sum(sequences[:, None, :] != sequences[None, :, :], axis=2)

# Fixed illustrative landscape.
# 000 is a local peak, 111 is the global peak, and 001 is intrinsically worse than 000.
g = np.array([1.00, 0.80, 0.20, 1.05, 0.10, 0.30, 0.60, 1.30])

# Mutation matrix: row-stochastic, p(t+1) = p'(t) Q.
Q = np.zeros((N, N))
for i in range(N):
    Q[i, i] = 1.0 - MU
    Q[i, distance[i] == 1] = MU / L

# Nearest-neighbor fitness coupling: a_0 = 0, a_1 = 1, a_{d>1} = 0.
A = np.zeros((N, N))
A[distance == 1] = 1.0

focus = [0, 1, 3, 7]  # 000 -> 001 -> 011 -> 111


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
    "mathtext.fontset": "cm",
    "font.size": 9,
    "axes.labelsize": 10,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
})

fig, axes = plt.subplots(1, 2, figsize=(6.8, 2.8), sharex=True, sharey=True)

for ax, beta, history, panel in zip(axes, BETAS, trajectories, ["a", "b"]):
    for i in focus:
        ax.plot(
            range(T + 1),
            history[:, i],
            lw=1.8,
            label=rf"$p_{{{labels[i]}}}$",
        )

    rest = 1.0 - history[:, focus].sum(axis=1)
    ax.plot(range(T + 1), rest, lw=1.2, ls="--", color="0.35", label="rest")

    ax.set_xlim(0, T)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel(r"generation $t$")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.text(
        -0.14,
        1.03,
        panel,
        transform=ax.transAxes,
        fontsize=11,
        fontweight="bold",
        fontfamily="sans-serif",
    )
    ax.text(0.05, 0.92, rf"$\beta={beta:g}$", transform=ax.transAxes)

axes[0].set_ylabel(r"frequency $p_i(t)$")

axes[0].annotate(
    r"$001$ stays near mutation scale",
    xy=(55, trajectories[0][55, 1]),
    xytext=(18, 0.11),
    arrowprops=dict(arrowstyle="->", lw=0.8),
    fontsize=8,
)
axes[1].annotate(
    r"$001$ is transiently amplified",
    xy=(18, trajectories[1][18, 1]),
    xytext=(34, 0.30),
    arrowprops=dict(arrowstyle="->", lw=0.8),
    fontsize=8,
)
axes[1].annotate(
    r"later flow reaches $111$",
    xy=(78, trajectories[1][78, 7]),
    xytext=(82, 0.88),
    arrowprops=dict(arrowstyle="->", lw=0.8),
    fontsize=8,
)

handles, legend_labels = axes[1].get_legend_handles_labels()
fig.legend(
    handles,
    legend_labels,
    ncol=5,
    frameon=False,
    loc="upper center",
    bbox_to_anchor=(0.5, 1.10),
    columnspacing=1.3,
    handlelength=2.0,
)

fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig(OUT, bbox_inches="tight")
plt.close(fig)

beta_escape = g[0] - g[1]
print(f"beta_escape(000 -> 001) = {beta_escape:.3f}")
print(OUT)

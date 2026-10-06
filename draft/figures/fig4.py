"""Local coexistence onset and separation from the global percolation scale."""

from math import erf, exp, log
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).with_suffix(".pdf")
SEED = 20261006
MU = 1e-3
ETA = 1.5
D0 = 1.2
DYNAMIC_SETTINGS = ((6, 40), (8, 30))
SCALE_L = np.arange(4, 13)
SCALE_REPEATS = 2000


def neighbors(L):
    n = 2**L
    nodes = np.arange(n, dtype=np.int32)
    return np.stack([nodes ^ (1 << b) for b in range(L)], axis=1)


def diversity(p):
    q = p[p > 0]
    return exp(-np.sum(q * np.log(q)))


def stationary_diversity(g, L, beta, neigh, steps=900, tail=100):
    n = len(g)
    p = np.zeros(n)
    p[np.argmax(g)] = 1.0
    values = []

    for t in range(steps):
        f = g + beta * p[neigh].sum(axis=1)
        z = ETA * f
        z -= z.max()
        w = p * np.exp(z)
        w /= w.sum()
        p_new = (1.0 - MU) * w + (MU / L) * w[neigh].sum(axis=1)

        if t >= steps - tail:
            values.append(diversity(p_new))
        if t > 100 and np.max(np.abs(p_new - p)) < 1e-11:
            return diversity(p_new)
        p = p_new

    return float(np.mean(values))


def peak_threshold(g, neigh):
    peak = int(np.argmax(g))
    return float(g[peak] - np.max(g[neigh[peak]]))


def diversity_onset(g, L, neigh, beta_star):
    lo = 0.0
    hi = max(3.5, 1.5 * beta_star + 0.5)

    while stationary_diversity(g, L, hi, neigh) <= D0:
        hi *= 1.5

    for _ in range(11):
        beta = 0.5 * (lo + hi)
        if stationary_diversity(g, L, beta, neigh) > D0:
            hi = beta
        else:
            lo = beta

    return hi


def two_type_factor():
    lo, hi = 0.5, 1.0 - 1e-12

    for _ in range(80):
        x = 0.5 * (lo + hi)
        D = exp(-(x * log(x) + (1.0 - x) * log(1.0 - x)))
        if D > D0:
            lo = x
        else:
            hi = x

    x = 0.5 * (lo + hi)
    return 1.0 / (2.0 * x - 1.0)


def independent_scale(L):
    target = 1.0 / L
    lo, hi = 0.0, 2.0

    for _ in range(80):
        beta = 0.5 * (lo + hi)
        if erf(beta / 2.0) < target:
            lo = beta
        else:
            hi = beta

    return 0.5 * (lo + hi)


rng = np.random.default_rng(SEED)
factor = two_type_factor()
dynamic = {}

for L, repeats in DYNAMIC_SETTINGS:
    neigh = neighbors(L)
    beta_star = np.empty(repeats)
    beta_D = np.empty(repeats)

    for r in range(repeats):
        g = rng.normal(size=2**L)
        beta_star[r] = peak_threshold(g, neigh)
        beta_D[r] = diversity_onset(g, L, neigh, beta_star[r])

    dynamic[L] = (beta_star, beta_D)
    corr = np.corrcoef(beta_star, beta_D)[0, 1]
    slope = np.polyfit(beta_star, beta_D, 1)[0]
    print(f"L={L}: corr={corr:.5f}, slope={slope:.4f}")

median = []
q25 = []
q75 = []

for L in SCALE_L:
    neigh = neighbors(int(L))
    values = np.empty(SCALE_REPEATS)

    for r in range(SCALE_REPEATS):
        g = rng.normal(size=2**L)
        values[r] = peak_threshold(g, neigh)

    median.append(np.median(values))
    q25.append(np.quantile(values, 0.25))
    q75.append(np.quantile(values, 0.75))

median = np.asarray(median)
q25 = np.asarray(q25)
q75 = np.asarray(q75)
beta0 = np.array([independent_scale(int(L)) for L in SCALE_L])

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

for L, _ in DYNAMIC_SETTINGS:
    beta_star, beta_D = dynamic[L]
    ax.scatter(
        beta_star,
        beta_D,
        s=13,
        alpha=0.65,
        label=rf"$L={L}$",
    )

limit = max(np.max(values[1]) for values in dynamic.values()) * 1.04
x = np.linspace(0, limit, 200)
ax.plot(
    x,
    factor * x,
    lw=1.4,
    color="0.15",
    label="two-genotype prediction",
)
ax.set_xlim(0, limit)
ax.set_ylim(0, limit)
ax.set_xlabel(r"first peak edge $\beta_*$")
ax.set_ylabel(r"diversity onset $\beta_D$")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(frameon=False, loc="upper left")
ax.text(-0.14, 1.03, "(a)", transform=ax.transAxes, fontsize=10)

ax = axes[1]
ax.plot(
    SCALE_L,
    median,
    marker="o",
    ms=3.2,
    lw=1.5,
    label=r"peak edge $\beta_*$",
)
ax.fill_between(
    SCALE_L,
    q25,
    q75,
    alpha=0.14,
    linewidth=0,
)
ax.plot(
    SCALE_L,
    beta0,
    marker="s",
    ms=3.0,
    lw=1.5,
    label=r"$c=1$ reference",
)
ax.set_yscale("log")
ax.set_xlabel(r"genotype dimension $L$")
ax.set_ylabel(r"coupling scale $\beta$")
ax.set_xticks([4, 6, 8, 10, 12])
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(frameon=False, loc="center right")
ax.text(-0.14, 1.03, "(b)", transform=ax.transAxes, fontsize=10)

fig.subplots_adjust(
    left=0.10,
    right=0.99,
    bottom=0.21,
    top=0.92,
    wspace=0.30,
)
fig.savefig(OUT, bbox_inches="tight")
plt.close(fig)

print(f"factor(D={D0}) = {factor:.6f}")
print(OUT)

# Pattern catalog

Use this file when creating new material or when a current implementation needs a concrete reference pattern.

These are examples, not architecture. Copy only what the task needs.

## Scientific paragraph

A common paragraph shape is:

```text
[State the scientific object, question, or result directly.]

[Introduce the definition, mechanism, assumption, or evidence needed to develop it.]

[Give the mathematical, numerical, or empirical consequence.]

[State the interpretation, scope, or connection to the next step when useful.]
```

Do not add all four sentences mechanically. The pattern describes logical roles, not sentence count.

## Results subsection

```text
descriptive subsection title

baseline object or known case
        ↓
new quantity / mechanism
        ↓
derivation or computation
        ↓
clean result / threshold / prediction
        ↓
figure or numerical validation
        ↓
short interpretation
```

Each subsection should answer one scientific question.

## Abstract

```text
1. concrete phenomenon/problem
2. precise unresolved issue
3. object/model/framework introduced
4. main result
5. validation or relevant scope
6. concrete consequence
```

Use fewer or more sentences when needed. Keep the result visible.

## Figure caption

```text
[Short descriptive statement of the figure.]

(a) What is plotted and the relevant case.
(b) What is plotted and the relevant case.

[Meaning of lines/markers/colors/bands/thresholds.]
[Sample size, averaging, model, or parameter details needed to interpret the figure.]
```

Do not reproduce the discussion inside the caption.

# Figure style fingerprints

Before copying a plotting template, recover the current paper's figure family.

## Serif family

Use only when sibling figures/manuscript are serif:

```python
plt.rc(
    "font",
    family="serif",
    serif=["Times New Roman", "Times", "Nimbus Roman", "DejaVu Serif"],
    size=10,
)
plt.rc("mathtext", fontset="cm")
```

## Sans-serif family

Use only when sibling figures/manuscript are sans-serif:

```python
plt.rc(
    "font",
    family="sans-serif",
    sans_serif=["Helvetica", "Arial", "DejaVu Sans"],
    size=10,
)
plt.rc("mathtext", fontset="dejavusans")
```

Do not pick between these from personal taste. Match the paper.

## Label patterns

Pure mathematical quantity:

```python
ax.set_xlabel(r"$\rho$")
ax.set_ylabel(r"$U(\theta)$")
```

Descriptive mathematical quantity:

```python
ax.set_xlabel(r"cycle current $|q|$")
ax.set_ylabel(r"modal decay rate $-\mathrm{Re}\,\lambda$")
```

Physical quantity with units:

```python
ax.set_xlabel(r"frequency $f$ (Hz)")
ax.set_ylabel(r"relaxation time $\tau$ (s)")
```

Natural symbolic ticks:

```python
ax.set_xticks([0, np.pi / 4, np.pi / 2, np.pi])
ax.set_xticklabels([r"$0$", r"$\pi/4$", r"$\pi/2$", r"$\pi$"])
```

Panel label:

```python
ax.text(
    -0.10,
    1.02,
    "a",
    transform=ax.transAxes,
    ha="left",
    va="bottom",
    fontsize=12,
    fontweight="bold",
    fontname="DejaVu Sans",
)
```

Compact legend:

```python
ax.legend(frameon=False, loc="best")
```

## Small figure script

```python
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT = Path(__file__).with_name("fig1.pdf")

rho = np.linspace(0.0, 2.0, 500)
value = np.exp(-rho)

fig, ax = plt.subplots(figsize=(4.2, 3.1))

ax.plot(rho, value, color="black", linewidth=1.5)
ax.set(xlabel=r"$\rho$", ylabel=r"$C(\rho)$")
ax.spines[["top", "right"]].set_visible(False)

fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight")
plt.close(fig)

print(f"saved {OUT}")
```

Use this only after adapting font family, figure size, notation, and output format to the current paper.

## Expensive computation plus plot

When polishing the figure should not rerun the experiment:

```text
fig3_data.py
    ↓
fig3_data.csv
    ↓
fig3_plot.py
    ↓
fig3.pdf
```

The data script owns the expensive computation and validation.

The plot script reads the canonical data and contains only the transformation needed to produce the figure.

Do not split cheap calculations this way.

## Small numerical experiment

```python
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT = Path(__file__).with_name("experiment.pdf")
RNG = np.random.default_rng(0)

STEPS = 1000


def simulate():
    return np.cumsum(RNG.normal(size=STEPS))


trajectory = simulate()

assert trajectory.shape == (STEPS,)
assert np.all(np.isfinite(trajectory))

fig, ax = plt.subplots(figsize=(4.2, 3.1))
ax.plot(trajectory, color="black", linewidth=1.5)
ax.set(xlabel="step", ylabel="state")
ax.spines[["top", "right"]].set_visible(False)

fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight")
plt.close(fig)
```

## Structure decisions

Extract a helper when:
- several scripts reuse the operation;
- it represents a named mathematical object;
- inline code obscures the scientific logic;
- it needs independent validation.

Add `main()` or argument parsing when the script has real user-facing modes or reuse as a command-line tool.

Add a class when persistent state and behavior genuinely belong together.

Add a dependency, file, directory, or configuration layer only when it solves a current problem.

Moving complexity is not removing it.

# Current draft

A population evolves on an explicit genotype graph while population composition changes relative fitness through

`f_i(p) = g_i + beta * (A p)_i`.

For a resident genotype `i` and a rare neighboring mutant `j`, the local invasion condition defines a directed mutational edge. With distance-dependent coupling and `Delta a = a_1 - a_0 > 0`, both directions of an edge become accessible above

`beta_ij = |g_i - g_j| / Delta a`.

The collective object is the reversible subgraph `R_beta`, containing edges accessible in both resident backgrounds. For independent Gaussian intrinsic fitnesses and `Delta a = 1`,

`q(beta) = erf(beta / 2)`

is the marginal probability that an edge is reversible, and `c = L q` is its mean degree. The process is not ordinary bond percolation: incident edges are correlated because their thresholds share genotype fitness values, while vertex-disjoint edges are independent.

Figure 2 isolates the transition on a three-bit cube. Figure 3 scales the problem to random landscapes with `L = 6, 8, 10, 12`. The current `P(S > 1/2)` curve is treated only as a macroscopic-connectivity diagnostic; it does not locate the critical point.

The biological question is whether the emergence of a giant reversible component predicts a change in persistent genotype diversity under the full mutation-selection dynamics. Connectivity and coexistence are kept distinct: the percolation result is structural, while diversity must be tested dynamically.

The manuscript is organized as **Literature** and **Results**. The previous resource-competition draft is archived in `archive/history-dependent-recovery/`.

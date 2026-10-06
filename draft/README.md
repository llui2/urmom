# Current draft

A population evolves on an explicit genotype graph while population composition changes relative fitness through

`f_i(p) = g_i + beta * (A p)_i`.

For neighboring genotypes, resident-dependent invasion makes both directions accessible above

`beta_ij = |g_i - g_j| / Delta a`.

The same threshold has an exact local dynamical meaning. In the two-genotype mutation-free problem, an interior frequency balance exists if and only if `beta > beta_ij`. Thus a reversible edge corresponds locally to mutual invasibility and coexistence.

The collective object `R_beta` contains all reversible edges. For independent Gaussian intrinsic fitnesses, its marginal edge probability is

`q(beta) = erf(beta / 2)`,

but incident edges are correlated because their thresholds share genotype fitness values. Figures 2 and 3 show the small-cube mechanism and the finite-size correlated-percolation problem.

Figure 4 separates this global connectivity scale from standing diversity. If `i_*` is the intrinsic global peak, the first reversible incident edge

`beta_* = min_j |g_i* - g_j|`

predicts the onset of long-time diversity in the full mutation-selection dynamics. For the operational threshold `D > 1.2`, the two-genotype calculation predicts `beta_D ~= 1.10 beta_*`, which is followed closely by simulations for `L = 6, 8`.

For Gaussian House-of-Cards landscapes, the global connectivity reference decreases as `1/L`, whereas the peak-neighborhood scale grows roughly as `sqrt(L)`. Global reversible connectivity and simultaneous coexistence are therefore distinct in this ensemble.

The manuscript is organized as **Literature** and **Results**. The previous resource-competition draft is archived in `archive/history-dependent-recovery/`.

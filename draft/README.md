# Current draft

A population evolves on an explicit genotype graph while population composition changes relative fitness through

\`f_i(p) = g_i + beta * (A p)_i\`.

For a resident genotype \`i\` and a rare neighboring mutant \`j\`, the local invasion condition defines a directed mutational edge. With distance-dependent coupling and \`Delta a = a_1 - a_0 > 0\`, both directions of an edge become accessible above

\`beta_ij = |g_i - g_j| / Delta a\`.

The current collective object is the reversible subgraph \`R_beta\`, containing edges accessible in both resident backgrounds. Its largest component gives a percolation-like order parameter on genotype space.

For independent Gaussian intrinsic fitnesses and \`Delta a = 1\`, an edge is reversible with probability

\`q(beta) = erf(beta / 2)\`,

so the mean reversible degree is \`c = L q\`. Incident edge states are correlated because their thresholds share genotype fitness values. The current numerical result is a finite-size sharpening of the largest reversible component for \`L = 6, 8, 10, 12\`.

The manuscript is organized as **Literature** and **Results**. The previous resource-competition draft is archived in \`archive/history-dependent-recovery/\`.

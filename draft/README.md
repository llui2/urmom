# Current draft

A population evolves on an explicit genotype space. Mutation determines which nearby genotypes can appear, while the current population changes genotype fitness through

`f_i(p) = g_i + beta * (A p)_i`.

Here `A` is a **fitness-coupling matrix**: `A_ij` measures how genotype `j` changes the fitness of genotype `i`.

For a resident `i` and a rare one-step mutant `j`, the selection step favors the mutant when

`g_j - g_i + beta * (A_ji - A_ii) > 0`.

The working problem is to determine how this frequency-dependent fitness correction changes mutational accessibility on a rugged intrinsic landscape.

The first setup keeps `A` low-dimensional, for example `A_ij = a[d_H(i,j)]`, and studies when coupling opens or closes routes from an intrinsic local peak. Diversity is an output, not an optimization target.

The previous resource-competition draft is archived in `archive/history-dependent-recovery/`.

The local invasion conditions also define a resident-conditioned directed graph on genotype space. For nearest-neighbor coupling with $a_1>a_0$, the reverse direction of an edge $\{i,j\}$ opens at $\beta^{\mathrm{rev}}_{ij}=|g_i-g_j|/(a_1-a_0)$. These are local thresholds, but their effect on reachability is collective.

In the current three-bit landscape, the largest strongly connected component grows from $1$ to $2$ to $4$ genotypes and then jumps to all $8$ at $\beta_c=0.5$. Just below the transition the components have sizes $4+2+2$; the single reverse direction opening on the $001$--$101$ edge is sufficient to merge them into one strongly connected genotype space. This local-to-global topological reorganization is the main mechanism to test beyond the illustrative cube.


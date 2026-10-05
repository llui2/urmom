# Current draft

A population evolves on an explicit genotype space. Mutation determines which nearby genotypes can appear, while the current population changes genotype fitness through

`f_i(p) = g_i + beta * (A p)_i`.

Here `A` is a **fitness-coupling matrix**: `A_ij` measures how genotype `j` changes the fitness of genotype `i`.

For a resident `i` and a rare one-step mutant `j`, the selection step favors the mutant when

`g_j - g_i + beta * (A_ji - A_ii) > 0`.

The working problem is to determine how this frequency-dependent fitness correction changes mutational accessibility on a rugged intrinsic landscape.

The first setup keeps `A` low-dimensional, for example `A_ij = a[d_H(i,j)]`, and studies when coupling opens or closes routes from an intrinsic local peak. Diversity is an output, not an optimization target.

The previous resource-competition draft is archived in `archive/history-dependent-recovery/`.

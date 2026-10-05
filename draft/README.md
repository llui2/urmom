# Current draft

## One-line idea

A population evolves on a genotype fitness landscape, but the population itself can change the fitness of each genotype.

## Model

- Genotypes are binary sequences.
- Mutation connects sequences one bit apart.
- `g_i` is the intrinsic fitness of genotype `i`.
- `p_i` is its current frequency.
- Effective fitness: `f_i(p) = g_i + beta * (A p)_i`.

`A` is a **fitness-coupling matrix**, not just a generic ecological interaction matrix.

`A_ij` means: increasing genotype `j` changes the fitness of genotype `i`.

Mutation and fitness coupling do different things:

- `Q` makes mutants appear.
- `A` changes whether those mutants are favored after they appear.

For a resident `i` and a one-step mutant `j`:

`s_{j|i} = g_j - g_i + beta * (A_ji - A_ii)`.

A mutation can therefore be intrinsically unfavorable, `g_j < g_i`, but become favorable because of the current population.

## Main question

**How does frequency-dependent fitness coupling change which mutational paths are accessible on genotype space?**

The first problem is to start at a local fitness peak and ask when coupling opens a route that is closed when `beta = 0`.

## First setup

1. Small binary genotype space.
2. Nearest-neighbor mutation.
3. A rugged intrinsic landscape with a known local and global peak.
4. A simple low-dimensional family of `A`.
5. Vary `beta`.
6. Track accessible edges, escape from local peaks, paths, and final population structure.

Do not optimize entropy in the first pass. Diversity should be observed, not imposed.

The previous resource-competition draft is archived under `archive/history-dependent-recovery/`.

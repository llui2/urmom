#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "$0")" && pwd)"
cd "$repo_root"

git pull --ff-only

cd draft

# Generated figure PDFs are build artifacts. Remove stale outputs such as an
# old fig2.pdf before rebuilding the figures that currently belong to the draft.
rm -f figures/fig*.pdf

for script in figures/fig*.py; do
    python3 "$script"
done

latexmk -g -pdf -interaction=nonstopmode -halt-on-error main.tex

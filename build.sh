#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "$0")" && pwd)"
figure_dir="$repo_root/draft/figures"

cd "$repo_root"
git pull --ff-only

shopt -s nullglob
scripts=("$figure_dir"/fig*.py)

if [ "${#scripts[@]}" -eq 0 ]; then
    echo "No figure scripts found in $figure_dir"
    exit 1
fi

rm -f "$figure_dir"/fig*.pdf

for script in "${scripts[@]}"; do
    python3 "$script"
done

cd "$repo_root/draft"
latexmk -g -pdf -interaction=nonstopmode -halt-on-error main.tex

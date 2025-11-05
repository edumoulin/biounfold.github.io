#!/usr/bin/env bash
set -euo pipefail
source .venv/bin/activate  # ensure venv is active
mkdir -p docs/assets/notebooks
for nb in analysis_notebooks/*.ipynb; do
  [ -e "$nb" ] || continue
  jupyter nbconvert --to html --output-dir docs/assets/notebooks "$nb"  
done


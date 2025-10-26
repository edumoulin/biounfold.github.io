# export_notebooks.sh
set -e
mkdir -p docs/assets/notebooks
for nb in analysis_notebooks/*.ipynb; do
  [ -e "$nb" ] || continue
  jupyter nbconvert --to html --output-dir docs/assets/notebooks "$nb"
done


# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     notebook_metadata_filter: all
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.18.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
#   language_info:
#     codemirror_mode:
#       name: ipython
#       version: 3
#     file_extension: .py
#     mimetype: text/x-python
#     name: python
#     nbconvert_exporter: python
#     pygments_lexer: ipython3
#     version: 3.11.14
# ---

# %%
import sys
sys.path.append("/work")

# %%
import matplotlib.pyplot as plt
from bio_unfold_viz.templates import bridge_diagram

fig, ax = plt.subplots(figsize=(8,3))
bridge_diagram(
    ax,
    left=["Biology constraints", "Assay limits", "Noise & bias"],
    right=["Model capabilities", "Generalization", "Failure modes"],
    caption="Translating biological reality into AI decisions (and back)",
)
plt.show()


# %%

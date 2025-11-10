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
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# ============================================================
# 1) Minimal RADAR (3 example compounds) — horizontal figure
#    - 5–7 properties recommended
#    - Optional "target" polygon to suggest direction of design
# ============================================================

def make_biounfold_007_radar_three(
    properties=("Potency", "Solubility", "Permeability", "Stability", "Clearance", "Selectivity"),
    # Values should be in [0, 1] (normalize upstream if needed)
    compound_A=(0.90, 0.35, 0.35, 0.60, 0.80, 0.70),  # early: potent, poor solubility/permeability
    compound_B=(0.70, 0.55, 0.50, 0.65, 0.65, 0.70),  # mid: more balanced
    compound_C=(0.65, 0.70, 0.65, 0.70, 0.55, 0.75),  # later: near desired profile
    target     =(0.65, 0.70, 0.65, 0.70, 0.55, 0.75),  # optional: dashed reference
    width_px=1200,
    height_px=639,
    dpi=200,
    title="Profiles Evolve Through Trade-offs",
    subtitle="Three illustrative compounds across key properties (normalized)",
    show_target=False,
):
    props = list(properties)
    n = len(props)

    # Close the loop
    def close(vals):
        vals = list(vals)
        return vals + [vals[0]]

    theta = np.linspace(0, 2*np.pi, n, endpoint=False)
    theta = np.concatenate([theta, [theta[0]]])

    # Figure
    fig_w, fig_h = width_px / dpi, height_px / dpi
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=dpi)
    ax = plt.subplot(1, 1, 1, polar=True)

    # Light grid and ticks
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(theta[:-1]), labels=props)
    ax.set_ylim(0, 1)
    ax.set_yticklabels([])

    # Plot three profiles (use default color cycle; only alpha/linewidth tuned)
    A = close(compound_A)
    B = close(compound_B)
    C = close(compound_C)

    ax.plot(theta, A, linewidth=2.0, alpha=0.6, label="Initial Lead")
    ax.fill(theta, A, alpha=0.04)

    ax.plot(theta, B, linewidth=2.25, alpha=0.75, label="Improved Variant")
    ax.fill(theta, B, alpha=0.06)

    ax.plot(theta, C, linewidth=2.5, alpha=0.95, label="Optimized Candidate")
    ax.fill(theta, C, alpha=0.10)

    # Optional target reference polygon (dashed, no fill)
    if show_target and target is not None:
        T = close(target)
        ax.plot(theta, T, linewidth=2.0, alpha=0.9, linestyle=(0, (3, 4)), label="Desired direction")

    # Titles
    if title:
        ax.set_title(title, pad=20, fontsize=16)
    if subtitle:
        ax.text(0.5, 1.15, subtitle, transform=ax.transAxes, ha="center", va="bottom", fontsize=11)

    # Legend (outside, right)
    leg = ax.legend(frameon=False, bbox_to_anchor=(1.15, 0.5), loc="center left", fontsize=11)

    plt.tight_layout()
    return fig

# -----------------------------
# Example (no files are saved):
fig = make_biounfold_007_radar_three()
plt.show()

# %%
save_path="../docs/assets/images/biounfold-007-beyond-binding.png"
pad_fraction = 0.02  # adjust this to taste (1–3% usually enough)
dpi=100
width_px = 1200
height_px = 639
pad_inches = (height_px / dpi) * pad_fraction

# 3) Save without transforming the plot
fig.savefig(
    save_path,
    dpi=dpi,
    bbox_inches="tight",   # include legends & titles
    pad_inches=pad_inches, # proportional white space
)

# %%

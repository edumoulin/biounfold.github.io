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
# ------------------------------------------------------------
# BioUnfold #10 — "Assay Reliability Space" (Density Map)
# ------------------------------------------------------------
# Purpose:
# Visualize reliability as a *measurable* property of an assay,
# driven by measurement reproducibility (y) and strengthened by
# control diversity (x). Transparency is *not* an axis here.
#
# Axes:
#   x-axis: Control Diversity  (few controls  → many controls)
#   y-axis: Measurement Reproducibility (fragile → stable)
#
# Encoding:
#   Color density encodes a reliability score R(x, y).
#   R is more sensitive to y than x, matching the essay's stance:
#   reliability must be *measured* and outranks transparency.
#
# Design:
#   - Single-plot matplotlib figure.
#   - No spines; minimal ticks.
#   - Contours + dashed threshold for the "Reliable zone".
#   - Example points annotate typical assay philosophies.
# ------------------------------------------------------------

import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.patheffects as path_effects

def reliability_score(x, y):
    """
    Reliability surface R(x, y).

    Args:
        x: ndarray or float in [0,1], Control diversity (orthogonal controls).
        y: ndarray or float in [0,1], Measurement reproducibility (low variance).

    Returns:
        R: Reliability score in [0,1]-ish (not strictly bounded), emphasizing y.

    Notes:
        - Nonlinear weights: y carries more weight (power 1.4 vs 0.6).
        - Small interaction term rewards having *both* dimensions.
    """
    x = np.clip(x, 0.0, 1.0)
    y = np.clip(y, 0.0, 1.0)
    return (x**0.6) * (y**1.4) * (0.85 + 0.15 * (x * y))

def make_biounfold_010_reliability_space(
    nx=400, ny=400,
    width_px=1400, height_px=900, dpi=200,
    title="Assay Reliability Space",
    caption=(
        "Reliability increases with measurement reproducibility (y) and control diversity (x). "
        "The highlighted region marks designs that are both stable and well-instrumented. "
        "Reliability is measurable — through controls, QC, and replicates."
    ),
    reliable_threshold=0.60,
    reliable_center=(0.80, 0.90),
    add_examples=True,
):
    """
    Create the BioUnfold #10 'Assay Reliability Space' figure.

    Args:
        nx, ny: Grid resolution for the density field.
        width_px, height_px, dpi: Figure size in pixels and DPI.
        title: Plot title.
        caption: Explanatory caption under the axis.
        reliable_threshold: Contour level for reliable-zone threshold (0..1).
        reliable_center: 'Reliable zone' position.
        add_examples: If True, annotate example assay philosophies.
        save_png_path, save_svg_path: File paths; if provided, will save outputs.

    Returns:
        fig, ax
    """
    # Grid
    x = np.linspace(0, 1, nx)
    y = np.linspace(0, 1, ny)
    X, Y = np.meshgrid(x, y)
    Z = reliability_score(X, Y)

    # Figure
    fig_w, fig_h = width_px / dpi, height_px / dpi
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=dpi)
    ax = plt.gca()

    # Smooth gradient: deep blue (low reliability) → teal → green (high reliability)
    BuGn_custom = colors.LinearSegmentedColormap.from_list(
        "BuGn_custom",
        [
            (0.00, (0.40, 0.55, 0.85)),  # light blue
            (0.50, (0.00, 0.60, 0.65)),  # teal
            (1.00, (0.10, 0.70, 0.30)),  # green
        ],
        N=256,
    )
    
    # Heatmap (no explicit colormap settings)
    im = ax.imshow(
        Z, origin="lower", extent=[0, 1, 0, 1], aspect="auto",
        interpolation="bilinear", cmap=BuGn_custom
    )

    # Contours (structure) + threshold (reliable zone)
    cs = ax.contour(X, Y, Z, levels=np.linspace(0.1, 0.9, 9), linewidths=0.6, alpha=0.8)
    ax.contour(X, Y, Z, levels=[reliable_threshold], linewidths=1.8, linestyles="--", colors=["white"])

    # Highlight "Reliable zone" with a soft ellipse
    ax.text(
        reliable_center[0], reliable_center[1] + 0.03, "Reliable zone",
        ha="center", va="center", fontsize=12, weight="bold", color="white",
        path_effects=[
            path_effects.withStroke(linewidth=2.5, foreground="black", alpha=0.6)
        ]
    )

    # Example points (optional)
    if add_examples:
        examples = [
            {"xy": (0.20, 0.62), "label": "Traditional assay\n(few controls, stable readout)"},
            {"xy": (0.72, 0.40), "label": "Exploratory screen\n(many conditions, low stability)"},
            {"xy": (0.95, 0.85), "label": "Data-validated assay\n(many controls, stable, QC-ed)"},
            {"xy": (0.30, 0.20), "label": "Uncontrolled signal\n(weak controls, fragile)"},
        ]
        for ex in examples:
            x0, y0 = ex["xy"]
            ax.scatter([x0], [y0], s=50, alpha=0.9, color="black")
            ax.annotate(
                ex["label"],
                xy=(x0, y0),
                xytext=(x0 + 0.08, y0),
                arrowprops=dict(arrowstyle="-", lw=0.8, alpha=0.9),
                fontsize=9, ha="left", va="bottom"
            )

    # Axes formatting
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xlabel("Control diversity (few → many)", labelpad=8)
    ax.set_ylabel("Measurement reproducibility (fragile → stable)", labelpad=8)
    ax.set_title(title, pad=14, fontsize=14)

    # Clean frame
    ax.set_xticks([]); ax.set_yticks([])
    ax.grid(False)

    # Caption below axis
    ax.text(0.0, -0.17, caption, ha="left", va="top", transform=ax.transAxes, fontsize=10, wrap=True)

    plt.tight_layout()


    return fig, ax

fig, ax = make_biounfold_010_reliability_space(
    reliable_threshold=0.60,
)
plt.show()


# %%
save_path="../docs/assets/images/biounfold-010-assay-reliability-space.png"
pad_fraction = 0.02  # adjust this to taste (1–3% usually enough)
dpi=200
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

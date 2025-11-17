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
from matplotlib.patches import Circle

# ------------------------------------------------------------
# BioUnfold #9 — "Target Constellation" (Force-map metaphor)
# ------------------------------------------------------------
# Updates in this version:
# - Correct symmetric projection: redundancy (r) pulls LEFT toward R pole.
# - Overall score via HARMONIC MEAN(s, n, d, 1-r).
# - Color encodes overall score using a continuous colormap (with colorbar legend).
# - Removed the outer plot frame (no spines).
# ------------------------------------------------------------

def harmonic_overall_score(s, n, d, r, eps=1e-8):
    """Harmonic mean of (s, n, d, 1-r). Strongly penalizes weak dimensions."""
    nr = 1.0 - r
    X = np.stack([s, n, d, nr], axis=-1).clip(eps, 1.0)
    return 4.0 / np.sum(1.0 / X, axis=-1)

def project_positions(s, n, d, r, ws=1.0, wn=1.0, wd=1.0, wr=1.0):
    """
    Symmetric barycentric projection onto a diamond.
    Poles: S=(+1,0), N=(0,+1), D=(0,-1), R=(-1,0).
    High redundancy (r) pulls LEFT toward R; low redundancy does not add rightward force.
    """
    pS = np.array([+1.0, 0.0])
    pN = np.array([0.0, +1.0])
    pD = np.array([0.0, -1.0])
    pR = np.array([-1.0, 0.0])

    num = (
        (ws * s)[..., None] * pS +
        (wn * n)[..., None] * pN +
        (wd * d)[..., None] * pD +
        (wr * r)[..., None] * pR
    )
    den = (ws * s + wn * n + wd * d + wr * r)[..., None].clip(1e-8, None)
    xy = num / den

    # Infinity-norm clamp to keep inside the diamond
    norm_inf = np.maximum(np.abs(xy[..., 0]), np.abs(xy[..., 1]))
    mask = norm_inf > 1.0
    if np.any(mask):
        xy[mask] = xy[mask] / norm_inf[mask, None]
    return xy[..., 0], xy[..., 1]

def make_biounfold_009_target_constellation(
    s=None, n=None, d=None, r=None,
    width_px=1400, height_px=800, dpi=200,
    title="Target Fitness Map",
    subtitle_golden="Golden circle: balanced",
    caption=(
        "Each point represents a candidate target positioned by competing pulls — "
        "Novelty (N), Specificity (S), Druggability (D), and Redundancy (R). "
        "The overall score, shown by color, is the harmonic mean of (S, N, D, 1−R)."
    ),
    sweet_radius=0.28,
    cmap_name="viridis",          # colormap for overall score
    add_colorbar=True,
    rng_seed=7,
):
    # --- Example data if none provided ---
    if s is None or n is None or d is None or r is None:
        rng = np.random.default_rng(rng_seed)
        k = 20
        s = rng.beta(0.8, 0.8, k)
        n = rng.beta(0.8, 0.8, k)
        d = rng.beta(0.8, 0.8, k)
        r = rng.beta(0.8, 0.8, k)
    s = np.asarray(s, float)
    n = np.asarray(n, float)
    d = np.asarray(d, float)
    r = np.asarray(r, float)
    assert s.shape == n.shape == d.shape == r.shape, "s, n, d, r must share shape"

    # --- Compute positions and overall score ---
    x, y = project_positions(s, n, d, r)
    O = harmonic_overall_score(s, n, d, r)

    # --- Figure setup ---
    fig_w, fig_h = width_px / dpi, height_px / dpi
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=dpi)
    ax = plt.gca()
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.05, 1.20)
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    ax.grid(False)

    # Remove outer frame (spines)
    for sp in ax.spines.values():
        sp.set_visible(False)

    # --- Diamond boundary (rotated square)
    diamond = np.array([[0, 1], [1, 0], [0, -1], [-1, 0], [0, 1]])
    ax.plot(diamond[:, 0], diamond[:, 1], linestyle='-', linewidth=1.0, alpha=0.9)

    # --- Sweet spot: central “golden circle” + label
    sweet = Circle((0, 0), sweet_radius, facecolor=(1, 0.9, 0.3, 0.06), edgecolor='gold', linewidth=1.1)
    ax.add_patch(sweet)
    ax.annotate(
        subtitle_golden,
        xy=(-sweet_radius * 0.707, sweet_radius * 0.707),  # on circle at 45°
        xytext=(-0.56, 0.77), textcoords='axes fraction',
        arrowprops=dict(arrowstyle='-', lw=0.8),
        ha='left', va='center', fontsize=10
    )

    # --- Pole labels
    pole_font = 11; sub_font = 9
    ax.text(0.0, 1.25, "N  Novelty", ha='center', va='center', fontsize=pole_font)
    ax.text(0.0, 1.1, "exploration", ha='center', va='center', fontsize=sub_font, fontstyle='italic', alpha=0.9)

    ax.text(1.5, 0.07, "S  Specificity", ha='center', va='center', fontsize=pole_font)
    ax.text(1.5, -0.07, "precision", ha='center', va='center', fontsize=sub_font, fontstyle='italic', alpha=0.9)

    ax.text(0.0, -1.1, "D  Druggability", ha='center', va='center', fontsize=pole_font)
    ax.text(0.0, -1.25, "feasibility", ha='center', va='center', fontsize=sub_font, fontstyle='italic', alpha=0.9)

    ax.text(-1.55, 0.07, "R  Redundancy", ha='center', va='center', fontsize=pole_font)
    ax.text(-1.55, -0.07, "bypass risk", ha='center', va='center', fontsize=sub_font, fontstyle='italic', alpha=0.9)

    # --- Light crosshairs (optional)
    ax.plot([-1.0, +1.0], [0, 0], linestyle='--', linewidth=0.6, alpha=0.5)
    ax.plot([0, 0], [-1.0, +1.0], linestyle='--', linewidth=0.6, alpha=0.5)

    # --- Scatter with colormap encoding overall score
    sc = ax.scatter(
        x, y,
        c=O, cmap=cmap_name, vmin=0.0, vmax=1.0,
        s=36, alpha=0.95, linewidths=0, edgecolors='none'
    )

    # Colorbar (acts as legend for overall score)
    if add_colorbar:
        cbar = plt.colorbar(sc, ax=ax, fraction=0.035, pad=0.25)
        cbar.set_label("Overall score (harmonic mean)", fontsize=9)
        cbar.ax.tick_params(labelsize=8)

    # --- Title and caption
    ax.set_title(title, fontsize=14, pad=14)
    ax.text(
        -0.5, -0.2, caption,
        ha='left', va='top', transform=ax.transAxes,
        fontsize=10, wrap=True
    )

    plt.tight_layout()
    return fig, ax

# --------------------
# Example usage:
# --------------------
fig, ax = make_biounfold_009_target_constellation()
plt.show()

# %%
save_path="../docs/assets/images/biounfold-009-target-fitness-map.png"
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

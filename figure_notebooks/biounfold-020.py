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
from matplotlib.patches import FancyBboxPatch, Polygon, FancyArrowPatch

# ----------------------------
# Style knobs (match your style)
# ----------------------------
FIGSIZE = (12.0, 3.8)
BG = "#f7f7f7"
INK = "#222222"
SOFT = "#666666"
BLUE = "#1f77b4"
RED = "#d62728"

def base_axes(ax):
    ax.set_facecolor(BG)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

# ----------------------------
# Helper drawing functions
# ----------------------------
def rounded_box(ax, xy, w, h, text, fc=BG, ec=INK, lw=1.6, fontsize=11, text_color=INK, alpha=1.0):
    x, y = xy
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.04",
        facecolor=fc, edgecolor=ec, linewidth=lw, alpha=alpha
    )
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, text, ha="center", va="center",
            fontsize=fontsize, color=text_color)
    return box

def arrow(ax, p0, p1, color=SOFT, lw=2.0, ms=14, alpha=0.9):
    a = FancyArrowPatch(
        p0, p1, arrowstyle='-|>', mutation_scale=ms,
        linewidth=lw, color=color, alpha=alpha,
        shrinkA=0, shrinkB=0
    )
    ax.add_patch(a)
    return a

def jitter_points(n, x, y0, y1, seed=0):
    rng = np.random.default_rng(seed)
    ys = rng.uniform(y0, y1, size=n)
    xs = rng.normal(loc=x, scale=0.012, size=n)
    return xs, ys

# ----------------------------
# Build figure
# ----------------------------
fig, ax = plt.subplots(1, 1, figsize=FIGSIZE)
fig.patch.set_facecolor(BG)
base_axes(ax)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# Title
fig.suptitle("Transcriptomics as a Control Surface",
             fontsize=18, y=0.98, color=INK)

# Regions (subtle shading)
ax.axvspan(0.00, 0.33, color=INK, alpha=0.03, lw=0)
ax.axvspan(0.33, 0.67, color=INK, alpha=0.05, lw=0)
ax.axvspan(0.67, 1.00, color=INK, alpha=0.03, lw=0)

ax.text(0.165, 0.93, "Upstream causes", ha="center", va="center", fontsize=11, color=SOFT)
ax.text(0.500, 0.93, "Regulatory control", ha="center", va="center", fontsize=11, color=SOFT)
ax.text(0.835, 0.93, "Biochemical execution", ha="center", va="center", fontsize=11, color=SOFT)

# Funnel geometry: wide -> narrow (control surface) -> wide
# We'll draw two translucent polygons to suggest "compression" then "expansion".
funnel_left = Polygon(
    [(0.27, 0.82), (0.34, 0.62), (0.34, 0.38), (0.27, 0.18), (0.42, 0.30), (0.42, 0.70)],
    closed=True, facecolor=BLUE, edgecolor="none", alpha=0.10
)
funnel_right = Polygon(
    [(0.58, 0.70), (0.58, 0.30), (0.73, 0.18), (0.66, 0.38), (0.66, 0.62), (0.73, 0.82)],
    closed=True, facecolor=RED, edgecolor="none", alpha=0.10
)
ax.add_patch(funnel_left)
ax.add_patch(funnel_right)

# Central "control surface" box
rounded_box(
    ax, (0.40, 0.42), 0.20, 0.16,
    "Transcriptome\n(coordinated programs)",
    fc=BG, ec=INK, lw=1.8, fontsize=11, text_color=INK
)

# Left: diverse causes (points + label)
xs, ys = jitter_points(18, x=0.12, y0=0.18, y1=0.82, seed=4)
ax.scatter(xs, ys, s=30, color=INK, alpha=0.85, zorder=5)
ax.text(0.12, 0.10, "Diverse\nperturbations", ha="center", va="top", fontsize=10.5, color=SOFT)

# Arrows from causes to control surface (thin, multiple)
for i, y in enumerate(np.linspace(0.22, 0.78, 6)):
    arrow(ax, (0.16, y), (0.40, 0.50), color=SOFT, lw=1.4, ms=10, alpha=0.55)

# Right: diverse execution (points + label)
xs2, ys2 = jitter_points(18, x=0.88, y0=0.18, y1=0.82, seed=9)
ax.scatter(xs2, ys2, s=30, color=INK, alpha=0.85, zorder=5)
ax.text(0.88, 0.10, "Diverse\nimplementations", ha="center", va="top", fontsize=10.5, color=SOFT)

# Arrows from control surface to execution
for i, y in enumerate(np.linspace(0.22, 0.78, 6)):
    arrow(ax, (0.60, 0.50), (0.84, y), color=SOFT, lw=1.4, ms=10, alpha=0.55)

# Add small callouts to reinforce "compression" and "expansion"
ax.text(0.31, 0.86, "many-to-few", ha="center", va="center", fontsize=10.5, color=SOFT)
ax.text(0.69, 0.86, "few-to-many", ha="center", va="center", fontsize=10.5, color=SOFT)

# Bottom thesis line
ax.text(
    0.5, 0.02,
    "Measuring control (regulatory adjustment) can be more legible than measuring execution directly.",
    ha="center", va="bottom", fontsize=11, color=INK
)

plt.tight_layout()

# %%
save_path="../docs/assets/images/biounfold-020-transcriptomics-as-a-control-surface.png"
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

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
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Arc
import numpy as np

# ----------------------------
# Minimal diagram: labels + arrows
# - Two branches from Live-cell imaging:
#   (1) No sorting -> orthogonal end-cap (no triangle)
#   (2) Sorting -> fans out to multiple Assay nodes
# - "Continuous" shown as a single unidirectional loop arrow around Live-cell node
# ----------------------------
FIGSIZE = (13.2, 3.0)
INK = "#222222"
SOFT = "#666666"

def base_axes(ax):
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

def arrow(ax, p0, p1, color=SOFT, lw=2.0, ms=14, alpha=0.9, rad=0.0, style='-|>'):
    a = FancyArrowPatch(
        p0, p1,
        arrowstyle=style,
        mutation_scale=ms,
        linewidth=lw,
        color=color,
        alpha=alpha,
        shrinkA=0,
        shrinkB=0,
        connectionstyle=f"arc3,rad={rad}"
    )
    ax.add_patch(a)
    return a

def endcap(ax, x, y, size=0.055, color=SOFT, lw=2.2, alpha=0.95):
    """Draw an orthogonal termination marker like '-|' at (x, y)."""
    ax.plot([x, x], [y - size, y + size], color=color, lw=lw, alpha=alpha)

def label(ax, x, y, s, size=12, color=INK, weight="normal", ha="center", va="center"):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight, ha=ha, va=va)

def loop_arrow(ax, center, rx=0.12, ry=0.20,
               theta1=210, theta2=-30,
               color=SOFT, lw=1.8, alpha=0.75, ms=14):
    """
    Draw a U-shaped continuous monitoring arrow.
    The arc is open at the bottom and has a single arrowhead at the top-left.
    """

    cx, cy = center

    # U-shaped arc (open at bottom)
    arc = Arc((cx, cy), 2*rx, 2*ry,
              angle=0,
              theta1=theta1,
              theta2=theta2,
              linewidth=lw,
              color=color,
              alpha=alpha)
    ax.add_patch(arc)

    # Arrowhead at top-left of the U
    th = np.deg2rad(theta1)

    # Endpoint on ellipse
    x_end = cx + rx * np.cos(th)
    y_end = cy + ry * np.sin(th)

    # Tangent direction (ellipse parameterization)
    dx = -rx * np.sin(th)
    dy =  ry * np.cos(th)
    norm = np.hypot(dx, dy)
    dx, dy = dx / norm, dy / norm

    # Short segment for arrowhead
    L = 0.05
    p0 = (x_end - L*dx, y_end - L*dy)
    p1 = (x_end, y_end)

    arrow(ax, p0, p1,
          color=color,
          lw=lw,
          ms=ms,
          alpha=alpha,
          style='-|>')

def loop_arrow(ax, center, rx=0.035, ry=0.32,
                 theta_left=215, theta_right=-35,
                 color=SOFT, lw=1.8, alpha=0.75, ms=12,
                 L=0.05):
    """
    Draw a U-shaped arc (open at bottom) with a single arrowhead at the LEFT end.
    Arrowhead direction is forced to go bottom->top and right->left (into the left end).
    
    Parameters:
      theta_left: angle (deg) for left/top end of U (e.g., 215)
      theta_right: angle (deg) for right/top end of U (e.g., -35)
      L: arrowhead segment length in data coords
    """

    cx, cy = center

    # Draw the U arc from left end to right end
    # (Matplotlib draws the shorter path in increasing angle sense modulo 360;
    #  for typical values like 215 to -35, it produces the "U" above.)
    arc = Arc((cx, cy), 2*rx, 2*ry,
              angle=0,
              theta1=theta_left,
              theta2=theta_right,
              linewidth=lw,
              color=color,
              alpha=alpha)
    ax.add_patch(arc)

    # Place arrowhead at LEFT end (theta_left)
    th = np.deg2rad(theta_left)

    # Endpoint on ellipse
    x_end = cx + rx * np.cos(th)
    y_end = cy + ry * np.sin(th)

    # Tangent direction on ellipse at theta_left (parameter direction increasing theta)
    dx = -rx * np.sin(th)
    dy =  ry * np.cos(th)
    norm = np.hypot(dx, dy)
    dx, dy = dx / norm, dy / norm

    # We want arrow pointing bottom->top AND right->left.
    # If the tangent points the opposite way, flip it.
    # Condition: prefer dx < 0 (leftward) and dy > 0 (upward)
    if not (dx < 0 and dy > 0):
        dx, dy = -dx, -dy

    # Draw arrowhead segment that ends at (x_end, y_end) pointing into it
    p0 = (x_end - L*dx, y_end - L*dy)
    p1 = (x_end, y_end)

    arrow(ax, p0, p1, color=color, lw=lw, ms=ms, alpha=alpha, style='-|>', rad=0.0)

# ----------------------------
# Figure
# ----------------------------
fig, ax = plt.subplots(1, 1, figsize=FIGSIZE)
base_axes(ax)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

fig.suptitle("Dynamic Experiment Design", fontsize=20, y=0.98, color=INK)

# ----------------------------
# Backbone: Cells -> Perturbation -> Live imaging + analysis
# ----------------------------
y_mid = 0.55
x_cells, x_pert, x_live = 0.10, 0.30, 0.52

label(ax, x_cells, y_mid, "Cells", size=14, weight="semibold")
label(ax, x_pert,  y_mid, "Perturbation", size=14, weight="semibold")
label(ax, x_live,  y_mid, "Live-cell imaging\n+ analysis", size=14, weight="semibold")

arrow(ax, (x_cells + 0.06, y_mid), (x_pert - 0.06, y_mid), lw=2.2, style='-|>')
arrow(ax, (x_pert + 0.08, y_mid), (x_live - 0.08, y_mid), lw=2.2, style='-|>')

# Continuous loop around Live-cell node (single direction)
rx=0.10  # width
ry=0.18  # height
theta1=200
theta2=-20

rx=0.07
ry=0.24
theta1=205
theta2=-25
ms=12

rx=0.055
ry=0.28
theta1=210
theta2=-30

rx=0.045
ry=0.32
theta1=215
theta2=-35

rx=0.035
ry=0.32
theta1=215
theta2=-35
ms=25

loop_arrow(ax, center=(x_live, y_mid - 0.14), rx=rx, ry=ry, theta_left=theta1, theta_right=theta2,
           color=SOFT, lw=1.7, alpha=0.70, ms=ms)
#loop_arrow(ax, center=(x_live, y_mid - 0.2), rx=0.05, ry=0.10, theta1=340, theta2=30,
#           color=SOFT, lw=1.7, alpha=0.70, ms=12)
#label(ax, x_live, y_mid + 0.30, "continuous", size=10.5, color=SOFT)

# ----------------------------
# Two branches out of Live:
#  (A) No sorting -> orthogonal end-cap
#  (B) Sorting
# ----------------------------
# Branch A: a plain line to an end-cap (no arrowhead triangle)
x_stop, y_stop = 0.70, 0.78
arrow(ax, (x_live + 0.10, y_mid + 0.02), (x_stop - 0.02, y_stop),
      lw=2.0, ms=1, alpha=0.75, style='-')
endcap(ax, x_stop - 0.02, y_stop, size=0.03)
label(ax, x_stop, y_stop, "no sorting", size=12, color=SOFT, ha="left")

# Branch B: Sorting (keep arrowhead)
x_sort, y_sort = 0.74, 0.42
label(ax, x_sort, y_sort, "Sorting", size=14, weight="semibold")
arrow(ax, (x_live + 0.10, y_mid - 0.02), (x_sort - 0.06, y_sort), lw=2.2, alpha=0.9, style='-|>')
label(ax, (x_live + x_sort)/2 + 0.02, (y_mid + y_sort)/2 - 0.15, "sometimes", size=12, color=SOFT)

# ----------------------------
# Fan-out from Sorting to multiple assays (arrowheads OK here)
# ----------------------------
x_assay = 0.92
ys = [0.25, 0.42, 0.59]  # 3 assays

for i, y in enumerate(ys, start=1):
    label(ax, x_assay, y, f"Assay {4 - i}", size=14.0, weight="semibold")
    rad = (y - y_sort) * 0.8
    arrow(ax, (x_sort + 0.07, y_sort), (x_assay - 0.06, y), lw=2.0, alpha=0.9, rad=rad, style='-|>')

label(ax, 0.84, 0.10, "one experiment → multiple downstream readouts", size=12, color=SOFT)

plt.tight_layout()
plt.show()


# %%
save_path="../docs/assets/images/biounfold-021-dynamic-experiment-design.png"
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

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
from matplotlib.patches import (
    FancyBboxPatch, Circle, Ellipse, Rectangle, FancyArrowPatch
)
import numpy as np

# ------------------------------------------------------------
# Simplified BioUnfold #24 figure
# Panels:
#   Single binding | Selectivity | Cellular context | Organism
# ------------------------------------------------------------

ACCENT = "#4C78A8"
DARK = "#222222"
MID = "#666666"
LIGHT = "#D9D9D9"
VERY_LIGHT = "#F6F6F6"

fig, ax = plt.subplots(figsize=(13.5, 5.2))
ax.set_xlim(0, 100)
ax.set_ylim(0, 42)
ax.axis("off")

# ----------------------------
# Helpers
# ----------------------------
def rounded_panel(x, y, w, h, title):
    panel = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.5,rounding_size=2.0",
        linewidth=1.2,
        edgecolor=MID,
        facecolor=VERY_LIGHT
    )
    ax.add_patch(panel)
    ax.text(x + w / 2, y + h - 1.0, title, ha="center", va="top",
            fontsize=12, color=DARK, fontweight="bold")
    return panel

def arrow(x1, y1, x2, y2, lw=1.8, color=MID, ms=11, style="-|>"):
    arr = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=style,
        mutation_scale=ms,
        linewidth=lw,
        color=color,
        shrinkA=0, shrinkB=0
    )
    ax.add_patch(arr)

def molecule(x, y, scale=1.0, color=ACCENT):
    pts = np.array([
        [0.0, 0.0],
        [1.1, 0.7],
        [2.2, 0.0],
        [3.3, 0.8],
        [4.4, 0.0]
    ]) * scale
    xs = x + pts[:, 0]
    ys = y + pts[:, 1]
    ax.plot(xs, ys, color=color, linewidth=2.2)
    for px, py in zip(xs, ys):
        ax.add_patch(Circle((px, py), 0.22 * scale, facecolor=color, edgecolor=color))

def protein(x, y, w=3.0, h=1.6, color="#E8E8E8"):
    rect = FancyBboxPatch(
        (x - w/2, y - h/2),
        w, h,
        boxstyle="round,pad=0.2,rounding_size=0.6",
        facecolor=color,
        edgecolor=MID,
        linewidth=1.0
    )
    ax.add_patch(rect)


def location_blob(x, y, w=5.5, h=3.5, color=LIGHT, edge=MID):
    ax.add_patch(Ellipse((x, y), w, h, facecolor=color, edgecolor=edge, linewidth=1.2))

def small_node(x, y, r=0.55, color=ACCENT):
    ax.add_patch(Circle((x, y), r, facecolor=color, edgecolor=color))

# ----------------------------
# Title
# ----------------------------
ax.text(50, 39.3, "From isolated mechanism to system consequence",
        ha="center", va="center", fontsize=17, fontweight="bold", color=DARK)

# ----------------------------
# Panels
# ----------------------------
panels = [
    (4, 7, 20, 27, "Single binding"),
    (28, 7, 20, 27, "Selectivity"),
    (52, 7, 20, 27, "Cellular context"),
    (76, 7, 20, 27, "Organism"),
]
minimum_fontsize = 13
for p in panels:
    rounded_panel(*p)

# arrows between panels
arrow(24.6, 20.5, 27.2, 20.5, lw=1.5, color=MID)
arrow(48.6, 20.5, 51.2, 20.5, lw=1.5, color=MID)
arrow(72.6, 20.5, 75.2, 20.5, lw=1.5, color=MID)

# ----------------------------
# Panel 1 — Single binding
# ----------------------------
x, y, w, h, _ = panels[0]

molecule(x + 3.6, y + 14.2, scale=0.95)
protein(x + 14.2, y + 15.0, w=7.0, h=4.5, color="#E8E8E8")
arrow(x + 8.2, y + 14.6, x + 10.2, y + 14.9, lw=2.0, color=ACCENT)

ax.text(x + 11, y + 15, "Target", ha="left", va="center", fontsize=minimum_fontsize, color=MID)

# ----------------------------
# Panel 2 — Selectivity
# ----------------------------
x, y, w, h, _ = panels[1]

molecule(x + 3.0, y + 14.0, scale=0.9)

protein(x + 12.0, y + 18.0, w=4.8, h=3.1, color="#E8E8E8")
protein(x + 16.0, y + 14.8, w=4.8, h=3.1, color="#E8E8E8")
protein(x + 12.0, y + 11.5, w=4.8, h=3.1, color="#E8E8E8")
protein(x + 16.2, y + 9.2,  w=4.8, h=3.1, color="#EFE3E3")

arrow(x + 7.8, y + 14.4, x + 10.0, y + 17.0, lw=1.8, color=ACCENT)
arrow(x + 7.9, y + 14.2, x + 13.7, y + 9.9, lw=1.6, color=ACCENT)

# ----------------------------
# Panel 3 — Cellular context
# ----------------------------
x, y, w, h, _ = panels[2]
BLUE_DARK   = "#9EC1E6"
BLUE_MEDIUM = "#C6DCF2"
BLUE_LIGHT  = "#E6F0FA"

# Cell boundary + nucleus
ax.add_patch(Circle((x + 10.0, y + 14.0), 8.0, facecolor="white", edgecolor=MID, linewidth=1.2))
ax.add_patch(Circle((x + 10.0, y + 14.0), 2.7, facecolor=BLUE_LIGHT, edgecolor=LIGHT, linewidth=1.0))

# ax.text(x + 9, y + 14 + 6.0, "Cell", ha="left", va="center", fontsize=minimum_fontsize, color=MID)
# ax.text(x + 9, y + 12 + 2.0, "Nucleus", ha="left", va="center", fontsize=minimum_fontsize, color=MID)

# Molecule outside cell
molecule(x + 0.2, y + 20, scale=0.72)

# a few contextual structures inside cell
# ax.text(x + 6.0, y + 9, "Mitochondria", ha="left", va="center", fontsize=minimum_fontsize, color=MID)
location_blob(x + 6.8, y + 10.4, w=2.8, h=1.8, color=BLUE_MEDIUM, edge=LIGHT)
# ax.text(x + 13.0, y + 16, "Lysosome", ha="left", va="center", fontsize=minimum_fontsize, color=MID)
location_blob(x + 14.9, y + 17.2, w=2.8, h=1.8, color=BLUE_DARK, edge=LIGHT)

# Membrane target
arrow(x + 2.0, y + 18.8, x + 3.0, y + 17.8, lw=1.8, color=ACCENT)

# ----------------------------
# Panel 4 — Organism
# ----------------------------
x, y, w, h, _ = panels[3]
BLUE_DARK   = "#9EC1E6"
BLUE_MEDIUM = "#C6DCF2"
BLUE_LIGHT  = "#E6F0FA"

# Make the figure use more of the available panel space
cx = x + w * 0.5   # body center x
top = y + h * 0.80  # head center y

# Head
ax.add_patch(Circle((cx, top), 2.1, facecolor="white", edgecolor=MID, linewidth=1.1))

# Torso
torso_w = 6.4
torso_h = 11.0
torso_x = cx - torso_w / 2
torso_y = y + h * 0.30
ax.add_patch(Rectangle((torso_x, torso_y), torso_w, torso_h,
                       facecolor="white", edgecolor=MID, linewidth=1.1))

# Arms as trapezoids
left_arm = np.array([
    [torso_x,             torso_y + torso_h - 1.2],
    [torso_x - 0.4,       torso_y + torso_h - 3.0],
    [torso_x - 4.0,       torso_y + torso_h - 6.8],
    [torso_x - 2.8,       torso_y + torso_h - 4.8],
])
right_arm = np.array([
    [torso_x + torso_w,   torso_y + torso_h - 1.2],
    [torso_x + torso_w + 0.4, torso_y + torso_h - 3.0],
    [torso_x + torso_w + 4.0, torso_y + torso_h - 6.8],
    [torso_x + torso_w + 2.8, torso_y + torso_h - 4.8],
])
ax.add_patch(plt.Polygon(left_arm,  closed=True, facecolor="white", edgecolor=MID, linewidth=1.1))
ax.add_patch(plt.Polygon(right_arm, closed=True, facecolor="white", edgecolor=MID, linewidth=1.1))

# Legs as trapezoids
left_leg = np.array([
    [torso_x + 0.9,       torso_y],
    [torso_x + 1.8,       torso_y],
    [torso_x - 0.8,       torso_y - 6.8],
    [torso_x - 2.0,       torso_y - 6.8],
])
right_leg = np.array([
    [torso_x + torso_w - 1.8, torso_y],
    [torso_x + torso_w - 0.9, torso_y],
    [torso_x + torso_w + 2.0, torso_y - 6.8],
    [torso_x + torso_w + 0.8, torso_y - 6.8],
])
ax.add_patch(plt.Polygon(left_leg,  closed=True, facecolor="white", edgecolor=MID, linewidth=1.1))
ax.add_patch(plt.Polygon(right_leg, closed=True, facecolor="white", edgecolor=MID, linewidth=1.1))

# Organs
# Heart on the right-hand side of the torso rectangle
heart = (torso_x + torso_w * 0.72, torso_y + torso_h * 0.67)
liver = (torso_x + torso_w * 0.50, torso_y + torso_h * 0.48)
kidney_l = (torso_x + torso_w * 0.15, torso_y + torso_h * 0.28)
kidney_r = (torso_x + torso_w * 0.85, torso_y + torso_h * 0.28)

ax.add_patch(Circle(heart, 0.95, facecolor=BLUE_DARK, edgecolor=MID, linewidth=0.9))
ax.add_patch(Circle(liver, 1.10, facecolor=BLUE_MEDIUM, edgecolor=MID, linewidth=0.9))
ax.add_patch(Circle(kidney_l, 0.78, facecolor=BLUE_LIGHT, edgecolor=MID, linewidth=0.9))
ax.add_patch(Circle(kidney_r, 0.78, facecolor=BLUE_LIGHT, edgecolor=MID, linewidth=0.9))

# Labels
#ax.text(heart[0] + 1, heart[1], "Heart", ha="left", va="center", fontsize=minimum_fontsize, color=MID)
#ax.text(liver[0] + 1, liver[1], "Liver", ha="left", va="center", fontsize=minimum_fontsize, color=MID)
#ax.text(kidney_r[0] + 1, kidney_r[1] - 0.1, "Kidneys", ha="left", va="center", fontsize=minimum_fontsize, color=MID)

# Incoming perturbation
molecule(x + 1.8, y + h * 0.78, scale=0.78)
arrow(x + 5.6, y + h * 0.79, cx - 1.4, top - 1.4, lw=1.8, color=ACCENT)

plt.tight_layout()
plt.show()

# %%
save_path="../docs/assets/images/biounfold-024-toxicity.png"
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

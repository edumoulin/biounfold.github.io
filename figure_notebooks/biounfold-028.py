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
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch
import numpy as np

fig, ax = plt.subplots(figsize=(12, 5.5))
ax.set_xlim(0, 12)
ax.set_ylim(0, 6)
ax.axis("off")

# ---------- Helper functions ----------

def add_node(ax, x, y, r=0.16, facecolor="white", edgecolor="black", linewidth=1.5):
    circ = Circle((x, y), r, facecolor=facecolor, edgecolor=edgecolor, linewidth=linewidth)
    ax.add_patch(circ)

def add_arrow(ax, start, end, connectionstyle="arc3,rad=0", linewidth=1.4, alpha=0.8):
    arrow = FancyArrowPatch(
        start, end,
        arrowstyle="-|>",
        mutation_scale=12,
        linewidth=linewidth,
        color="black",
        alpha=alpha,
        connectionstyle=connectionstyle
    )
    ax.add_patch(arrow)

def add_label_box(ax, x, y, text, width=2.5, height=0.55, fontsize=10):
    box = FancyBboxPatch(
        (x - width / 2, y - height / 2),
        width,
        height,
        boxstyle="round,pad=0.08,rounding_size=0.08",
        facecolor="white",
        edgecolor="black",
        linewidth=1.0
    )
    ax.add_patch(box)
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize)

# ---------- Title ----------

ax.text(6, 5.6, "From isolated hits to structured evidence",
        ha="center", va="center", fontsize=18, fontweight="bold")

# ---------- Panel labels ----------

ax.text(1.5, 5.0, "1. Single hit", ha="center", fontsize=12, fontweight="bold")
ax.text(6.0, 5.0, "2. Plate-wide expansion", ha="center", fontsize=12, fontweight="bold")
ax.text(10.2, 5.0, "3. Recurring signal", ha="center", fontsize=12, fontweight="bold")

# ---------- Panel 1: Single hit ----------

hit_x, hit_y = 1.5, 3.2
add_node(ax, hit_x, hit_y, r=0.26, linewidth=1.8)
ax.text(hit_x, hit_y - 0.6, "Active", ha="center", fontsize=10)

add_label_box(
    ax, 1.5, 1.4,
    "Ambiguous\nartifact? off-target? real?",
    width=2.3, height=0.9, fontsize=9
)

add_arrow(ax, (2.0, 3.2), (3.3, 3.2))

# ---------- Panel 2: Expansion ----------

center_x, center_y = 4.0, 3.2
add_node(ax, center_x, center_y, r=0.22, linewidth=1.6)
ax.text(center_x, center_y - 0.55, "Starting\npoint", ha="center", fontsize=9)

np.random.seed(8)
angles = np.linspace(-1.25, 1.25, 14)
radii = np.array([1.2, 1.5, 1.35, 1.65, 1.4, 1.7, 1.25, 1.6, 1.35, 1.55, 1.45, 1.65, 1.3, 1.5])

positions = []
for angle, radius in zip(angles, radii):
    x = center_x + 2.2 + radius * np.cos(angle)
    y = center_y + radius * np.sin(angle)
    positions.append((x, y))

active_indices = {2, 5, 8, 11}

for i, (x, y) in enumerate(positions):
    rad = 0.15 if y > center_y else -0.15
    add_arrow(ax, (center_x + 0.25, center_y), (x - 0.18, y),
              connectionstyle=f"arc3,rad={rad}", linewidth=0.9, alpha=0.45)

    if i in active_indices:
        add_node(ax, x, y, r=0.17, facecolor="black")
    else:
        add_node(ax, x, y, r=0.14)

ax.text(6.2, 1.05,
        "Many expansions\nMost inactive, some active",
        ha="center", fontsize=10)

add_arrow(ax, (8.2, 3.2), (9.2, 3.2))

# ---------- Panel 3: Evidence ----------

evidence_positions = [(10.0, 3.9), (10.55, 3.45), (9.85, 2.9), (10.65, 2.75)]
for x, y in evidence_positions:
    add_node(ax, x, y, r=0.19, facecolor="black")

group = Circle((10.3, 3.2), 0.9, fill=False, linestyle="--", linewidth=1.4)
ax.add_patch(group)

add_label_box(
    ax, 10.3, 1.4,
    "Evidence\nsignal survives expansion",
    width=2.4, height=0.9, fontsize=9
)

# ---------- Legend ----------

add_node(ax, 4.2, 0.35, r=0.09)
ax.text(4.4, 0.35, "inactive / no clear signal", va="center", fontsize=9)

add_node(ax, 6.4, 0.35, r=0.09, facecolor="black")
ax.text(6.6, 0.35, "active signal", va="center", fontsize=9)

plt.tight_layout()
plt.show()

# %%
save_path="../docs/assets/images/biounfold-028-plate-wide-chemistry.png"
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

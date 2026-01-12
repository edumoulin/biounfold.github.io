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

rng = np.random.default_rng(3)

# -------------------------
# Synthetic embedding points
# -------------------------
centers = {
    "green":  np.array([-1.0,  0.6]),
    "red":    np.array([-0.6,  0.9]),
    "orange": np.array([ 0.7, -0.4]),
    "blue":   np.array([ 1.1, -0.1]),
}

colors = {
    "green":  "#2ca02c",
    "red":    "#d62728",
    "orange": "#ff7f0e",
    "blue":   "#1f77b4",
}

def cloud(center, n=25, scale=0.18):
    return center + rng.normal(0, scale, size=(n, 2))

points = {k: cloud(v) for k, v in centers.items()}

# -------------------------
# Figure layout
# -------------------------
fig, axes = plt.subplots(
    1, 3, figsize=(8.4, 2.7),
    gridspec_kw={
        "wspace": 0.10,
        "right": 0.90 
    }
)

# -------------------------
# Panel 1 — What we measure
# -------------------------
ax = axes[0]
for k in points:
    ax.scatter(points[k][:, 0], points[k][:, 1],
               s=22, color=colors[k], alpha=0.85)

ax.set_title("Measurements", fontsize=18)
ax.set_xlabel("embedding dim 1")
ax.set_ylabel("embedding dim 2")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="both", which="both", labelsize=9)
ax.xaxis.label.set_alpha(0.7)
ax.yaxis.label.set_alpha(0.7)

# -------------------------
# Panel 2 — What we know
# -------------------------
ax = axes[1]

# Symbols
ax.scatter([0.30], [0.70], s=140, color=colors["green"])
ax.scatter([0.70], [0.70], s=140, color=colors["red"])
ax.text(0.50, 0.70, "=", fontsize=20, ha="center", va="center")

ax.scatter([0.30], [0.40], s=140, color=colors["orange"])
ax.scatter([0.70], [0.40], s=140, color=colors["blue"])
ax.text(0.50, 0.40, "=", fontsize=20, ha="center", va="center")

ax.set_title("Knowledge", fontsize=18)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)
ax.set_facecolor("#f7f7f7")
bbox = ax.get_position()
rect = Rectangle(
    (bbox.x0, 0),
    bbox.width,
    1.0,
    transform=fig.transFigure,
    color="#f7f7f7",
    zorder=0,
    linewidth=0
)
fig.add_artist(rect)

# -------------------------
# Panel 3 — What we want to know
# -------------------------
ax = axes[2]

ax.scatter([0.35], [0.6], s=140, color=colors["green"])
ax.scatter([0.65], [0.6], s=140, color=colors["orange"])
ax.text(0.50, 0.6, "?", fontsize=24, ha="center", va="center")

ax.set_title("Hypothesis", fontsize=18)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout()
plt.show()

# %%
save_path="../docs/assets/images/biounfold-014-measurements-knowledge-hypothesis.png"
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

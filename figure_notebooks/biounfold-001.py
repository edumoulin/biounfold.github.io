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
from matplotlib.patches import Ellipse
import matplotlib.cm as cm

# ----- Output size (LinkedIn) -----
W_PX, H_PX = 1200, 639
DPI = 300  # exact pixels = inches * dpi
W_IN, H_IN = W_PX / DPI, H_PX / DPI

# ----- Canvas -----
fig, ax = plt.subplots(figsize=(W_IN, H_IN), dpi=DPI)
ax.set_aspect('equal')
ax.axis('off')
fig.patch.set_facecolor("white")  # explicit background

# ----- Layout -----
# Ellipses: wider than tall to free horizontal space
rx, ry = 1.55, 1.05         # radii (x, y)
cx_L, cy_L = -1.05, 0.00    # left center
cx_R, cy_R =  1.05, 0.00    # right center

# Colors (single hue family, subtle shift)
cmap = cm.get_cmap("PuBuGn")
col_L = cmap(0.55)
col_R = cmap(0.75)

# Draw ellipses (slightly translucent)
left  = Ellipse((cx_L, cy_L), 2*rx, 2*ry, facecolor=col_L, edgecolor='black', linewidth=0.8, alpha=0.42, zorder=1)
right = Ellipse((cx_R, cy_R), 2*rx, 2*ry, facecolor=col_R, edgecolor='black', linewidth=0.8, alpha=0.42, zorder=1)
ax.add_patch(left); ax.add_patch(right)

# ----- Labels (smaller, shifted) -----
fs_main = 13   # main label size
fs_mid  = 11   # overlap label size
y_up    = 0.22 # Biology/AI up-shift
y_down  = -0.22# Drug Development down-shift

ax.text(cx_L - 0.3, y_up, "Biology", ha='center', va='center', fontsize=fs_main, weight='bold', zorder=2)
ax.text(cx_R + 0.3, y_up, "AI",      ha='center', va='center', fontsize=fs_main, weight='bold', zorder=2)
ax.text(0.0, y_down, "Drug\nDiscovery", ha='center', va='center', fontsize=fs_mid, zorder=2)

# ----- Framing (fixed limits so margins stay consistent) -----
# Add gentle margins around the widest points
marg_x, marg_y = 0.45, 0.40
x_min = min(cx_L - rx, cx_R - rx) - marg_x
x_max = max(cx_L + rx, cx_R + rx) + marg_x
y_min = -ry - marg_y - 0.15  # a touch more room below for the overlap label
y_max =  ry + marg_y
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
plt.show()


# %%
# ----- Save exact pixel size for LinkedIn -----
out_base = "../docs/assets/images/biounfold-001-venn-li"
fig.savefig(f"{out_base}.png", dpi=DPI, transparent=True)

# %%

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
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D

# ----------------------------
# Style knobs (match your aesthetic)
# ----------------------------
FIGSIZE = (12.0, 3.1)   # wide for blog/social
BG = "#f7f7f7"
INK = "#222222"
SOFT = "#666666"

def base_axes(ax):
    ax.set_facecolor(BG)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

def add_trapezoid(ax, x0, x1, h0, h1, y=0.0, **kwargs):
    """Horizontal trapezoid centered on y."""
    pts = [(x0, y - h0/2), (x0, y + h0/2),
           (x1, y + h1/2), (x1, y - h1/2)]
    poly = Polygon(pts, closed=True, **kwargs)
    ax.add_patch(poly)
    return poly

def center_label(ax, x0, x1, text, y=0.0, size=11, weight="regular"):
    ax.text((x0+x1)/2, y, text, ha="center", va="center",
            fontsize=size, color=INK, weight=weight)

# ----------------------------
# Plot
# ----------------------------
fig, ax = plt.subplots(figsize=FIGSIZE)
base_axes(ax)

ax.set_xlim(0, 10)
ax.set_ylim(-1.7, 1.7)

# Funnel geometry (left -> right)
x_width = 1.7
x_start = 0.6
segments = [
    # label,                 x0,  x1,   h0,   h1
    ("Pseudo-Simulation",      0.6, x_start+x_width, 3.0, 2),
    ("Filtering\nplausibility",x_start+x_width, x_start+2*x_width, 2, 1.25),
    ("Experiment",             x_start+2*x_width, x_start+3*x_width, 1.25, 0.75),
    ("Simulation", x_start+3*x_width, x_start+4*x_width, 0.75, 0.5),
    ("Auditing", x_start+4*x_width, x_start+5*x_width, 0.5, 0.25),
]

# Draw trapezoids (outline only)
for label, x0, x1, h0, h1 in segments:
    add_trapezoid(
        ax, x0, x1, h0, h1,
        facecolor=BG, edgecolor=INK,
        linewidth=1.7, joinstyle="round"
    )
    center_label(ax, x0, x1, label, size=11)

# Subtle direction arrow along the centerline
#ax.add_line(Line2D([0.55, 9.75], [0, 0], lw=1.2, color=SOFT, alpha=0.35,
#                   solid_capstyle="round"))
ax.annotate(
    "", xy=(x_start+5*x_width+0.25, 0), xytext=(x_start+5*x_width, 0),
    arrowprops=dict(arrowstyle="-|>", lw=1.2, color=SOFT, alpha=0.55)
)

fig.suptitle("Where Simulation Now Lives", fontsize=30.0, y=0.98, color=INK)
plt.tight_layout()
plt.show()

# %%
save_path="../docs/assets/images/biounfold-017-where-simulation-now-lives.png"
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

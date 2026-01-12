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
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch, Circle
from matplotlib.lines import Line2D

# ----------------------------
# Style knobs
# ----------------------------
FIGSIZE = (9.6, 3.1)
BG = "#f7f7f7"
INK = "#222222"
SOFT = "#666666"

def base_axes(ax):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_facecolor(BG)

def draw_house_outline(ax):
    # Ground
    ground = Line2D([0.8, 9.2], [1.0, 1.0], lw=2.0, color=INK, alpha=0.9)
    ax.add_line(ground)

    # Walls
    walls = Rectangle((2.2, 1.0), 5.6, 3.2, fill=False, lw=2.0, edgecolor=INK, alpha=0.95)
    ax.add_patch(walls)

    # Roof
    roof = Polygon([[2.0, 4.2], [5.0, 6.2], [8.0, 4.2]], closed=True,
                   fill=False, lw=2.0, edgecolor=INK, alpha=0.95)
    ax.add_patch(roof)

def add_door_window(ax):
    # Door
    door = Rectangle((4.6, 1.0), 0.8, 1.6, fill=False, lw=1.6, edgecolor=INK, alpha=0.9)
    ax.add_patch(door)
    knob = Circle((5.25, 1.8), 0.06, color=INK, alpha=0.8)
    ax.add_patch(knob)

    # Window
    window = Rectangle((3.1, 2.2), 1.2, 1.0, fill=False, lw=1.6, edgecolor=INK, alpha=0.9)
    ax.add_patch(window)
    ax.add_line(Line2D([3.1, 4.3], [2.7, 2.7], lw=1.0, color=INK, alpha=0.7))
    ax.add_line(Line2D([3.7, 3.7], [2.2, 3.2], lw=1.0, color=INK, alpha=0.7))

def add_chimney_and_stickman(ax):
    chimney = Rectangle((6.3, 4.9), 0.35, 1.0, fill=True,
                        lw=1.6, edgecolor=INK, facecolor=BG, alpha=1.0)
    ax.add_patch(chimney)

    # Smoke hint
    ax.plot([6.45, 6.6], [6.0, 6.3], lw=1.0, color=SOFT, alpha=0.6)
    ax.plot([6.6, 6.45], [6.25, 6.55], lw=1.0, color=SOFT, alpha=0.6)

    # Stick-man
    head = Circle((5.9, 2.3), 0.18, fill=False, lw=1.4, edgecolor=INK, alpha=0.9)
    ax.add_patch(head)
    ax.plot([5.9, 5.9], [2.1, 1.4], lw=1.4, color=INK, alpha=0.9)
    ax.plot([5.6, 6.2], [1.9, 1.9], lw=1.2, color=INK, alpha=0.9)
    ax.plot([5.9, 5.6], [1.4, 1.0], lw=1.2, color=INK, alpha=0.9)
    ax.plot([5.9, 6.2], [1.4, 1.0], lw=1.2, color=INK, alpha=0.9)

def add_caption(fig, text):
    fig.text(0.5, 0.03, text, ha="center", va="bottom",
             fontsize=10.5, color=SOFT, alpha=0.95)

def add_between_axes_arrow(fig, ax_left, ax_right, lw=3.0, ms=18):
    """
    Draw a thick arrow in figure coordinates between two axes.
    """
    b0 = ax_left.get_position()
    b1 = ax_right.get_position()

    x0 = b0.x1 + 0.006
    x1 = b1.x0 - 0.006
    y = (b0.y0 + b0.y1) / 2.0

    arrow = FancyArrowPatch(
        (x0, y), (x1, y),
        transform=fig.transFigure,
        arrowstyle="-|>",
        mutation_scale=ms,
        linewidth=lw,
        color=INK,
        alpha=0.9,
        shrinkA=0,
        shrinkB=0
    )
    fig.add_artist(arrow)

def label(ax, x, y, text, ha="left", va="center", alpha=0.75):
    ax.text(x, y, text, fontsize=9, color=SOFT, ha=ha, va=va, alpha=alpha)

# ----------------------------
# Build figure
# ----------------------------
fig, axes = plt.subplots(1, 3, figsize=FIGSIZE, gridspec_kw={"wspace": 0.16})

for ax in axes:
    base_axes(ax)

# Panel 1: minimal encoding
draw_house_outline(axes[0])

# Panel 2: richer encoding
draw_house_outline(axes[1])
add_door_window(axes[1])

# Panel 3: usable encoding (context + agent)
draw_house_outline(axes[2])
add_door_window(axes[2])
add_chimney_and_stickman(axes[2])

label(axes[0], 3.5, 3.85, "Encoding v1", ha="left", va="center", alpha=0.65)
label(axes[1], 3.5, 3.85, "Encoding v2", ha="left", va="center", alpha=0.65)
label(axes[2], 3.5, 3.85, "Encoding v3", ha="left", va="center", alpha=0.65)


# Title
fig.suptitle("Data Encoding Evolves", fontsize=18, y=0.98, color=INK)

# Arrows between panels
add_between_axes_arrow(fig, axes[0], axes[1], lw=3.2, ms=18)
add_between_axes_arrow(fig, axes[1], axes[2], lw=3.2, ms=18)

# Less-literal caption
add_caption(fig, "Data systems evolve by introducing new entities and relationships that change what the organization can do.")

plt.show()


# %%
save_path="../docs/assets/images/biounfold-015-hidden-theory-of-biology.png"
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

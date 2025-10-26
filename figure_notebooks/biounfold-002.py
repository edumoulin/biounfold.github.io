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
from matplotlib.patches import Wedge, FancyArrowPatch
from matplotlib import patheffects as pe


def make_figure(
    theta_deg: float = 28,   # half-angle of cone (narrow)
    r_max: float = 1.15,     # overall scale
    opt_r: float = 0.96,     # radius of the "optimal solution"
    opt_ang: float = 0.15,   # angle of "optimal solution" (radians; 0 = straight ahead)
    n_paths: int = 6,        # number of phenotypic paths
    seed: int = 7,           # RNG seed for reproducibility
    width_px: int = 1200,    # LinkedIn width
    height_px: int = 639,    # LinkedIn height
    dpi: int = 100,          # export DPI for PNG
):
    # Colors
    blue = "#1f77b4"        # target-based
    green = "#2ca02c"       # phenotypic
    green_light = "#b7e1b5" # cone fill
    orange = "#d66000"      # Optimal point
    ring_color = "#c7c7c7"  # background rings

    np.random.seed(seed)

    fig_w, fig_h = width_px / dpi, height_px / dpi
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
    #ax.set_aspect("equal")
    ax.axis("off")

    # Background rings (progress cues)
    rings = np.linspace(0.25, r_max, 4)
    for rr in rings:
        circ = plt.Circle((0, 0), rr, fill=False, linewidth=0.8, alpha=0.35, edgecolor=ring_color)
        ax.add_patch(circ)

    # Phenotypic search cone
    cone = Wedge(
        center=(0, 0),
        r=r_max,
        theta1=-theta_deg,
        theta2=theta_deg,
        width=r_max * 0.98,
        facecolor=green_light,
        edgecolor=green,
        linewidth=1.2,
        alpha=0.9,
    )
    ax.add_patch(cone)

    # Phenotypic exploratory paths
    angles = np.linspace(-np.deg2rad(theta_deg-5), np.deg2rad(theta_deg-5), n_paths)
    angles += np.deg2rad(np.random.uniform(-theta_deg * 0.12, theta_deg * 0.12, size=n_paths))
    for ang in angles:
        r_end = r_max * np.random.uniform(0.55, 0.92)
        x2, y2 = r_end * np.cos(ang), r_end * np.sin(ang)
        arr = FancyArrowPatch(
            (0, 0), (x2, y2),
            arrowstyle="-|>",
            mutation_scale=16,
            linewidth=1.8,
            alpha=0.75,
            color=green,
        )
        # subtle white stroke to lift from background
        arr.set_path_effects([pe.Stroke(linewidth=2.6, foreground="white", alpha=0.6), pe.Normal()])
        ax.add_patch(arr)

    # Target-based straight path (clarity)
    tb = FancyArrowPatch(
        (0, 0), (r_max * 0.95, 0),
        arrowstyle="-|>",
        mutation_scale=22,
        linewidth=3.0,
        color=blue,
        alpha=0.95,
    )
    tb.set_path_effects([pe.Stroke(linewidth=4.2, foreground="white", alpha=0.8), pe.Normal()])
    ax.add_patch(tb)

    # Optimal solution marker
    x_opt, y_opt = opt_r * np.cos(opt_ang), opt_r * np.sin(opt_ang)
    opt = ax.plot([x_opt], [y_opt], marker="o", ms=11, color=orange, zorder=5)[0]
    opt.set_path_effects([pe.Stroke(linewidth=4, foreground="white", alpha=0.9), pe.Normal()])
    ax.text(x_opt - 0.040, 
            y_opt + 0.05, 
            "Optimal\nsolution", 
            fontsize=18, 
            ha="left", 
            va="bottom", 
            color=orange, 
            path_effects=[pe.Stroke(linewidth=1, foreground=orange), pe.Normal()]
           )

    # Labels
    ax.text(r_max * 0.8, 
            -0.11, 
            "Clarity (target-based)", 
            fontsize=18, 
            ha="center", 
            va="top", 
            color=blue, 
            path_effects=[pe.Stroke(linewidth=1, foreground=blue), pe.Normal()])
    ax.text(
        r_max * 0.34 * np.cos(np.deg2rad(theta_deg * 0.92)),
        r_max * 0.34 * np.sin(np.deg2rad(theta_deg * 0.92)),
        "Discovery (phenotypic)",
        rotation=theta_deg * 0.3,
        fontsize=18,
        ha="center",
        va="bottom",
        color=green, 
        path_effects=[pe.Stroke(linewidth=1, foreground=green), pe.Normal()]
    )

    # Start marker
    ax.text(-0.0, 
            -0.09, 
            "Start", 
            fontsize=18, 
            ha="right", 
            va="center", 
            alpha=0.8,
            path_effects=[pe.Stroke(linewidth=1, foreground="black"), pe.Normal()])
    ax.plot([0], [0], marker="o", ms=4, color="black", alpha=0.8)

    # Frame and limits
    m = 0.14
    ax.set_xlim(-m, r_max + m * 0.4)   # extra space on the right for labels
    ax.set_ylim(-r_max - m, r_max + m)
    return fig
dpi = 100
fig = make_figure(dpi=dpi)
plt.show()

# %%
# ----- Save exact pixel size for LinkedIn -----
out_base = "../docs/assets/images/biounfold-002-discovery-clarity"
fig.savefig(f"{out_base}.png", dpi=dpi, transparent=True)

# %%

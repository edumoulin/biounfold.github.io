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
from matplotlib.patches import Ellipse
import matplotlib.patheffects as path_effects


def _draw_ellipse(ax, xy, width, height, angle=0,
                  edgecolor="black", facecolor="none",
                  alpha=0.4, lw=1.2):
    e = Ellipse(
        xy=xy,
        width=width,
        height=height,
        angle=angle,
        edgecolor=edgecolor,
        facecolor=facecolor,
        lw=lw,
        alpha=alpha,
    )
    ax.add_patch(e)
    return e


def make_biounfold_011_diagnosis_to_prediction(
    width_px=1600,
    height_px=900,
    dpi=100,
    title="Hit Discovery: From Diagnosis to Prediction",
    caption=(
        "Assay optimization (panel a) focuses on control classes, separation, drift, and QC in the "
        "representation space.\nHit discovery (panel b) operates in a dense space where "
        "the controls anchor the interpretation of emerging hits."
    ),
    seed=42,
):
    """
    BioUnfold #11 figure: two embedding panels (PC1 / PC2).

    (a) Assay optimization (diagnosis)  – sparse, control classes only.
    (b) Hit discovery (prediction)      – dense population + same control classes.

    Returns
    -------
    fig, axes : matplotlib Figure and array of Axes
    """
    rng = np.random.default_rng(seed)

    # -------------------------------------------------------------------------
    # Synthetic "embedding" coordinates for visualization
    # -------------------------------------------------------------------------
    # Six control classes: NEG, POS, Tool 1–4
    control_specs = {
        "NEG":    {"mean": (-1.8, -0.4), "scale": (0.22, 0.20)},
        "POS":    {"mean": ( 1.0,  0.6), "scale": (0.22, 0.20)},
        "Tool 1": {"mean": ( 0.0, -0.8), "scale": (0.22, 0.18)},
        "Tool 2": {"mean": ( 0.1,  1.2), "scale": (0.22, 0.18)},
        "Tool 3": {"mean": ( 1.6,  -0.3), "scale": (0.22, 0.18)},
        "Tool 4": {"mean": ( 1.9,  1.0), "scale": (0.22, 0.18)},
    }

    control_colors = {
        "NEG":    "#4C6FAE",  # muted blue
        "POS":    "#2E8B57",  # muted green
        "Tool 1": "#BC5090",  # magenta
        "Tool 2": "#FF7F0E",  # orange
        "Tool 3": "#9467BD",  # purple
        "Tool 4": "#1F77B4",  # blue variant
    }

    n_per_class = 35

    controls = {}
    for name, spec in control_specs.items():
        mean = np.array(spec["mean"])
        scale = np.array(spec["scale"])
        pts = rng.normal(loc=mean, scale=scale, size=(n_per_class, 2))
        controls[name] = pts

    # Dense background "screen" for hit discovery panel
    screen_bg = rng.normal(loc=[0.0, 0.1], scale=[1.4, 1.1], size=(500, 2))

    # Combined limits so both panels share the same PC space
    all_x = np.concatenate([screen_bg[:, 0]] + [pts[:, 0] for pts in controls.values()])
    all_y = np.concatenate([screen_bg[:, 1]] + [pts[:, 1] for pts in controls.values()])
    x_pad, y_pad = 0.5, 0.5
    x_min, x_max = all_x.min() - x_pad, all_x.max() + x_pad
    y_min, y_max = all_y.min() - y_pad, all_y.max() + y_pad

    # -------------------------------------------------------------------------
    # Figure and axes
    # -------------------------------------------------------------------------
    fig_w, fig_h = width_px / dpi, height_px / dpi
    fig, axes = plt.subplots(1, 2, figsize=(fig_w, fig_h), dpi=dpi)
    ax_opt, ax_hit = axes

    # -------------------------------------------------------------------------
    # Left panel: Assay optimization (diagnosis) – (a)
    # -------------------------------------------------------------------------
    for name, pts in controls.items():
        ax_opt.scatter(
            pts[:, 0], pts[:, 1],
            s=32, alpha=0.9,
            color=control_colors[name],
            label=name
        )

    # Ellipses around NEG and POS to evoke "assay window" / separation
    _draw_ellipse(ax_opt, xy=control_specs["NEG"]["mean"], width=1.0, height=0.9,
                  edgecolor=control_colors["NEG"], alpha=0.4, lw=1.4)
    _draw_ellipse(ax_opt, xy=control_specs["POS"]["mean"], width=1.0, height=0.9,
                  edgecolor=control_colors["POS"], alpha=0.4, lw=1.4)

    txt = ax_opt.text(
        0.03, 0.96,
        "(a) Assay optimization",
        transform=ax_opt.transAxes,
        ha="left", va="top", fontsize=30, weight="bold",
        color="black",
    )
    txt.set_path_effects([path_effects.withStroke(linewidth=3, foreground="white", alpha=0.85)])

    # -------------------------------------------------------------------------
    # Right panel: Hit discovery (prediction) – (b)
    # -------------------------------------------------------------------------
    # Dense background of screened compounds (neutral grey)
    ax_hit.scatter(
        screen_bg[:, 0], screen_bg[:, 1],
        s=12, alpha=0.35,
        color="#BBBBBB",
        label="Screened compounds"
    )

    # Same control classes as in optimization panel
    for name, pts in controls.items():
        ax_hit.scatter(
            pts[:, 0], pts[:, 1],
            s=30, alpha=0.95,
            color=control_colors[name],
            label=name
        )

    txt2 = ax_hit.text(
        0.03, 0.96,
        "(b) Hit discovery",
        transform=ax_hit.transAxes,
        ha="left", va="top", fontsize=30, weight="bold",
        color="black",
    )
    txt2.set_path_effects([path_effects.withStroke(linewidth=3, foreground="white", alpha=0.85)])

    # -------------------------------------------------------------------------
    # Shared axis limits, labels, styling, and grid
    # -------------------------------------------------------------------------
    # Define a small set of tick locations to support the grid
    x_ticks = np.linspace(np.floor(x_min), np.ceil(x_max), 5)
    y_ticks = np.linspace(np.floor(y_min), np.ceil(y_max), 5)

    for ax in axes:
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

        ax.set_xlabel("PC1 (assay representation)", labelpad=10, fontsize=24)
        if ax is ax_opt:
            ax.set_ylabel("PC2", labelpad=10, fontsize=24)
        else:
            ax.set_ylabel("")

        ax.set_xticks(x_ticks)
        ax.set_yticks(y_ticks)

        # Light grid, but hide tick labels for a clean look
        ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.25)
        ax.set_xticklabels([])
        ax.set_yticklabels([])

        # Remove spines
        for spine in ax.spines.values():
            spine.set_visible(False)

    # -------------------------------------------------------------------------
    # Legend – right-hand side
    # -------------------------------------------------------------------------
    handles, labels = ax_hit.get_legend_handles_labels()

    desired_order = ["NEG", "POS", "Tool 1", "Tool 2", "Tool 3", "Tool 4", "Screened compounds"]
    order = [labels.index(lbl) for lbl in desired_order if lbl in labels]

    handles = [handles[i] for i in order]
    labels = [labels[i] for i in order]

    fig.legend(
        handles,
        labels,
        loc="center left",
        bbox_to_anchor=(0.85, 0.5),
        frameon=False,
        fontsize=24,
        handletextpad=0.8,
        columnspacing=1.4,
    )

    # -------------------------------------------------------------------------
    # Global title, caption, and arrow text
    # -------------------------------------------------------------------------
    #fig.suptitle(title, fontsize=36, y=0.97)

    return fig, axes

# Example usage in a notebook:
fig, axes = make_biounfold_011_diagnosis_to_prediction()
plt.show()


# %%
save_path="../docs/assets/images/biounfold-011-from-diagnosis-to-prediction.png"
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

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


def make_biounfold_012_exploration_exploitation(
    width_px=1600,
    height_px=900,
    dpi=100,
    title="Lead Optimization: Exploration vs Exploitation Across DMTA Cycles",
    caption=(
        "Exploration is intentionally high in early DMTA cycles and cools over time, "
        "as decisions shift from mapping tolerated chemical space toward refining "
        "PK, safety, and developability."
    ),
    max_cycles=30,
    early_end=10,
    mid_end=20,
):
    """
    BioUnfold #12 figure: exploration vs exploitation over DMTA cycles.

    - Single panel.
    - Exploration starts high and decays over cycles.
    - Exploitation starts low and rises as the program matures.

    Returns
    -------
    fig, ax : matplotlib Figure and Axes
    """
    # -------------------------------------------------------------------------
    # Figure setup
    # -------------------------------------------------------------------------
    fig_w, fig_h = width_px / dpi, height_px / dpi
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)

    # -------------------------------------------------------------------------
    # Curves: exploration and exploitation
    # -------------------------------------------------------------------------
    x = np.linspace(0, max_cycles, 500)

    # Logistic decay for exploration; center roughly in early/mid transition
    center = (early_end + mid_end) / 2.0
    width = (mid_end - early_end) / 2.0 if mid_end > early_end else 3.0

    exploration = 1.0 / (1.0 + np.exp((x - center) / width))
    exploitation = 1.0 - exploration

    # Plot curves
    exploration_line, = ax.plot(
        x,
        exploration,
        label="Exploration",
        linewidth=3.0,
        alpha=0.95,
    )
    exploitation_line, = ax.plot(
        x,
        exploitation,
        label="Exploitation",
        linewidth=3.0,
        alpha=0.95,
    )

    # Soft fills under each curve
    ax.fill_between(x, 0, exploration, alpha=0.12)
    ax.fill_between(x, 0, exploitation, alpha=0.12)

    # -------------------------------------------------------------------------
    # Regime bands: early, middle, late cycles
    # -------------------------------------------------------------------------
    ax.axvspan(0, early_end, alpha=0.06)
    ax.axvspan(early_end, mid_end, alpha=0.04)
    ax.axvspan(mid_end, max_cycles, alpha=0.06)

    # Regime labels (slightly above the top)
    y_label = 1.03
    ax.text(
        0.5 * early_end,
        y_label,
        "Early cycles\nExploration-heavy",
        ha="center",
        va="bottom",
        fontsize=20,
        weight="bold",
        clip_on=False,
    )
    ax.text(
        0.5 * (early_end + mid_end),
        y_label,
        "Middle cycles\nBalanced regime",
        ha="center",
        va="bottom",
        fontsize=20,
        weight="bold",
        clip_on=False,
    )
    ax.text(
        0.5 * (mid_end + max_cycles),
        y_label,
        "Late cycles\nExploitation-heavy",
        ha="center",
        va="bottom",
        fontsize=20,
        weight="bold",
        clip_on=False,
    )

    # -------------------------------------------------------------------------
    # Axes styling
    # -------------------------------------------------------------------------
    ax.set_xlim(0, max_cycles)
    ax.set_ylim(0, 1.1)

    ax.set_xlabel("DMTA cycles in lead optimization", fontsize=24, labelpad=12)
    ax.set_ylabel("Relative emphasis", fontsize=24, labelpad=12)

    # Tick formatting
    ax.set_xticks(np.linspace(0, max_cycles, 7))
    ax.set_yticks(np.linspace(0.0, 1.0, 6))
    ax.tick_params(axis="both", which="major", labelsize=18)

    # Light grid
    ax.grid(True, axis="y", linestyle="--", linewidth=0.6, alpha=0.3)

    # Remove top and right spines for a cleaner look
    for spine_name in ["top", "right"]:
        ax.spines[spine_name].set_visible(False)

    # -------------------------------------------------------------------------
    # Legend
    # -------------------------------------------------------------------------
    legend = ax.legend(
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),   # just outside the right spine, vertically centered
        frameon=False,
        fontsize=20,
        ncol=1,                       # vertical legend
        handlelength=2.8,
        borderaxespad=0.0,
    )


    # -------------------------------------------------------------------------
    # Title and caption
    # -------------------------------------------------------------------------
    if title:
        fig.suptitle(title, fontsize=30, y=0.96)

    if caption:
        fig.text(
            0.5,
            0.04,
            caption,
            ha="center",
            va="top",
            fontsize=16,
        )

    fig.tight_layout(rect=[0.04, 0.08, 0.96, 0.9])

    return fig, ax


fig, ax = make_biounfold_012_exploration_exploitation(caption=False)
plt.show()


# %%
save_path="../docs/assets/images/biounfold-012-learning-the-chemistry.png"
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

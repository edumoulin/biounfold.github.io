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
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
from matplotlib.lines import Line2D
from matplotlib import patheffects as pe


def noncrossing_map(sources, targets, min_in=1, max_in=2, rng=None):
    """Order-preserving wiring from sources -> targets to avoid crossings (adjacent columns)."""
    if rng is None:
        rng = random
    S = len(sources)
    T = len(targets)
    conns = []
    last_used = -1
    for t_idx in range(T):
        center = int(round((t_idx + 0.5) * S / T - 0.5))
        low = max(last_used, center - 1, 0)
        high = min(center + 1, S - 1)
        if low > high:
            low = max(last_used + 1, 0)
            high = min(S - 1, low)
        k = rng.randint(min_in, max_in)
        available = list(range(low, high + 1))
        while len(available) < k and available[-1] < S - 1:
            available.append(available[-1] + 1)
        chosen = sorted(rng.sample(available, k=min(k, len(available))))
        last_used = chosen[-1]
        conns.append(chosen)
    return conns


def layout_columns(n_left_cols=3, n_right_cols=3, seed=7):
    """Build column node positions with a single knee column in the middle."""
    rng = random.Random(seed)
    left_counts = [rng.randint(2, 4) for _ in range(n_left_cols)]
    right_counts = [rng.randint(2, 4) for _ in range(n_right_cols)]
    counts = left_counts + [1] + right_counts
    knee_idx = len(left_counts)

    spacing_x = 2.8
    xs = [i * spacing_x for i in range(len(counts))]

    cols = []
    for c_idx, (x, n) in enumerate(zip(xs, counts)):
        if n == 1 and c_idx == knee_idx:
            cols.append([(x, 1.2)])  # knee lifted above baseline to form the bend
        else:
            total_h = 5.0
            ys = [0.0] if n == 1 else np.linspace(-total_h / 2, total_h / 2, n)
            cols.append([(x, float(y)) for y in ys])
    return cols, knee_idx


def draw_process_knee(
    n_left_cols=3,
    n_right_cols=3,
    seed=7,
    width_px=1200,
    height_px=639,
    dpi=100,
    node_r=0.09,
    arrow_lw=2.0,
    two_back_prob=0.65,  # chance a target also connects to the 2-back column
    knee_error=1.4,      # total error-bar height centered on the knee
    save_png="biounfold_process_knee_1200x639.png",
    save_svg="biounfold_process_knee_1200x639.svg",
):
    rng = random.Random(seed)
    cols, knee_idx = layout_columns(n_left_cols, n_right_cols, seed=seed)
    black = "#000000"
    green = "#2ca02c"

    # Set up figure
    fig_w, fig_h = width_px / dpi, height_px / dpi
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
    ax.axis("off")
    ax.set_aspect("equal")

    # Title
    title_pe = [pe.Stroke(linewidth=1, foreground=black), pe.Normal()]
    all_x = [x for col in cols for (x, _) in col]
    all_y = [y for col in cols for (_, y) in col]
    ax.text(
        (min(all_x) + max(all_x)) / 2,
        max(all_y) + 1.2,
        "Where AI matters most",
        ha="center",
        va="center",
        fontsize=30,
        color=black,
        path_effects=title_pe,
    )

    # Limits
    margin_left_x = 0.2
    margin_right_x = 1.5
    margin_top_y = 0.2
    margin_bottom_y = 2.5
    ax.set_xlim(min(all_x) - margin_left_x, max(all_x) + margin_right_x)
    ax.set_ylim(min(all_y) - margin_bottom_y, max(all_y) + margin_top_y)


    # 1) Adjacent-column straight edges (non-crossing via order-preserving wiring)
    for c in range(len(cols) - 1):
        src = cols[c]
        dst = cols[c + 1]
        conns = noncrossing_map(
            sources=list(range(len(src))),
            targets=list(range(len(dst))),
            min_in=1, max_in=2, rng=rng
        )
        for t_idx, src_idxs in enumerate(conns):
            x2, y2 = dst[t_idx]
            for s_idx in src_idxs:
                x1, y1 = src[s_idx]
                arr = FancyArrowPatch(
                    (x1, y1), (x2, y2),
                    arrowstyle="-|>",
                    mutation_scale=14,
                    linewidth=arrow_lw,
                    color=black,
                    shrinkA=6, shrinkB=6,
                    joinstyle="miter", capstyle="round",
                )
                ax.add_patch(arr)

    # 2) Two-back arcs ABOVE — but never across the red knee
    # Block the specific case: from column (knee_idx - 1) to (knee_idx + 1).
    for c in range(len(cols) - 2):
        if c == knee_idx - 1:
            continue  # would jump across the knee; skip entirely
        src = cols[c]
        dst = cols[c + 2]
        base_map = noncrossing_map(
            sources=list(range(len(src))),
            targets=list(range(len(dst))),
            min_in=1, max_in=1, rng=rng
        )
        for t_idx, s_choices in enumerate(base_map):
            if rng.random() > two_back_prob:
                continue
            s_idx = s_choices[0]
            x1, y1 = src[s_idx]
            x2, y2 = dst[t_idx]
            dx = x2 - x1
            rad = 0.22 + 0.07 * (dx)
            arr = FancyArrowPatch(
                (x1, y1), (x2, y2),
                arrowstyle="-|>",
                mutation_scale=13,
                linewidth=arrow_lw * 0.9,
                color=black,
                connectionstyle=f"arc3,rad={rad}",
                shrinkA=6, shrinkB=6,
                alpha=0.9,
            )
            ax.add_patch(arr)

    # 3) Draw vertices — knee red (with vertical error bar), others black
    knee_x, knee_y = cols[knee_idx][0]
    # Draw non-knee nodes
    for c_idx, col in enumerate(cols):
        for (x, y) in col:
            if c_idx == knee_idx:
                continue  # handled separately
            circ = Circle((x, y), radius=node_r, facecolor=black, edgecolor="white", linewidth=1.3, zorder=3)
            ax.add_patch(circ)

    circ = Circle((knee_x, knee_y), radius=node_r*2.0, facecolor=green, edgecolor="white", linewidth=1.3, zorder=3)
    ax.add_patch(circ)
    arr = FancyArrowPatch(
                    (knee_x, knee_y + 1.2), (knee_x, knee_y),
                    arrowstyle="-|>",
                    mutation_scale=20,
                    linewidth=arrow_lw*2.0,
                    color=green,
                    shrinkA=6, shrinkB=6,
                    joinstyle="miter", capstyle="round",
                )
    ax.add_patch(arr)
    ax.text(
        knee_x,
        min(all_y) - 2.0,
        "Process",
        ha="center",
        va="center",
        fontsize=20,
        color=black,
        path_effects=title_pe,
    )

    # Legend handles
    process_handle = Line2D(
        [0], [0],
        marker='o',
        color='w',
        markerfacecolor=black,
        markeredgecolor='white',
        markersize=10,
        label='Process step'
    )
    
    dependency_handle = Line2D(
        [0], [0],
        color=black,
        lw=2,
        label='Dependency'
    )

    legend = ax.legend(
        handles=[process_handle, dependency_handle],
        loc="upper left",
        bbox_to_anchor=(0.92, 0.20),
        frameon=True,
        framealpha=0.9,
        facecolor="white",
        edgecolor="#dddddd",
        fontsize=12
    )
    return fig

dpi = 100
fig = draw_process_knee(n_left_cols=3, n_right_cols=3, seed=7, dpi=dpi)
plt.show()

# %%
fig.savefig("../docs/assets/images/biounfold-003-where-ai-matters-most.png", dpi=dpi)
plt.close(fig)

# %%

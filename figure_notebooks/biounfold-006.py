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
from matplotlib.ticker import PercentFormatter
from matplotlib.lines import Line2D

def make_biounfold_006(
    width_px=1200,
    height_px=639,
    dpi=200,
    # Curve styling
    color_late="#4B6463",      # Biology-first (computation added late)
    color_early="#2F7E79",     # Biology + Computation early
    # Curves: positions & plateaus (still in normalized 0..1)
    late_x0=0.20,
    late_k=9.0,
    late_plateau=0.78,
    early_x0=0.35,
    early_k=9.5,
    early_plateau=0.95,
    # Timeline (months) + milestones in months (match your earlier 0.48/0.72 scaled to 6M)
    duration_months=6.0,
    x_opt_late=2.88,   # ≈ 0.48 * 6
    x_opt_early=4.32,  # ≈ 0.72 * 6
    # Typography
    title_text="Start AI Early to Capture More Biology",
    y_label="Meaningful Signal",
    x_label="Time (months)",
):
    fig_w, fig_h = width_px / dpi, height_px / dpi
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=dpi)
    ax = fig.add_subplot(1, 1, 1)

    # Time domain in months; normalize to 0..1 for curve shapes
    x = np.linspace(0, duration_months, 800)
    x_norm = x / duration_months

    y_late  = logistic(x_norm, x0=late_x0,  k=late_k,  L=late_plateau)
    y_early = logistic(x_norm, x0=early_x0, k=early_k, L=early_plateau)

    # Truncate each curve at its own milestone (keep shapes via NaNs)
    y_late  = np.where(x <= x_opt_late,  y_late,  np.nan)
    y_early = np.where(x <= x_opt_early, y_early, np.nan)

    # Plot
    ax.plot(x, y_early, label="Biology + Computation early", linewidth=4, color=color_early)
    ax.plot(x, y_late,  label="Biology-first (computation later)", linewidth=4, color=color_late)

    # Vertical markers (no extra labels or movement)
    ax.axvline(x_opt_early, ymin=0.0, ymax=1.0, linestyle=(0, (2, 4)), linewidth=2.2, color=color_early)
    ax.axvline(x_opt_late,  ymin=0.0, ymax=1.0, linestyle=(0, (2, 4)), linewidth=2.2, color=color_late)

    # Proxy artist for legend
    opt_line = Line2D([0], [0], linestyle=(0, (5, 6)), linewidth=2.2, color="black")
    
    # Axes
    ax.set_xlim(0, duration_months)
    ax.set_ylim(0, 1)
    ax.set_xticks(np.arange(0, duration_months + 0.001, 1))
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=0))
    ax.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])

    # Labels, grid, legend, title
    ax.set_ylabel(y_label, labelpad=10, fontsize=16)
    ax.set_xlabel(x_label, labelpad=8, fontsize=16)
    ax.grid(True, linewidth=0.6, alpha=0.25)

    # --- Get handles for the existing curve legend ---
    handles, labels = ax.get_legend_handles_labels()
    
    # --- Add proxy dashed-line entry ---
    opt_handle = Line2D([0], [0],
                        linestyle=(0, (2, 4)),
                        linewidth=2.2,
                        color="black")  # or use color_early if preferred
    
    handles.append(opt_handle)
    labels.append("End of assay optimization")
    
    # --- Now draw a single combined legend ---
    ax.legend(handles, labels,
              frameon=False,
              loc="center left",
              bbox_to_anchor=(1.02, 0.5),
              fontsize=13)
    
    if title_text:
        ax.set_title(title_text, fontsize=18, pad=14)

    return fig

    
# Default export to repo docs asset path
fig = make_biounfold_006()

# %%
save_path="../docs/assets/images/biounfold-006-start-ai-early.png"
pad_fraction = 0.02  # adjust this to taste (1–3% usually enough)
dpi=100
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

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
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_ai_vs_bio_contrast(
    n=450, 
    seed=7, 
    threshold=0.65, 
    noise=0.15,
    width_px=1200,
    height_px=639,
    dpi=100,
):
    """
    Two-panel illustration:
      Left  = 'AI without biology' (naive threshold -> misleading hits)
      Right = 'AI + biology' (colored by mechanism; structure becomes clear)
    """

    rng = np.random.default_rng(seed)

    # Simulate "features" and mechanisms
    n_a = n // 3
    n_b = n // 3
    n_c = n - n_a - n_b

    x_a = rng.normal(0.0, 1.0, n_a)
    y_a = 0.9 * x_a + rng.normal(0, noise, n_a) + 0.4

    x_b = rng.normal(0.5, 1.1, n_b)
    y_b = 0.3 * x_b + rng.normal(0, noise, n_b) + 0.15

    x_c = rng.normal(-0.3, 0.9, n_c)
    y_c = -0.6 * x_c + rng.normal(0, noise, n_c) + 0.25

    x = np.concatenate([x_a, x_b, x_c])
    y = np.concatenate([y_a, y_b, y_c])
    mech = (["MOA_A"] * n_a) + (["MOA_B"] * n_b) + (["MOA_C"] * n_c)

    # Add small off-target pocket near threshold
    m = n // 8
    x_fp = rng.normal(2.0, 0.25, m)
    y_fp = rng.normal(threshold + 0.02, 0.015, m)
    mech_fp = ["OffTarget"] * m

    x = np.concatenate([x, x_fp])
    y = np.concatenate([y, y_fp])
    mech = mech + mech_fp

    df = pd.DataFrame({"feature_x": x, "activity": y, "mechanism": mech})
    df["is_hit_naive"] = df["activity"] >= threshold

    # Plot setup
    fig_w, fig_h = width_px / dpi, height_px / dpi
    fig, axes = plt.subplots(1, 2, figsize=(fig_w, fig_h), dpi=dpi)
    sns.set(context="talk", style="whitegrid")

    # Left: naive hits
    ax = axes[0]
    sns.scatterplot(
        data=df, x="feature_x", y="activity",
        hue="is_hit_naive", style="is_hit_naive",
        alpha=0.8, edgecolor="none", ax=ax
    )
    ax.axhline(threshold, linestyle="--", linewidth=1)
    ax.set_title("Raw Results")
    ax.set_xlabel("Feature projection")
    ax.set_ylabel("Predicted activity")

    # Right: biology-aware
    ax = axes[1]
    sns.scatterplot(
        data=df, x="feature_x", y="activity",
        hue="mechanism", alpha=0.85, edgecolor="none", ax=ax
    )
    ax.axhline(threshold, linestyle="--", linewidth=1)
    ax.set_title("Biology-aware Results")
    ax.set_xlabel("Feature projection")
    ax.set_ylabel("Predicted activity")

    # Harmonize y-limits
    y_min, y_max = df["activity"].min(), df["activity"].max()
    pad = 0.1 * (y_max - y_min)
    for ax in axes:
        ax.set_ylim(y_min - pad, y_max + pad)

    # Legends outside
    axes[0].legend(
        title="Naive 'hit'",
        bbox_to_anchor=(-0.7, 1),
        loc="upper left",
        borderaxespad=0.
    )
    axes[1].legend(
        title="Mechanism",
        bbox_to_anchor=(1.60, 1),
        loc="upper right",
        borderaxespad=0.
    )
    return fig
dpi=100
fig = plot_ai_vs_bio_contrast(dpi=dpi)
plt.show()

# %%
dpi = 100
width_px = 1200
height_px = 639

fig = plot_ai_vs_bio_contrast(width_px=width_px, height_px=height_px, dpi=dpi)

# 1) Ensure legends are included in layout
for ax in fig.axes:
    leg = ax.get_legend()
    if leg is not None:
        leg.set_in_layout(True)

# 2) Compute proportional padding (e.g. 2% of figure size)
#    pad_inches is in *inches*, so convert from pixels.
pad_fraction = 0.02  # adjust this to taste (1–3% usually enough)
pad_inches = (height_px / dpi) * pad_fraction

# 3) Save without transforming the plot
fig.savefig(
    "../docs/assets/images/biounfold-004-why-ai-needs-biology-literacy.png",
    dpi=dpi,
    bbox_inches="tight",   # include legends & titles
    pad_inches=pad_inches, # proportional white space
)

# %%

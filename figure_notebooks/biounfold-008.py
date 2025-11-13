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
from matplotlib.patches import Rectangle, Polygon

def make_biounfold_008_coverage_context(
    width_px=1200,
    height_px=675,
    dpi=200,
    title="Coverage × Context in Biology",
):
    # --- Figure setup ---
    fig_w, fig_h = width_px / dpi, height_px / dpi
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=dpi)
    ax = plt.gca()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # --- Remove ticks/grid, keep a clean canvas ---
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)

    # --- Quadrant separators (subtle, dashed) ---
    ax.axvline(0.5, linestyle="--", linewidth=0.8, alpha=0.8)
    ax.axhline(0.5, linestyle="--", linewidth=0.8, alpha=0.8)

    # --- Sweet spot shading (top-right quadrant) ---
    sweet_spot = Rectangle((0.5, 0.5), 0.5, 0.5, alpha=0.08)
    ax.add_patch(sweet_spot)

    # --- Axis labels (two-line, second line italic) ---
    #ax.set_xlabel("Biological Coverage", labelpad=18)
    ax.text(0.5, -0.10, "Biological Coverage",
            transform=ax.transAxes, ha="center", va="top", fontsize=12)
    ax.text(0.5, -0.20, "tissues • perturbations • modalities",
            transform=ax.transAxes, ha="center", va="top", fontsize=10, fontstyle="italic")

    ax.text(-0.12, 0.5, "Biological Context",
            transform=ax.transAxes, ha="right", va="center", rotation=90, fontsize=12)
    ax.text(-0.08, 0.5, "metadata • design • outcomes",
            transform=ax.transAxes, ha="right", va="center", rotation=90, fontsize=10, fontstyle="italic")

    # --- Non-numerical axis cues: Low/High + tiny triangle arrows ---
    # X-axis: Low (left), High (right) + right-pointing triangle
    ax.text(0.05, -0.04, "Low", transform=ax.transAxes, ha="left", va="top", fontsize=9)
    ax.text(0.95, -0.04, "High", transform=ax.transAxes, ha="right", va="top", fontsize=9)
    tri_x = Polygon([[0.985, -0.02], [0.995, -0.04], [0.995, 0.00]], transform=ax.transAxes, closed=True)
    ax.add_patch(tri_x)

    # Y-axis: Low (bottom), High (top) + upward triangle
    ax.text(-0.04, 0.05, "Low", transform=ax.transAxes, ha="right", va="bottom", fontsize=9, rotation=90)
    ax.text(-0.04, 0.95, "High", transform=ax.transAxes, ha="right", va="top", fontsize=9, rotation=90)
    tri_y = Polygon([[-0.02, 0.985], [-0.04, 0.995], [0.00, 0.995]], transform=ax.transAxes, closed=True)
    ax.add_patch(tri_y)

    # --- Quadrant labels (two lines; second line italic) ---
    # Bottom-left
    ax.text(0.01, 0.4, "Single-condition imaging screens", ha="left", va="bottom", fontsize=10)
    ax.text(0.01, 0.32, "one cell line • minimal metadata", ha="left", va="bottom", fontsize=9, fontstyle="italic")

    # Bottom-right
    ax.text(0.51, 0.4, "Large cross-study omics", ha="left", va="bottom", fontsize=10)
    ax.text(0.51, 0.32, "batch heterogeneity • shallow labels", ha="left", va="bottom", fontsize=9, fontstyle="italic")

    # Top-left
    ax.text(0.01, 0.96, "Clinical / disease cohorts", ha="left", va="top", fontsize=10)
    ax.text(0.01, 0.88, "deep labels • small N", ha="left", va="top", fontsize=9, fontstyle="italic")

    # Top-right
    ax.text(0.51, 0.96, "Integrated patient platforms", ha="left", va="top", fontsize=10)
    ax.text(0.51, 0.88, "omics + imaging • curated outcomes", ha="left", va="top", fontsize=9, fontstyle="italic")

    # --- Stars + recommendations per quadrant ---
    def stars(x, y, n, text):
        # horizontally place up to 3 stars centered at (x,y)
        spacing = 0.04
        xs = [x] if n == 1 else [x - spacing/2, x + spacing/2] if n == 2 else [x - spacing, x, x + spacing]
        for xi in xs:
            ax.plot([xi], [y], marker="*", markersize=12, color="gold")
        ax.text(x, y - 0.1, text,
                ha="center", va="bottom", fontsize=9)

    # BL: 1 star → transfer/adapt
    stars(0.25, 0.25, 1, "Transfer / adapt")

    # BR: 2 stars → fine-tune on public FM
    stars(0.75, 0.25, 2, "Fine-tune baseline")

    # TL: 2 stars → integrate & fine-tune
    stars(0.25, 0.70, 2, "Integrate + fine-tune")

    # TR: 3 stars → fine-tune + consider FM
    stars(0.75, 0.70, 3, "Fine-tune • evaluate foundation")

    # --- Title ---
    ax.set_title(title, pad=14, fontsize=14)

    plt.tight_layout()
    return fig, ax

fig, ax = make_biounfold_008_coverage_context()
plt.show()


# %%
save_path="../docs/assets/images/biounfold-008-coverage-context.png"
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

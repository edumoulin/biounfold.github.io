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
from matplotlib.patches import Rectangle

# --------------------------------------------------------
# Configuration
# --------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 5))
ax.axis('off')

# Column titles and content
left_labels = ["Example", "Advantage", "Challenge"]

extracellular = [
    "Pembrolizumab\n(PD-1 blockade)",
    "High specificity",
    "Target accessibility"
]

intracellular = [
    "Onpattro\n(siRNA for TTR)",
    "Versatile mechanisms",
    "Delivery constraints"
]

genomic = [
    "Luxturna\n(AAV gene therapy)",
    "Potentially curative",
    "Permanence,\nimmunity"
]

columns = [extracellular, intracellular, genomic]
col_titles = ["Extracellular", "Intracellular", "Genome-Level"]

# Layout parameters
n_rows = len(left_labels)
n_cols = 4  # label column + 3 modality columns

cell_width = 0.22
cell_height = 0.18
x_start = 0.05
y_start = 0.75

colors = {
    "label": "#E8E8E8",
    "extracellular": "#D6EAF8",
    "intracellular": "#FCF3CF",
    "genomic": "#E8DAEF"
}

content_colors = [
    colors["extracellular"],
    colors["intracellular"],
    colors["genomic"]
]

# --------------------------------------------------------
# Draw column titles
# --------------------------------------------------------
for col_idx, title in enumerate(col_titles):
    x = x_start + (col_idx + 1) * cell_width
    y = y_start + cell_height / 2
    ax.text(x + cell_width/2, y, title,
            ha='center', va='center', fontsize=14, fontweight='bold')

# --------------------------------------------------------
# Draw left labels + content columns
# --------------------------------------------------------
for row in range(n_rows):
    # Left label column
    x = x_start
    y = y_start - row * cell_height
    rect = Rectangle((x, y - cell_height), cell_width, cell_height,
                     linewidth=1.2, edgecolor="black", facecolor=colors["label"])
    ax.add_patch(rect)
    ax.text(x + cell_width/2, y - cell_height/2, left_labels[row],
            ha='center', va='center', fontsize=12, fontweight='bold')

    # Content columns
    for col_idx in range(3):
        x = x_start + (col_idx + 1) * cell_width
        rect = Rectangle((x, y - cell_height), cell_width, cell_height,
                         linewidth=1.2, edgecolor="black",
                         facecolor=content_colors[col_idx])
        ax.add_patch(rect)

        ax.text(x + cell_width/2, y - cell_height/2,
                columns[col_idx][row],
                ha='center', va='center', fontsize=11)

plt.tight_layout()
plt.show()


# %%
save_path="../docs/assets/images/biounfold-013-sum-table.png"
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

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
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle

# --- Figure setup ---
fig, ax = plt.subplots(figsize=(14, 7))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# --- Title / subtitle inside figure ---
ax.text(50, 95, "Two Engines, One Drug", ha="center", va="center", fontsize=22, fontweight="bold")
ax.text(50, 90, "Selling unfinished drugs to finance discovery", ha="center", va="center", fontsize=12)

# --- Main blocks ---
discovery = Rectangle((8, 30), 28, 40, fill=False, linewidth=2)
licensing = Rectangle((43, 35), 14, 30, fill=False, linewidth=2)
development = Rectangle((64, 30), 28, 40, fill=False, linewidth=2)

ax.add_patch(discovery)
ax.add_patch(licensing)
ax.add_patch(development)

# --- Block labels ---
ax.text(22, 66, "Discovery Engine", ha="center", fontsize=16, fontweight="bold")
ax.text(50, 61, "Licensing", ha="center", fontsize=14, fontweight="bold")
ax.text(78, 66, "Development Engine", ha="center", fontsize=16, fontweight="bold")

# --- Discovery content ---
discovery_items = [
    "biology understanding",
    "assays",
    "screening",
    "hypotheses",
    "high throughput",
    "indirect patient relevance",
]
for i, item in enumerate(discovery_items):
    ax.text(22, 58 - i * 5, item, ha="center", fontsize=10)

# --- Licensing content ---
licensing_items = ["upfront", "milestones", "royalties"]
for i, item in enumerate(licensing_items):
    ax.text(50, 54 - i * 7, item, ha="center", fontsize=11)

# --- Development content ---
development_items = [
    "patients",
    "clinical trials",
    "regulators",
    "manufacturing",
    "low throughput",
    "high relevance",
]
for i, item in enumerate(development_items):
    ax.text(78, 58 - i * 5, item, ha="center", fontsize=10)

# --- Molecule / asset path ---
path_y = 25
ax.plot([15, 85], [path_y, path_y], linewidth=2)

# Molecule nodes
for x in [22, 50, 78]:
    ax.add_patch(Circle((x, path_y), 1.8, fill=False, linewidth=2))

ax.text(50, 19, "unfinished drug", ha="center", fontsize=11)

# Forward movement arrow
forward_arrow = FancyArrowPatch((24, path_y), (76, path_y), arrowstyle="->", mutation_scale=15, linewidth=2)
ax.add_patch(forward_arrow)
ax.text(50, 28, "asset moves forward", ha="center", fontsize=10)

# --- Top arrows: time / confidence / cost ---
time_arrow = FancyArrowPatch((10, 80), (90, 80), arrowstyle="->", mutation_scale=15, linewidth=1.8)
ax.add_patch(time_arrow)
ax.text(50, 83, "time", ha="center", fontsize=11)

confidence_arrow = FancyArrowPatch((10, 85), (90, 85), arrowstyle="->", mutation_scale=15, linewidth=1.8)
ax.add_patch(confidence_arrow)
ax.text(50, 88, "confidence increases", ha="center", fontsize=11)

cost_arrow = FancyArrowPatch((10, 75), (90, 75), arrowstyle="->", mutation_scale=15, linewidth=1.8)
ax.add_patch(cost_arrow)
ax.text(50, 72, "cost increases", ha="center", fontsize=11)

# --- Bottom arrow: capital returning to discovery ---
capital_arrow = FancyArrowPatch((82, 12), (18, 12), arrowstyle="->", mutation_scale=15, linewidth=2)
ax.add_patch(capital_arrow)
ax.text(50, 8, "capital returns to discovery", ha="center", fontsize=11)

# --- Conceptual footer ---
ax.text(50, 2,
        "Discovery produces hypotheses about biology     |     Development produces evidence about patients",
        ha="center", fontsize=10)

plt.tight_layout()
plt.show()

# %%
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle

# --- Figure setup ---
fig, ax = plt.subplots(figsize=(15, 7))
ax.set_xlim(0, 110)
ax.set_ylim(0, 100)
ax.axis("off")

# --- Title / subtitle ---
ax.text(55, 95, "Two Engines, One Drug", ha="center", va="center", fontsize=28, fontweight="bold")
ax.text(55, 90, "Selling unfinished drugs to finance discovery", ha="center", va="center", fontsize=16)

# --- Main blocks ---
discovery = Rectangle((8, 45), 28, 30, fill=False, linewidth=2)
licensing = Rectangle((43, 45), 14, 30, fill=False, linewidth=2)
development = Rectangle((64, 45), 28, 30, fill=False, linewidth=2)
revenue = Rectangle((95, 50), 12, 20, fill=False, linewidth=2)

ax.add_patch(discovery)
ax.add_patch(licensing)
ax.add_patch(development)
ax.add_patch(revenue)

# --- Block labels ---
ax.text(22, 71, "Discovery Engine", ha="center", fontsize=18, fontweight="bold")
ax.text(50, 71, "Licensing", ha="center", fontsize=18, fontweight="bold")
ax.text(78, 71, "Development Engine", ha="center", fontsize=18, fontweight="bold")
ax.text(101, 60, "Revenue", ha="center", va="center", fontsize=18, fontweight="bold")

# --- Discovery content ---
discovery_items = [
    "biology",
    "assays",
    "high throughput",
]
for i, item in enumerate(discovery_items):
    ax.text(22, 64 - i * 7, item, ha="center", fontsize=14)

# --- Licensing content ---
licensing_items = ["upfront", "milestones", "royalties"]
for i, item in enumerate(licensing_items):
    ax.text(50, 64 - i * 7, item, ha="center", fontsize=14)

# --- Development content ---
development_items = [
    "patients",
    "trials",
    "high relevance",
]
for i, item in enumerate(development_items):
    ax.text(78, 64 - i * 7, item, ha="center", fontsize=14)

# --- Asset path ---
path_y = 30

for x in [50, 101]:
    ax.add_patch(Circle((x, path_y), 1.8, fill=False, linewidth=2))

forward_arrow = FancyArrowPatch((24, path_y), (99, path_y), arrowstyle="->", mutation_scale=15, linewidth=2)
ax.add_patch(forward_arrow)

ax.text(50, 24, "unfinished drug", ha="center", fontsize=16)
ax.text(100, 24, "commercial product", ha="center", fontsize=16)

# --- Footer concept ---
ax.text(
    55,
    13,
    "Discovery produces hypotheses about biology     |     Development produces evidence about patients",
    ha="center",
    fontsize=20
)

plt.tight_layout()
plt.show()

# %%
save_path="../docs/assets/images/biounfold-026-two-engines-one-drug.png"
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

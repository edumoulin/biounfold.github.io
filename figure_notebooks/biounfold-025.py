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
from matplotlib.patches import Rectangle

# ------------------------------------------------------------
# BioUnfold #25 — Intelligence as Execution
# Context-dependent value with overlap and constrained execution
# ------------------------------------------------------------

np.random.seed(42)

ACCENT_INTERNAL = "#4C78A8"
ACCENT_PARTNER = "#F28E2B"
DARK = "#222222"
MID = "#666666"
LIGHT = "#D9D9D9"
VERY_LIGHT = "#F6F6F6"

# ----------------------------
# Synthetic hypotheses
# ----------------------------
# Broad background
base = np.random.multivariate_normal(
    mean=[0.45, 0.45],
    cov=[[0.035, 0.012], [0.012, 0.035]],
    size=110
)

# Better for your organization
your_cluster = np.random.multivariate_normal(
    mean=[0.78, 0.42],
    cov=[[0.010, 0.002], [0.002, 0.010]],
    size=28
)

# Better for partner
partner_cluster = np.random.multivariate_normal(
    mean=[0.42, 0.78],
    cov=[[0.010, 0.002], [0.002, 0.010]],
    size=28
)

# High value for both
shared_cluster = np.random.multivariate_normal(
    mean=[0.82, 0.82],
    cov=[[0.008, 0.003], [0.003, 0.008]],
    size=12
)

pts = np.vstack([base, your_cluster, partner_cluster, shared_cluster])

# Keep within plot bounds
x = np.clip(pts[:, 0], 0.02, 0.98)
y = np.clip(pts[:, 1], 0.02, 0.98)

# ----------------------------
# Selection logic
# ----------------------------
n_internal = 5
n_partner = 6

# Internal score: strong preference for own value, some appreciation for shared value
internal_score = x
internal_idx = np.argsort(internal_score)[-n_internal:]

# Partner score on remaining points: strong preference for partner value
remaining_idx = np.array([i for i in range(len(x)) if i not in internal_idx])
partner_score = y[remaining_idx]
partner_idx = remaining_idx[np.argsort(partner_score)[-n_partner:]]

selected = set(internal_idx).union(set(partner_idx))
rest_idx = np.array([i for i in range(len(x)) if i not in selected])

# ----------------------------
# Plot
# ----------------------------
fig, ax = plt.subplots(figsize=(8.8, 7.2))
fig.patch.set_facecolor("white")
ax.set_facecolor(VERY_LIGHT)

# Soft emphasis regions
ax.add_patch(Rectangle((0.72, 0.00), 0.28, 1.00,
                       facecolor=ACCENT_INTERNAL, alpha=0.04, lw=0))
ax.add_patch(Rectangle((0.00, 0.72), 1.00, 0.28,
                       facecolor=ACCENT_PARTNER, alpha=0.04, lw=0))

# All hypotheses
ax.scatter(
    x[rest_idx], y[rest_idx],
    s=42, color=LIGHT, edgecolor="white", linewidth=0.5,
    alpha=0.95, zorder=2, label="Possible hypotheses"
)

# Internal selection
ax.scatter(
    x[internal_idx], y[internal_idx],
    s=95, color=ACCENT_INTERNAL, edgecolor="white", linewidth=0.9,
    zorder=4, label="Executed internally"
)

# Externalized / partner-executed
ax.scatter(
    x[partner_idx], y[partner_idx],
    s=95, color=ACCENT_PARTNER, edgecolor="white", linewidth=0.9,
    zorder=4, label="Externalized / partner-executed"
)

# Labels
ax.set_title(
    "Execution selects from a shared opportunity space",
    fontsize=15, color=DARK, pad=16
)
ax.set_xlabel("Value for your organization", fontsize=12, color=DARK, labelpad=10)
ax.set_ylabel("Value for partner", fontsize=12, color=DARK, labelpad=10)

# Region annotations
ax.text(0.80, 0.10, "Better for\nyour organization", ha="center", va="center",
        fontsize=10.5, color=ACCENT_INTERNAL, fontweight="bold", zorder=10)
ax.text(0.12, 0.82, "Better for\npartner", ha="center", va="center",
        fontsize=10.5, color=ACCENT_PARTNER, fontweight="bold", zorder=10)
ax.text(0.80, 0.84, "High value\nfor both", ha="center", va="center",
        fontsize=10.5, color=MID, fontweight="bold", zorder=10)
ax.text(0.14, 0.12, "Low value\nfor both", ha="center", va="center",
        fontsize=10, color=MID, zorder=10)

# Style
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.02, 1.02)
ax.set_xticks([])
ax.set_yticks([])

for spine in ax.spines.values():
    spine.set_color(MID)
    spine.set_linewidth(1.0)

legend = ax.legend(
    loc="center left",
    frameon=True,
    facecolor="white",
    edgecolor=LIGHT,
    fontsize=10
)
for txt in legend.get_texts():
    txt.set_color(DARK)

caption = (
    "Each point represents a plausible hypothesis. Execution is limited, so only a small subset is acted on internally. "
    "Other hypotheses may be better suited to specialized partners, making externalization a way to realize value."
)
ax.text(
    0.02, -0.14, caption,
    transform=ax.transAxes, ha="left", va="top",
    fontsize=12, color=MID, wrap=True
)

plt.tight_layout()
plt.show()

# %%
save_path="../docs/assets/images/biounfold-025-intelligence.png"
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

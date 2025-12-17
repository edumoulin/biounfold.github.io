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
from matplotlib.patches import FancyArrowPatch, Rectangle

rng = np.random.default_rng(7)

# -------------------------
# Helpers
# -------------------------
def unit(v):
    v = np.asarray(v, dtype=float)
    return v / (np.linalg.norm(v) + 1e-12)

def cosine(a, b):
    return float(np.dot(unit(a), unit(b)))

def rotate(v, theta):
    c, s = np.cos(theta), np.sin(theta)
    R = np.array([[c, -s], [s, c]])
    return R @ v

# -------------------------
# Construct pairs in embedding space
# Goal: same cosine similarity, different equivalence due to non-systematic components
# -------------------------
target_cos = 0.85
theta = np.arccos(target_cos)

# Base "mechanistic" direction (systematic)
m = unit([1.0, 0.2])

# Pair 1: truly equivalent (same mechanism), mostly systematic
a1 = 1.0 * m
b1 = 1.0 * rotate(m, theta)

# Pair 2: not equivalent, but accidentally same cosine because of non-systematic components
# Add secondary-effect / experimental noise components that distort without a stable rule.
sec1 = unit([-0.2, 1.0])
sec2 = unit([0.6, 0.8])

a2 = 1.0 * m + 0.9 * sec1 + rng.normal(0, 0.05, 2)
# Choose b2 so cosine(a2, b2) ~ target_cos but direction comes from different mixture
b2_dir = rotate(unit(m + 0.9 * sec2), theta)
b2 = 1.0 * b2_dir + 0.9 * sec2 + rng.normal(0, 0.05, 2)

# Make the cosines close (for the visual claim)
# (Small adjustment if needed)
for _ in range(20):
    c2 = cosine(a2, b2)
    if abs(c2 - target_cos) < 0.01:
        break
    # Nudge b2 slightly along a direction orthogonal to a2 to tune cosine
    ortho = unit(np.array([-a2[1], a2[0]]))
    b2 = b2 + (target_cos - c2) * 0.15 * ortho

c1 = cosine(a1, b1)
c2 = cosine(a2, b2)

# Replicates: non-systematic scatter around each point
def replicates(center, n=18, scale=0.10):
    return center + rng.normal(0, scale, size=(n, 2))

A1 = replicates(a1, scale=0.07)
B1 = replicates(b1, scale=0.07)
A2 = replicates(a2, scale=0.12)
B2 = replicates(b2, scale=0.12)

# Middle panel: show distribution overlap in the "similarity readout"
# Build many pseudo-pairs by sampling replicates.
def sample_pair_cos(A, B, n=120):
    idxA = rng.integers(0, len(A), size=n)
    idxB = rng.integers(0, len(B), size=n)
    return np.array([cosine(A[i], B[j]) for i, j in zip(idxA, idxB)])

cos_eq = sample_pair_cos(A1, B1)
cos_neq = sample_pair_cos(A2, B2)

# -------------------------
# Plot
# -------------------------
fig = plt.figure(figsize=(9.2, 2.8))
gs = fig.add_gridspec(1, 3, width_ratios=[1.45, 1.15, 1.05], wspace=0.55)
ax0 = fig.add_subplot(gs[0, 0])
ax1 = fig.add_subplot(gs[0, 1])
ax2 = fig.add_subplot(gs[0, 2])

# --- Panel 1: embedding space with non-systematic scatter ---
ax0.scatter(A1[:, 0], A1[:, 1], s=14, alpha=0.6)
ax0.scatter(B1[:, 0], B1[:, 1], s=14, alpha=0.6)
ax0.scatter(A2[:, 0], A2[:, 1], s=14, alpha=0.6)
ax0.scatter(B2[:, 0], B2[:, 1], s=14, alpha=0.6)

# Highlight the representative points
ax0.scatter([a1[0], b1[0]], [a1[1], b1[1]], s=90, facecolors="none", linewidths=1.8)
ax0.scatter([a2[0], b2[0]], [a2[1], b2[1]], s=90, facecolors="none", linewidths=1.8, linestyle="--")

# Connect pairs
ax0.plot([a1[0], b1[0]], [a1[1], b1[1]], linewidth=1.2)
ax0.plot([a2[0], b2[0]], [a2[1], b2[1]], linewidth=1.2)

# Annotate pair labels
ax0.text((a1[0]+b1[0])/2, (a1[1]+b1[1])/2, "equivalent", fontsize=9, ha="left", va="bottom")
ax0.text((a2[0]+b2[0])/2, (a2[1]+b2[1])/2, "not equivalent", fontsize=9, ha="left", va="top")

# A small arrow to suggest "secondary / non-systematic effects"
o = np.array([np.min([A1[:,0].min(),A2[:,0].min()]) - 0.25,
              np.min([A1[:,1].min(),A2[:,1].min()]) - 0.15])
ax0.add_patch(FancyArrowPatch(posA=o, posB=o + 0.55*unit(sec1), arrowstyle='-|>', mutation_scale=12))
ax0.text(o[0] + 0.60*unit(sec1)[0], o[1] + 0.60*unit(sec1)[1],
         "non-systematic\nvariation", fontsize=9, ha="left", va="bottom")

ax0.set_title("What we measure\n(embeddings + non-systematic effects)", fontsize=11)
ax0.set_xlabel("latent 1")
ax0.set_ylabel("latent 2")
ax0.spines["top"].set_visible(False)
ax0.spines["right"].set_visible(False)

# --- Panel 2: similarity readout that overlaps ---
# Jittered strip plot style (no seaborn)
y_eq = 0.18 + rng.normal(0, 0.015, size=len(cos_eq))
y_neq = -0.18 + rng.normal(0, 0.015, size=len(cos_neq))
ax1.scatter(cos_eq, y_eq, s=10, alpha=0.45)
ax1.scatter(cos_neq, y_neq, s=10, alpha=0.45)

# Mark the representative cosines (nearly equal)
ax1.scatter([c1], [0.18], s=85, facecolors="none", linewidths=1.8)
ax1.scatter([c2], [-0.18], s=85, facecolors="none", linewidths=1.8, linestyle="--")
ax1.vlines([target_cos], -0.33, 0.33, linewidth=1.0)

ax1.text(target_cos, 0.30, "same score", ha="center", va="bottom", fontsize=9)
ax1.text(0.02, 0.18, "equivalent", transform=ax1.transAxes, fontsize=9, va="center")
ax1.text(0.02, 0.05, "not equivalent", transform=ax1.transAxes, fontsize=9, va="center")

ax1.set_yticks([])
ax1.set_xlim(0.0, 1.0)
ax1.set_title("What we compute\n(cosine similarity)", fontsize=11)
ax1.set_xlabel("cos(f(Pa|c), f(Pb|c))")
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.spines["left"].set_visible(False)

# --- Panel 3: equivalence as learned relation, not readout ---
ax2.set_axis_off()
ax2.set_title("What we want\n(equivalence)", fontsize=11, pad=10)

ax2.add_patch(Rectangle((0.08, 0.58), 0.84, 0.28, fill=False, linewidth=1.5))
ax2.add_patch(Rectangle((0.08, 0.18), 0.84, 0.28, fill=False, linewidth=1.5))

ax2.text(0.50, 0.72, "g(Pa, Pb | c) = 1", ha="center", va="center", fontsize=11)
ax2.text(0.50, 0.32, "g(Pa, Pb | c) = 0", ha="center", va="center", fontsize=11)

ax2.text(0.50, 0.05,
         "Same similarity does not\nimply the same mechanism.\nNon-systematic variation breaks the rule.",
         ha="center", va="bottom", fontsize=9)

# Big arrows between panels
fig.text(0.39, 0.50, "→", fontsize=18, va="center", ha="center")
fig.text(0.68, 0.50, "→", fontsize=18, va="center", ha="center")

plt.tight_layout()
plt.show()


# %%
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(3)

# -------------------------
# Synthetic embedding points
# -------------------------
centers = {
    "green":  np.array([-1.0,  0.6]),
    "red":    np.array([-0.6,  0.9]),
    "orange": np.array([ 0.7, -0.4]),
    "blue":   np.array([ 1.1, -0.1]),
}

colors = {
    "green":  "#2ca02c",
    "red":    "#d62728",
    "orange": "#ff7f0e",
    "blue":   "#1f77b4",
}

def cloud(center, n=25, scale=0.18):
    return center + rng.normal(0, scale, size=(n, 2))

points = {k: cloud(v) for k, v in centers.items()}

# -------------------------
# Figure layout
# -------------------------
fig, axes = plt.subplots(1, 3, figsize=(8.6, 2.8), gridspec_kw={"wspace": 0.45})

# -------------------------
# Panel 1 — What we measure
# -------------------------
ax = axes[0]
for k in points:
    ax.scatter(points[k][:, 0], points[k][:, 1], s=22, color=colors[k], alpha=0.85)

ax.set_title("What we measure", fontsize=11)
ax.set_xlabel("embedding dim 1")
ax.set_ylabel("embedding dim 2")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# -------------------------
# Panel 2 — What we know
# -------------------------
ax = axes[1]
for k in points:
    ax.scatter(points[k][:, 0], points[k][:, 1], s=22, color=colors[k], alpha=0.85)

# Annotate known equivalences
ax.text(-0.85, 1.15, "green = red", color="black", fontsize=10, ha="center")
ax.text( 0.95,-0.85, "orange = blue", color="black", fontsize=10, ha="center")

ax.set_title("What we know", fontsize=11)
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# -------------------------
# Panel 3 — What we want to know
# -------------------------
ax = axes[2]
ax.scatter([0.35], [0.5], s=140, color=colors["green"])
ax.scatter([0.65], [0.5], s=140, color=colors["orange"])

ax.text(0.50, 0.5, "?", fontsize=24, ha="center", va="center")

ax.text(0.35, 0.32, "green", ha="center", fontsize=10)
ax.text(0.65, 0.32, "orange", ha="center", fontsize=10)

ax.set_title("What we want to know", fontsize=11)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout()
plt.show()


# %%
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(3)

# -------------------------
# Synthetic embedding points
# -------------------------
centers = {
    "green":  np.array([-1.0,  0.6]),
    "red":    np.array([-0.6,  0.9]),
    "orange": np.array([ 0.7, -0.4]),
    "blue":   np.array([ 1.1, -0.1]),
}

colors = {
    "green":  "#2ca02c",
    "red":    "#d62728",
    "orange": "#ff7f0e",
    "blue":   "#1f77b4",
}

def cloud(center, n=25, scale=0.18):
    return center + rng.normal(0, scale, size=(n, 2))

points = {k: cloud(v) for k, v in centers.items()}

# -------------------------
# Figure layout
# -------------------------
fig, axes = plt.subplots(
    1, 3, figsize=(8.4, 2.7),
    gridspec_kw={
        "wspace": 0.10,
        "right": 0.90 
    }
)

# -------------------------
# Panel 1 — What we measure
# -------------------------
ax = axes[0]
for k in points:
    ax.scatter(points[k][:, 0], points[k][:, 1],
               s=22, color=colors[k], alpha=0.85)

ax.set_title("Measurements", fontsize=18)
ax.set_xlabel("embedding dim 1")
ax.set_ylabel("embedding dim 2")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="both", which="both", labelsize=9)
ax.xaxis.label.set_alpha(0.7)
ax.yaxis.label.set_alpha(0.7)

# -------------------------
# Panel 2 — What we know
# -------------------------
ax = axes[1]

# Symbols
ax.scatter([0.30], [0.70], s=140, color=colors["green"])
ax.scatter([0.70], [0.70], s=140, color=colors["red"])
ax.text(0.50, 0.70, "=", fontsize=20, ha="center", va="center")

ax.scatter([0.30], [0.40], s=140, color=colors["orange"])
ax.scatter([0.70], [0.40], s=140, color=colors["blue"])
ax.text(0.50, 0.40, "=", fontsize=20, ha="center", va="center")

ax.set_title("Knowledge", fontsize=18)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)
ax.set_facecolor("#f7f7f7")
bbox = ax.get_position()
rect = Rectangle(
    (bbox.x0, 0),
    bbox.width,
    1.0,
    transform=fig.transFigure,
    color="#f7f7f7",
    zorder=0,
    linewidth=0
)
fig.add_artist(rect)

# -------------------------
# Panel 3 — What we want to know
# -------------------------
ax = axes[2]

ax.scatter([0.35], [0.6], s=140, color=colors["green"])
ax.scatter([0.65], [0.6], s=140, color=colors["orange"])
ax.text(0.50, 0.6, "?", fontsize=24, ha="center", va="center")

ax.set_title("Hypothesis", fontsize=18)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout()
plt.show()

# %%
save_path="../docs/assets/images/biounfold-014-measurements-knowledge-hypothesis.png"
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

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
from matplotlib.lines import Line2D

# ----------------------------
# Style knobs (match your aesthetic)
# ----------------------------
FIGSIZE = (9.6, 3.1)
BG = "#f7f7f7"
INK = "#222222"
SOFT = "#666666"

def base_axes(ax):
    ax.set_facecolor(BG)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

def pulse_timeline(ax, pulses, y=-0.12, x0=0.15, x1=0.95, lw=1.4):
    """
    Draw a tiny timeline in axes coordinates.
    pulses: list of floats in [0,1] indicating pulse locations along the line.
    """
    # baseline (axes coords)
    ax.add_line(Line2D([x0, x1], [y, y], transform=ax.transAxes,
                       lw=lw, color=SOFT, alpha=0.55, solid_capstyle="round"))
    # pulses (axes coords)
    for p in pulses:
        x = x0 + (x1 - x0) * p
        ax.add_line(Line2D([x, x], [y-0.05, y+0.05], transform=ax.transAxes,
                           lw=lw, color=INK, alpha=0.85, solid_capstyle="round"))

def label(ax, x, y, text, ha="left", va="center", alpha=0.85, size=10):
    ax.text(x, y, text, transform=ax.transAxes, ha=ha, va=va,
            fontsize=size, color=SOFT, alpha=alpha)

# ----------------------------
# Generate signals
# ----------------------------
x = np.linspace(0, 2*np.pi, 600)

s1 = np.sin(x)
s2 = 0.7*np.sin(2*x + 0.5)
s3 = 0.5*np.sin(3*x - 0.8)

# Nonlinear entangled version (components distort each other)
entangled = (
    np.sin(x + 0.4*s2) +
    0.7*np.sin(2*x + 0.6*s3) +
    0.5*np.sin(3*x + 0.3*s1)
)

# ----------------------------
# Plot
# ----------------------------
fig, axes = plt.subplots(1, 2, figsize=FIGSIZE, gridspec_kw={"wspace": 0.12})

for ax in axes:
    base_axes(ax)

# Left: separated readouts
axes[0].set_prop_cycle(color=plt.rcParams['axes.prop_cycle'].by_key()['color'][1:])
axes[0].plot(x, s1, alpha=0.55, linewidth=1.5)
axes[0].plot(x, s2, alpha=0.55, linewidth=1.5)
axes[0].plot(x, s3, alpha=0.55, linewidth=1.5)

# Right: entangled composite readout
axes[1].plot(x, entangled, linewidth=2.2)

# Labels (bottom-left, as you suggested)
label(axes[0], 0.03, 0.15, "Perturbation", alpha=0.9, size=10.5)
label(axes[0], 0.03, 0.05, "Separated readouts", alpha=0.75, size=9.5)

label(axes[1], 0.03, 0.15, "Treatment", alpha=0.9, size=10.5)
label(axes[1], 0.03, 0.05, "Readout becomes a trajectory (mixed)", alpha=0.75, size=9.5)

# Minimal pulse timelines (now in axes coordinates, robust)
pulse_timeline(axes[0], pulses=[0.18])                     # single-shot perturbation
pulse_timeline(axes[1], pulses=[0.18, 0.40, 0.62, 0.84])   # repeated dosing regimen

# Title
fig.suptitle("From Perturbation to Treatment", fontsize=15.5, y=0.98, color=INK)

plt.tight_layout()
plt.show()


# %%
save_path="../docs/assets/images/biounfold-016-from-perturbation-to-treatment.png"
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

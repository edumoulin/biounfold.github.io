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

# ----------------------------
# Style knobs (match your style)
# ----------------------------
FIGSIZE = (12.0, 3.6)
BG = "#f7f7f7"
INK = "#222222"
SOFT = "#666666"
BLUE = "#1f77b4"
RED = "#d62728"

def base_axes(ax):
    ax.set_facecolor(BG)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

# ----------------------------
# Schematic model
# Goals:
#  - Non-zero value at x=0 (simple assay still has value)
#  - Low analysis quality: almost monotonically decreases with heterogeneity
#  - Higher analysis quality: peak shifts right and increases
# ----------------------------
x = np.linspace(0.0, 1.0, 700)

def signal_curve(x, q, baseline=0.18, sat=0.20,
                 a=3.4, noise_pow=3.1, q_pow=2.3,
                 amplitude_gain=0.22, gain_pow=1.2):
    """
    baseline: shared value at x=0 (simple, homogeneous assay has some value)
    diversity: added hypothesis bandwidth (rises then saturates)
    penalty: ambiguity cost (worse with heterogeneity), mitigated by analysis quality
    amplitude_gain: how much extra value heterogeneity *can* provide (if analysis can exploit it)
    """
    # Adds potential signal as heterogeneity increases (then saturates)
    diversity = 1.0 - np.exp(-x / sat)

    # Ambiguity cost grows quickly with heterogeneity; analysis quality mitigates it
    penalty = np.exp(-a * (x ** noise_pow) / (q ** q_pow + 1e-12))

    # How effectively analysis turns diversity into usable signal (superlinear in q)
    gain = (q ** gain_pow)

    return baseline + amplitude_gain * gain * diversity * penalty

# Choose qualities so low is nearly monotone decreasing
q_low, q_mid, q_high = 0.35, 0.85, 1.80

# Increase ambiguity cost for low-quality only to make it monotone-ish
y_low  = signal_curve(x, q_low,  a=7.0, noise_pow=2.8, q_pow=2.2, amplitude_gain=0.26)
y_mid  = signal_curve(x, q_mid,  a=3.8, noise_pow=3.0, q_pow=2.3, amplitude_gain=0.26)
y_high = signal_curve(x, q_high, a=3.0, noise_pow=3.2, q_pow=2.4, amplitude_gain=0.26)

# Normalize for aesthetics (keeps baseline > 0, but compresses into [0,1])
m = max(y_low.max(), y_mid.max(), y_high.max())
y_low, y_mid, y_high = y_low/m, y_mid/m, y_high/m

# ----------------------------
# Plot
# ----------------------------
fig, ax = plt.subplots(1, 1, figsize=FIGSIZE)
fig.patch.set_facecolor(BG)
base_axes(ax)

ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.05, 1.12)

# Shade "homogeneity enforced" region
homo_end = 0.22
ax.axvspan(0.00, homo_end, color=INK, alpha=0.05, lw=0)
ax.text(0.02, 0.09, "Highly homogeneous screen\n(simple, tractable, but capped)",
        transform=ax.transAxes, ha="left", va="bottom",
        fontsize=11, color=SOFT)

# Curves (legend encodes analysis quality)
ax.plot(x, y_low,  color=INK,  lw=2.2, alpha=0.95, label="Low")
ax.plot(x, y_mid,  color=BLUE, lw=2.4, alpha=0.95, label="Medium")
ax.plot(x, y_high, color=RED,  lw=2.6, alpha=0.95, label="High")

# Mark maxima (if interior maxima exist)
def mark_max(x, y, color):
    i = int(np.argmax(y))
    ax.scatter(x[i], y[i], s=45, color=color, zorder=6)
    return x[i], y[i]

xm_low,  ym_low  = mark_max(x, y_low,  INK)
xm_mid,  ym_mid  = mark_max(x, y_mid,  BLUE)
xm_high, ym_high = mark_max(x, y_high, RED)

# Arrow: optimal heterogeneity shifts right (from mid->high, since low may max at x=0)
ax.annotate("optimal heterogeneity\nshifts right",
            xy=(xm_high, ym_high),
            xytext=(xm_mid,  ym_high),
            arrowprops=dict(arrowstyle="->", lw=2.0, color=SOFT, alpha=0.9),
            fontsize=11, color=SOFT, ha="center", va="bottom")

# Arrow: analysis improves
xA = 0.55
ax.annotate("analysis improves",
            xy=(xA, np.interp(xA, x, y_high)),
            xytext=(xA, np.interp(xA, x, y_low)- 0.1),
            arrowprops=dict(arrowstyle="->", lw=2.0, color=SOFT, alpha=0.9),
            fontsize=11, color=SOFT, ha="center", va="center")

# Axis titles (annotations, no ticks)
ax.text(0.5, -0.02, "Controlled heterogeneity (contexts / time / assays)",
        transform=ax.transAxes, ha="center", va="top",
        fontsize=11, color=INK)

ax.text(-0.02, 0.5, "Signal extracted\n(usable / classifiable structure)",
        transform=ax.transAxes, ha="right", va="center",
        fontsize=11, color=INK, rotation=90)

fig.suptitle("Signal Extraction in Imaging Screens",
             fontsize=18, y=0.98, color=INK)

leg = ax.legend(
    title="Analysis quality",
    loc="upper right",
    frameon=True,
    fontsize=11
)

# Style legend background to hide curves
leg.get_frame().set_facecolor(BG)
leg.get_frame().set_edgecolor("none")
leg.get_frame().set_alpha(1.0)

# Title + text styling
plt.setp(leg.get_title(), fontsize=12, color=INK)
for t in leg.get_texts():
    t.set_color(SOFT)

plt.tight_layout()
plt.show()


# %%
save_path="../docs/assets/images/biounfold-019-signal-extraction-in-imaging-screens.png"
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

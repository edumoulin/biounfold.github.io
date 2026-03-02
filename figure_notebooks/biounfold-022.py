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
# Helpers
# ----------------------------
def hill_increasing(x, ec50, hill=1.0, top=100.0, bottom=0.0):
    """Increasing dose-response (effect increases with concentration)."""
    return bottom + (top - bottom) * (x**hill) / (ec50**hill + x**hill)

def radar_axes(fig, rect, n_vars):
    ax = fig.add_axes(rect, polar=True)
    angles = np.linspace(0, 2*np.pi, n_vars, endpoint=False)
    ax.set_theta_offset(np.pi / 2)   # start at top
    ax.set_theta_direction(-1)       # clockwise
    return ax, angles

def plot_radar_with_uncertainty(ax, angles, mean, sd, labels, title=None):
    mean = np.asarray(mean)
    sd = np.asarray(sd)

    # clamp to [0, 1] for display
    lo = np.clip(mean - sd, 0, 1)
    hi = np.clip(mean + sd, 0, 1)

    # close the loop
    ang_c = np.r_[angles, angles[0]]
    mean_c = np.r_[mean, mean[0]]
    lo_c = np.r_[lo, lo[0]]
    hi_c = np.r_[hi, hi[0]]

    ax.plot(ang_c, mean_c, linewidth=2.0)
    ax.fill_between(ang_c, lo_c, hi_c, alpha=0.12)

    ax.set_xticks(angles)
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["", "", "", ""])  # cleaner
    ax.set_ylim(0, 1.0)

    if title:
        ax.set_title(title, fontsize=12, pad=12)

def plot_two_subpops(ax, x, yA, yB, sdA, sdB, title=None):
    ax.plot(x, yA, linewidth=2.0, label="Subpop A")
    ax.fill_between(x, yA - sdA, yA + sdA, alpha=0.25)

    ax.plot(x, yB, linewidth=2.0, label="Subpop B")
    ax.fill_between(x, yB - sdB, yB + sdB, alpha=0.25)

    ax.set_xscale("log")
    ax.set_xlim(x.min(), x.max())
    ax.set_ylim(-5, 105)
    ax.set_yticks([0, 50, 100])
    ax.set_xlabel("Concentration", fontsize=10)
    ax.set_ylabel("Effect", fontsize=10)
    ax.grid(True, which="both", linewidth=0.6, alpha=0.35)
    ax.legend(frameon=False, fontsize=9, loc="lower right")

    if title:
        ax.set_title(title, fontsize=11, pad=8)

# ----------------------------
# Synthetic data
# ----------------------------
proteins = ["Protein A", "Protein B", "Protein C", "Protein D", "Protein E"]

# Binding (0..1) means + uncertainty bands
# Unoptimized: broad-ish binding + higher uncertainty
bind_unopt_mean = [0.55, 0.35, 0.45, 0.40, 0.30]
bind_unopt_sd   = [0.12, 0.10, 0.10, 0.10, 0.08]

# Path 1: sharpen A
bind_p1_mean = [0.90, 0.18, 0.20, 0.12, 0.12]
bind_p1_sd   = [0.05, 0.06, 0.06, 0.05, 0.05]

# Path 2: sharpen D
bind_p2_mean = [0.12, 0.18, 0.20, 0.92, 0.10]
bind_p2_sd   = [0.05, 0.06, 0.06, 0.05, 0.05]

# Dose-response x grid
x = np.logspace(-10, -4, 240)

# We want "reverse improvement":
# - Path 1: Subpop A improves (lower EC50), Subpop B worsens (higher EC50)
# - Path 2: Subpop B improves, Subpop A worsens

# Unoptimized: both subpops mediocre, similar
y0_A = hill_increasing(x, ec50=2e-7, hill=1.0)
y0_B = hill_increasing(x, ec50=3e-7, hill=1.0)

# Path 1: A improves, B worsens
y1_A = hill_increasing(x, ec50=2e-9, hill=1.2)
y1_B = hill_increasing(x, ec50=8e-7, hill=1.0)

# Path 2: B improves, A worsens
y2_A = hill_increasing(x, ec50=7e-7, hill=1.0)
y2_B = hill_increasing(x, ec50=5e-9, hill=1.4)

# Uncertainty bands (simple heteroscedastic heuristic: bigger around mid-response)
def response_sd(y, base=3.5, mid=9.0):
    # larger around ~50% effect
    return base + mid * np.exp(-((y - 50.0) ** 2) / (2 * 18.0 ** 2))

sd0_A = response_sd(y0_A, base=4.0, mid=10.0)
sd0_B = response_sd(y0_B, base=4.0, mid=10.0)

sd1_A = response_sd(y1_A, base=3.0, mid=8.0)
sd1_B = response_sd(y1_B, base=3.5, mid=8.5)

sd2_A = response_sd(y2_A, base=3.5, mid=8.5)
sd2_B = response_sd(y2_B, base=3.0, mid=8.0)

# ----------------------------
# Layout
# ----------------------------
FIGSIZE = (12.8, 6.4)
fig = plt.figure(figsize=FIGSIZE)
fig.suptitle("Affinity can sharpen a hypothesis while activity diverges across biological context",
             fontsize=20, y=1.1)

col_lefts = [0.05, 0.37, 0.69]
w = 0.27

radar_rects = [[L, 0.53, w, 0.40] for L in col_lefts]
dose_rects  = [[L, 0.10, w, 0.32] for L in col_lefts]

# Radars
rad_axes = []
angles = None
for rect in radar_rects:
    ax_r, ang = radar_axes(fig, rect, n_vars=len(proteins))
    rad_axes.append(ax_r)
    angles = ang

plot_radar_with_uncertainty(rad_axes[0], angles, bind_unopt_mean, bind_unopt_sd, proteins,
                            title="Unoptimized\n(broad engagement)")
plot_radar_with_uncertainty(rad_axes[1], angles, bind_p1_mean, bind_p1_sd, proteins,
                            title="Path 1\n(sharpen A)")
plot_radar_with_uncertainty(rad_axes[2], angles, bind_p2_mean, bind_p2_sd, proteins,
                            title="Path 2\n(sharpen D)")

# Dose-response (two subpops)
ax0 = fig.add_axes(dose_rects[0])
ax1 = fig.add_axes(dose_rects[1])
ax2 = fig.add_axes(dose_rects[2])

plot_two_subpops(ax0, x, y0_A, y0_B, sd0_A, sd0_B, title="Activity (context-dependent)")
plot_two_subpops(ax1, x, y1_A, y1_B, sd1_A, sd1_B, title="Activity (Subpop A improves,\nSubpop B worsens)")
plot_two_subpops(ax2, x, y2_A, y2_B, sd2_A, sd2_B, title="Activity (Subpop B improves,\nSubpop A worsens)")

# Small footnote/caption text
fig.text(
    0.05, 0.005,
    "Top: binding profile (mean ± uncertainty). Bottom: activity can reverse across subpopulations even when binding looks sharper.",
    fontsize=10, alpha=0.85
)

plt.show()


# %%
save_path="../docs/assets/images/biounfold-022-binding-affinity.png"
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

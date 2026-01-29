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
# Style knobs
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
# Toy landscape (same as before)
# ----------------------------
def f(x):
    return (
        0.08 * x**2
        - 1.50 * np.exp(-((x - 0.25) ** 2) / (2 * 0.28**2))   # global
        - 0.95 * np.exp(-((x + 2.10) ** 2) / (2 * 0.35**2))   # local left
        - 0.85 * np.exp(-((x - 2.30) ** 2) / (2 * 0.38**2))   # local right
    )

def df(x, eps=1e-4):
    return (f(x + eps) - f(x - eps)) / (2 * eps)

xs = np.linspace(-4.0, 4.0, 1200)
ys = f(xs)

# ----------------------------
# Gradient descent trajectory (left)
# ----------------------------
x0 = -3.4
lr = 0.15
steps = 22
traj = [x0]
x = x0
for _ in range(steps):
    x = x - lr * df(x)
    traj.append(x)
traj = np.array(traj)
traj_y = f(traj)

# ----------------------------
# "Samples" for the right panel
# (pretend these are the expensive wet queries)
# ----------------------------
samples_x = np.array([-2.7, -1.9, -0.05, 0.5, 1.6, 2.8])
samples_y = f(samples_x)  # observed values (could add noise if you want)

# Sort samples for interpolation
order = np.argsort(samples_x)
samples_x = samples_x[order]
samples_y = samples_y[order]

# ----------------------------
# Build a smooth interpolant that passes through sample points
# ----------------------------
use_scipy = True
try:
    from scipy.interpolate import CubicSpline
except Exception:
    use_scipy = False

if use_scipy:
    spline = CubicSpline(samples_x, samples_y, bc_type="natural")
    mean = spline(xs)
else:
    # Fallback: piecewise-linear interpolation (not as smooth, but passes points)
    mean = np.interp(xs, samples_x, samples_y)

# ----------------------------
# Uncertainty band grows with distance to nearest sample point
# ----------------------------
# distance to nearest sampled x
d = np.min(np.abs(xs[:, None] - samples_x[None, :]), axis=1)

# Turn distance into a sigma in y-units
yr = ys.max() - ys.min()
d_norm = d / (d.max() + 1e-12)

sigma_floor = 0.02 * yr          # tight near samples
sigma_scale = 0.25 * yr          # how wide gaps can get
p = 1.2                          # growth curve; >1 makes it grow faster in big gaps
sigma = sigma_floor + sigma_scale * (d_norm ** p)

upper = mean + sigma
lower = mean - sigma

# ----------------------------
# Plot
# ----------------------------
fig, (axL, axR) = plt.subplots(1, 2, figsize=FIGSIZE, gridspec_kw=dict(wspace=0.18))
fig.patch.set_facecolor(BG)
for ax in (axL, axR):
    base_axes(ax)

ymin, ymax = ys.min(), ys.max()
pad = 0.10 * (ymax - ymin)
ymin -= pad
ymax += pad

# Left: landscape + GD trap
axL.plot(xs, ys, color=INK, lw=2.0)
axL.set_xlim(xs.min(), xs.max())
axL.set_ylim(ymin, ymax)

axL.scatter([traj[0]], [traj_y[0]], s=45, color=RED, zorder=4)
axL.text(traj[0], traj_y[0] + 0.06 * (ymax - ymin), "start",
         ha="center", va="bottom", fontsize=10, color=SOFT)

axL.plot(traj, traj_y, color=RED, lw=2.0, alpha=0.9, zorder=3)
for i in range(0, len(traj) - 1, 4):
    axL.annotate("", xy=(traj[i+1], traj_y[i+1]), xytext=(traj[i], traj_y[i]),
                 arrowprops=dict(arrowstyle="->", lw=1.5, color=RED, alpha=0.8))

axL.text(0.02, 0.95, "Local optimization\n(trapped)",
         transform=axL.transAxes, ha="left", va="top",
         fontsize=12, color=INK)

# Right: landscape + sampled points + interpolant + distance-based uncertainty
axR.plot(xs, ys, color=INK, lw=2.0, alpha=0.85)
axR.set_xlim(xs.min(), xs.max())
axR.set_ylim(ymin, ymax)

# sample markers
axR.scatter(samples_x, samples_y, s=35, color=INK, alpha=0.9, zorder=5)
for sx, sy in zip(samples_x, samples_y):
    axR.plot([sx, sx], [ymin, sy], color=SOFT, lw=1.1, alpha=0.18)

# belief/model curve + uncertainty band
axR.fill_between(xs, lower, upper, color=BLUE, alpha=0.10, lw=0)
axR.plot(xs, mean, color=BLUE, lw=2.2, alpha=0.95)

axR.text(0.02, 0.95, "Belief-guided sampling",
         transform=axR.transAxes, ha="left", va="top",
         fontsize=12, color=INK)

fig.suptitle("Two regimes of Learning (schematic)",
             fontsize=20, y=0.98, color=INK)

plt.tight_layout()
plt.show()


# %%
save_path="../docs/assets/images/biounfold-018-two-regimes-of-learning.png"
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

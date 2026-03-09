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
# Concept: Same potency, different exposure trajectories
# Decision is NOT trivial because there are three exposure regimes:
#   - Below efficacy threshold: "risk-only" (pure risk, no intended benefit)
#   - Between efficacy and safety: "benefit–risk trade-off"
#   - Above safety threshold: "toxic"
#
# Requested changes vs your last pasted baseline:
#   - Remove the wedge-like fills inside the therapeutic window
#   - Fill ONLY TWO areas under each curve:
#       (1) Below efficacy threshold  -> label "risk"
#       (2) Above safety threshold    -> label "toxic"
#   - Keep the window band shading for context
# ----------------------------

def one_comp_oral_pk(t, dose=1.0, ka=1.5, ke=0.25, V=1.0, F=1.0):
    """
    1-compartment oral PK with first-order absorption (ka) and elimination (ke).
    C(t) = (F*dose*ka)/(V*(ka-ke)) * (exp(-ke*t) - exp(-ka*t)) for ka != ke
    """
    t = np.asarray(t)
    if np.isclose(ka, ke):
        return (F * dose / V) * (ka * t) * np.exp(-ke * t)
    return (F * dose * ka) / (V * (ka - ke)) * (np.exp(-ke*t) - np.exp(-ka*t))

def time_in_band(t, c, lo, hi):
    """Approximate time where lo <= c <= hi."""
    t = np.asarray(t)
    c = np.asarray(c)
    mask = (c >= lo) & (c <= hi)
    if mask.sum() < 2:
        return 0.0
    dt = np.diff(t)
    return float(np.sum(dt * mask[:-1]))

def time_above(t, c, thr):
    """Approximate time where c >= thr."""
    t = np.asarray(t)
    c = np.asarray(c)
    mask = c >= thr
    if mask.sum() < 2:
        return 0.0
    dt = np.diff(t)
    return float(np.sum(dt * mask[:-1]))

# ----------------------------
# Synthetic setup
# ----------------------------
t = np.linspace(0, 24, 800)  # hours

# Same in vitro potency assumption -> same efficacy threshold
C_eff = 1.0

# Safety threshold (toy stand-in)
C_safe = 2.2

molecules = [
    dict(name="Molecule A", ka=3.2, ke=0.60, dose=7.0),
    dict(name="Molecule B", ka=1.4, ke=0.25, dose=5.2),
    dict(name="Molecule C", ka=0.7, ke=0.10, dose=4.4),
]

curves = []
metrics = []
for m in molecules:
    c = one_comp_oral_pk(t, dose=m["dose"], ka=m["ka"], ke=m["ke"], V=1.0, F=1.0)
    curves.append(c)

    t_window = time_in_band(t, c, C_eff, C_safe)
    t_above_safe = time_above(t, c, C_safe)
    cmax = float(np.max(c))

    metrics.append(dict(t_window=t_window, t_above_safe=t_above_safe, cmax=cmax))

# ----------------------------
# Plot
# ----------------------------
fig, ax = plt.subplots(figsize=(11.2, 6.2))
ax.set_title("Exposure is segmented into regimes: risk, trade-off, and toxic", fontsize=18, pad=12)

# Background regime shading (context only)
ax.axhspan(0, C_eff, alpha=0.06)        # risk-only band
ax.axhspan(C_eff, C_safe, alpha=0.10)  # trade-off band (therapeutic window)
ax.axhspan(C_safe, 10, alpha=0.06)     # toxic band (top clipped by y-lim later)

ax.text(0.35, C_eff * 0.55, "Risk", fontsize=10, va="center")
ax.text(0.35, (C_eff + C_safe) / 2, "Benefit–risk trade-off", fontsize=10, va="center")
ax.text(0.35, C_safe * 1.35, "Toxic", fontsize=10, va="center")

# Threshold lines
ax.axhline(C_eff, linewidth=1.6, linestyle="--")
ax.axhline(C_safe, linewidth=1.6, linestyle="--")
ax.text(24.0, C_eff * 1.02, "Efficacy threshold", fontsize=10, va="bottom", ha="right")
ax.text(24.0, C_safe * 1.02, "Safety threshold", fontsize=10, va="bottom", ha="right")

# Curves + ONLY TWO filled areas under curves:
#   (1) below efficacy threshold (risk)
#   (2) above safety threshold (toxic)
for m, c, met in zip(molecules, curves, metrics):
    ax.plot(t, c, linewidth=2.2, label=m["name"])

    # Risk area: between y=0 and min(c, C_eff)
    ax.fill_between(t, 0, np.minimum(c, C_eff), alpha=0.18, 
                    facecolor="0.85", hatch="///", edgecolor="0.6")

    # Toxic area: between y=C_safe and c (only where c >= C_safe)
    ax.fill_between(t, C_safe, c, where=(c >= C_safe), alpha=0.14, 
                    facecolor="0.85", hatch="xxx", edgecolor="0.6")

    # Annotate metrics near peak
    # idx_max = int(np.argmax(c))
    # ax.text(
    #     t[idx_max],
    #     c[idx_max] * 1.03,
    #     f"Cmax={met['cmax']:.2f}\n"
    #     f"{met['t_window']:.1f} h in window\n"
    #     f"{met['t_above_safe']:.1f} h in toxic",
    #     fontsize=9,
    #     ha="center",
    #     va="bottom"
    # )

# Axis styling
ax.set_xlim(0, 24)
ymax = max(float(np.max(c)) for c in curves) * 1.12
ax.set_ylim(0, ymax)

ax.set_xlabel("Time", fontsize=11)
ax.set_ylabel("Concentration (a.u.)", fontsize=11)
ax.grid(True, linewidth=0.6, alpha=0.35)

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles, frameon=False, fontsize=10, loc="upper right")

fig.text(
    0.02, -0.05,
    "Filled areas under curves highlight two measurable extremes: time spent below efficacy (risk) and above safety (toxic).\n"
    "The band between thresholds represents a positive benefit–risk trade-off rather than a zero-risk zone.",
    fontsize=12,
    alpha=0.85
)

plt.tight_layout()
plt.show()

# %%
save_path="../docs/assets/images/biounfold-023-adme.png"
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

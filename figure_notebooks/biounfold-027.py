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

fig, ax = plt.subplots(figsize=(12, 4.2))
ax.set_xlim(0, 3)
ax.set_ylim(0, 1)
ax.axis("off")

xs = [0.45, 1.5, 2.55]
y_top = 0.64
y_mid = 0.50
y_bottom = 0.30

top_labels = ["plates", "organ-on-chip", "mouse"]
bottom_labels = ["isolate", "reconstruct", "confront"]

for x, top, bottom in zip(xs, top_labels, bottom_labels):
    ax.text(x, y_top, top, ha="center", va="center",
            fontsize=22, fontweight="bold")
    ax.text(x, y_bottom, bottom, ha="center", va="center",
            fontsize=15)
    ax.plot([x, x], [y_top - 0.08, y_bottom + 0.06], lw=1)

ax.annotate(
    "",
    xy=(xs[1] - 0.18, y_mid),
    xytext=(xs[0] + 0.18, y_mid),
    arrowprops=dict(arrowstyle="->", lw=2)
)
ax.annotate(
    "",
    xy=(xs[2] - 0.16, y_mid),
    xytext=(xs[1] + 0.23, y_mid),
    arrowprops=dict(arrowstyle="->", lw=2)
)

ax.text(1.5, 0.9, "From Isolation to Entanglement",
        ha="center", va="center", fontsize=18)

plt.tight_layout()
plt.show()

# %%
save_path="../docs/assets/images/biounfold-027-organ-on-chip.png"
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

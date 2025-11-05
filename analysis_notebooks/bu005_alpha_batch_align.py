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

# %% [markdown]
# <style>
#   /* Sticky bar at the very top */
#   #nb-sticky-bar {
#     position: sticky;
#     top: 0;
#     z-index: 1000;
#     background: white;
#     border-bottom: 1px solid #ddd;
#     padding: 8px 12px;
#   }
#
#   /* Respect dark mode if the page has it */
#   @media (prefers-color-scheme: dark) {
#     #nb-sticky-bar {
#       background: #111;
#       border-bottom-color: #333;
#     }
#     #nb-sticky-bar button {
#       color: #eee;
#       border-color: #444;
#       background: #222;
#     }
#   }
#
#   /* Button styling */
#   #nb-sticky-bar button {
#     padding: 6px 12px;
#     border: 1px solid #ccc;
#     border-radius: 6px;
#     background: #f9f9f9;
#     cursor: pointer;
#     font-size: 14px;
#   }
#   #nb-sticky-bar button:hover { background: #eee; }
#
#   /* Hide only CODE cell inputs when body has .hide-code */
#   body.hide-code .jp-CodeCell .jp-Cell-inputWrapper{
#     display: none;
#   }
#
#   /* Always show code when printing and hide the bar */
#   @media print {
#     body.hide-code .jp-CodeCell .jp-Cell-inputWrapper{
#       display: block !important;
#     }
#     #nb-sticky-bar { display: none; }
#   }
# </style>
#
# <script>
# (function () {
#   function ready(fn) {
#     if (document.readyState === 'loading') {
#       document.addEventListener('DOMContentLoaded', fn, { once: true });
#     } else {
#       fn();
#     }
#   }
#
#   ready(function () {
#     // Create the sticky bar and button
#     const bar = document.createElement('div');
#     bar.id = 'nb-sticky-bar';
#
#     const btn = document.createElement('button');
#     btn.id = 'toggle-code';
#     btn.type = 'button';
#     bar.appendChild(btn);
#
#     // Find the main notebook container so we can place the bar before it
#     const mainCandidates = [
#       'main',                            // generic main container
#     ];
#
#     let mainEl = null;
#     for (const sel of mainCandidates) {
#       const el = document.querySelector(sel);
#       if (el) { mainEl = el; break; }
#     }
#
#     if (mainEl && mainEl.parentElement === document.body) {
#       document.body.insertBefore(bar, mainEl);
#     } else {
#       // Fallback: put at the very top of <body>
#       document.body.prepend(bar);
#     }
#
#     function isHidden() { return document.body.classList.contains('hide-code'); }
#     function setHidden(hidden) {
#       document.body.classList.toggle('hide-code', hidden);
#       btn.textContent = hidden ? 'Show code' : 'Hide code';
#     }
#
#     btn.addEventListener('click', () => setHidden(!isHidden()));
#     // Hide on load
#     setHidden(true);
#   });
# })();
# </script>
#

# %% [markdown]
# Educational Notebook — Batch Align: Design-Aware Correction
# ================================================================================
#
# This notebook provides an **educational reimplementation of Batch Align**,  
# a simple and intuitive method for correcting batch effects in
# high-dimensional biological data.
#
# Unlike advanced empirical-Bayes methods such as **ComBat**
# (Johnson et al., *Biostatistics*, 2007),
# Batch Align relies only on **mean and variance alignment** —  
# making it transparent, easy to visualize, and ideal for explaining the
# *logic* behind batch correction.
#
# The goal is not to reproduce production-ready software,
# but to **illustrate the principle**:
# how batch correction works, and how including or omitting
# biological covariates (the “design”) changes what is preserved or erased.
#
# ⚠️ DISCLAIMER
# -------------
# This code is for **educational and exploratory purposes only**.  
# It is **not** intended for production or publication analyses.  
#
# For real-world data, use validated implementations such as:
# - R: `sva::ComBat()` (Bioconductor)
# - Python: `scanpy.pp.combat()`, `neuroCombat`, or `pycombat`
# - RNA-seq counts: `ComBat-Seq` (Zhang et al., 2020)
#
# These packages provide full empirical-Bayes estimation,  
# robust handling of small batches, and tested defaults.
#
# Notebook structure
# ------------------
# 1. **Concept** – what batch effects are and why design-aware correction matters  
# 2. **Simulation** – generate data with confounded biology and batch effects  
# 3. **Batch Align** – correct batches *with and without* biological covariates
# 4. **Takeaways** – what this simple method teaches about design-aware correction
#
# **Author**: Etienne Dumoulin  
# **Series**: BioUnfold #5α — *Noise & Signal*  
# **Date**: Nov-03-2025
#

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import StandardScaler

plt.rcParams["figure.figsize"] = (10, 4)
plt.rcParams["axes.grid"] = True
plt.rcParams["figure.dpi"] = 120


# %% [markdown]
# ## 1. Concept — Why Design-Aware Correction Matters
#
# When biological and technical sources of variation overlap,
# a naïve batch correction can remove the very signal we care about.
# **Batch Align** offers a transparent way to illustrate this risk.
#
# It standardizes each feature within each batch (mean and variance)
# and then re-centers everything to a common reference —  
# simple enough to visualize, yet powerful enough to show how
# design choices affect the outcome.
#
# In this notebook, we will see two cases:
#
# - **Without design:** batch correction removes part of the biology.  
# - **With design:** biology is preserved, while batch effects collapse.
#
# That difference captures the essence of *design-aware correction* —  
# and why it matters long before we reach complex models like ComBat.
#

# %% [markdown]
# ## 2. Simulation — Building a Simple Confounded Dataset
#
# To explore how Batch Align behaves, we first need data where
# **biology and batch are partially confounded** — a realistic scenario in
# omics or imaging experiments.
#
# We will simulate:
# - Two batches with different means and variances  
# - A binary biological label (e.g., treatment vs. control)  
# - Imbalance of labels across batches
#
# This imbalance ensures that batch effects and biology overlap,
# so we can observe what happens when correction is applied
# **without** and **with** a biological design matrix.
#
# The goal is not realism in every detail, but **clarity**:
# a dataset simple enough that the geometry of the correction
# is visible in a PCA plot.
#

# %%
def simulate_batch_data(
    n_features=500,
    n_samples_per_batch=(60, 60),
    group=(0.5, 0.5),
    group_shift=0.8
):
    """
    Simulate high-dimensional 'omics-like' data with:
    - Two batches with distinct offsets/scales
    - A biological grouping (0/1) with optional imbalance per batch

    Parameters
    ----------
    n_features : int
        Number of features.
    n_samples_per_batch : tuple of int
        Number of samples per batch.
    group : tuple of float
        Probability of biological group=1 in each batch (must match number of batches).
    group_shift : float
        Mean shift applied to a subset of features for biological group=1.

    Returns
    -------
    X : pd.DataFrame (features × samples)
    batch : pd.Series (per-sample batch label)
    group : pd.Series (per-sample biological group label)
    """
    batches = []
    batch_labels = []
    group_labels = []

    n_total = sum(n_samples_per_batch)
    base = np.random.normal(0, 1, size=(n_features, n_total))

    start = 0
    for b, n in enumerate(n_samples_per_batch):
        end = start + n
        # group imbalance: proportion group=1 depends on batch
        p = group[b] if b < len(group) else group[-1]
        g = (np.random.rand(n) < p).astype(int)
        group_labels.extend(g)

        # batch-specific offset/scale
        loc_shift = np.random.normal(0.5 * (b + 1), 0.1)
        scale_mult = np.random.uniform(0.9, 1.3)
        base[:, start:end] = (base[:, start:end] + loc_shift) * scale_mult
        batch_labels.extend([f"batch_{b+1}"] * n)
        start = end

    # biological signal
    X = base.copy()
    affected = np.random.choice(n_features, size=n_features // 5, replace=False)
    group_labels = np.array(group_labels)
    X[affected[:, None], np.where(group_labels == 1)[0]] += group_shift

    # wrap in pandas
    samples = [f"S{i+1}" for i in range(n_total)]
    X_df = pd.DataFrame(X, index=[f"F{i+1}" for i in range(n_features)], columns=samples)
    batch = pd.Series(batch_labels, index=samples, name="batch")
    group = pd.Series(group_labels, index=samples, name="group")
    return X_df, batch, group



# %%
np.random.seed(42)

# Simulate data
X, batch, group = simulate_batch_data(
    n_features=600,
    n_samples_per_batch=(70, 70),
    group=(0.2, 0.8),
    group_shift=0.8
)


# Include an intercept + group indicator
design = pd.DataFrame(
    {
        "Intercept": 1.0,
        "Group": group.values
    },
    index=group.index
)


# %% [markdown]
# We now have a synthetic dataset where batch effects and biology overlap.
# Before correction, the batches will appear as separate clusters in PCA space.
# Next, we apply **Batch Align** to see how a design matrix changes what the
# algorithm preserves or removes.

# %%
def pca2d(X: pd.DataFrame, n_components: int = 2, random_state: int = 42):
    """
    Fit a 2D PCA on samples (columns) of a features×samples matrix X.
    Returns:
      coords : (n_samples, 2) array of PC coordinates
      var_sum : float, sum of explained variance ratio for PC1+PC2
    Notes:
      - Features are standardized (z-scored) across samples before PCA.
      - X must be features (rows) × samples (cols).
    """
    scaler = StandardScaler(with_mean=True, with_std=True)
    Xz = scaler.fit_transform(X.T)          # samples × features
    pca = PCA(n_components=n_components, random_state=random_state)
    coords = pca.fit_transform(Xz)
    var_sum = float(np.sum(pca.explained_variance_ratio_[:2]))
    return coords, var_sum


def pca_scatter(ax, coords: np.ndarray, labels=None, title: str = "", 
                alpha: float = 0.85, s: float = 18.0, palette=None):
    """
    Scatter plot of 2D PCA coordinates.
    - If `labels` is provided (array-like or pandas Series), points are grouped and a legend is shown.
    - Does not set explicit colors; relies on Matplotlib defaults.
    """
    if labels is None:
        ax.scatter(coords[:, 0], coords[:, 1], alpha=alpha, s=s)
    else:
        lab = pd.Series(labels)
        cats = pd.Categorical(lab).categories

        # Choose palette
        if palette is None:
            if lab.name and "batch" in lab.name.lower():
                colors = sns.color_palette("tab10", n_colors=len(cats))
            elif lab.name and "group" in lab.name.lower():
                colors = sns.color_palette("Set2", n_colors=len(cats))
            else:
                colors = sns.color_palette("tab10", n_colors=len(cats))
        else:
            colors = sns.color_palette(palette, n_colors=len(cats))
            
        for val, col in zip(cats, colors):
            idx = (lab == val).values
            ax.scatter(coords[idx, 0], coords[idx, 1], label=str(val),
                       color=col, alpha=alpha, s=s)
        ax.legend(loc="best", fontsize=8, frameon=True)

    ax.set_title(title)
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")

# PCA before correction (two small panels)
coords, var = pca2d(X)

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
pca_scatter(axes[0], coords, labels=batch,  title=f"Before — color: Batch (var≈{var:.2f})")
pca_scatter(axes[1], coords, labels=group,  title=f"Before — color: Biology (var≈{var:.2f})")
fig.suptitle("PCA before Batch Correction", y=1.03)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 3. Batch Align — Minimal Implementation
#
# The goal here is to show the **mechanics** of batch correction with as little code as possible.
#
# Steps:
# 1) **Standardize** each feature across all samples.  
# 2) **Optionally preserve biology** by regressing out a design matrix (e.g., intercept + group).  
# 3) On the **residuals**, estimate per-batch mean and variance.  
# 4) **Align** each batch by removing its mean and scaling to unit variance.  
# 5) **Recombine** the preserved biology and de-standardize back to the original scale.
#
# This version omits edge-case handling (NaNs, tiny batches, shrinkage).  
# It is intentionally simple so the geometry of the correction is easy to see.
#

# %%
import numpy as np
import pandas as pd

def _zscore_features(X: pd.DataFrame):
    """
    Z-score per feature (rows) across samples (cols).
    Assumes numeric, finite values (no NaNs/Infs).
    Returns: Z, mean, std
    """
    mean = X.mean(axis=1)
    std = X.std(axis=1, ddof=1).replace(0, np.nan).fillna(1.0)
    Z = X.sub(mean, axis=0).div(std, axis=0)
    return Z, mean, std

def _fit_design(Z: pd.DataFrame, design: pd.DataFrame | None):
    """
    If a design is provided, fit Z ~ design (OLS) feature-wise and return:
      fitted (design part) and residuals R = Z - fitted.
    If no design, fitted = 0 and R = Z.
    """
    if design is None:
        fitted = pd.DataFrame(0.0, index=Z.index, columns=Z.columns)
        return fitted, Z.copy()

    # OLS: solve Z ≈ X β by minimizing ||Z - Xβ||².
    # Intercept captures baseline; Group coefficient captures group difference.
    # This isolates biological signal so batch correction does not remove it.
    # β = (XᵀX)⁺ Xᵀ Z is computed via pseudoinverse (SVD) for stability.
    Xmat = design.loc[Z.columns].values
    XtX_inv_Xt = np.linalg.pinv(Xmat.T @ Xmat) @ Xmat.T
    # Solve feature-wise in one go: Beta^T = (XtX)^-1 X^T Z^T
    Beta_T = XtX_inv_Xt @ Z.T.values
    fitted = (Xmat @ Beta_T).T

    fitted_df = pd.DataFrame(fitted, index=Z.index, columns=Z.columns)
    R = Z - fitted_df
    return fitted_df, R

def batch_align_minimal(X: pd.DataFrame,
                        batch: pd.Series,
                        design: pd.DataFrame | None = None):
    """
    Minimal Batch Align (location–scale) without shrinkage.

    X      : features × samples
    batch  : per-sample batch labels (index aligned to X.columns)
    design : optional design matrix (e.g., intercept + biology) to preserve

    Returns: X_aligned (same shape as X)
    """
    # 1) Standardize features globally
    Z, mu, sd = _zscore_features(X)

    # 2) Preserve design effects (optional)
    design_aligned = None if design is None else design.loc[X.columns]
    fitted, R = _fit_design(Z, design_aligned)

    # 3) Estimate per-batch mean/var on residuals
    bcat = pd.Categorical(batch.loc[X.columns])
    levels = list(bcat.categories)

    R_adj = R.copy()
    for lev in levels:
        cols = R.columns[bcat == lev]
        Rij = R.loc[:, cols]
        g = Rij.mean(axis=1).values
        v = Rij.var(axis=1, ddof=1).replace(0, np.nan).fillna(1.0)
        # 4) Align this batch: remove mean, scale to unit variance
        R_adj.loc[:, cols] = (Rij.sub(g, axis=0)).div(np.sqrt(v), axis=0)

    # 5) Recombine design and de-standardize to original scale
    Z_adj = fitted + R_adj
    X_adj = Z_adj.mul(sd, axis=0).add(mu, axis=0)
    return X_adj


# %%
# Without design (will partially erase biology)
X_align_noMM = batch_align_minimal(X, batch, design=None)

# With design (preserves biology)
X_align_MM = batch_align_minimal(X, batch, design=design)

# %% [markdown]
# Now that we have a minimal implementation of **Batch Align**,  
# we can apply it to our simulated dataset — first **without** a biological design matrix,
# and then **with** one.
#
# The two results will show how a design-aware correction changes what is preserved:
# - *Without design*, batch effects are removed but part of the biological separation disappears.  
# - *With design*, the same correction collapses batches while keeping biological structure intact.
#
# Let’s visualize these effects side by side using PCA.

# %%
# 3×2 PCA grid:
# Columns: Before | No design | With design
# Row 1: color = Batch
# Row 2: color = Biology

mats = [
    ("Before", X),
    ("No design", X_align_noMM),
    ("With design", X_align_MM),
]

# Precompute PCA coords + variance for each matrix
coords_map = {}
for name, Xmat in mats:
    coords, var = pca2d(Xmat)
    coords_map[name] = (coords, var)

# 2x3 grid: Batch (top), Biology (bottom)
fig, axes = plt.subplots(2, 3, figsize=(14, 8), dpi=150)
for col, (name, _) in enumerate(mats):
    coords, var = coords_map[name]
    # Row 1: batch
    pca_scatter(axes[0, col], coords, labels=batch,
                title=f"{name} — color: Batch (var≈{var:.2f})")
    # Row 2: biology
    pca_scatter(axes[1, col], coords, labels=group,
                title=f"{name} — color: Biology (var≈{var:.2f})")

fig.suptitle("PCA Before/After Batch Align — Batch vs Biology", y=1.03, fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.98])
plt.show()

# Optional: Save in LinkedIn-friendly format
fig.savefig(
    "../docs/assets/images/biounfold-005-figure-batch-align-grid-linkedin.png",
    dpi=300,
    bbox_inches="tight",
    facecolor="white",
    transparent=False
)
plt.close(fig)


# %% [markdown]
# ## 4. Takeaways — Seeing Correction in Numbers
#
# The PCA plots make the geometry visible.  
# To quantify it, we can check how each sample’s nearest neighbours
# relate to **batch** and **biology** before and after correction.
#
# If correction works, we expect:
# - **Batch consistency** (neighbours from same batch) to **decrease**  
# - **Biology consistency** (neighbours from same group) to **increase or remain high**
#
# This simple nearest-neighbour check offers a numeric view of how
# well the correction aligns data across batches while keeping biology intact.
#

# %%
from sklearn.metrics import pairwise_distances
import numpy as np
import pandas as pd

def nn_consistency(X: pd.DataFrame, labels: pd.Series, k: int = 5) -> float:
    """
    Mean fraction of k nearest neighbours sharing the same label.
    Operates on samples (columns) of a features×samples matrix X.
    """
    D = pairwise_distances(X.T, metric="euclidean")
    np.fill_diagonal(D, np.inf)
    nn_idx = np.argsort(D, axis=1)[:, :k]
    lab = labels.values
    same = (lab[nn_idx] == lab[:, None]).astype(float)
    return float(same.mean())

def nn_consistency_zscored(X: pd.DataFrame, labels: pd.Series, k: int = 5) -> float:
    """
    NN consistency computed after global per-feature z-scoring.
    (Removes scale effects from de-standardization.)
    """
    mu = X.mean(axis=1).values[:, None]
    sd = X.std(axis=1, ddof=1).replace(0, 1.0).values[:, None]
    Xz = (X.values - mu) / sd
    Xz = pd.DataFrame(Xz, index=X.index, columns=X.columns)
    return nn_consistency(Xz, labels, k=k)

def nn_summary_table(mats, batch, group, k: int = 5) -> pd.DataFrame:
    """
    mats: list of (name, Xmatrix) pairs
    Returns a tidy DataFrame with NN consistency for batch and biology.
    """
    rows = []
    for name, Xmat in mats:
        rows.append({
            "Condition": name,
            "Batch NN (z)":   nn_consistency_zscored(Xmat, batch, k=k),
            "Biology NN (z)": nn_consistency_zscored(Xmat, group, k=k),
        })
    df = pd.DataFrame(rows).set_index("Condition")
    return df.round(3)

# Build and display the table
mats = [("Before", X), ("No design", X_align_noMM), ("With design", X_align_MM)]
nn_table = nn_summary_table(mats, batch=batch, group=group, k=5)
nn_table

# %% [markdown]
# Batch correction is a balancing act:  
# it should **reduce technical structure** (batches mixing better)  
# while **preserving biological structure** (groups staying distinct).
#
# | Condition | Batch NN (z) ↓ | Biology NN (z) ↑ |
# |:-----------|:---------------|:----------------|
# | Before | 0.700 | 0.906 |
# | No design | 0.380 | 0.559 |
# | With design | 0.651 | 0.860 |
#
# The **“No design”** correction removes batch effects but also erases real biology.  
# Adding a **design matrix** restores biological separation while keeping batches aligned —  
# showing how statistical awareness can preserve meaning, not just remove variance.
#

# %%

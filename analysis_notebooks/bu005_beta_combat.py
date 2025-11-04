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
# # Educational Notebook — Batch Correction with ComBat (Empirical Bayes)
# ================================================================================
#
# This notebook extends the previous *Batch Align* demonstration by implementing
# the **ComBat algorithm** (Johnson et al., *Biostatistics*, 2007) — a cornerstone
# method for batch effect correction in high-dimensional biological data.
#
# Where *Batch Align* equalized batches by mean and variance,  
# **ComBat** goes further by applying **Empirical Bayes (EB) shrinkage**,  
# borrowing information across features to stabilize estimates — especially
# when batches are small or noisy.
#
# ⚠️ **DISCLAIMER**
# ----------------
# This notebook is for **educational purposes only**.
# It is **not** intended for production or publication analyses.
#
# For real data, use the validated implementations:
# - **R**: `sva::ComBat()` (Bioconductor)  
# - **Python**: `scanpy.pp.combat()`, `pycombat`, or `neuroCombat`  
# - **RNA-seq counts**: `ComBat-Seq` (Zhang et al., *NAR*, 2020)
#
# ---
#
# ## Notebook structure
#
# 1. **Concept** – from Batch Align to Empirical Bayes  
# 2. **Simulation** – reuse the confounded dataset from *Batch Align*  
# 3. **ComBat** – implement the full EB correction step
# 4. **Takeaways** – when shrinkage helps (and when it can mislead)
#
# ---
#
# **Author:** Etienne Dumoulin  
# **Date:** Nov-04-2025  
# **Series:** BioUnfold #5β — *AI in Drug Discovery: Dealing with Noise (Part II)*
#

# %%
# Cell 0 — Imports & global setup (run once)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import StandardScaler

# Matplotlib defaults (neutral; no specific colors forced)
plt.rcParams["figure.figsize"] = (10, 4)
plt.rcParams["axes.grid"] = True
plt.rcParams["figure.dpi"] = 120


# %% [markdown]
# ## 1. Concept — From Batch Align to Empirical Bayes
#
# In the previous notebook, we used **Batch Align** to correct systematic differences
# between batches by re-centering and rescaling each one.  
# That method works well when batches are large and balanced,  
# but it estimates a separate mean and variance for every feature in every batch —
# which becomes unstable when sample sizes are small.
#
# **ComBat** addresses this problem using **Empirical Bayes (EB) shrinkage**.
#
# Instead of trusting each batch estimate independently,  
# it **shares information across features**, learning how batch effects behave
# *on average* and pulling noisy estimates toward those global trends.  
# The result is a correction that is both smoother and more reliable,
# especially for small or uneven batches.
#
# Conceptually:
#
# | Step | Batch Align | ComBat |
# |:-----|:-------------|:--------|
# | Estimation | Per-batch mean + variance | Same, but stabilized with EB priors |
# | Assumption | Each feature independent | Features share hyper-parameters |
# | Benefit | Simple, fast | Robust when data are limited |
# | Risk | Over-correction | Mild shrinkage bias |
#
# In practice, **ComBat ≈ Batch Align + regularization**.  
# It trades a bit of flexibility for much greater stability —  
# a principle that applies far beyond batch correction itself.
#
# For simplicity, we will **omit biological covariates** in this notebook.
#
# The goal here is to see how **Empirical Bayes shrinkage** behaves on its own —
# how it stabilizes correction when batches are small, unbalanced, or noisy.
# In real analyses, ComBat can combine both ideas —  
# design-awareness (*as in the previous notebook*) and empirical shrinkage (*as here*).
# But keeping them separate makes each concept easier to understand.

# %% [markdown]
# ## 2. Simulation — Small, Unequal, Heteroscedastic Batches (No Biology)
#
# To isolate what **Empirical Bayes** contributes, we simulate only **batch effects**:
# each batch has its own mean and scale, and batch sizes are **unequal** (some are small).
# This stresses per-feature estimates — exactly the regime where shrinkage helps.
#
# There is **no biology label** here; the task is purely to remove technical structure
# in a way that is stable when some batches are tiny.
#

# %%
def simulate_batches_only(
    n_features: int = 800,
    n_samples_per_batch = (6, 10, 4, 18),   # intentionally small & unequal
    loc_mu: float = 0.4,                     # average mean shift magnitude across batches
    loc_sd: float = 0.05,                    # variability of mean shifts
    scale_low: float = 0.9,                  # min multiplicative scale per batch
    scale_high: float = 1.8,                 # max multiplicative scale per batch
    noise_sigma: float = 1.0,
    seed: int | None = 42,
):
    """
    Simulate a features×samples matrix with batch-only effects:
      - Base noise ~ N(0, noise_sigma)
      - Per-batch location shift ~ N(loc_mu * (b+1), loc_sd)
      - Per-batch multiplicative scale ~ Uniform(scale_low, scale_high)

    Returns
    -------
    X : pd.DataFrame
        Features × samples matrix.
    batch : pd.Series
        Per-sample batch label aligned to X.columns.
    """
    rng = np.random.default_rng(seed)
    n_batches = len(n_samples_per_batch)
    n_total = int(np.sum(n_samples_per_batch))

    # base noise
    X = rng.normal(0.0, noise_sigma, size=(n_features, n_total))

    # apply per-batch location/scale
    start = 0
    batch_labels = []
    for b, n in enumerate(n_samples_per_batch):
        end = start + n
        loc = rng.normal(loc_mu * (b + 1), loc_sd)      # increasing mean by batch index
        sca = rng.uniform(scale_low, scale_high)        # heteroscedastic scales
        X[:, start:end] = (X[:, start:end] + loc) * sca
        batch_labels.extend([f"batch_{b+1}"] * n)
        start = end

    # wrap
    cols = [f"S{i+1}" for i in range(n_total)]
    X_df = pd.DataFrame(X, index=[f"F{i+1}" for i in range(n_features)], columns=cols)
    batch = pd.Series(batch_labels, index=cols, name="batch")
    return X_df, batch



# %%
# Example usage
np.random.seed(42)
X, batch = simulate_batches_only(
    n_features=800,
    n_samples_per_batch=(6, 10, 4, 18),  # stress-test small/unequal batches
    loc_mu=0.4, loc_sd=0.10,
    scale_low=0.7, scale_high=2.3,
    noise_sigma=1.0,
    seed=42
)

print(X.shape, batch.value_counts().to_dict())


# %% [markdown]
# We visualize samples in PC1/PC2 space, colored by **batch**.

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


def pca_scatter(ax, coords: np.ndarray, labels=None, title: str = "", alpha: float = 0.85, s: float = 18.0):
    """
    Scatter plot of 2D PCA coordinates.
    - If `labels` is provided (array-like or pandas Series), points are grouped and a legend is shown.
    - Does not set explicit colors; relies on Matplotlib defaults.
    """
    if labels is None:
        ax.scatter(coords[:, 0], coords[:, 1], alpha=alpha, s=s)
    else:
        lab = pd.Series(labels)
        for val in pd.Categorical(lab).categories:
            idx = (lab == val).values
            ax.scatter(coords[idx, 0], coords[idx, 1], label=str(val), alpha=alpha, s=s)
        ax.legend(loc="best", fontsize=8, frameon=True)

    ax.set_title(title)
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")

# PCA before correction (two small panels)
coords, var = pca2d(X)

fig, axes = plt.subplots(1, 1, figsize=(10, 4))
pca_scatter(axes, coords, labels=batch,  title=f"Before — color: Batch (var≈{var:.2f})")

# %% [markdown]
# ## 4. ComBat — Empirical Bayes Shrinkage
#
# The **Batch Align** approach estimates a separate mean and variance
# for each batch and feature — a simple *location–scale correction*.
# However, when some batches are small or noisy, these estimates become unstable,
# and the correction can amplify noise instead of removing it.
#
# **ComBat** improves this by adding a layer of **Empirical Bayes shrinkage**:
# instead of trusting each batch estimate in isolation,
# it borrows information across all features to estimate *how much*
# each batch mean and variance should deviate from the global trend.
#
# Mathematically, each batch–feature mean (`γ̂`) and variance (`δ̂²`)
# is pulled toward shared priors (`γ̄`, `δ̄²`) using a data-driven
# “borrowing strength” rule — balancing *fit* and *stability*.
#
# Conceptually:
#
# | Step | Batch Align | ComBat |
# |:------|:-------------|:--------|
# | Estimate per-feature batch means | Raw sample means | Shrunk toward global mean |
# | Estimate per-feature batch variances | Raw sample variances | Shrunk toward pooled variance |
# | Correction formula | Normalize per batch | Normalize with EB-smoothed parameters |
#
# In other words, **ComBat = Batch Align + regularization**.
#
# We will now implement a compact, self-contained version of ComBat
# to show how this empirical shrinkage stabilizes correction
# when some batches have few samples.
#

# %%
# %%capture
from bu005_alpha_batch_align import batch_align_minimal


# %%
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
    
def combat_minimal(X: pd.DataFrame, batch: pd.Series, eps: float = 1e-8) -> pd.DataFrame:
    """
    Minimal ComBat (parametric EB) without covariates.
    - Standardize features globally (z-score).
    - Estimate per-batch mean (gamma_hat) & variance (delta_hat) on standardized data.
    - Shrink gamma_hat toward batch-wise global mean via Normal–Normal EB.
    - Shrink delta_hat via Inverse-Gamma EB (method-of-moments priors).
    - Normalize residuals with EB-shrunk params, then de-standardize.

    Assumes: X is features×samples, batch aligns to X.columns, no NaNs/Infs.
    """
    # 1) Standardize globally: Z = (X - mu) / sd
    Z, mu, sd = _zscore_features(X)

    # 2) Residuals (no design in this notebook)
    R = Z

    # 3) Per-batch estimates on residuals
    bcat   = pd.Categorical(batch.loc[X.columns])
    levels = list(bcat.categories)
    G, N   = R.shape[0], R.shape[1]

    gamma_hat = np.zeros((G, len(levels)), dtype=float)  # mean per feature/batch
    delta_hat = np.ones((G, len(levels)),  dtype=float)  # var  per feature/batch
    n_j       = np.zeros(len(levels), dtype=int)

    # residual variance across all samples (for s2_gamma)
    sigma2_g = R.var(axis=1, ddof=1).to_numpy() + eps

    for j, lev in enumerate(levels):
        cols = R.columns[bcat == lev]
        Rij  = R.loc[:, cols]                          # features × n_j
        g    = Rij.mean(axis=1).to_numpy()             # per-feature residual mean in batch j
        v    = Rij.var(axis=1, ddof=1).to_numpy()      # per-feature residual var  in batch j
        n    = Rij.shape[1]
        gamma_hat[:, j] = g
        delta_hat[:, j] = np.where(np.isfinite(v) & (v > 0), v, 1.0)
        n_j[j]          = n

    # 4) EB shrinkage for means: Normal–Normal posterior
    # prior per batch: gamma ~ N(gamma0, tau2), estimate gamma0, tau2 across features
    gamma0 = gamma_hat.mean(axis=0)                    # batch-wise mean across features
    tau2   = gamma_hat.var(axis=0, ddof=1)            # batch-wise var  across features
    tau2   = np.where(tau2 > 1e-6, tau2, 1e-3)        # guard

    # sampling variance of gamma_hat (per feature, per batch)
    s2_gamma = np.stack([sigma2_g / max(n, 1) for n in n_j], axis=1)

    # posterior mean (elementwise): (tau2*gamma_hat + s2*gamma0) / (tau2 + s2)
    gamma_star = (tau2[None, :] * gamma_hat + s2_gamma * gamma0[None, :]) / (tau2[None, :] + s2_gamma + eps)

    # 5) EB shrinkage for variances: Inv-Gamma(a,b) via MoM + posterior
    m = delta_hat.mean(axis=0)                         # per-batch mean of variances across features
    v = delta_hat.var(axis=0, ddof=1)
    v = np.where(v > 1e-12, v, (m**2) * 10.0)          # guard tiny var
    a = 2.0 + (m**2) / v
    b = m * (a - 1.0)

    # posterior parameters per feature/batch
    a_star = np.stack([a[j] + 0.5 * max(n_j[j], 1) for j in range(len(levels))], axis=0)         # shape: J
    b_star = np.stack([b[j] + 0.5 * (max(n_j[j]-1, 0)) * delta_hat[:, j] for j in range(len(levels))], axis=1)  # G×J

    # posterior mean of delta: E[δ | data] = b_star / (a_star - 1)
    den = np.maximum(a_star - 1.0, 1.0001)             # avoid divide by ~0
    delta_star = b_star / den[None, :]
    delta_star = np.clip(delta_star, 1e-3, 1e3)

    # 6) Adjust residuals with EB-shrunk params, recombine, de-standardize
    R_adj = R.copy()
    for j, lev in enumerate(levels):
        cols = R.columns[bcat == lev]
        R_adj.loc[:, cols] = (R.loc[:, cols].to_numpy() - gamma_star[:, [j]]) / np.sqrt(delta_star[:, [j]])

    Z_adj = R_adj                                      # no design to add back
    X_adj = Z_adj.mul(sd, axis=0).add(mu, axis=0)
    return X_adj



# %%
# Baseline (from α): simple alignment
X_align = batch_align_minimal(X, batch, design=None)

# ComBat (EB, no design)
X_combat = combat_minimal(X, batch)

# %%
# 3×2 PCA grid:
# Columns: Before | No design | With design
# Row 1: color = Batch
# Row 2: color = Biology

mats = [("Before", X), ("Align", X_align), ("ComBat", X_combat)]

# Precompute PCA coords + variance for each matrix
coords_map = {}
for name, Xmat in mats:
    coords, var = pca2d(Xmat)
    coords_map[name] = (coords, var)

fig, axes = plt.subplots(1, 3, figsize=(14, 8))
for col, (name, _) in enumerate(mats):
    coords, var = coords_map[name]
    # Row 1: batch
    pca_scatter(axes[col], coords, labels=batch, title=f"{name} — color: Batch (var≈{var:.2f})")

fig.suptitle("PCA Before/After Combat", y=1.02)
plt.tight_layout()
plt.show()


# %% [markdown]
# ## 4. Takeaways — A Small Numeric Check
#
# Batch correction should **reduce technical structure** (batches mix better)
# without inventing new artefacts. A simple way to quantify this is the
# nearest-neighbour (NN) consistency by **batch** on z-scored features:
# lower is better (less batch clustering).
#

# %%
# ----- NN metric (batch-only) -----
def nn_consistency(X: pd.DataFrame, labels: pd.Series, k: int = 5) -> float:
    D = pairwise_distances(X.T, metric="euclidean")
    np.fill_diagonal(D, np.inf)
    nn_idx = np.argsort(D, axis=1)[:, :k]
    lab = labels.values
    same = (lab[nn_idx] == lab[:, None]).astype(float)
    return float(same.mean())

def nn_consistency_z(X: pd.DataFrame, labels: pd.Series, k: int = 5) -> float:
    mu = X.mean(axis=1).values[:, None]
    sd = X.std(axis=1, ddof=1).replace(0, 1.0).values[:, None]
    Xz = (X.values - mu) / sd
    Xz = pd.DataFrame(Xz, index=X.index, columns=X.columns)
    return nn_consistency(Xz, labels, k=k)

def nn_batch_table(mats, batch, k: int = 5) -> pd.DataFrame:
    rows = []
    for name, Xmat in mats:
        rows.append({"Condition": name, "Batch NN (z)": nn_consistency_z(Xmat, batch, k=k)})
    return pd.DataFrame(rows).set_index("Condition").round(3)

# Evaluate Before | Batch Align | ComBat
mats = [("Before", X), ("Batch Align", X_align), ("ComBat", X_combat)]
nn_table = nn_batch_table(mats, batch=batch, k=5)
nn_table

# %% [markdown]
# **Interpretation.**  
# - **Before**: high Batch-NN ⇒ strong batch clustering.  
# - **Batch Align**: Batch-NN drops — location/scale differences reduced.  
# - **ComBat**: Batch-NN drops at least as much, often further — EB shrinkage stabilizes correction when some batches are small or noisy.
#
# > In short: *ComBat ≈ Batch Align + regularization* — a steadier correction in the small/unequal-batch regime.

# %%

---
layout: null
title: "BioUnfold #11 — Hit Discovery: From Diagnosis to Prediction (LinkedIn Summary)"
date: 2025-12-01
summary_for: biounfold-011-from-diagnosis-to-prediction
published: false
---

Hit discovery is the moment when biology, chemistry, and computation finally converge. It is where months of assay design, optimization, and QC collapse into a single practical question:

**Which molecules do something meaningful to the system?**

At this stage, the workflow shifts from exploratory interpretation to *repeatable interpretation*. Most of the biology behaves as expected, and the anomalies — the 5 percent of odd wells, subtle drifts, or unexpected phenotypes — become the places where insight emerges.

**Hit discovery only works when a strong upstream foundation exists.** Assays must already be stable. Biomarkers must be known. Preprocessing must be standardized. And QC must be *live* — embedded during the run, not applied afterwards. Many failure modes come from partial QC: biologists catch biological artefacts, computational teams catch statistical or imaging artefacts, and true reliability appears only when both perspectives are integrated.

Representation choice is equally important. Whether teams use handcrafted features, lightweight embeddings, pretrained encoders, or foundation models, what matters is **biological fidelity and reproducibility** — and this must be evaluated during assay optimization, not improvised at hit discovery.

Teams typically rely on four complementary routes to call hits:

- **Single-feature scoring** for fast, interpretable biomarkers  
- **Classifier-based scoring** anchored by strong controls  
- **Unsupervised clustering** to reveal families of phenotypes  
- **Active learning** when experimentation and computation can run at the same pace  

Across imaging, biochemical assays, and binding screens, the logic stays the same: trustworthy signal, strong QC, stable representations, and clear hit criteria.

By hit discovery, AI shifts from **diagnostic** to **predictive** — ranking hits, surfacing subtle responders, and guiding validation. When experiment and computation finally operate at the same rhythm, hit discovery becomes not a bottleneck but a multiplier for the entire discovery engine.


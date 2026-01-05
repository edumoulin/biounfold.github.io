---
layout: null
title: "Similarity Is Not Mechanism: Limits of Representation in Biology"
date: 2026-01-05
summary_for: biounfold-014-measurements-knowledge-hypothesis
published: false
---

Self-supervised learning is now the default approach for biological foundation models. It promises scale without labels and unified representations across assays. But self-supervision is not a single idea. It is a set of architectural choices that encode assumptions about how biological variation should be organized.

Those assumptions matter. Biological measurements mix morphology, dose effects, stress responses, experimental artifacts, and context. Different self-supervised objectives organize that variation differently. Reconstruction-based models tend to capture local physical structure. Alignment and distillation-based models emphasize global invariances and often amplify structured artifacts when trained at scale.

In practice, embeddings are frequently evaluated using similarity or clustering. These analyses reward visual coherence, not mechanism. Cosine similarity assumes linearity and consistency that biology rarely satisfies, especially across dose and context.

This motivates a clearer separation:

**Measurements** describe perturbations.
**Knowledge** encodes known equivalences.
**Hypotheses** ask whether two perturbations are mechanistically equivalent.

Embeddings represent measurements. Equivalence is not a geometric property of representation space—it is a hypothesis that must be learned and tested.

Full article in the comments.

#TechBio #AIForScience #ComputationalBiology #DrugDiscovery #BioUnfold

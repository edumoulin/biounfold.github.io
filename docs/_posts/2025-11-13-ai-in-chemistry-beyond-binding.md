---
layout: post
title: "AI in Chemistry: Beyond Binding"
date: 2025-11-13
tags: [AI / Computation, Chemistry / Design]
---

### BioUnfold #7 — AI in Chemistry: Beyond Binding

![Beyond Binding](/assets/images/biounfold-007-beyond-binding.png){: width="90%"}

Recent advances in structure and docking models have meaningfully improved how we explore chemical space. AlphaFold and flexible docking models shorten early optimization cycles. They help teams generate and evaluate ideas faster.

But they mostly solve **one part** of the problem: **binding**.

In real drug programs, failure usually comes **after** binding is solved:

- Will the molecule dissolve where it needs to?
- Can it cross the right membranes?
- Does it clear too fast — or not at all?
- Does it interact with proteins we did not intend?

Drug design is always **multi-parameter**. Improving one property often worsens another:

| If you optimize for… | You often lose… |
|---|---|
| Stability | Clearance (risk of accumulation) |
| Potency | Solubility or permeability |
| Selectivity | Tissue access |

These trade-offs are not mistakes — they are the **work**.

#### A Practical Example

In a recent project, potency against the primary target was achieved early in lead optimization.  
The real effort was **solubility**.

Every gain in solubility reduced activity; restoring activity reduced solubility again. This is a common pattern. And the cost here is not just running the assay — it is the **chemistry effort required to make each new variant** we want to test. Solubility is difficult to predict computationally, and generating the right structure–property data is expensive.

The work was not finding “the best model.”  
The work was **making the trade-off intentional**.

#### Toxicology Is About Context

Toxicity rarely comes from a single bad interaction. More often, it reflects **where and when** the molecule acts.

Two patterns come up repeatedly:

1. **Off-target interactions**  
   Binding in a different tissue or cell state than intended.

2. **Persistence**  
   Slow clearance → accumulation → dose becomes damage.

One practical strategy (especially in oncology) is to target **cellular programs that are active in tumors but largely silent in healthy adult tissue**.  
This reduces the risk of interfering with essential functions elsewhere.

And when these risks are uncertain, **cell-based phenotypic screens** help validate whether the molecule’s overall behavior is tolerable — not at every cycle, but at **key turning points** where the chemistry meaningfully shifts.

#### Where AI Helps Today

The most useful AI systems in chemistry today do not replace decisions.  
They **help teams explore trade-offs faster**:

- Combine binding predictions with early solubility screens  
- Model stability alongside clearance estimates  
- Consider weak interactions, not just primary affinity  

This does not eliminate experimentation —  
it **makes the next experiment better**.

> **AI expands what we can try, not what we can skip.**

#### A Practical Step Forward

If you are integrating AI into chemistry workflows, one shift helps:

> **Choose one non-binding property and treat it as a first-class design objective early.**

Do not just generate molecules that bind.  
Generate molecules that **have a chance to behave well in a biological system**.

The goal is not perfect prediction.  
It is **shorter, more informed learning loops** — and these loops move drug discovery forward.


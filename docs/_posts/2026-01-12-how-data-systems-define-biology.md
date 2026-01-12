---
layout: post
title: "How Data Systems Define Biology"
date: 2026-01-09
tags: [ Strategy / Platforms ]
image: /assets/images/biounfold-015-hidden-theory-of-biology.png
---

### BioUnfold #15 — How Data Systems Define Biology

![Data Encoding Evolves](/assets/images/biounfold-015-hidden-theory-of-biology.png){: width="90%"}

Data systems are often treated as containers for biology. In reality, they are representations of biology. And discovery unfolds inside those representations.

**Every biotech company operates with a theory of biology.** Scientists usually experience this theory as experimental intuition, mechanistic belief, or program strategy. But the version that actually governs the organization is the one implemented in data systems. And there is always a gap between them. Experiments are conceptually rich and context-dependent; their encodings are sparse, rigid, and operational. The problem is not that this mismatch exists. The problem is when no one knows what it is.

This embedded theory lives in schemas and workflows. It determines what the organization can notice, retrieve, and connect. In doing so, it determines what “an experiment,” “a result,” or even “mechanism” can mean internally. Like any representation, data management systems simplify, omit, and formalize. But unlike a diagram in a paper, they are operational. Experiments, analyses, and decisions must pass through them.

#### Data is not an asset. It is a product.

In biotech, molecules are assets. Data is not. Data has no intrinsic value at rest. Static data does not guide experiments, change strategy, or generate insight. Treated as an asset, data becomes something to store, protect, and periodically migrate. That framing almost guarantees neglect.

**Data acquires value only when it is shaped into something people use**: to compare experiments, revisit failures, design new assays, or make decisions. In that sense, data management is not support. It is production. It is the continuous development of a product whose users are scientists, analysts, and leaders. The relevant question is not “where is the data stored,” but “what work does it enable.”

#### Data management is representation

Once data is treated as a product, its real design surface becomes visible. The core decisions are representational: what entities exist, what context must be captured, what variation is structured, and what makes two experiments comparable. These choices define the internal biological language of the company.

One of the most common failures is context. Most systems encode assays as endpoints: a phenotypic screen, an RNA-seq follow-up, an SAR optimization. What is rarely encoded is how assays relate to each other, what prior results motivated them, what external knowledge was incorporated, and what hypothesis they were meant to test. Downstream pipelines are captured. Conceptual lineage is not. Organizations can retrieve measurements, but not reasoning. They can aggregate results, but not belief updates.

Hypotheses almost always live in documents, meetings, and memory, not in data systems, which means they are invisible to computation and fragile to turnover.

A system that treats experiments as independent rows supports a different biology than one that treats them as linked interventions evolving over time. Many “data problems” are failures of this representational layer, not of technology.

#### Ownership is the structural bottleneck

Every coherent product has an owner. Most data systems in biotech do not. Responsibility is split across IT, informatics, scientists, and vendors. When asked who owns a workflow, the answer is often “it is complicated.” That already explains most failures.

Owning data management means owning the biological language of the company. It requires scope to define concepts, authority to change processes, and accountability for user impact. This is not an administrative role. It is a product role. Without ownership, systems grow by accumulation. Local fixes multiply. Global coherence erodes.

This is also where many data initiatives stall. Standards and FAIR principles are necessary, but they mainly address exchange and compliance. They do not define what the data is for, which users it serves, or how the organization’s biological concepts should evolve. FAIR can make data easier to move. It cannot decide what an experiment means.

#### Failure modes

When no one owns the representational layer, the same pathological patterns appear:

- **No owner.** Systems grow by historical accident. Each new project adds a tool. Nothing integrates.  
- **Too many owners with narrow scope.** Each team defines its own concepts. Comparability collapses.  
- **No product evaluation.** Systems are judged by deployment, not by changed behavior.

Some failure modes are structural. Research evolves. Assays change. Representations become wrong. Technical debt is not a pathology; it is the cost of learning what matters. The real failure is building systems that cannot revise their assumptions.

Friction is also inevitable. As organizations scale, multiple data products emerge. Boundaries will be imperfect. Mature data organizations are not frictionless. They are legible. Ownership is explicit. Concepts do not drift invisibly.

#### Why AI collides with this layer

AI is often described as a consumer of data. In practice, it stress-tests how biology has been represented. Models require that experiments are comparable across time, that context is explicit, that negative results exist, and that entities are stable enough to align.

These are not modeling details. They are commitments about what an experiment is. When models fail, they often fail because the organization does not have a coherent internal definition of its own data. AI does not sit on top of data management. It collides with it.

#### The claim

Data management is not infrastructure, documentation, or compliance. It is the system through which a discovery organization reasons about biology. Every schema encodes assumptions. Every workflow defines what can be learned.

**The real cost of getting this wrong is not inefficiency. It is limitation.** Data systems define what kinds of capabilities can ever emerge. If hypotheses are not representable, they cannot become computable. If context is not preserved, it cannot become institutional memory. If assay relationships are not encoded, they cannot become platforms.

Biotech companies build a theory of biology into software, and discovery unfolds inside it. The difference between organizations that compound and those that stall is whether this layer is treated as an evolving product or as invisible plumbing.


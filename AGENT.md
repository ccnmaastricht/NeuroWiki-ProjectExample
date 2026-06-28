# AGENT.md

Read this file at the start of every session, regardless of which workflow you are running.
After reading this file, read the module file for the current task.

---

## 1. Project Identity

This file is the identity and rule layer for one specific project wiki. Each project or research line gets its own copy of this template repository with its own `AGENT.md`.

```
Project name:             Example Wiki: The role of gamma synchrony in early visual cortex
Main research question:   Does gamma synchrony play a functional role in early visual cortex?
Model type(s):            Biophysical, Functional
Theories:                 Theory of Weakly Coupled Oscillators, Binding Through Synchrony, Binding By Enhanced Firing, etc.
Brain region(s):          V1, V4
Organism / data type:     Human, macaque
Key phenomena to explain: Gamma synchrony
  - 
Project-specific glossary: none
Contributors:             Mario Senden
```

---

## 2. Repository Structure

```
project-root/
├── AGENT.md              ← read first, every session
├── INGESTION.md          ← workflow: processing new PDFs
├── REFINE_A.md           ← workflow: structural harmonization
├── REFINE_B.md           ← workflow: depth audit
├── REFINE_C.md           ← workflow: cross-link audit
├── README.md             ← human-facing project overview
├── QUICKSTART.md         ← human-facing setup and usage guide
├── VERIFICATION.md       ← human-facing verification protocol
├── raw/                  ← source PDFs; never modified by agent
│   └── *.pdf
└── wiki/
    ├── primary.bib       ← BibTeX: papers with PDFs in raw/
    ├── secondary.bib     ← BibTeX: papers cited within PDFs but not in raw/
    ├── log.md    ← human verification log
    ├── index.md          ← wiki root index; agent navigation entry point
    └── pages/
        └── <TYPE>_<slug>.md
```

---

## 3. Page Types

There are no per-paper pages. Papers are sources synthesized into concept pages. The `.bib` files are the citation layer.

| Prefix | Type | Covers |
|--------|------|--------|
| `PHE_` | Phenomenon / empirical finding | An observed neural or behavioral regularity |
| `MOD_` | Model or method | A computational model, analysis method, or algorithm |
| `THE_` | Neuroscientific theory | A full theory that provides explanatory schema for models and has explanatory scope over phenomena |
| `REG_` | Brain region or cell type | Anatomy, physiology, connectivity of a region or cell class |
| `PAR_` | Experimental paradigm or dataset | A task, recording protocol, or canonical dataset |

Slug convention: lowercase, hyphenated, descriptive.
Examples: `PHE_place-cell-remapping`, `MOD_ring-attractor`, `REG_v1-layer4`, `PAR_morris-water-maze`

---

## 4. Citation Model

| Notation | Meaning | Source |
|----------|---------|--------|
| `(@OKeefe1971)` | Verified from a PDF in `raw/` | `primary.bib` |
| `(@Buzsaki2015†)` | Reconstructed from another paper's citation | `secondary.bib` |

The `†` dagger is never optional. Omitting it on a secondary citation misrepresents the reliability of a claim.

Citation key format: `AuthorYYYY`. Collisions: `Buzsaki2015a`, `Buzsaki2015b`.
Keys are stable across promotion: `(@Key†)` becomes `(@Key)` — the key itself does not change.

**primary.bib** — one entry per PDF in `raw/`. All fields verified against the PDF. Required field:
```
annote = {<one-line description of main contribution>}
```

**secondary.bib** — reconstructed from citations within PDFs. Uncertain fields flagged:
```
note = {reconstructed from @SourceKey}
```

---

## 5. Confidence Levels and Theory Status

### Confidence (PHE_, MOD_, REG_ pages)

Every `PHE_`, `MOD_`, and `REG_` page must carry a confidence field. Default to `speculative` when evidence is thin.

| Level | Meaning |
|-------|---------|
| `established` | Replicated across multiple independent labs, species, or methods; field consensus. Requires at minimum two independent sources. |
| `debated` | Genuine disagreement in the literature; conflicting evidence or interpretations exist |
| `speculative` | Based on limited evidence, a single study, or theoretical inference without strong empirical grounding |

Confidence upgrades and downgrades both require a note in the page's **Controversies** section citing the evidence that motivated the change.

> **Note**: `speculative` reflects thin evidence, not design purpose. A MOD_ page with `explanatory_role: how-possibly` is not speculative by default — how-possibly models are legitimate epistemic stages regardless of evidence quality. Distinguish evidence quality (confidence field) from explanatory status (`explanatory_role` field and **Explanatory Scope** section).

### Status (THE_ pages)

`THE_` pages do not carry a confidence or quality rating. Instead they carry a neutral **Status** field describing the theory's current standing in the field.

| Status | Meaning |
|--------|---------|
| `active-research-area` | The theory is actively developed, debated, and applied in current research |
| `settled` | The theory is broadly accepted; major disputes resolved; still used but no longer a frontier |
| `abandoned` | The theory has been superseded or discredited and is no longer actively pursued |

---

## 6. Page Templates

All pages use YAML frontmatter for structured metadata, followed by a markdown body.
The frontmatter `type` field is the only strictly required field; all others are strongly expected.

---

### 6.1 PHE_ — Phenomenon / Empirical Finding

```markdown
---
type: phenomenon
title: <full human-readable name>
confidence: established | debated | speculative
updated: YYYY-MM-DD
related:
  - REG_<slug>
  - PAR_<slug>
  - MOD_<slug>
tags: []
---

# <Phenomenon name>

## Description

<What is the phenomenon? Define it precisely, including conditions of observation.>

## Empirical Basis

<Synthesized summary across sources. Cite each claim: (@Key) primary, (@Key†) secondary.
Multiple sources for one claim: (@Key1, @Key2).>

## Key Parameters and Quantitative Signatures

<Specific numerical values: timescales, magnitudes, tuning widths, effect sizes.
Every number must be cited. Vague ranges without citations are not acceptable.>

## Generality

<Species, brain states, recording methods, behavioral conditions across which this holds.
Explicitly note where it breaks down or has not been tested.>

## Controversies

<Findings that contradict, qualify, or reframe the phenomenon.
All confidence changes explained here with citations.>

## Modeling Implications

<What must any model engaging with this phenomenon produce or respect?
Link to [[MOD_...]] pages.>
```

---

### 6.2 MOD_ — Model or Method

```markdown
---
type: model
title: <full human-readable name>
subtype: mechanistic | normative | data-driven | behavioral | analysis-method
explanatory_role: how-possibly | how-actually | phenomenological
confidence: established | debated | speculative
updated: YYYY-MM-DD
related:
  - PHE_<slug>
  - REG_<slug>
  - PAR_<slug>
tags: []
---

# <Model or method name>

## Description

<What is this model/method? What problem was it designed to solve?
What idealization strategy does it use: Galilean (distortions intended for progressive de-idealization), minimalist (incompleteness is the point), or multiple-models (one of several incompatible models pursuing different representational ideals)?>

## Descriptive Target

<What regularities does this model fit? What data or phenomena is it empirically adequate to?
A phenomenon showing a different pattern falsifies the model with respect to its descriptive target.>

## Explanatory Scope

<At what level of organization does this model have genuine mechanistic or constitutive grounding?
If phenomenological at one level, state which — and state whether it is mechanistic at another level.
Level-relativity is mandatory: a model may be phenomenological at one level and mechanistic at another; both must be stated explicitly.>

## Formal Description

<Equations, variables, interpretations. $inline$ and $$block$$ LaTeX.
Always present equations before prose interpretation.>

## Core Assumptions

- **Assumption**: <statement>
  - *Biological justification*: <what supports it> (@Key)
  - *When violated*: <conditions under which this breaks down>

## Empirical Support

<Evidence that the model captures real phenomena. (@Key)>

## Empirical Challenges

<Evidence that contradicts, limits, or complicates the model. (@Key)>

## Comparison to Alternatives

<How does this differ from competing models/methods? What does each handle better?>

## Controversies

<Ongoing disputes about validity, interpretation, or applicability.>

## Usage in the Literature

<Notable applications. What has this been used to explain or analyze? (@Key)>
```

---

### 6.3 THE_ — Neuroscientific Theory

```markdown
---
type: theory
title: <full human-readable name>
status: active-research-area | settled | abandoned
updated: YYYY-MM-DD
related:
  - PHE_<slug>
  - MOD_<slug>
  - REG_<slug>
tags: []
---

# <Theory name>

## Core Claims

<What does this theory assert? State the central theoretical commitments as precisely as possible. (@Key)>

## Explanatory Schema

<State the abstract pattern of explanation. Must satisfy three conditions:
1. Verbal and general: covers the full model family without fixing mathematical form.
2. Constraining: specify what would fail to instantiate it. A schema that excludes nothing is a slogan, not a schema.
3. Predictively inert alone: note which phenomena fall within scope but require specific model instances to test or falsify.
(@Key)>

## Model Family

<What formal models instantiate this theory? What do they share structurally?
Link to relevant [[MOD_...]] pages.>

## Mechanistic Grounding

<At what level of organization does this theory operate?
What mechanisms does it invoke, and which does it leave unspecified or treat as black boxes? (@Key)>

## Empirical Scope

<What phenomena is this theory designed to explain?
What is explicitly outside its scope or left for other frameworks?
Link to relevant [[PHE_...]] pages.>

## Controversies

<Disputed claims, competing interpretations, or unresolved debates within or about this theory.>

## Key Sources

<Foundational and landmark papers. (@Key)>
```

---

### 6.4 REG_ — Brain Region or Cell Type

```markdown
---
type: region
title: <full human-readable name>
confidence: established | debated | speculative
updated: YYYY-MM-DD
related:
  - PHE_<slug>
  - MOD_<slug>
  - PAR_<slug>
tags: []
---

# <Region or cell type name>

## Anatomical Identity

<Location, laminar structure, major subregions or subtypes. (@Key)>

## Physiology

<Firing rates, spiking patterns, intrinsic currents. All values cited. (@Key)>

## Connectivity

<Major inputs and outputs. Feedforward/feedback/lateral distinction.
Laminar, cell-type, and synaptic specificity where known. (@Key)>

## Functional Role(s)

<What computations or behaviors is this region/cell type implicated in? (@Key)>

## Controversies

<Disputed claims about anatomy, physiology, or function.>

## Modeling Considerations

<What properties must a model of this region capture?
What simplifications are common and when do they fail? Link to [[MOD_...]] pages.>
```

---

### 6.5 PAR_ — Experimental Paradigm or Dataset

```markdown
---
type: paradigm
title: <full human-readable name>
updated: YYYY-MM-DD
related:
  - PHE_<slug>
  - REG_<slug>
  - MOD_<slug>
tags: []
---

# <Paradigm or dataset name>

## Description

<What is this paradigm or dataset? What is the experimental logic or data structure?>

## What It Measures / Reveals

<What neural or behavioral variables does it give access to?
What phenomena has it been used to characterize? (@Key)>

## Standard Variants

<Common protocol variants and what they emphasize differently.>

## Limitations and Confounds

<Known confounds, what the paradigm cannot distinguish, species/state dependencies.>

## Key Studies and Datasets

<Landmark papers or publicly available datasets. (@Key) or (@Key†)>

## Relevance to This Project

<How is or could this paradigm be used in the current project's context?>
```

---

## 7. wiki/index.md Structure

`wiki/index.md` is the agent's navigation entry point for the entire wiki. It must be kept current by every workflow that creates or modifies pages. The agent reads this file first when navigating the wiki, then follows links to relevant pages rather than scanning the full `pages/` directory.

```markdown
---
type: index
title: Wiki Root Index
updated: YYYY-MM-DD
---

# Wiki Index — <Project Name>

## Phenomena
| Page | Title | Confidence | Updated |
|------|-------|------------|---------|
| [PHE_place-cell-remapping](pages/PHE_place-cell-remapping.md) | Place cell remapping | established | 2025-03-10 |

## Models & Methods
| Page | Title | Confidence | Updated |
|------|-------|------------|---------|

## Theories
| Page | Title | Status | Updated |
|------|-------|--------|---------|

## Brain Regions & Cell Types
| Page | Title | Confidence | Updated |
|------|-------|------------|---------|

## Paradigms & Datasets
| Page | Title | Updated |
|------|-------|---------|
```

Links in `index.md` use relative markdown paths (`pages/TYPE_slug.md`), not `[[TYPE_slug]]` notation, so the file is navigable by both agents and standard markdown renderers.

Cross-links within page bodies continue to use `[[TYPE_slug]]` notation.

---

## 8. Conflict Resolution Rules

The agent is never permitted to silently choose one position over another when papers conflict.

### Conflict types

| Type | Description |
|------|-------------|
| Quantitative | Same measure, different values |
| Qualitative | Contradictory direction or existence of an effect |
| Interpretive | Same data, different conclusions |
| Scope | Both correct but under different conditions |

### Handling

**Quantitative and scope**: represent both values/conditions with citations. Note the likely source of discrepancy. Do not average or choose. Set confidence to `debated` if not already.

**Qualitative**: both positions in Empirical Basis with neutral framing. Structured Controversies entry:

```
### <Conflict title>
- **Position A**: <statement> (@Key1)
- **Position B**: <statement> (@Key2)
- **Possible resolution**: <if one exists>
- **Status**: unresolved | partially resolved | resolved
- **⚑ Human review requested**: <reason, if modeling-relevant>
```

**Interpretive**: represent both interpretations with citations. Do not adjudicate.

**Irreconcilable** (bearing on core modeling choices): add to Controversies, set confidence to `debated`, add to page header:

```
> ⚑ **Human review required**: Irreconcilable conflict between (@Key1) and (@Key2) on [topic].
> See Controversies section.
```

List all such flags in the session summary.

---

## 9. Citation Integrity Rules

**When writing or rewriting:**
- Every factual claim carries at least one citation
- Every quantitative value is cited — a number without a citation is never acceptable
- Confidence changes cite the motivating evidence in the Controversies section
- Method descriptions cite the original source of the method

**When reading existing pages:**
- Uncited factual claim, source identifiable: add the citation inline
- Uncited factual claim, source not identifiable: flag as `<!-- UNCITED: <claim summary>, flagged YYYY-MM-DD -->`
- Do not delete or rewrite a claim solely because it lacks a citation
- List all flags added in the session summary

---

## 10. Behavioral Rules

1. Read AGENT.md first, then the module file, before any file operation.
2. Never modify files in `raw/`.
3. Never fabricate citations. Unresolvable secondary references: `<!-- UNRESOLVED: <description> -->`.
4. The `†` dagger is mandatory on every secondary citation.
5. Equations before prose on all MOD_ pages.
6. PHE_ and REG_ pages describe observations. MOD_ pages describe proposals. Never conflate.
7. Confidence is mandatory on every PHE_, MOD_, and REG_ page.
8. Cross-link using `[[TYPE_slug]]` within page bodies. Use relative paths in `index.md`.
9. Flag uncertainty with `> ⚠️ Uncertain: <reason>`.
10. Rewrite, don't append. Git history is the changelog.
11. Promotions are content reviews, not find-and-replace. Re-evaluate every claim previously citing the secondary source against the actual PDF.
12. End every session with a structured summary covering: files modified, flags raised, conflicts found, citation integrity issues.

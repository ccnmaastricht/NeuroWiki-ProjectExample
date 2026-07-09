# TEMPLATES.md

Read this file when creating or restructuring wiki pages.
Referenced by INGESTION.md (Steps 5–6) and REFINE_A.md (Steps A1–A3).

---

## 1. Page Templates

All pages use YAML frontmatter for structured metadata, followed by a markdown body.
The frontmatter `type` field is the only strictly required field; all others are strongly expected.

---

### 1.1 PHE_ — Phenomenon

```markdown
---
type: phenomenon
title: <full human-readable name>
confidence: established | debated | speculative
updated: YYYY-MM-DD
related:
  - REG_<slug>
  - CEL_<slug>
  - MOD_<slug>
tags: []
---

# <Phenomenon name>

## Description

<What is the phenomenon? Define it precisely, including conditions of observation.
Covers neural and behavioral regularities at any level — firing patterns, oscillations,
psychophysical effects, learning phenomena, and functional network patterns (e.g. DMN).>

## Empirical Basis

<Synthesized summary across sources. Cite each claim: (@Key) primary, (@Key†) secondary.
Multiple sources for one claim: (@Key1, @Key2).>

## Key Parameters and Quantitative Signatures

<Specific numerical values: timescales, magnitudes, tuning widths, effect sizes.
Every number must be cited. Vague ranges without citations are not acceptable.>

## Generality

<Species, brain states, recording methods, behavioral conditions across which this holds.
Explicitly note where it breaks down or has not been tested.>

## Controversies *(add only if encountered)*

<Only include this section when the source material directly presents conflicting findings,
disputed claims, or competing interpretations. Do not speculate about potential controversies.
If confidence changes, document the motivating evidence here. Omit the section entirely if
none of the above apply.>

## Modeling Implications

<What must any model or theory engaging with this phenomenon produce or respect?
Link to [[MOD_...]] and [[THE_...]] pages.>
```

---

### 1.2 MOD_ — Computational Model

> **MOD_ vs ANA_ boundary**: if the model makes claims about neural computation, representation,
> or mechanism — even implicitly — it belongs in MOD_. Models used purely as measurement or
> summarization tools without mechanistic interpretation belong in ANA_.

> **MOD_ vs SIM_ boundary**: a MOD_ page describes the model; a SIM_ page describes the software
> that integrates it. Hodgkin-Huxley is MOD_; NEURON, which numerically solves it, is SIM_.
> Name a model's reference implementation on the SIM_ page, not here.

> **Classification guide**
>
> `marr_level` — choose all that apply:
> - `computational`: characterizes *what problem* the system solves and *why*. May involve a
>   normative claim (optimal, rational, efficient) but need not — a purely descriptive
>   information-processing account also sits here.
> - `algorithmic`: specifies the representations and processes that implement the solution;
>   abstracts over biophysical details. Example: attractor dynamics, update rules, Kalman filter.
> - `implementational`: maps onto specific biological hardware — neurons, ion channels, synapses,
>   anatomical pathways. Example: Hodgkin-Huxley, conductance-based networks.
>
> `explanatory_character`:
> - `phenomenological`: model variables fit input-output regularities without corresponding to
>   identifiable biological components. Could be replaced by any equivalent function with equal
>   validity as a description of the target.
> - `mechanistic`: satisfies the 3M criterion (Kaplan & Craver 2011): (a) model variables
>   correspond to components, activities, properties, or organizational features of the target
>   mechanism; AND (b) dependencies among variables correspond to causal relations among those
>   components. Diagnostic question: does removing a variable lose a structural claim about the
>   mechanism, or only fit quality?

```markdown
---
type: model
title: <full human-readable name>
explanatory_character: phenomenological | mechanistic
marr_level:           # list; computational level may carry a normative claim
  - computational
  - algorithmic
  - implementational
construction: theory-derived | data-driven | hybrid
exploratory: true | false
confidence: established | debated | speculative
updated: YYYY-MM-DD
related:
  - PHE_<slug>
  - NET_<slug>
  - THE_<slug>
tags: []
---

# <Model name>

## Description

<What is this model? What problem was it designed to solve?
If exploratory (exploratory: true), state what class of mechanisms it demonstrates are in
principle sufficient — and why this constrains theorizing about the target phenomenon.
If the model involves idealization choices worth noting (e.g. deliberate distortions intended
for progressive refinement, or intentional incompleteness), describe them here or in Core
Assumptions — not in Explanatory Scope.>

## Descriptive Target

<What regularities does this model fit? What data or phenomena is it empirically adequate to?
A phenomenon showing a different pattern falsifies the model with respect to its descriptive target.
If exploratory: true, state what the model demonstrates is possible rather than what it fits.>

## Explanatory Scope

<State what level(s) of organization this model operates at (from marr_level) and what kind
of explanatory claim it makes (from explanatory_character).
If explanatory_character: mechanistic, state which components, activities, properties, or
organizational features of the target mechanism the model's variables correspond to, and which
causal relations among those components the model's dependencies capture (3M criterion:
Kaplan & Craver 2011).
If marr_level includes computational and the model makes a normative claim, state the objective
or optimality principle being invoked.
Level-relativity is mandatory: a model may be phenomenological at one level and mechanistic
at another; both must be stated explicitly.>

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

<How does this differ from competing models? What does each handle better?>

## Controversies *(add only if encountered)*

<Only include this section when the source material directly presents disputes about validity,
interpretation, or applicability. Do not speculate. If confidence changes, document the
motivating evidence here. Omit the section entirely if none of the above apply.>

## Usage in the Literature

<Notable applications. What has this been used to explain or analyze? (@Key)>
```

---

### 1.3 THE_ — Neuroscientific Theory

> **Umbrella theories**: when a theory subsumes other theories as sub-cases (e.g. the Bayesian
> brain hypothesis encompassing predictive coding, efficient coding, and optimal control),
> represent it as a THE_ page with links to sub-theory THE_ pages in the **Model Family**
> section and in `related`. The relationship is theoretical architecture, not a type distinction.

```markdown
---
type: theory
title: <full human-readable name>
status: emerging | active-research-area | settled | abandoned
updated: YYYY-MM-DD
related:
  - PHE_<slug>
  - MOD_<slug>
  - THE_<slug>
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
For umbrella theories: list sub-theories and what they contribute; link to [[THE_...]] pages.
For emerging theories: describe the model family as it currently exists, noting where it is
incomplete or contested.
Link to relevant [[MOD_...]] pages.>

## Mechanistic Grounding

<At what level of organization does this theory operate?
What mechanisms does it invoke, and which does it leave unspecified or treat as black boxes? (@Key)>

## Empirical Scope

<What phenomena is this theory designed to explain?
What is explicitly outside its scope or left for other theories?
Link to relevant [[PHE_...]] pages.>

## Controversies *(add only if encountered)*

<Only include this section when the source material directly presents disputed claims,
competing interpretations, or unresolved debates. Do not speculate. Omit entirely if none
of the above apply.>

## Key Sources

<Foundational and landmark papers. (@Key)>
```

---

### 1.4 REG_ — Brain Region

```markdown
---
type: region
title: <full human-readable name>
confidence: established | debated | speculative
updated: YYYY-MM-DD
related:
  - CEL_<slug>
  - NET_<slug>
  - PHE_<slug>
tags: []
---

# <Region name>

## Anatomical Identity

<Location, boundaries, major subdivisions, cytoarchitectonic characteristics. (@Key)>

## Connectivity

<Major inputs and outputs. Feedforward/feedback/lateral distinction.
Laminar and cell-type specificity where known. (@Key)>

## Functional Role(s)

<What computations or behaviors is this region implicated in? (@Key)>

## Principal Cell Types

<Dominant neuronal populations. Link to [[CEL_...]] pages.>

## Controversies *(add only if encountered)*

<Only include this section when the source material directly presents disputed claims about
anatomy, connectivity, or functional role. Do not speculate. Omit entirely if none apply.>

## Modeling Considerations

<What properties must a model of this region capture?
What simplifications are common and when do they fail?
Link to [[MOD_...]] and [[NET_...]] pages.>
```

---

### 1.5 CEL_ — Cell Type

```markdown
---
type: cell_type
title: <full human-readable name>
confidence: established | debated | speculative
updated: YYYY-MM-DD
related:
  - REG_<slug>
  - PHE_<slug>
  - NET_<slug>
tags: []
---

# <Cell type name>

## Identity

<Defining properties: morphology, molecular markers, intrinsic membrane properties.
For functionally-defined types (place cells, grid cells), state both the functional
criterion and any known molecular or morphological correlates. (@Key)>

## Distribution

<Which regions contain this cell type. Layer specificity and prevalence where known. (@Key)>

## Physiology

<Firing patterns, intrinsic currents, membrane time constants, adaptation properties.
All quantitative values cited. (@Key)>

## Connectivity

<Synaptic targets and sources. Cell-type and compartment (soma/dendrite/axon) specificity. (@Key)>

## Functional Role(s)

<What computations or behaviors is this cell type implicated in? (@Key)>

## Controversies *(add only if encountered)*

<Only include this section when the source material directly presents disputed claims about
classification, physiology, or function. Note where molecularly-defined and
functionally-defined boundaries diverge, but only when the source material raises this
explicitly. Omit entirely if none apply.>

## Modeling Considerations

<What properties must a model representing this cell type capture?
What simplifications are common and when do they fail?
Link to [[MOD_...]] pages.>
```

---

### 1.6 NET_ — Neural Circuit / Network

```markdown
---
type: circuit
title: <full human-readable name>
scale: local | mesoscale | large-scale
confidence: established | debated | speculative
updated: YYYY-MM-DD
related:
  - REG_<slug>
  - CEL_<slug>
  - PHE_<slug>
tags: []
---

# <Circuit / network name>

## Description

<What circuit or network is this? What system does it belong to?
State the spatial scale: local microcircuit (<1 mm), mesoscale (within a system),
or large-scale (between brain regions).>

## Components

<Key nodes — regions and cell types — and their roles within the circuit.
Link to [[REG_...]] and [[CEL_...]] pages.>

## Connectivity Architecture

<Known connection patterns, directionality, synaptic properties, and laminar specificity.
Distinguish established from inferred connections. All claims cited. (@Key)>

## Functional Organization

<How is computation organized across this circuit?
What is the role of each component in the circuit's overall function? (@Key)>

## Controversies *(add only if encountered)*

<Only include this section when the source material directly presents disputed claims about
connectivity or functional organization. Do not speculate. Omit entirely if none apply.>

## Modeling Considerations

<What structural or functional properties must a model of this circuit respect?
What abstractions are common and when do they break down?
Link to [[MOD_...]] pages.>
```

---

### 1.7 PAR_ — Experimental Paradigm

```markdown
---
type: paradigm
title: <full human-readable name>
updated: YYYY-MM-DD
related:
  - PHE_<slug>
  - TECH_<slug>
  - ANA_<slug>
tags: []
---

# <Paradigm name>

## Description

<What is this paradigm? Describe the experimental logic: what the subject experiences,
what conditions or contrasts are built into the protocol, and what behavioral responses
are required or measured. No equipment or recording specifications here.>

## What It Measures / Reveals

<What behavioral or neural observables does this paradigm provide access to?
What phenomena has it been used to characterize? (@Key)>

## Standard Variants

<Common protocol variants and what they emphasize or isolate differently.>

## Limitations and Confounds

<What the paradigm cannot distinguish. Known demand characteristics, species dependencies,
or boundary conditions on interpretation. (@Key)>

## Key Studies

<Landmark papers that established or canonically employed this paradigm. (@Key)>

## Relevance to This Project

<How is or could this paradigm be used in the current project's context?>
```

---

### 1.8 TECH_ — Technical Method

```markdown
---
type: technique
title: <full human-readable name>
subtype: acquisition | preprocessing | stimulation
confidence: established | debated | speculative
updated: YYYY-MM-DD
related:
  - PAR_<slug>
  - ANA_<slug>
  - REG_<slug>
tags: []
---

# <Technique name>

## Description

<What does this technique do? What signals does it produce (acquisition),
transform (preprocessing), or deliver (stimulation)?
State the biological target and the physical or computational principle of operation.>

## Spatial and Temporal Resolution

<Key performance characteristics with citations. Include trade-offs where relevant. (@Key)>

## Key Assumptions and Limitations

<What must be true of the preparation or signal for valid results?
Known artifacts, failure modes, and conditions that invalidate the technique. (@Key)>

## Species and Preparation Compatibility

<Where this technique can and cannot be applied: species, in vivo/ex vivo/in vitro,
anesthetized vs. awake, chronic vs. acute. (@Key)>

## Standard Variants

<Common implementations, configurations, or pipelines and what they emphasize differently.>

## Decision Guidance *(add only if source material addresses this)*

<When to prefer this technique: key criteria based on research question, required resolution,
species, preparation, or infrastructure constraints. When to avoid it or prefer an
alternative: conditions under which another technique would be more appropriate and why.
Draw from methodological comparisons and review papers; do not speculate. (@Key)>

## Software and Hardware

<Key platforms, pipelines, equipment, or reference implementations.
Acquisition and preprocessing pipelines belong here. Simulation software belongs on its own
[[SIM_...]] page — link to it rather than describing it here.>

## Controversies *(add only if encountered)*

<Only include this section when the source material directly presents disputed claims about
signal validity, interpretation, or species generalizability. Do not speculate. Omit
entirely if none apply.>
```

---

### 1.9 ANA_ — Analysis Method

```markdown
---
type: analysis
title: <full human-readable name>
confidence: established | debated | speculative
updated: YYYY-MM-DD
related:
  - PHE_<slug>
  - TECH_<slug>
  - MOD_<slug>
tags: []
---

# <Analysis method name>

## Description

<What does this method do? What input does it take and what output does it produce?
State the computational or statistical principle.>

## Key Assumptions

<What must be true of the data for the method to be valid?
Assumptions about signal structure, noise, stationarity, independence, or sample size. (@Key)>

## Known Artifacts and Limitations

<What systematic biases or distortions does it introduce?
Under what conditions does it fail or produce misleading results? (@Key)>

## Standard Variants

<Common algorithmic or implementation variants and what they emphasize or sacrifice.>

## Decision Guidance *(add only if source material addresses this)*

<When to use this method: data requirements, question types, and assumptions that must hold
for this to be the right choice. When to prefer an alternative: common situations where
another method is more appropriate and why. Draw from methodological papers and comparative
evaluations; do not speculate. (@Key)>

## Software Implementations

<Key tools, packages, or reference implementations.
Analysis toolboxes (e.g. Elephant, MNE) belong here, not on a [[SIM_...]] page: they consume
data rather than generate it.>

## Usage in the Literature

<How has this been applied in neuroscience? What has it been used to measure or reveal? (@Key)>
```

---

### 1.10 SIM_ — Simulation Software

> **SIM_ boundary**: a SIM_ page describes software that instantiates a model and numerically
> integrates it to produce simulated data. Analysis toolboxes belong in ANA_ (they consume data);
> acquisition and preprocessing pipelines belong in TECH_ (they handle real signals). SIM_ pages
> carry no `confidence` field — a simulator is an artifact, not an empirical claim. Evidence
> *about* a simulator (benchmark agreement, reproduction of reference solutions) goes in
> **Verification and Validation**, with citations.

> **Classification guide**
>
> `subtype`:
> - `engine`: numerically integrates models directly. Example: NEST, NEURON, Arbor, Brian2, STEPS.
> - `interface`: a model-specification layer over one or more engines, defining no solver of its
>   own. Example: PyNN, NetPyNE, NESTML.
> - `platform`: bundles an engine with data, connectivity, and workflow tooling into an integrated
>   environment. Example: The Virtual Brain, Open Source Brain.

```markdown
---
type: simulator
title: <full human-readable name>
subtype: engine | interface | platform
scale:                # list; all that apply
  - molecular
  - single-neuron
  - microcircuit
  - large-scale-network
  - whole-brain
formalism:            # list; all that apply
  - reaction-diffusion
  - multicompartment-biophysical
  - point-neuron-spiking
  - rate-based
  - neural-mass
  - neural-field
updated: YYYY-MM-DD
related:
  - MOD_<slug>
  - NET_<slug>
  - SIM_<slug>
tags: []
---

# <Simulator name>

## Description

<What is this software? Who developed it and toward what design goal?
State the core abstraction it exposes to the user — the objects a model is built from
(e.g. point neurons and spike-event synapses; branched morphologies obeying the cable
equation; neural masses coupled on a connectome).>

## Modeling Scope

<What classes of model can be expressed in this simulator, and what cannot?
This is the bridge between a model and the software able to instantiate it.
Link to the [[MOD_...]], [[NET_...]], and [[CEL_...]] pages it can and cannot realize.
State exclusions explicitly: what a user must leave the tool to do.>

## Numerical Methods and Implementation

<Integration scheme, time-stepping (fixed grid vs. adaptive/variable step), spike handling
(clock-driven vs. event-driven), solver choices, and the parallelization model
(MPI / OpenMP / GPU). Present the scheme formally before prose interpretation.
$inline$ and $$block$$ LaTeX. (@Key)>

## Built-in Assumptions and Idealizations

<What does using this simulator commit the user to, whether or not they intend it?
Discretization of spike times and delays, default synapse and neuron models, boundary
conditions, floating-point and ordering effects on reproducibility.>

- **Assumption**: <statement>
  - *Justification*: <why the design makes this choice> (@Key)
  - *When this matters*: <the class of scientific question whose answer this changes>

## Verification and Validation

<Evidence that the software computes what it claims to. Reproduction of analytic or reference
solutions, cross-simulator benchmark agreement, published comparison studies.
Every claim cited. This section carries the evidential weight that a confidence field would
otherwise hold — where sources disagree, record all positions in Controversies. (@Key)>

## Performance and Scaling

<Quantitative claims: neurons or synapses simulated per second, real-time factor, memory
footprint, strong and weak scaling behaviour, core and node counts.
Every number must be cited, and the hardware it was measured on stated. (@Key)>

## Interoperability and Model Specification

<How is a model described to this simulator (native API, domain-specific language, declarative
format)? Which interchange standards does it read or emit (NeuroML, LEMS, SONATA, PyNN)?
What can be imported from and exported to other simulators?
Link to related [[SIM_...]] pages. This section governs whether published work is reproducible.>

## Decision Guidance *(add only if source material addresses this)*

<When to prefer this simulator: the model class, scale, and infrastructure that make it the
right choice. When to prefer an alternative: conditions under which another simulator is more
appropriate and why. Draw from published comparisons and benchmark papers; do not speculate. (@Key)>

## Availability

<Repository, documentation, license, and the canonical citation to use.
URLs, licenses, and version numbers are pointers rather than factual claims and need no
citation; any claim about version-specific *behaviour* does. State the version these
statements describe.>

## Controversies *(add only if encountered)*

<Only include this section when the source material directly presents disputed benchmark
results, contested claims of equivalence between simulators, or disagreement over whether an
implementation faithfully realizes a model. Do not speculate. Omit entirely if none apply.>

## Usage in the Literature

<Notable studies built with this simulator. What has it been used to model? (@Key)>

## Relevance to This Project

<How this simulator is or could be used in the current project's context.>
```

---

### 1.11 DAT_ — Canonical Dataset

```markdown
---
type: dataset
title: <full human-readable name>
updated: YYYY-MM-DD
related:
  - PAR_<slug>
  - TECH_<slug>
  - PHE_<slug>
tags: []
---

# <Dataset name>

## Description

<What is this dataset? What neural or behavioral system does it cover?
What motivated its creation or curation?> (@Key)

## Recording Conditions

<Species, preparation (in vivo / ex vivo), brain regions or behaviors covered,
subject population and sample size. (@Key)>

## Modality and Scale

<Recording technique (link to [[TECH_...]]). Number of subjects, sessions, neurons,
trials, or voxels as appropriate. Temporal and spatial resolution. (@Key)>

## Data Structure and Access

<File formats, repository location, versioning, and licensing.
Any preprocessing applied to the released data.>

## Key Publications

<Papers that introduced, described, or canonically analyzed this dataset. (@Key)>

## Relevance to This Project

<How this resource is or could be used in the current project's context.>
```

---

## 2. wiki/index.md Structure

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

## Computational Models
| Page | Title | Confidence | Updated |
|------|-------|------------|---------|

## Theories
| Page | Title | Status | Updated |
|------|-------|--------|---------|

## Brain Regions
| Page | Title | Confidence | Updated |
|------|-------|------------|---------|

## Cell Types
| Page | Title | Confidence | Updated |
|------|-------|------------|---------|

## Neural Circuits & Networks
| Page | Title | Confidence | Updated |
|------|-------|------------|---------|

## Experimental Paradigms
| Page | Title | Updated |
|------|-------|---------|

## Technical Methods
| Page | Title | Confidence | Updated |
|------|-------|------------|---------|

## Analysis Methods
| Page | Title | Confidence | Updated |
|------|-------|------------|---------|

## Simulation Software
| Page | Title | Subtype | Updated |
|------|-------|---------|---------|

## Canonical Datasets
| Page | Title | Updated |
|------|-------|---------|
```

Links in `index.md` use relative markdown paths (`pages/TYPE_slug.md`), not `[[TYPE_slug]]` notation, so the file is navigable by both agents and standard markdown renderers.

Cross-links within page bodies continue to use `[[TYPE_slug]]` notation.

---

## 3. Conflict Resolution Rules

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

**Qualitative**: all positions in Empirical Basis with neutral framing. Structured Controversies entry:

```
### <Conflict title>
- **Position A**: <statement> (@Key1)
- **Position B**: <statement> (@Key2)
- *(add further positions as needed)*
- **Possible resolution**: <if one exists>
- **Status**: unresolved | partially resolved | resolved
```

**Interpretive**: represent all interpretations with citations. Do not adjudicate.

For all conflict types: set confidence to `debated` when conflicting evidence or interpretations cannot be reconciled. Do not escalate empirical disagreements to human review — document them in Controversies with all positions and citations. The wiki records what the literature says, not who is right. This applies even when multiple sources disagree on what a theory claims or what a model predicts: note the disagreement and cite it.

### When to raise a ⚑ Human review flag

Raise a ⚑ flag only on **MOD_ and THE_ pages**, and only when the source material does not settle a **philosophy-of-science classification question** — i.e., a question about how to characterize or categorize the model or theory that requires judgment beyond reading the article. Examples: whether a model's variables satisfy the 3M criterion, what level of Marr's hierarchy a model operates at, whether a theory's scope is genuinely explanatory or merely descriptive, how to characterize a theory's mechanistic commitments.

Do not flag for: empirical claims, theory content (what a theory asserts), model predictions, method comparisons, or any question that is answered by the literature even if the literature disagrees — those belong in Controversies.

**Format for ⚑ flags** (MOD_ and THE_ pages only):

Add a line to the relevant Controversies entry (or create a dedicated entry):
```
- **⚑ Human review requested**: <the specific classification question the agent cannot resolve from the source material>
```

Add a banner to the page header:
```
> ⚑ **Human review requested**: [Classification question]. See Controversies section.
```

List all ⚑ flags in the session summary.

---

## 4. Citation Integrity Rules

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

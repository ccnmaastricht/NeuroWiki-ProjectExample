# CLAUDE.md — NeuroWiki Project Context

This file is loaded automatically by Claude Code at the start of every session.
It contains all project context and rules. Read it fully before taking any action.
For task-specific instructions, read the relevant module file listed under **Workflows** below.

---

## Project Identity

Project name:             Example Wiki: The role of gamma synchrony in early visual cortex
Main research question:   Does gamma synchrony play a functional role in early visual cortex?
Model type(s):            Biophysical, Functional
Theories:                 Theory of Weakly Coupled Oscillators, Binding Through Synchrony, Binding By Enhanced Firing, etc.
Brain region(s):          V1, V4
Organism / data type:     Human, macaque
Key phenomena to explain: 
  - Gamma synchrony
Project-specific glossary: 
Contributors:             Mario Senden

---

## Repository Structure

```
project-root/
├── README.md             ← human-facing project overview
├── CLAUDE.md             ← Claude Code context (this file; auto-read on launch)
├── AGENTS.md             ← OpenAI Codex context
├── CURSOR.md             ← Cursor context
├── GEMINI.md             ← Gemini CLI context
├── agent/                ← agent instruction files
│   ├── TEMPLATES.md      ← page templates, index structure, conflict resolution, citation rules
│   ├── INGESTION.md      ← workflow: processing new PDFs
│   ├── REVIEW.md         ← workflow: agent-assisted flag resolution
│   ├── REFINE_A.md       ← workflow: structural harmonization
│   ├── REFINE_B.md       ← workflow: depth audit
│   └── REFINE_C.md       ← workflow: cross-link audit
├── docs/                 ← human-facing documentation
│   ├── QUICKSTART.md     ← setup and usage guide
│   ├── VERIFICATION.md   ← verification protocol
│   └── CONTRIBUTING.md   ← lab wiki submission guide
├── scripts/              ← tools
│   ├── validate.py       ← pre-submission structural validator
│   └── setup.sh          ← one-command project initialization
├── raw/                  ← source PDFs; never modified by agent
│   └── *.pdf
└── wiki/
    ├── primary.bib       ← BibTeX: papers with PDFs in raw/
    ├── secondary.bib     ← BibTeX: papers cited within PDFs but not in raw/
    ├── log.md            ← human verification log
    ├── index.md          ← wiki root index; agent navigation entry point
    └── pages/
        └── <TYPE>_<slug>.md
```

---

## Page Types

There are no per-paper pages. Papers are sources synthesized into concept pages. The `.bib` files are the citation layer.

| Prefix | Type | Covers |
|--------|------|--------|
| `PHE_` | Phenomenon | An observed neural or behavioral regularity at any level, including functional network patterns |
| `MOD_` | Computational model | A formal model (mechanistic, normative, or data-driven) making specific, testable claims about a target system |
| `THE_` | Neuroscientific theory | A full theory with explanatory schema, a defined model family, mechanistic grounding, and explicit empirical scope; umbrella theories link to sub-theory THE_ pages |
| `REG_` | Brain region | Anatomically defined structure: location, cytoarchitecture, connectivity |
| `CEL_` | Cell type | Neuronal or glial population defined by morphological, molecular, or functional properties; may span regions |
| `NET_` | Neural circuit / network | Structured connectivity pattern between regions or cell types, at a defined spatial scale |
| `PAR_` | Experimental paradigm | Behavioral task or protocol: what the subject experiences and does; no equipment or analysis details |
| `TECH_` | Technical method | Procedure for acquiring, preprocessing, or stimulating neural/behavioral signals |
| `ANA_` | Analysis method | Post-hoc data analysis procedure: statistics, dimensionality reduction, decoding, inference |
| `SIM_` | Simulation software | Software that instantiates a model and numerically integrates it to produce simulated data |
| `DAT_` | Canonical dataset | Curated, publicly accessible data collection serving as a community reference |

Slug convention: lowercase, hyphenated, descriptive.
Examples: `PHE_place-cell-remapping`, `MOD_ring-attractor`, `REG_v1`, `CEL_pv-interneuron`, `NET_basal-ganglia-thalamic-loop`, `PAR_morris-water-maze`, `TECH_two-photon-imaging`, `ANA_population-decoding`, `SIM_nest`, `DAT_allen-brain-atlas`

Full page templates, `wiki/index.md` structure, conflict resolution rules, and citation integrity rules: see `agent/TEMPLATES.md`.

---

## Citation Model

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

## Confidence Levels and Theory Status

### Confidence (PHE_, MOD_, REG_, CEL_, NET_, TECH_, ANA_ pages)

Every `PHE_`, `MOD_`, `REG_`, `CEL_`, `NET_`, `TECH_`, and `ANA_` page must carry a confidence field. Default to `speculative` when evidence is thin.

| Level | Meaning |
|-------|---------|
| `established` | Replicated across multiple independent labs, species, or methods; field consensus. Requires at minimum two independent sources. |
| `debated` | Genuine disagreement in the literature; conflicting evidence or interpretations exist |
| `speculative` | Based on limited evidence, a single study, or theoretical inference without strong empirical grounding |

Confidence upgrades and downgrades both require a note citing the motivating evidence. Add or extend the **Controversies** section to record this; create the section if it does not yet exist.

> **Note**: `speculative` reflects thin evidence, not design purpose. A MOD_ page with `exploratory: true` is not speculative by default — exploratory models are legitimate epistemic stages regardless of evidence quality. Distinguish evidence quality (confidence field) from explanatory status (`explanatory_character`, `marr_level`, and **Explanatory Scope** section).

### Status (THE_ pages)

`THE_` pages do not carry a confidence field. Instead they carry a neutral **Status** field.

| Status | Meaning |
|--------|---------|
| `emerging` | Has an explanatory schema and initial formal models but the model family is not yet mature |
| `active-research-area` | The theory is actively developed, debated, and applied in current research |
| `settled` | The theory is broadly accepted; major disputes resolved; still used but no longer a frontier |
| `abandoned` | The theory has been superseded or discredited and is no longer actively pursued |

---

## Behavioral Rules

1. Never modify files in `raw/`.
2. Never fabricate citations. Unresolvable secondary references: `<!-- UNRESOLVED: <description> -->`.
3. The `†` dagger is mandatory on every secondary citation.
4. Equations before prose on all MOD_ pages.
5. PHE_, REG_, CEL_, and NET_ pages describe observations. MOD_ pages describe proposals. THE_ pages describe theories and their explanatory architecture. SIM_ pages describe software that implements models, not the models themselves. Never conflate.
6. Confidence is mandatory on every PHE_, MOD_, REG_, CEL_, NET_, TECH_, and ANA_ page.
7. Cross-link using `[[TYPE_slug]]` within page bodies. Use relative paths in `index.md`.
8. Flag uncertainty with `> ⚠️ Uncertain: <reason>`.
9. Rewrite, don't append. Git history is the changelog.
10. Promotions are content reviews, not find-and-replace. Re-evaluate every claim previously citing the secondary source against the actual PDF.
11. End every session by appending a log entry to `wiki/log.md` using the format in the **Session Log** section below, then printing the entry to the conversation. The final line of every entry must be `**Sign-off**: *(pending)*` — the human replaces this with `**Sign-off**: ✓ Verified — <name>, <date>` after completing the checklist in `docs/VERIFICATION.md`.
12. Every MOD_ page must populate `explanatory_character`, `marr_level`, `construction`, and `exploratory` in the frontmatter, and the **Explanatory Scope** section in the body. State level-relativity explicitly — phenomenological at one level and mechanistic at another are not contradictory and both must appear. If `marr_level` includes `computational` and the model makes a normative claim, state the objective or optimality principle in the Explanatory Scope section.

---

## Session Log

Every session ends by appending a new entry to `wiki/log.md`, directly after the opening `---` separator (newest entry first). Print the entry to the conversation as well.

Each workflow file specifies what goes in the **Changes** section; everything else is standard across all session types.

```markdown
## Session YYYY-MM-DD — <Ingestion: filename.pdf | Structural Harmonization | Depth Audit | Cross-Link Audit | Review: session-date>

**Run by**: <name or "agent">

### Changes

<session-specific content — see workflow file for exact fields>

### Flags raised
- ⚑ Human review: <page — issue, or "none">
- `<!-- UNCITED -->`: <page — claim summary, or "none">
- `<!-- UNRESOLVED -->`: <description, or "none">

### Flags resolved this session
- <list, or "none">

### Action items
- <list, or "none">

**Sign-off**: *(pending)*
```

The human replaces `*(pending)*` with `✓ Verified — <name>, <date>` after completing the post-session checklist in `docs/VERIFICATION.md`. The CI validator rejects lab wiki submissions that contain any `*(pending)*` entry.

---

## Workflows

Read the relevant module file when a specific workflow is requested:

| Task | Read |
|------|------|
| Process new PDFs | `agent/INGESTION.md` and `agent/TEMPLATES.md` |
| Resolve open flags | `agent/REVIEW.md` |
| Structural harmonization | `agent/REFINE_A.md` and `agent/TEMPLATES.md` |
| Depth audit | `agent/REFINE_B.md` |
| Cross-link audit | `agent/REFINE_C.md` |

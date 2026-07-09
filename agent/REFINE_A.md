# REFINE_A.md — Structural Harmonization

```
Read agent/REFINE_A.md fully, then read agent/TEMPLATES.md fully.
Run Structural Harmonization across all pages in wiki/pages/ and wiki/index.md.
Follow this workflow exactly. Print the session summary when done.
```

---

## Rules

This workflow does not add, remove, or rewrite content.
It only restructures, reformats, and repairs metadata.
If a required section is missing, add a stub — never invented text.

---

## Step A1 — Canonical Structure Checklist

The authoritative page templates are in `agent/TEMPLATES.md` Section 1. The checklist below distils the structural requirements for auditing purposes.

### YAML frontmatter — required fields by type

| Type | Required frontmatter fields |
|------|-----------------------------|
| All pages | `type`, `title`, `updated`, `related` (list; empty list `[]` acceptable if no links yet) |
| PHE_, MOD_, REG_, CEL_, NET_, TECH_, ANA_ | + `confidence` |
| THE_ | + `status` |
| MOD_ | + `explanatory_character`, `marr_level` (list), `construction`, `exploratory` |
| NET_ | + `scale` (scalar) |
| TECH_ | + `subtype` |
| SIM_ | + `subtype`, `scale` (list), `formalism` (list) |
| PAR_, DAT_ | *(no additional fields)* |

Valid `type` values: `phenomenon`, `model`, `theory`, `region`, `cell_type`, `circuit`, `paradigm`, `technique`, `analysis`, `simulator`, `dataset`, `index`

`TECH_` and `SIM_` both use `subtype`, but the vocabularies are disjoint:
`acquisition | preprocessing | stimulation` for TECH_, `engine | interface | platform` for SIM_.

### Section order by page type

Sections marked *(conditional)* appear only when the source material warrants them. Never stub a
conditional section — its absence is not a defect.

| Type | Required sections, in order |
|------|-----------------------------|
| PHE_ | Description · Empirical Basis · Key Parameters and Quantitative Signatures · Generality · Controversies *(conditional)* · Modeling Implications |
| MOD_ | Description · Descriptive Target · Explanatory Scope · Formal Description · Core Assumptions · Empirical Support · Empirical Challenges · Comparison to Alternatives · Controversies *(conditional)* · Usage in the Literature |
| THE_ | Core Claims · Explanatory Schema · Model Family · Mechanistic Grounding · Empirical Scope · Controversies *(conditional)* · Key Sources |
| REG_ | Anatomical Identity · Connectivity · Functional Role(s) · Principal Cell Types · Controversies *(conditional)* · Modeling Considerations |
| CEL_ | Identity · Distribution · Physiology · Connectivity · Functional Role(s) · Controversies *(conditional)* · Modeling Considerations |
| NET_ | Description · Components · Connectivity Architecture · Functional Organization · Controversies *(conditional)* · Modeling Considerations |
| PAR_ | Description · What It Measures / Reveals · Standard Variants · Limitations and Confounds · Key Studies · Relevance to This Project |
| TECH_ | Description · Spatial and Temporal Resolution · Key Assumptions and Limitations · Species and Preparation Compatibility · Standard Variants · Decision Guidance *(conditional)* · Software and Hardware · Controversies *(conditional)* |
| ANA_ | Description · Key Assumptions · Known Artifacts and Limitations · Standard Variants · Decision Guidance *(conditional)* · Software Implementations · Usage in the Literature |
| SIM_ | Description · Modeling Scope · Numerical Methods and Implementation · Built-in Assumptions and Idealizations · Verification and Validation · Performance and Scaling · Interoperability and Model Specification · Decision Guidance *(conditional)* · Availability · Controversies *(conditional)* · Usage in the Literature · Relevance to This Project |
| DAT_ | Description · Recording Conditions · Modality and Scale · Data Structure and Access · Key Publications · Relevance to This Project |

### Notation standards

- Citations: `(@Key)` or `(@Key†)` — not bare `Key`, `[Key]`, or `(Key)`
- Cross-links in page bodies: `[[TYPE_slug]]`
- Links in `wiki/index.md`: relative markdown paths `(pages/TYPE_slug.md)`
- LaTeX: `$...$` inline, `$$...$$` block
- No `PAP_` prefixes anywhere (deprecated)

---

## Step A2 — Audit Each Page

For every file in `wiki/pages/` and `wiki/index.md`:

1. Check YAML frontmatter is present and contains all required fields for the page type
2. Check all required sections are present and in canonical order
3. Check no non-canonical heading names are used
4. Check citation, link, and LaTeX notation conforms to standards above

---

## Step A3 — Repair Each Page

| Issue | Action |
|-------|--------|
| Missing frontmatter block | Add block with all fields set to `<!-- MISSING -->` |
| Missing required frontmatter field | Add field with `<!-- MISSING -->` value |
| Missing section | Add heading + `<!-- SECTION STUB: populate in next ingestion session -->` |
| Wrong section order | Reorder verbatim — do not alter content |
| Non-canonical heading | Rename — do not alter content |
| Inconsistent citation notation | Correct to `(@Key)` or `(@Key†)` |
| Inconsistent link notation | Correct to `[[TYPE_slug]]` in bodies; relative paths in `index.md` |
| Malformed LaTeX delimiters | Correct delimiters only — do not alter equation content |

---

## Step A4 — Write Session Log Entry

Append a new entry to `wiki/log.md`, directly after the opening `---` separator (newest entry first):

```markdown
## Session YYYY-MM-DD — Structural Harmonization

**Run by**: <name or "agent">

### Changes

- Pages audited: N
- Pages with no issues: N
- Pages repaired: N
- Missing frontmatter fields added: <page: field, or "none">
- Missing sections stubbed: <page: section, or "none">
- Section reordering: <page, or "none">
- Heading renames: <page: old → new, or "none">
- Notation corrections: N instances across M pages (or "none")

### Flags raised
- ⚑ Human review: <page — issue, or "none">
- `<!-- UNCITED -->`: <page — claim summary, or "none">
- `<!-- UNRESOLVED -->`: <description, or "none">

### Flags resolved this session
- <list, or "none">

### Action items
- <list any `<!-- MISSING -->` stubs added, so the human knows what needs populating in
  the next ingestion session, or "none">

**Sign-off**: *(pending)*
```

Print the completed entry to the conversation.

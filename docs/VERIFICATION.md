# VERIFICATION.md — Human Verification Protocol

No wiki content should be used in a manuscript, grant, or modeling decision
until the verification checklist for that page's most recent session has been signed off.

---

## Responsibilities

| Role | Responsibility |
|------|---------------|
| PI | Signs off on all confidence changes and all `⚑ Human review requested` flags (MOD_ and THE_ pages — philosophy-of-science classification questions) |
| PhD students | Spot-check pages in their domain after sessions they initiate; sign off |
| Any lab member running a session | Complete the post-session checklist before closing |

---

## Post-Session Checklist — Ingestion

### 1. Read the session summary

- [ ] Pages created and modified
- [ ] Confidence changes
- [ ] Secondary entries added
- [ ] Flags: `⚑`, `<!-- UNCITED -->`, `<!-- UNRESOLVED -->`
- [ ] Promotion performed (yes/no)

### 2. Spot-check claims

| Pages modified | Minimum claims to verify |
|----------------|--------------------------|
| 1–3 | 3 per page |
| 4–6 | 2 per page |
| 7+ | 1 per page + all flagged items |

Prioritize: new claims, `†` citations, quantitative claims, Empirical Basis and Core Assumptions sections.
For promoted papers: verify minimum 5 claims on the most heavily affected page.

To verify: open the source PDF, confirm the claim accurately represents the source including its caveats. If inaccurate: correct in the page and note in the session log.

### 3. Review confidence changes

- [ ] Is the change justified by cited evidence in the Controversies section?
- [ ] Upgrades to `established`: are there genuinely two or more independent sources? If not, revert to `debated`.
- [ ] Downgrades: is the contradicting evidence strong or a single outlier?

### 4. Resolve flags

Use the agent-assisted **Review workflow** (`agent/REVIEW.md`) to work through flags systematically — it presents each item one at a time and applies resolutions immediately. Run it with:

```
Read agent/REVIEW.md fully.
Run a Review Session. Follow agent/REVIEW.md exactly.
```

Alternatively, resolve flags manually:

**`⚑ Human review requested`** (PI — MOD_ and THE_ pages only):
- Read the classification question and the relevant page context
- Provide your judgment on the philosophy-of-science question (e.g., Marr level, mechanistic vs. phenomenological character, explanatory scope)
- If resolved: update the relevant frontmatter field(s), update the Controversies entry, set status, remove flag from page header
- If not yet resolvable: leave flag; discuss with project team

**`<!-- UNCITED -->`**:
- If source identifiable: add citation, remove flag
- If not: leave flag; schedule for next relevant ingestion session

**`<!-- UNRESOLVED -->`**:
- If important: add PDF to `raw/` and process in next ingestion session
- If peripheral: note in session log

### 5. Sign off

The agent writes `**Sign-off**: *(pending)*` at the end of every session entry. After completing steps 1–4 above, replace that line in `wiki/log.md` with:

```
**Sign-off**: ✓ Verified — <your name>, <date>
```

The validator fails if any `*(pending)*` remains in the log, so submission is blocked until every session is signed.

---

## Post-Session Checklist — Refinement

**After REFINE_A:**
- [ ] Note all `<!-- MISSING -->` stubs for the next ingestion session
- [ ] Spot-check 3–5 pages to confirm content was not altered during restructuring
- [ ] Confirm no citation notation was corrupted

**After REFINE_B:**
- [ ] PI reads `wiki/depth-audit-YYYY-MM-DD.md` in full
- [ ] Prioritize PDF acquisition list; schedule ingestion accordingly
- [ ] Note action items in session log

**After REFINE_C:**
- [ ] Spot-check 5 added links — confirm correct target and substantive mention
- [ ] Review the "concepts with no page" list — decide which warrant new pages
- [ ] Confirm no links were added inside headings, metadata fields, or citations

---

## Periodic Review

**Monthly** (PhD student, reviewed by PI):
- Read `wiki/index.md` in full
- For each `debated` or `speculative` page: has new literature been added that should change it?
- Identify accumulating `<!-- UNCITED -->` and `<!-- UNRESOLVED -->` flags without resolution
- Run REFINE_B if not done in the past month

**Before manuscript submission** (PI):
- [ ] Verify all manuscript citations against their source PDFs
- [ ] Confirm no `†` citations used for manuscript claims without independent verification
- [ ] Confirm confidence levels are appropriate for the claims being made
- [ ] Resolve all outstanding `⚑` and `<!-- UNCITED -->` flags on cited pages

**Before a modeling decision** (PI + PhD student):
- [ ] Relevant sections are `established` or explicitly `debated`
- [ ] All quantitative values used are cited to primary sources (no `†`)
- [ ] Any `†` claim either promoted or explicitly flagged as an assumption in the modeling write-up

---

## Red Lines

| Situation | Action |
|-----------|--------|
| Spot-check finds a claim directly contradicted by its cited source | Check all claims from that session — possible systematic agent error |
| Page is `established` but rests on a single primary source | Downgrade to `debated`; investigate |
| A `†` citation is significantly misrepresented relative to the source | Re-evaluate all secondary citations on that page |
| A modeling parameter is uncited or incorrectly cited | Halt use of that parameter until verified |

For any red line, add to the top of the affected page:

```
> 🛑 PAGE UNDER REVIEW — do not use for modeling or writing
> Reason: <description> — flagged YYYY-MM-DD by <name>
```

Remove only after PI sign-off on a corrected, re-verified version.

---

## Session Log Format

The canonical log entry format is defined in the **Session Log** section of your agent's bootstrap file. Every session produces one entry in `wiki/log.md`, newest first.

When spot-checking, add your findings directly into the relevant session entry under a `### Spot-check results` subsection before signing off:

```
### Spot-check results
- <page>, "<claim>": verified ✓ / corrected: <correction>
```

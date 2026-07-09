#!/usr/bin/env python3
"""
NeuroWiki validate.py
Lightweight pre-submission structural validator for a local project wiki.

Usage:
    python3 validate.py --source wiki/ [--report report.json]

Exits 0 if all checks pass, 1 if any errors are found.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import date

# The frontmatter `type` value for each page-type prefix, plus the wiki root index.
# Nothing else in the repo enforces the prefix-to-type mapping, so an unlisted value
# here is the only signal that a page carries a typo'd or invented type.
VALID_TYPES = {
    "phenomenon", "model", "theory", "region", "cell_type", "circuit",
    "paradigm", "technique", "analysis", "simulator", "dataset", "index"
}

# Confidence is mandatory on PHE_, MOD_, REG_, CEL_, NET_, TECH_, ANA_ pages
# (CLAUDE.md rule 6). These are the corresponding frontmatter `type` values.
# SIM_ pages are deliberately absent: a simulator is an artifact, not an
# empirical claim.
CONFIDENCE_TYPES = {
    "phenomenon", "model", "region", "cell_type", "circuit", "technique",
    "analysis"
}
VALID_CONFIDENCE = {"established", "debated", "speculative"}

STATUS_TYPES = {"theory"}
VALID_STATUS = {"emerging", "active-research-area", "settled", "abandoned"}

# MOD_ pages must populate all four classification fields (CLAUDE.md rule 12).
EXPLANATORY_CHARACTER_TYPES = {"model"}
VALID_EXPLANATORY_CHARACTER = {"phenomenological", "mechanistic"}
VALID_CONSTRUCTION = {"theory-derived", "data-driven", "hybrid"}
VALID_EXPLORATORY = {"true", "false"}
VALID_MARR_LEVEL = {"computational", "algorithmic", "implementational"}

# NET_ pages carry a single spatial scale; SIM_ pages carry a list of scales.
SCALE_TYPES = {"circuit"}
VALID_SCALE = {"local", "mesoscale", "large-scale"}

# TECH_ and SIM_ both carry `subtype`, but the vocabularies are disjoint.
SUBTYPE_BY_TYPE = {
    "technique": {"acquisition", "preprocessing", "stimulation"},
    "simulator": {"engine", "interface", "platform"},
}

# SIM_ pages declare what they can express: coarse scale, and precise formalism.
SIMULATOR_TYPES = {"simulator"}
VALID_SIM_SCALE = {
    "molecular", "single-neuron", "microcircuit", "large-scale-network",
    "whole-brain"
}
VALID_FORMALISM = {
    "reaction-diffusion", "multicompartment-biophysical", "point-neuron-spiking",
    "rate-based", "neural-mass", "neural-field"
}


def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_text = text[4:end]
    body = text[end + 4:].lstrip("\n")
    fm = {}
    current_key = None
    for line in fm_text.splitlines():
        if not line.strip():
            continue
        stripped = line.lstrip()
        if not line.startswith(" ") and ":" in line:
            k, _, v = line.partition(":")
            k = k.strip()
            v = v.strip()
            fm[k] = v  # tentatively a scalar; becomes a list if items follow
            current_key = k if v == "" else None
        elif current_key is not None and stripped.startswith("- "):
            if not isinstance(fm.get(current_key), list):
                fm[current_key] = []
            fm[current_key].append(stripped[2:].strip())
    return fm, body


def scalar(fm, key):
    """Frontmatter value as a string; '' if absent or list-valued."""
    v = fm.get(key, "")
    return v if isinstance(v, str) else ""


def check_list_field(fm, key, valid):
    """Errors for a frontmatter field that must be a non-empty list of `valid` values."""
    val = fm.get(key, "")
    if isinstance(val, list):
        if not val:
            return [f"Missing {key} field"]
        bad = [v for v in val if v not in valid]
        return [f"Invalid {key} value(s): {bad}"] if bad else []
    if not val or "MISSING" in val:
        return [f"Missing {key} field"]
    return [f"{key} must be a list"]


def parse_bib_keys(bib_path):
    keys = set()
    if not bib_path.exists():
        return keys
    text = bib_path.read_text(encoding="utf-8")
    for match in re.finditer(r"@\w+\{(\w+),", text):
        keys.add(match.group(1))
    return keys


def extract_citations(body):
    """Return (primary_keys, secondary_keys) cited in a page body."""
    primary = set()
    secondary = set()
    for match in re.finditer(r'\((@[^)]+)\)', body):
        for part in re.split(r',\s*', match.group(1)):
            part = part.strip()
            if not part.startswith('@'):
                continue
            key = part[1:]
            if key.endswith('†'):
                secondary.add(key[:-1])
            else:
                primary.add(key)
    return primary, secondary


def validate_page(path, fm, body):
    errors = []
    page_type = scalar(fm, "type")

    for field in ["type", "title", "updated"]:
        val = scalar(fm, field)
        if not val or "MISSING" in val:
            errors.append(f"Missing required frontmatter field: {field}")

    if page_type and "MISSING" not in page_type and page_type not in VALID_TYPES:
        errors.append(f"Unknown type value: {page_type!r}")

    if page_type in CONFIDENCE_TYPES:
        val = scalar(fm, "confidence")
        if not val or "MISSING" in val:
            errors.append("Missing confidence field")
        elif val not in VALID_CONFIDENCE:
            errors.append(f"Invalid confidence value: {val!r}")

    if page_type in STATUS_TYPES:
        val = scalar(fm, "status")
        if not val or "MISSING" in val:
            errors.append("Missing status field")
        elif val not in VALID_STATUS:
            errors.append(f"Invalid status value: {val!r}")

    if page_type in EXPLANATORY_CHARACTER_TYPES:
        val = scalar(fm, "explanatory_character")
        if not val or "MISSING" in val:
            errors.append("Missing explanatory_character field")
        elif val not in VALID_EXPLANATORY_CHARACTER:
            errors.append(f"Invalid explanatory_character value: {val!r}")

        val = scalar(fm, "construction")
        if not val or "MISSING" in val:
            errors.append("Missing construction field")
        elif val not in VALID_CONSTRUCTION:
            errors.append(f"Invalid construction value: {val!r}")

        val = scalar(fm, "exploratory")
        if not val or "MISSING" in val:
            errors.append("Missing exploratory field")
        elif val not in VALID_EXPLORATORY:
            errors.append(
                f"Invalid exploratory value: {val!r} (expected true or false)")

        errors += check_list_field(fm, "marr_level", VALID_MARR_LEVEL)

    if page_type in SCALE_TYPES:
        val = scalar(fm, "scale")
        if not val or "MISSING" in val:
            errors.append("Missing scale field")
        elif val not in VALID_SCALE:
            errors.append(f"Invalid scale value: {val!r}")

    if page_type in SIMULATOR_TYPES:
        errors += check_list_field(fm, "scale", VALID_SIM_SCALE)
        errors += check_list_field(fm, "formalism", VALID_FORMALISM)

    if page_type in SUBTYPE_BY_TYPE:
        val = scalar(fm, "subtype")
        if not val or "MISSING" in val:
            errors.append("Missing subtype field")
        elif val not in SUBTYPE_BY_TYPE[page_type]:
            errors.append(f"Invalid subtype value: {val!r}")

    updated_val = scalar(fm, "updated")
    if updated_val and "MISSING" not in updated_val:
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', updated_val):
            errors.append(
                f"Invalid updated date format: {updated_val!r} (expected YYYY-MM-DD)"
            )

    full_text = path.read_text(encoding="utf-8")
    if "<!-- MISSING -->" in full_text:
        errors.append("Contains unfilled <!-- MISSING --> placeholder(s)")

    if body.count("SECTION STUB") > 2:
        errors.append(
            "Page is mostly stubs — insufficient content for submission")

    return errors


def check_log(wiki_path):
    log = wiki_path / "log.md"
    if not log.exists():
        return ["log.md not found"]
    text = log.read_text(encoding="utf-8")
    errors = []
    if "✓ Verified" not in text:
        errors.append(
            "log.md contains no signed verification entry (missing '✓ Verified')"
        )
    if "*(pending)*" in text:
        errors.append(
            "log.md contains unsigned session(s) — all sessions must be signed off before submission"
        )
    return errors


def main():
    parser = argparse.ArgumentParser(
        description="NeuroWiki pre-submission validator")
    parser.add_argument("--source",
                        required=True,
                        help="Path to wiki/ directory")
    parser.add_argument("--report",
                        default=None,
                        help="Output JSON report path (optional)")
    parser.add_argument("--skip-log",
                        action="store_true",
                        help="Skip the log.md verification check (used in CI)")
    args = parser.parse_args()

    wiki_path = Path(args.source)
    pages_dir = wiki_path / "pages"

    report = {
        "date": date.today().isoformat(),
        "page_errors": [],
        "citation_errors": [],
        "log_errors": [],
        "summary": {}
    }

    primary_keys = parse_bib_keys(wiki_path / "primary.bib")
    secondary_keys = parse_bib_keys(wiki_path / "secondary.bib")

    all_cited_primary = set()
    all_cited_secondary = set()
    page_count = 0

    if pages_dir.exists():
        for p in sorted(pages_dir.glob("*.md")):
            page_count += 1
            text = p.read_text(encoding="utf-8")
            fm, body = parse_frontmatter(text)

            errors = validate_page(p, fm, body)
            if errors:
                report["page_errors"].append({
                    "page": p.name,
                    "errors": errors
                })

            cited_p, cited_s = extract_citations(body)
            all_cited_primary.update(cited_p)
            all_cited_secondary.update(cited_s)

    for key in sorted(all_cited_primary - primary_keys):
        if key in secondary_keys:
            report["citation_errors"].append(
                f"(@{key}) cited without the † dagger but @{key} is in "
                "secondary.bib — secondary citations require the dagger")
        else:
            report["citation_errors"].append(
                f"(@{key}) used as primary citation but not found in primary.bib"
            )
    for key in sorted(all_cited_secondary - secondary_keys):
        if key in primary_keys:
            report["citation_errors"].append(
                f"(@{key}†) cited with the † dagger but @{key} is in "
                "primary.bib — primary citations must not carry the dagger")
        else:
            report["citation_errors"].append(
                f"(@{key}†) used as secondary citation but not found in "
                "secondary.bib")
    for key in sorted(primary_keys - all_cited_primary):
        report["citation_errors"].append(
            f"@{key} in primary.bib but not cited in any page")
    for key in sorted(secondary_keys - all_cited_secondary):
        report["citation_errors"].append(
            f"@{key} in secondary.bib but not cited in any page")

    report["log_errors"] = [] if args.skip_log else check_log(wiki_path)

    total_errors = (len(report["page_errors"]) +
                    len(report["citation_errors"]) + len(report["log_errors"]))
    report["summary"] = {
        "pages_checked": page_count,
        "pages_with_errors": len(report["page_errors"]),
        "citation_errors": len(report["citation_errors"]),
        "log_errors": len(report["log_errors"]),
        "total_errors": total_errors,
        "passed": total_errors == 0
    }

    if args.report:
        Path(args.report).write_text(json.dumps(report, indent=2),
                                     encoding="utf-8")
        print(f"[validate.py] Report written to {args.report}")

    if report["summary"]["passed"]:
        print(
            f"[validate.py] All checks passed. {page_count} page(s) validated."
        )
        sys.exit(0)
    else:
        print(
            f"[validate.py] Validation failed. {total_errors} error(s) found.")
        for entry in report["page_errors"]:
            for err in entry["errors"]:
                print(f"  [page] {entry['page']}: {err}")
        for err in report["citation_errors"]:
            print(f"  [cite] {err}")
        for err in report["log_errors"]:
            print(f"  [log]  {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()

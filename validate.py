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


CONFIDENCE_TYPES = {"phenomenon", "model", "region"}
VALID_CONFIDENCE = {"established", "debated", "speculative"}
STATUS_TYPES = {"theory"}
VALID_STATUS = {"active-research-area", "settled", "abandoned"}
EXPLANATORY_ROLE_TYPES = {"model"}
VALID_EXPLANATORY_ROLE = {"how-possibly", "how-actually", "phenomenological"}


def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_text = text[4:end]
    body = text[end + 4:].lstrip("\n")
    fm = {}
    for line in fm_text.splitlines():
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm, body


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

    for field in ["type", "title", "updated"]:
        val = fm.get(field, "")
        if not val or "MISSING" in val:
            errors.append(f"Missing required frontmatter field: {field}")

    if fm.get("type") in CONFIDENCE_TYPES:
        val = fm.get("confidence", "")
        if not val or "MISSING" in val:
            errors.append("Missing confidence field")
        elif val not in VALID_CONFIDENCE:
            errors.append(f"Invalid confidence value: {val!r}")

    if fm.get("type") in STATUS_TYPES:
        val = fm.get("status", "")
        if not val or "MISSING" in val:
            errors.append("Missing status field")
        elif val not in VALID_STATUS:
            errors.append(f"Invalid status value: {val!r}")

    if fm.get("type") in EXPLANATORY_ROLE_TYPES:
        val = fm.get("explanatory_role", "")
        if not val or "MISSING" in val:
            errors.append("Missing explanatory_role field")
        elif val not in VALID_EXPLANATORY_ROLE:
            errors.append(f"Invalid explanatory_role value: {val!r}")

    updated_val = fm.get("updated", "")
    if updated_val and "MISSING" not in updated_val:
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', updated_val):
            errors.append(f"Invalid updated date format: {updated_val!r} (expected YYYY-MM-DD)")

    full_text = path.read_text(encoding="utf-8")
    if "<!-- MISSING -->" in full_text:
        errors.append("Contains unfilled <!-- MISSING --> placeholder(s)")

    if body.count("SECTION STUB") > 2:
        errors.append("Page is mostly stubs — insufficient content for submission")

    return errors


def check_log(wiki_path):
    log = wiki_path / "log.md"
    if not log.exists():
        return ["log.md not found"]
    if "✓ Verified" not in log.read_text(encoding="utf-8"):
        return ["log.md contains no signed verification entry (missing '✓ Verified')"]
    return []


def main():
    parser = argparse.ArgumentParser(description="NeuroWiki pre-submission validator")
    parser.add_argument("--source", required=True, help="Path to wiki/ directory")
    parser.add_argument("--report", default=None, help="Output JSON report path (optional)")
    parser.add_argument("--skip-log", action="store_true", help="Skip the log.md verification check (used in CI)")
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
                report["page_errors"].append({"page": p.name, "errors": errors})

            cited_p, cited_s = extract_citations(body)
            all_cited_primary.update(cited_p)
            all_cited_secondary.update(cited_s)

    for key in sorted(all_cited_primary - primary_keys):
        report["citation_errors"].append(
            f"(@{key}) used as primary citation but not found in primary.bib"
        )
    for key in sorted(all_cited_secondary - secondary_keys):
        report["citation_errors"].append(
            f"(@{key}†) used as secondary citation but not found in secondary.bib"
        )
    for key in sorted(primary_keys - all_cited_primary):
        report["citation_errors"].append(
            f"@{key} in primary.bib but not cited in any page"
        )
    for key in sorted(secondary_keys - all_cited_secondary):
        report["citation_errors"].append(
            f"@{key} in secondary.bib but not cited in any page"
        )

    report["log_errors"] = [] if args.skip_log else check_log(wiki_path)

    total_errors = (
        len(report["page_errors"]) +
        len(report["citation_errors"]) +
        len(report["log_errors"])
    )
    report["summary"] = {
        "pages_checked": page_count,
        "pages_with_errors": len(report["page_errors"]),
        "citation_errors": len(report["citation_errors"]),
        "log_errors": len(report["log_errors"]),
        "total_errors": total_errors,
        "passed": total_errors == 0
    }

    if args.report:
        Path(args.report).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"[validate.py] Report written to {args.report}")

    if report["summary"]["passed"]:
        print(f"[validate.py] All checks passed. {page_count} page(s) validated.")
        sys.exit(0)
    else:
        print(f"[validate.py] Validation failed. {total_errors} error(s) found.")
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

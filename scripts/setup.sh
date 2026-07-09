#!/usr/bin/env bash
# NeuroWiki project setup script
# Usage: bash scripts/setup.sh
# Run from the repository root. Safe to re-run — updates project.md and re-syncs.

set -e

echo "=== NeuroWiki Project Setup ==="
echo ""
echo "Fill in your project identity (press Enter to leave any field blank for now)."
echo ""

# ── Collect project identity interactively ─────────────────────────────────────

ask() { read -rp "$1: " "$2"; }

ask "Project name"             PROJECT_NAME
PROJECT_NAME="${PROJECT_NAME:-My NeuroWiki Project}"

ask "Main research question"   RESEARCH_QUESTION
ask "Model type(s)"            MODEL_TYPES
ask "Theories"                 THEORIES
ask "Brain region(s)"          BRAIN_REGIONS
ask "Organism / data type"     ORGANISM

echo "Key phenomena to explain (one per line; empty line to finish):"
PHENOMENA=""
while true; do
    read -rp "  - " item
    [ -z "$item" ] && break
    PHENOMENA="${PHENOMENA}  - ${item}"$'\n'
done
[ -z "$PHENOMENA" ] && PHENOMENA="  - "$'\n'

ask "Project-specific glossary" GLOSSARY
ask "Contributors"              CONTRIBUTORS

echo ""

# ── Write project.md (single source of truth for project identity) ─────────────

cat > project.md << EOF
Project name:             ${PROJECT_NAME}
Main research question:   ${RESEARCH_QUESTION}
Model type(s):            ${MODEL_TYPES}
Theories:                 ${THEORIES}
Brain region(s):          ${BRAIN_REGIONS}
Organism / data type:     ${ORGANISM}
Key phenomena to explain:
${PHENOMENA}Project-specific glossary: ${GLOSSARY}
Contributors:             ${CONTRIBUTORS}
EOF

echo "project.md written."

# ── Sync project identity into all bootstrap files ─────────────────────────────
# Replaces the content between "## Project Identity" and the next "---" separator.

sync_identity() {
    local file="$1"
    [ -f "$file" ] || return
    awk '
        /^## Project Identity$/ {
            print; print ""
            while ((getline line < "project.md") > 0) print line
            close("project.md")
            print ""
            skip=1; next
        }
        skip && /^---$/ { skip=0; print; next }
        skip { next }
        { print }
    ' "$file" > "${file}.tmp" && mv "${file}.tmp" "$file"
    echo "  synced → $file"
}

echo "Syncing project identity to bootstrap files..."
sync_identity CLAUDE.md
sync_identity GEMINI.md
sync_identity CURSOR.md
sync_identity AGENTS.md

# ── Create directory structure ─────────────────────────────────────────────────

mkdir -p raw wiki/pages
grep -q "^raw/$" .gitignore 2>/dev/null || echo "raw/" >> .gitignore
echo "raw/ excluded from git (via .gitignore)"

# ── Initialise wiki files (only if not already present) ───────────────────────

if [ ! -f wiki/primary.bib ]; then
    cat > wiki/primary.bib << 'EOF'
% primary.bib — papers with PDFs in raw/
% Managed by NeuroWiki agent. Do not edit manually.
EOF
fi

if [ ! -f wiki/secondary.bib ]; then
    cat > wiki/secondary.bib << 'EOF'
% secondary.bib — papers cited within PDFs but not held locally
% Entries marked with: note = {reconstructed from @SourceKey}
% Managed by NeuroWiki agent. Do not edit manually.
EOF
fi

if [ ! -f wiki/log.md ]; then
    cat > wiki/log.md << 'EOF'
# Session Log

One entry per agent session. Each entry signed off by a lab member after verification.
See docs/VERIFICATION.md for the verification protocol.

---
EOF
fi

cat > wiki/index.md << INDEXEOF
---
type: index
title: Wiki Root Index
updated: $(date +%Y-%m-%d)
---

# Wiki Index — ${PROJECT_NAME}

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
INDEXEOF

# ── Done ──────────────────────────────────────────────────────────────────────

echo ""
echo "Setup complete."
echo ""
echo "Next steps:"
echo "  1. Add PDFs to raw/ (git-ignored; never committed)"
echo "  2. Start a session using a prompt from docs/QUICKSTART.md"
echo ""
echo "To update project identity later: edit project.md and re-run this script."

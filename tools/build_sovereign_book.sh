#!/bin/bash
# ==============================================================================
# 📜 DSOM Sovereign Book Generator (v3.9) - THE MASTER PROTOCOL
#
# Date:    2026-01-28
# Author:  Harisfazillah Jamel (LinuxMalaysia)
# Partner: Generated with the help of Google Gemini
# License: GNU GPL v3.0 or later (Script) / CC BY-SA 4.0 (Output Content)
#
# Logic: Adds high-resolution timestamps and CC BY-SA 4.0 licensing to
# both the filename and internal metadata for archival integrity.
# Logic: Implements Fail-Safe Directory Management. Uses traps for cleanup
# and strict verification of TEMP_DIR creation/deletion to protect the SSoT.
# Logic: Includes Automated Git Integration to commit the final PDF artifact
# into the sovereign repository, ensuring archival persistence.
# Logic: Complete Sovereign Build Pipeline. Features OS-aware dependency 
# checks (Apt/Dnf), fail-safe directory traps, table flattening, 
# and automated Git archival of the final PDF artifact.
# Logic: Unified Build Pipeline. Includes OS-aware dependency checks (Apt/Dnf),
# fail-safe directory traps, YAML alias protection, table flattening,
# and automated Git archival of the final PDF artifact.
# Logic: Unified Build Pipeline. Includes OS-aware dependency checks (Apt/Dnf),
# fail-safe directory traps, YAML alias protection, table flattening,
# and automated Git archival.
# Discovery Logic: Scans for .md/.txt files missing from SUMMARY.md to ensure
# no sovereign artifacts are left behind.
# Logic: Unified Build Pipeline with Emoji Support (Noto Color Emoji).
# Includes OS-aware checks, Fail-safe traps, Discovery, and Full Git Ritual.
# Logic: Switched to LuaLaTeX for robust Noto Color Emoji support.
# No hardcoded member paths; dynamically resolves via $(whoami).
# Logic: Hardened LuaLaTeX dependencies. Includes a comprehensive check for
# TeX Live font metrics and emoji support.
#
# ==============================================================================
# Logic 1: High-res timestamps & CC BY-SA 4.0 metadata.
# Logic 2: Fail-safe Traps & strict TEMP_DIR verification.
# Logic 3: OS-aware Dependency Checks (Apt/Dnf) + SVG & Emoji Tools.
# Logic 4: YAML Alias Protection & Table Flattening.
# Logic 5: Artifact Discovery (find/audit against SUMMARY.md).
# Logic 6: Dynamic User Path Resolution ($(whoami)).
# Logic 7: FULL ATOMIC RITUAL (Updates PDF, HISTORY.md, and walkthrough.md).
# ==============================================================================

TIMESTAMP=$(date +%Y%m%d_%H%M)
ISO_DATE=$(date +"%Y-%m-%d %H:%M:%S")
OUTPUT_FILE="DSOM_Sovereign_Brain_${TIMESTAMP}.pdf"
METADATA_FILE="metadata.yaml"
TEMP_DIR="build_tmp_${TIMESTAMP}"

# Dynamic Identity Resolution
CURRENT_USER=$(whoami)
WALKTHROUGH_PATH=".agent/brain/member/${CURRENT_USER}/walkthrough.md"

# --- [1. Fail-Safe Cleanup] ---
cleanup() {
    echo "🧹 Performing Fail-Safe Cleanup..."
    if [ -n "${TEMP_DIR}" ] && [ -d "${TEMP_DIR}" ]; then
        rm -rf "${TEMP_DIR:?}"
    fi
    if [ -f "${METADATA_FILE}" ]; then
        rm -f "${METADATA_FILE:?}"
    fi
}
trap cleanup EXIT SIGINT SIGTERM

# --- [2. Dependency Check (Ubuntu/RHEL) + Expanded LaTeX Fonts] ---
check_dependencies() {
    echo "🔍 Verifying environment prerequisites..."
    if ! command -v pandoc &> /dev/null || ! command -v lualatex &> /dev/null; then
        echo "❌ Error: Missing core dependencies (Pandoc or LuaLaTeX)."
        if [ -f /etc/debian_version ]; then
            echo "👉 Run: sudo apt-get update && sudo apt-get install -y pandoc librsvg2-bin fonts-noto-color-emoji texlive-luatex texlive-latex-extra texlive-fonts-recommended texlive-plain-generic"
        elif [ -f /etc/redhat-release ]; then
            echo "👉 Run: sudo dnf install -y pandoc librsvg2-tools google-noto-emoji-color-fonts texlive-scheme-medium"
        fi
        exit 1
    fi
}
check_dependencies

# --- [3. Artifact Discovery Audit] ---
echo "🔍 Auditing Sovereign Artifacts..."
if [ ! -f "SUMMARY.md" ]; then echo "❌ Error: SUMMARY.md missing."; exit 1; fi
LISTED_FILES=$(sed -n 's/.*(\(.*\))/\1/p' SUMMARY.md | grep -v "http" | grep -E "\.(md|txt)$")
ACTUAL_FILES=$(find . -type f \( -name "*.md" -o -name "*.txt" \) -not -path "*/.*" -not -path "./$TEMP_DIR/*" | sed 's|./||')

echo "📂 Discovery Report:"
for f in $ACTUAL_FILES; do
    if ! echo "$LISTED_FILES" | grep -q "^$f$"; then
        echo "⚠️  UNTRACKED: $f (Not in SUMMARY.md)"
    fi
done

# --- [4. Build Prep & Metadata for LuaLaTeX] ---
mkdir -p "$TEMP_DIR"
cat > "$METADATA_FILE" <<EOF
---
title: "DSOM For My AI: Sovereign Repository Manual"
author: "${CURRENT_USER^} (via DSOM Protocol)"
date: "${ISO_DATE}"
copyright: "© 2026 Harisfazillah Jamel. Licensed under CC BY-SA 4.0."
lang: "en-GB"
geometry: "a5paper, margin=1.5cm"
mainfont: "DejaVu Serif"
header-includes:
  - \usepackage{fancyhdr}
  - \pagestyle{empty}
  - \usepackage{fontspec}
  - \setmainfont{DejaVu Serif}
  - \setmonofont{DejaVu Sans Mono}
  - \newfontfamily{\emoji}{Noto Color Emoji}[Renderer=HarfBuzz]

---
EOF

# --- [5. Process & Flatten Artifacts] ---
echo "🚜 Normalising artifacts for AI ingestion..."
PROCESSED_FILES=""
for file in $LISTED_FILES; do
    if [ -f "$file" ]; then
        target="$TEMP_DIR/$(basename "$file")"
        pandoc "$file" --from markdown-yaml_metadata_block -t markdown-grid_tables+pipe_tables -o "$target"
        PROCESSED_FILES="$PROCESSED_FILES $target"
    fi
done

# --- [6. Build Engine (LuaLaTeX)] ---
echo "🏗️  Building Sovereign Book for ${CURRENT_USER} via LuaLaTeX..."
if pandoc $PROCESSED_FILES \
    --output="$OUTPUT_FILE" \
    --metadata-file="$METADATA_FILE" \
    --toc \
    --number-sections \
    --pdf-engine=lualatex \
    --columns=1000 \
    -V links-as-notes=true; then
    
    echo "⭐ Success: ${OUTPUT_FILE}"

    # --- [7. THE FULL ATOMIC RITUAL] ---
    echo "📡 Executing Atomic Git Ritual..."
    git add "$OUTPUT_FILE"
    echo "- **[${TIMESTAMP}]:** Automated Build v3.8 (Hardened LuaLaTeX)." >> HISTORY.md
    git add HISTORY.md
    if [ -f "$WALKTHROUGH_PATH" ]; then
        echo -e "\n## [${TIMESTAMP}] | Build Ritual: Font Metric Fix\n- Upgraded to v3.8 with complete TeX Live font libraries.\n- Artifact archived: ${OUTPUT_FILE}" >> "$WALKTHROUGH_PATH"
        git add "$WALKTHROUGH_PATH"
    fi
    git commit -m "feat(archive): auto-build v3.8 with hardened luatex"
    echo "✅ All ledgers for ${CURRENT_USER} updated and committed."
else
    echo "❌ Build failed. Please verify TeX Live font packages."
    exit 1
fi


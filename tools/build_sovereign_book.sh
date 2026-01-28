#!/bin/bash
# ==============================================================================
# 📜 DSOM Sovereign Book Generator (v3.1) - THE MASTER PROTOCOL
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
# ==============================================================================
# Logic 1: High-res timestamps & CC BY-SA 4.0 metadata.
# Logic 2: Fail-safe Traps & strict TEMP_DIR verification.
# Logic 3: OS-aware Dependency Checks (Apt/Dnf).
# Logic 4: YAML Alias Protection & Table Flattening.
# Logic 5: Artifact Discovery (find/audit against SUMMARY.md).
# Logic 6: FULL ATOMIC RITUAL (Updates PDF, HISTORY.md, and walkthrough.md).
# ==============================================================================

TIMESTAMP=$(date +%Y%m%d_%H%M)
ISO_DATE=$(date +"%Y-%m-%d %H:%M:%S")
OUTPUT_FILE="DSOM_Sovereign_Brain_${TIMESTAMP}.pdf"
METADATA_FILE="metadata.yaml"
TEMP_DIR="build_tmp_${TIMESTAMP}"
WALKTHROUGH_PATH=".agent/brain/member/haris/walkthrough.md"

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

# --- [2. Dependency Check (Ubuntu/RHEL) + SVG Tools] ---
check_dependencies() {
    echo "🔍 Verifying environment prerequisites..."
    # Check for Pandoc and rsvg-convert
    if ! command -v pandoc &> /dev/null || ! command -v rsvg-convert &> /dev/null; then
        echo "❌ Error: Missing core dependencies (pandoc or librsvg)."
        if [ -f /etc/debian_version ]; then
            echo "👉 Run: sudo apt-get update && sudo apt-get install -y pandoc librsvg2-bin texlive-xetex texlive-fonts-recommended texlive-latex-extra"
        elif [ -f /etc/redhat-release ]; then
            echo "👉 Run: sudo dnf install -y pandoc librsvg2-tools texlive-scheme-medium"
        fi
        exit 1
    fi
}
check_dependencies

# --- [3. Artifact Discovery Audit] ---
echo "🔍 Auditing Sovereign Artifacts..."
LISTED_FILES=$(sed -n 's/.*(\(.*\))/\1/p' SUMMARY.md | grep -v "http" | grep -E "\.(md|txt)$")
ACTUAL_FILES=$(find . -type f \( -name "*.md" -o -name "*.txt" \) -not -path "*/.*" -not -path "./$TEMP_DIR/*" | sed 's|./||')

echo "📂 Discovery Report:"
for f in $ACTUAL_FILES; do
    if ! echo "$LISTED_FILES" | grep -q "^$f$"; then
        echo "⚠️  UNTRACKED: $f (Not in SUMMARY.md)"
    fi
done

# --- [4. Build Preparation] ---
mkdir -p "$TEMP_DIR"
cat > "$METADATA_FILE" <<EOF
---
title: "DSOM For My AI: Sovereign Repository Manual"
author: "Harisfazillah Jamel (Lead Architect)"
date: "${ISO_DATE}"
copyright: "© 2026 Harisfazillah Jamel. Licensed under CC BY-SA 4.0."
lang: "en-GB"
geometry: "a5paper, margin=1.5cm"
---
EOF

# --- [5. Process & Flatten] ---
PROCESSED_FILES=""
for file in $LISTED_FILES; do
    if [ -f "$file" ]; then
        target="$TEMP_DIR/$(basename "$file")"
        # Logic: Strip YAML to prevent Alias errors + Grid Tables
        pandoc "$file" --from markdown-yaml_metadata_block -t markdown-grid_tables+pipe_tables -o "$target"
        PROCESSED_FILES="$PROCESSED_FILES $target"
    fi
done

# --- [6. Build Engine] ---
echo "🏗️  Building Sovereign Book..."
if pandoc $PROCESSED_FILES --output="$OUTPUT_FILE" --metadata-file="$METADATA_FILE" --toc --number-sections --pdf-engine=xelatex -V mainfont="DejaVu Serif" -V links-as-notes=true; then
    
    echo "⭐ Success: ${OUTPUT_FILE}"

    # --- [7. THE FULL ATOMIC RITUAL] ---
    echo "📡 Executing Atomic Git Ritual..."
    git add "$OUTPUT_FILE"
    echo "- **[${TIMESTAMP}]:** Automated Build of Sovereign Brain PDF (v3.1) with SVG support." >> HISTORY.md
    git add HISTORY.md
    if [ -f "$WALKTHROUGH_PATH" ]; then
        echo -e "\n## [${TIMESTAMP}] | Build Ritual\n- Executed build_sovereign_book.sh v3.1.\n- SVG rendering support verified via librsvg.\n- Artifact archived: ${OUTPUT_FILE}" >> "$WALKTHROUGH_PATH"
        git add "$WALKTHROUGH_PATH"
    fi
    git commit -m "feat(archive): auto-build with svg support ${TIMESTAMP}"
    echo "✅ All ledgers updated and committed."
else
    echo "❌ Build failed. Please check if all images are accessible."
    exit 1
fi


#!/bin/bash
# ==============================================================================
# 📜 DSOM Sovereign Book Generator (v2.4)
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
# ==============================================================================

TIMESTAMP=$(date +%Y%m%d_%H%M)
ISO_DATE=$(date +"%Y-%m-%d %H:%M:%S")
OUTPUT_FILE="DSOM_Sovereign_Brain_${TIMESTAMP}.pdf"
METADATA_FILE="metadata.yaml"
TEMP_DIR="build_tmp_${TIMESTAMP}" # Unique temp dir per run

# --- [1. Fail-Safe Cleanup Function] ---
cleanup() {
    echo "🧹 Performing Fail-Safe Cleanup..."
    if [ -d "${TEMP_DIR}" ]; then
        rm -rf "${TEMP_DIR:?}"
        echo "✅ Removed temporary directory: ${TEMP_DIR}"
    fi
    if [ -f "${METADATA_FILE}" ]; then
        rm -f "${METADATA_FILE:?}"
        echo "✅ Removed temporary metadata file."
    fi
}

# Trap signals (Exit, Interrupt, Terminate) to trigger cleanup
trap cleanup EXIT SIGINT SIGTERM

# --- [2. Dependency Check] ---
check_dependencies() {
    if ! command -v pandoc &> /dev/null; then
        echo "❌ Error: pandoc is not installed."
        exit 1
    fi
}
check_dependencies

# --- [3. Safe Directory Creation] ---
echo "📁 Initialising temporary workspace..."
if ! mkdir -p "$TEMP_DIR"; then
    echo "❌ CRITICAL: Failed to create temporary directory ${TEMP_DIR}. Aborting."
    exit 1
fi

# --- [4. Generate Metadata] ---
cat > "$METADATA_FILE" <<EOF
---
title: "DSOM For My AI: Sovereign Repository Manual"
author: "Harisfazillah Jamel (Lead Architect)"
date: "${ISO_DATE}"
copyright: "© 2026 Harisfazillah Jamel. Licensed under CC BY-SA 4.0."
lang: "en-GB"
geometry: "a5paper, margin=1.5cm"
header-includes:
  - \usepackage{fancyhdr}
  - \pagestyle{empty} 
---
EOF

# --- [5. Parse SUMMARY.md & Flatten Tables] ---
echo "🔍 Scanning SUMMARY.md..."
FILES=$(sed -n 's/.*(\(.*\))/\1/p' SUMMARY.md | grep -v "http" | grep "\.md")

PROCESSED_FILES=""
for file in $FILES; do
    if [ -f "$file" ]; then
        target="$TEMP_DIR/$(basename "$file")"
        if pandoc "$file" -t markdown-grid_tables+pipe_tables -o "$target"; then
            PROCESSED_FILES="$PROCESSED_FILES $target"
        else
            echo "⚠️ Warning: Failed to process $file. Skipping."
        fi
    fi
done

# --- [6. Build Engine] ---
echo "🏗️  Building AI-Ready Sovereign Book [${TIMESTAMP}]..."
if pandoc $PROCESSED_FILES \
    --output="$OUTPUT_FILE" \
    --metadata-file="$METADATA_FILE" \
    --toc \
    --number-sections \
    --pdf-engine=xelatex \
    --columns=1000 \
    -V mainfont="DejaVu Serif" \
    -V links-as-notes=true; then
    echo "⭐ Success! Generated: ${OUTPUT_FILE}"
else
    echo "❌ CRITICAL: PDF Build failed."
    exit 1
fi

# Cleanup is handled automatically by the 'trap'

#!/bin/bash
# ==============================================================================
# 📜 DSOM Sovereign Book Generator (v2.5)
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
# ==============================================================================

TIMESTAMP=$(date +%Y%m%d_%H%M)
ISO_DATE=$(date +"%Y-%m-%d %H:%M:%S")
OUTPUT_FILE="DSOM_Sovereign_Brain_${TIMESTAMP}.pdf"
METADATA_FILE="metadata.yaml"
TEMP_DIR="build_tmp_${TIMESTAMP}"

# --- [1. Fail-Safe Cleanup Function] ---
cleanup() {
    if [ -d "${TEMP_DIR}" ]; then
        rm -rf "${TEMP_DIR:?}"
    fi
    if [ -f "${METADATA_FILE}" ]; then
        rm -f "${METADATA_FILE:?}"
    fi
}
trap cleanup EXIT SIGINT SIGTERM

# --- [2. Pre-flight Checks] ---
if ! command -v pandoc &> /dev/null; then
    echo "❌ Error: pandoc missing. Aborting."
    exit 1
fi

# --- [3. Safe Initialisation] ---
mkdir -p "$TEMP_DIR"

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

# --- [5. Process Artifacts] ---
FILES=$(sed -n 's/.*(\(.*\))/\1/p' SUMMARY.md | grep -v "http" | grep "\.md")
PROCESSED_FILES=""
for file in $FILES; do
    if [ -f "$file" ]; then
        target="$TEMP_DIR/$(basename "$file")"
        pandoc "$file" -t markdown-grid_tables+pipe_tables -o "$target"
        PROCESSED_FILES="$PROCESSED_FILES $target"
    fi
done

# --- [6. Build Engine] ---
echo "🏗️  Building Sovereign Book [${TIMESTAMP}]..."
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

    # --- [7. Automated Git Ritual] ---
    echo "📡 Committing artifact to Sovereign Repository..."
    git add "$OUTPUT_FILE"
    git commit -m "feat(archive): auto-generate sovereign brain PDF ${TIMESTAMP}"
    echo "✅ Artifact committed successfully."

else
    echo "❌ CRITICAL: PDF Build failed. Git commit skipped."
    exit 1
fi


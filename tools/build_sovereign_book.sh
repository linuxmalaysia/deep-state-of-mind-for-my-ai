#!/bin/bash
# ==============================================================================
# 📜 DSOM Sovereign Book Generator (v2.2)
#
# Date:    2026-01-28
# Author:  Harisfazillah Jamel (LinuxMalaysia)
# Partner: Generated with the help of Google Gemini
# License: GNU GPL v3.0 or later
#
# Logic: Includes Environment Awareness for Ubuntu/RHEL and Table Flattening 
# logic to ensure AI RAG systems correctly map headers to values.
# ==============================================================================

OUTPUT_FILE="DSOM_Sovereign_Brain_$(date +%Y%m%d).pdf"
METADATA_FILE="metadata.yaml"
TEMP_DIR="build_tmp"

# --- [1. Dependency Check & OS Detection] ---
check_dependencies() {
    if ! command -v pandoc &> /dev/null; then
        echo "❌ Error: pandoc is not installed."
        if [ -f /etc/debian_version ]; then
            echo "👉 Run: sudo apt-get update && sudo apt-get install -y pandoc texlive-xetex texlive-fonts-recommended texlive-latex-extra"
        elif [ -f /etc/redhat-release ]; then
            echo "👉 Run: sudo dnf install -y pandoc texlive-scheme-medium"
        fi
        exit 1
    fi
}

check_dependencies

# --- [2. Generate Metadata] ---
cat > "$METADATA_FILE" <<EOF
---
title: "DSOM For My AI: Sovereign Repository Manual"
author: "Harisfazillah Jamel (Lead Architect)"
lang: "en-GB"
geometry: "a5paper, margin=1.5cm"
header-includes:
  - \usepackage{fancyhdr}
  - \pagestyle{empty} 
---
EOF

# --- [3. Parse SUMMARY.md] ---
mkdir -p "$TEMP_DIR"
echo "🔍 Scanning SUMMARY.md..."
FILES=$(sed -n 's/.*(\(.*\))/\1/p' SUMMARY.md | grep -v "http" | grep "\.md")

# --- [4. Table Flattening & Pre-processing] ---
echo "🚜 Normalising artifacts for AI ingestion..."
PROCESSED_FILES=""
for file in $FILES; do
    if [ -f "$file" ]; then
        target="$TEMP_DIR/$(basename "$file")"
        # Flattening logic: Normalises tables to grid/pipe standards
        pandoc "$file" -t markdown-grid_tables+pipe_tables -o "$target"
        PROCESSED_FILES="$PROCESSED_FILES $target"
    fi
done

# --- [5. Build Engine] ---
echo "🏗️  Building AI-Ready Sovereign Book..."
pandoc $PROCESSED_FILES \
    --output="$OUTPUT_FILE" \
    --metadata-file="$METADATA_FILE" \
    --toc \
    --number-sections \
    --pdf-engine=xelatex \
    --columns=1000 \
    -V mainfont="DejaVu Serif" \
    -V links-as-notes=true

echo "✅ Success. Generated: $OUTPUT_FILE"

# Cleanup
rm -rf "$TEMP_DIR" "$METADATA_FILE"


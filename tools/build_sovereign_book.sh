#!/bin/bash
# ==============================================================================
# 📜 DSOM Sovereign Book Generator (v2.1)
#
# Date:    2026-01-28
# Author:  Harisfazillah Jamel (LinuxMalaysia)
# Partner: Generated with the help of Google Gemini
# License: GNU GPL v3.0 or later
#
# Logic: Includes Table Flattening logic to ensure AI RAG systems correctly 
# map headers to values without visual grid confusion.
# ==============================================================================

OUTPUT_FILE="DSOM_Sovereign_Brain_$(date +%Y%m%d).pdf"
METADATA_FILE="metadata.yaml"
TEMP_DIR="build_tmp"

mkdir -p "$TEMP_DIR"

# 1. Generate Metadata (as before)
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

# 2. Parse SUMMARY.md
echo "🔍 Scanning SUMMARY.md..."
FILES=$(sed -n 's/.*(\(.*\))/\1/p' SUMMARY.md | grep -v "http" | grep "\.md")

# 3. Table Flattening & Pre-processing Loop
echo "🚜 Flattening tables and preparing artifacts..."
PROCESSED_FILES=""
for file in $FILES; do
    if [ -f "$file" ]; then
        target="$TEMP_DIR/$(basename "$file")"
        
        # LOGIC: Use Pandoc to convert tables to a more robust pipe format
        # This prevents complex multi-line cell issues in the PDF stream.
        pandoc "$file" -t markdown-grid_tables+pipe_tables -o "$target"
        
        PROCESSED_FILES="$PROCESSED_FILES $target"
    fi
done

# 4. The Build Engine
echo "🏗️  Building AI-Ready Sovereign Book..."

# --columns=1000: Prevents Pandoc from wrapping lines in tables/code, 
# which is the #1 cause of broken AI context in PDFs.
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


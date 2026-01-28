#!/bin/bash
# ==============================================================================
# 📜 DSOM Sovereign Book Generator (v2.0)
#
# Purpose: Generates an AI-optimised PDF for RAG and Human E-readers.
# Author:  Harisfazillah Jamel (LinuxMalaysia)
# Logic:   Strips visual noise (headers/footers) to ensure semantic continuity.
# ==============================================================================

OUTPUT_FILE="DSOM_Sovereign_Brain_$(date +%Y%m%d).pdf"
METADATA_FILE="metadata.yaml"

# 1. Generate Enhanced Metadata Block
cat > "$METADATA_FILE" <<EOF
---
title: "DSOM For My AI: Sovereign Repository Manual"
author: "Harisfazillah Jamel (Lead Architect)"
subject: "IT Infrastructure, AI Governance, Linux Architecture"
keywords: [DSOM, Linux, High-Availability, Federated-AI]
lang: "en-GB"
geometry: "a5paper, margin=1.5cm"
fontsize: 10pt
header-includes:
  - \usepackage{fancyhdr}
  - \pagestyle{empty} 
  - \fancyhf{} 
---
EOF

# 2. Parse SUMMARY.md ensuring sequence is maintained
echo "🔍 Scanning SUMMARY.md for Sovereign Artifacts..."
FILES=$(sed -n 's/.*(\(.*\))/\1/p' SUMMARY.md | grep -v "http" | grep "\.md")

# 3. Validation and Member Log Injection
VALID_FILES=""
for file in $FILES; do
    if [ -f "$file" ]; then
        VALID_FILES="$VALID_FILES $file"
    else
        echo "⚠️ Warning: Skipped missing artifact: $file"
    fi
done

# 4. The Build Engine (Pandoc + XeLaTeX)
echo "🏗️  Building Semantic PDF (AI-Ready)..."

pandoc $VALID_FILES \
    --output="$OUTPUT_FILE" \
    --metadata-file="$METADATA_FILE" \
    --toc \
    --toc-depth=3 \
    --number-sections \
    --highlight-style=tango \
    --pdf-engine=xelatex \
    -V mainfont="DejaVu Serif" \
    -V monofont="DejaVu Sans Mono" \
    -V colorlinks=true \
    -V links-as-notes=true

echo "✅ Success. Generated: $OUTPUT_FILE"
rm "$METADATA_FILE"


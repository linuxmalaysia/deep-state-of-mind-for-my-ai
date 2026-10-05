#!/bin/sh
# ==============================================================================
# Protocol    : Deep State of Mind (DSOM) For My AI
# Author      : Harisfazillah Jamel (LinuxMalaysia)
# Timestamp   : 2026-10-04
# License     : GNU General Public License v3.0
# Standard    : UK English | DBP-standard Bahasa Melayu Malaysia (Piawai)
# ==============================================================================
# OKF v0.2 Core Conformance Validator (POSIX-compliant)
# Checks for:
#   1. YAML frontmatter boundaries (---)
#   2. Closing '---' delimiter detection
#   3. Non-empty 'type' attribute
#   4. Deprecation of legacy v0.1 fields (timestamp -> generated)
#   5. Rejection of unparsed citations in body
# ==============================================================================
set -eu

FAILURES=0

echo "[INFO] Commencing OKF v0.2 structural audit..."

file_list=$(mktemp)
find . -type f -name "*.md" ! -path "*/.git/*" ! -path "*/.venv/*" ! -path "*/node_modules/*" ! -path "*/.pytest_cache/*" > "$file_list"

while read -r file; do
    if [ -z "$file" ]; then
        continue
    fi

    # Skip reserved index.md and log.md files
    filename=$(basename "$file")
    if [ "$filename" = "index.md" ] || [ "$filename" = "log.md" ]; then
        continue
    fi

    # 1. Assert frontmatter existence (normalize carriage returns)
    first_line=$(head -n 1 "$file" | tr -d '\r')
    if [ "$first_line" != "---" ]; then
        echo "[ERROR] $file: Missing opening YAML frontmatter '---'"
        FAILURES=$((FAILURES + 1))
        continue
    fi

    # 2. Extract frontmatter content (between line 1 and closing '---')
    # Check if a closing '---' exists starting from line 2
    closing_line=$(tail -n +2 "$file" | tr -d '\r' | grep -n '^---$' | head -n 1 | cut -d: -f1 || true)
    if [ -z "$closing_line" ]; then
        echo "[ERROR] $file: Missing closing YAML frontmatter '---'"
        FAILURES=$((FAILURES + 1))
        continue
    fi

    # Extract lines between line 1 and closing line (excluding delimiters)
    frontmatter=$(tail -n +2 "$file" | tr -d '\r' | head -n "$((closing_line - 1))")

    # 3. Assert 'type' field
    if ! echo "$frontmatter" | grep -Eq "^type:[[:space:]]+.+"; then
        echo "[ERROR] $file: Missing or empty 'type' field in frontmatter"
        FAILURES=$((FAILURES + 1))
    fi

    # 4. Check for deprecated v0.1 'timestamp'
    if echo "$frontmatter" | grep -Eq "^timestamp:[[:space:]]+"; then
        echo "[WARN]  $file: Contains legacy v0.1 'timestamp'. Upgrade to 'generated: { by, at }'"
    fi

    # 5. Check for legacy body citations header
    if grep -Eq "^#[[:space:]]+(Citations|Sources)" "$file"; then
        echo "[WARN]  $file: Found '# Citations' in body. Migrate to frontmatter 'sources:'"
    fi

done < "$file_list"

rm -f "$file_list"

if [ "$FAILURES" -gt 0 ]; then
    echo "[FAIL] OKF v0.2 validation failed with $FAILURES hard errors."
    exit 1
else
    echo "[SUCCESS] All scanned files conform to OKF v0.2 requirements."
    exit 0
fi

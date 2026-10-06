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
#   3. Presence and non-empty status of okf_version, type, title, timestamp, topics
#   4. Rejection of empty values, empty strings (""), and empty lists ([])
#   5. Rejection of unparsed citations in body
# ==============================================================================
set -eu

FAILURES=0

echo "[INFO] Commencing OKF v0.2 structural audit..."

file_list=$(mktemp)
find . -type f -name "*.md" ! -path "*/.git/*" ! -path "*/.venv/*" ! -path "*/node_modules/*" ! -path "*/.pytest_cache/*" > "$file_list"

# Check the first matching field line in frontmatter text, without parsing YAML.
# Arguments: diagnostic file path, field name, frontmatter text without delimiters.
# Return 1 and print an error to stdout for a missing or empty value, including
# exact values "", '', and []. Return 0 otherwise. Trailing spaces are preserved.
# Overwrites the shell variables file_path, field_name, fm_content, and val.
check_field() {
    file_path="$1"
    field_name="$2"
    fm_content="$3"

    val=$(echo "$fm_content" | grep -E "^${field_name}:" | head -n 1 | sed "s/^${field_name}:[[:space:]]*//" | tr -d '\r')

    if [ -z "$val" ]; then
        echo "[ERROR] $file_path: Missing or empty '$field_name' field in frontmatter"
        return 1
    fi

    # Reject quotes-only empty strings "" or '' or empty lists []
    if [ "$val" = "\"\"" ] || [ "$val" = "''" ] || [ "$val" = "[]" ]; then
        echo "[ERROR] $file_path: Field '$field_name' contains empty string or list in frontmatter"
        return 1
    fi

    return 0
}

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
    closing_line=$(tail -n +2 "$file" | tr -d '\r' | grep -n '^---$' | head -n 1 | cut -d: -f1 || true)
    if [ -z "$closing_line" ]; then
        echo "[ERROR] $file: Missing closing YAML frontmatter '---'"
        FAILURES=$((FAILURES + 1))
        continue
    fi

    # Extract lines between line 1 and closing line (excluding delimiters)
    frontmatter=$(tail -n +2 "$file" | tr -d '\r' | head -n "$((closing_line - 1))")

    # 3. Assert mandatory frontmatter attributes
    check_field "$file" "okf_version" "$frontmatter" || FAILURES=$((FAILURES + 1))
    check_field "$file" "type" "$frontmatter" || FAILURES=$((FAILURES + 1))
    check_field "$file" "title" "$frontmatter" || FAILURES=$((FAILURES + 1))
    check_field "$file" "timestamp" "$frontmatter" || FAILURES=$((FAILURES + 1))
    check_field "$file" "topics" "$frontmatter" || FAILURES=$((FAILURES + 1))

    # 4. Check for legacy body citations header
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

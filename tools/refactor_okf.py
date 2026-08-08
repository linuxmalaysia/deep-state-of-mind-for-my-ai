#!/usr/bin/env python3

# ==============================================================================
# Protocol    : Deep State of Mind (DSOM) For My AI
# Author      : Harisfazillah Jamel (LinuxMalaysia)
# Timestamp   : 2026-08-07
# License     : GNU General Public License v3.0
# Standard    : UK English | DBP-standard Bahasa Melayu Malaysia (Piawai)
# ==============================================================================
"""
OKF Frontmatter Refactoring Script.
Scans the entire repository and rewrites all .md files with OKF compliant
frontmatter written in UTF-8 without a BOM, ensuring strings with emojis,
colons, brackets, or other special characters are double-quoted.
This script imports the canonical implementations from tools/apply_okf_frontmatter.py.
"""
import os
import sys
import argparse

# Insert repository root to sys.path to allow importing from tools
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.apply_okf_frontmatter import (
    FRONTMATTER_RE,
    CustomLoader,
    get_okf_type,
    extract_title,
    get_default_topics,
    needs_double_quotes,
    serialise_val,
    process_file
)

def main():
    parser = argparse.ArgumentParser(description="Ensure OKF v0.1 compliance on all Markdown files with refactoring.")
    parser.add_argument("directory", nargs="?", default=".", help="Root directory to scan (default: '.')")
    parser.add_argument("--dry-run", action="store_true", help="Print planned rewrites without modifying files")
    args = parser.parse_args()

    root_dir = os.path.abspath(args.directory)
    modified_count = 0
    total_count = 0

    exclude_dirs = {'.git', 'node_modules', '.pytest_cache', '.venv'}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

        for filename in filenames:
            if not filename.endswith('.md'):
                continue

            filepath = os.path.join(dirpath, filename)

            if os.path.islink(filepath):
                continue

            try:
                real_root = os.path.realpath(root_dir)
                real_filepath = os.path.realpath(filepath)
                if os.path.commonpath([real_root, real_filepath]) != real_root:
                    continue
            except Exception:
                continue

            total_count += 1
            try:
                if process_file(filepath, root_dir, dry_run=args.dry_run):
                    rel = os.path.relpath(filepath, root_dir).replace('\\', '/')
                    if args.dry_run:
                        print(f"[DRY RUN] Would refactor OKF: {rel}")
                    else:
                        print(f"Refactored OKF: {rel}")
                    modified_count += 1
            except Exception as e:
                print(f"Error processing {filepath}: {e}", file=sys.stderr)
                sys.exit(1)

    if args.dry_run:
        print(f"\n[DRY RUN] Refactor scan complete. Total markdown files checked: {total_count}")
        print(f"[DRY RUN] Total files that would be modified/rewritten: {modified_count}")
    else:
        print(f"\nRefactor complete. Total markdown files checked: {total_count}")
        print(f"Total files modified/rewritten: {modified_count}")

if __name__ == "__main__":
    main()

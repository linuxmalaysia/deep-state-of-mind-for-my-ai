#!/usr/bin/env python3

# ==============================================================================
# Protocol    : Deep State of Mind (DSOM) For My AI
# Author      : Harisfazillah Jamel (LinuxMalaysia)
# Timestamp   : 2026-08-05
# License     : GNU General Public License v3.0
# Standard    : UK English | DBP-standard Bahasa Melayu Malaysia (Piawai)
# ==============================================================================
"""
OKF Frontmatter Compliance Script.
Scans a target directory and ensures all .md files use OKF v0.1 YAML frontmatter
with the required fields (okf_version, type, title, timestamp, topics).
This script imports the canonical implementations from tools/apply_okf_frontmatter.py.
"""
import os
import sys
import argparse

# Insert repository root to sys.path to allow importing from tools
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

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
    parser = argparse.ArgumentParser(description="Ensure OKF v0.1 compliance on all Markdown files.")
    parser.add_argument("directory", nargs="?", default=".", help="Root directory to scan (default: '.')")
    args = parser.parse_args()

    root_dir = os.path.abspath(args.directory)
    modified_count = 0
    total_count = 0

    # Exclude list for directories we should not modify/add frontmatter to
    exclude_dirs = {'.git', 'node_modules', '.pytest_cache'}
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Prune excluded directories in place
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
        
        for filename in filenames:
            if not filename.endswith('.md'):
                continue

            filepath = os.path.join(dirpath, filename)

            # Reject symlinks
            if os.path.islink(filepath):
                continue
                
            # Verify resolved path remains within the resolved root_dir
            try:
                real_root = os.path.realpath(root_dir)
                real_filepath = os.path.realpath(filepath)
                if os.path.commonpath([real_root, real_filepath]) != real_root:
                    continue
            except Exception:
                continue

            total_count += 1
            if process_file(filepath, root_dir):
                rel = os.path.relpath(filepath, root_dir).replace('\\', '/')
                print(f"Standardised/Injected OKF: {rel}")
                modified_count += 1

    print(f"\nScan complete. Total markdown files checked: {total_count}")
    print(f"Total files modified to be OKF-compliant: {modified_count}")

if __name__ == "__main__":
    main()

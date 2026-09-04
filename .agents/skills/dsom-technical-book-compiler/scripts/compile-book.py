#!/usr/bin/env python3
"""
Technical Ebook & Handbook Compiler Script.

Compiles multi-file Markdown documentation suites and source code repositories
into publication-grade PDF, standalone HTML, EPUB 3, and ODT handbooks.
"""

import os
import sys
import re
import shutil
import subprocess
import argparse
import zipfile
from pathlib import Path


def audit_artifact(file_path: Path) -> bool:
    """Inspect artifact for absolute path and build directory leaks."""
    patterns = [r"file:///", r"[A-Za-z]:/", r"\bbuild/"]

    if file_path.suffix.lower() in [".epub", ".odt"]:
        try:
            with zipfile.ZipFile(file_path, "r") as zf:
                for member in zf.namelist():
                    content = zf.read(member).decode("utf-8", errors="ignore")
                    for pat in patterns:
                        if re.search(pat, content):
                            print(f"ERROR: Path leak ('{pat}') detected in {file_path.name} member '{member}'!")
                            return True
        except Exception as e:
            print(f"ERROR: Failed to inspect zip archive {file_path.name}: {e}")
            return True
    else:
        content = file_path.read_bytes().decode("utf-8", errors="ignore")
        for pat in patterns:
            if re.search(pat, content):
                print(f"ERROR: Path leak ('{pat}') detected in {file_path.name}!")
                return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Compile technical ebook & handbook.")
    parser.add_argument("--src", type=str, default="docs", help="Source directory containing Markdown files.")
    parser.add_argument("--out", type=str, default="build/book", help="Output directory for compiled books.")
    parser.add_argument("--title", type=str, default="Technical Handbook", help="Book title.")
    parser.add_argument("--author", type=str, default="Compile by: Harisfazillah Jamel", help="Book author/compiler.")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    src_dir = Path(args.src)
    if not src_dir.exists():
        print(f"ERROR: Source directory '{args.src}' does not exist.")
        sys.exit(1)

    print(f"Compiling handbook from '{args.src}' to '{args.out}'...")

    pandoc_bin = shutil.which("pandoc")
    if not pandoc_bin:
        print("ERROR: Pandoc executable not found. Cannot execute compilation pipeline.")
        sys.exit(1)

    expected_formats = ["html", "pdf", "epub", "odt"]

    try:
        master_md = out_dir / "master_book.md"
        md_files = sorted(src_dir.rglob("*.md"))
        if not md_files:
            print(f"ERROR: No Markdown files found in '{args.src}'.")
            sys.exit(1)

        with open(master_md, "w", encoding="utf-8") as outfile:
            for f in md_files:
                outfile.write(f.read_text(encoding="utf-8", errors="ignore"))
                outfile.write("\n\n")

        # HTML
        html_out = out_dir / "handbook.html"
        subprocess.run([pandoc_bin, str(master_md), "-o", str(html_out), "--standalone"], check=True)

        # EPUB
        epub_out = out_dir / "handbook.epub"
        subprocess.run([pandoc_bin, str(master_md), "-o", str(epub_out), "-t", "epub3"], check=True)

        # ODT
        odt_out = out_dir / "handbook.odt"
        subprocess.run([pandoc_bin, str(master_md), "-o", str(odt_out)], check=True)

        # PDF via Headless Chromium / Edge if available
        pdf_out = out_dir / "handbook.pdf"
        edge_bin = shutil.which("msedge") or shutil.which("msedge.exe") or shutil.which("chromium") or shutil.which("google-chrome")
        if edge_bin:
            file_uri = html_out.resolve().as_uri()
            subprocess.run([edge_bin, "--headless=new", "--disable-gpu", "--run-all-compositor-stages-before-draw", "--virtual-time-budget=8000", f"--print-to-pdf={pdf_out}", file_uri], timeout=60, check=True)
        else:
            subprocess.run([pandoc_bin, str(master_md), "-o", str(pdf_out)], check=True)

    except Exception as e:
        print(f"ERROR: Compilation pipeline execution failed: {e}")
        sys.exit(1)

    # Format-aware leak audit
    leaks_found = False
    for fmt in expected_formats:
        target_file = out_dir / f"handbook.{fmt}"
        if not target_file.exists():
            print(f"ERROR: Expected artifact '{target_file.name}' was not generated.")
            leaks_found = True
        elif audit_artifact(target_file):
            leaks_found = True

    if leaks_found:
        sys.exit(1)

    print("Compilation completed successfully.")


if __name__ == "__main__":
    main()

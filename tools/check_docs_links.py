#!/usr/bin/env python3
"""
Zero-Dependency Diátaxis Documentation Link Validator.

Recursively scans all Markdown files in the new Diátaxis quadrant directories
(tutorials, how-to, reference, explanation) and docs/SUMMARY.md to verify
that all relative links resolve to existing files on disk.
Exits with a non-zero code if any broken link is found.
"""
import os
import re
import sys
from pathlib import Path

def find_repo_root() -> Path:
    current = Path(__file__).resolve().parent
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    return Path(__file__).resolve().parent.parent

def is_external_or_special(url: str) -> bool:
    """Checks if a URL is external, mailto, or anchor-only."""
    return url.startswith(("http://", "https://", "mailto:", "ftp:", "#", "file://"))

def validate_links(repo_root: Path) -> list[str]:
    """
    Scans the Diátaxis documentation files and validates all relative links.

    Returns:
        list[str]: A list of error messages describing broken links.
    """
    errors = []
    link_re = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

    # Target directories and files representing our new Diátaxis documentation system
    target_paths = [
        repo_root / "docs" / "tutorials",
        repo_root / "docs" / "how-to",
        repo_root / "docs" / "reference",
        repo_root / "docs" / "explanation",
        repo_root / "docs" / "SUMMARY.md"
    ]

    md_files = []
    for path in target_paths:
        if path.is_file():
            md_files.append(path)
        elif path.is_dir():
            for root, _, files in os.walk(path):
                for f in files:
                    if f.endswith(".md"):
                        md_files.append(Path(root) / f)

    print(f"Scanning {len(md_files)} Diátaxis documentation files for broken references...")

    for filepath in md_files:
        try:
            content = filepath.read_text(encoding="utf-8")
        except Exception as e:
            errors.append(f"Could not read file {filepath}: {e}")
            continue

        links = link_re.findall(content)
        for text, url in links:
            url_clean = url.split("#")[0].strip() # Strip anchors
            if not url_clean or is_external_or_special(url):
                continue

            # Treat relative paths relative to the current file's parent directory
            resolved_path = (filepath.parent / url_clean).resolve()

            # Verify resolved path is within repo boundaries
            try:
                resolved_path.relative_to(repo_root)
            except ValueError:
                errors.append(f"In {filepath.relative_to(repo_root)}: link '{url}' goes outside repository bounds.")
                continue

            # Assert file exists
            if not resolved_path.exists():
                errors.append(
                    f"In {filepath.relative_to(repo_root)}: Broken link '{url}' (resolved to non-existent path: {resolved_path.relative_to(repo_root)})"
                )

    return errors

def main():
    repo_root = find_repo_root()
    errors = validate_links(repo_root)
    if errors:
        print("\n❌ Found Broken Links / Dead References inside Diátaxis Space:")
        for error in errors:
            print(f"  - {error}")
        print(f"\nTotal broken references found: {len(errors)}")
        sys.exit(1)
    else:
        print("\n✅ All Diátaxis relative links and references validated successfully! Zero dead references found.")
        sys.exit(0)

if __name__ == "__main__":
    main()

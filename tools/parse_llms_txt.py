#!/usr/bin/env python3
"""
LLM Context and Sitemap Compiler for llms.txt.

Parses llms.txt to extract all referenced local Markdown files, merges their content
into a unified llms-full.txt file, and outputs a structured llms-context.xml file.
Provides both a CLI and programmatic Python API.
"""
import argparse
import datetime
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

# Find repository root
def find_repo_root() -> Path:
    current = Path(__file__).resolve().parent
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    return Path(__file__).resolve().parent.parent

def parse_llms_txt(llms_path: Path, repo_root: Path) -> list[tuple[str, Path]]:
    """
    Parses llms.txt to extract title and path for each local Markdown link.

    Returns:
        list[tuple[str, Path]]: List of (title, absolute_path) tuples.
    """
    if not llms_path.exists():
        raise FileNotFoundError(f"llms.txt not found at {llms_path}")

    content = llms_path.read_text(encoding="utf-8")

    # Matches [anchor text](path.md)
    matches = re.findall(r'\[([^\]]+)\]\(([^)]+\.md)\)', content)

    discovered_files = []
    seen_paths = set()

    for title, rel_path in matches:
        # Ignore external HTTP links if any matched
        if rel_path.startswith(("http://", "https://")):
            continue

        abs_path = (repo_root / rel_path).resolve()

        # Verify the file is inside the repository
        try:
            abs_path.relative_to(repo_root)
        except ValueError as e:
            raise ValueError(f"Out-of-bounds path detected in llms.txt: {rel_path}") from e

        if not abs_path.exists():
            raise FileNotFoundError(f"Referenced file in llms.txt does not exist: {rel_path} (resolved: {abs_path})")

        if not abs_path.is_file():
            raise FileNotFoundError(f"Referenced path in llms.txt is not a file: {rel_path} (resolved: {abs_path})")

        if str(abs_path) not in seen_paths:
            discovered_files.append((title, abs_path))
            seen_paths.add(str(abs_path))

    return discovered_files

def generate_llms_full_txt(files: list[tuple[str, Path]], output_path: Path, repo_root: Path):
    """
    Consolidates the full content of all discovered markdown files into one flat file.
    """
    print(f"Generating consolidated text catalog at {output_path}...")
    separator = "\n\n" + "=" * 80 + "\n"
    parts = []

    for title, filepath in files:
        rel_path = filepath.relative_to(repo_root).as_posix()
        try:
            content = filepath.read_text(encoding="utf-8")
            parts.append(f"FILE: {rel_path}\nTITLE: {title}\n{'-' * 40}\n{content}")
        except Exception as e:
            raise IOError(f"Failed to read file {rel_path} while compiling llms-full.txt: {e}") from e

    output_path.write_text(separator.join(parts), encoding="utf-8")
    print(f"Wrote {len(files)} files to {output_path}")

def generate_llms_context_xml(files: list[tuple[str, Path]], output_path: Path, repo_root: Path):
    """
    Compiles discovered file contents into a highly structured XML context document.
    """
    print(f"Generating XML context file at {output_path}...")

    root = ET.Element("context")
    current_utc_time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    root.set("timestamp", current_utc_time)
    root.set("total_files", str(len(files)))

    for title, filepath in files:
        rel_path = filepath.relative_to(repo_root).as_posix()
        try:
            content = filepath.read_text(encoding="utf-8")
            doc_elem = ET.SubElement(root, "document")
            doc_elem.set("path", rel_path)
            doc_elem.set("title", title)

            content_elem = ET.SubElement(doc_elem, "content")
            # Preserve raw text structure inside CDATA or simple text
            content_elem.text = content
        except Exception as e:
            raise IOError(f"Failed to read file {rel_path} while compiling llms-context.xml: {e}") from e

    # Write tree to output
    tree = ET.ElementTree(root)
    # Use standard indenting for readability
    ET.indent(tree, space="  ", level=0)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"Wrote {len(files)} files to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Parse llms.txt and compile consolidated context files.")
    parser.add_argument("--input", default="llms.txt", help="Path to input llms.txt (default: llms.txt)")
    parser.add_argument("--output-txt", default="llms-full.txt", help="Path to output llms-full.txt")
    parser.add_argument("--output-xml", default="llms-context.xml", help="Path to output llms-context.xml")

    args = parser.parse_args()

    repo_root = find_repo_root()
    input_path = repo_root / args.input
    output_txt_path = repo_root / args.output_txt
    output_xml_path = repo_root / args.output_xml

    print(f"Starting parsing of {input_path}...")
    try:
        discovered_files = parse_llms_txt(input_path, repo_root)
        print(f"Discovered {len(discovered_files)} local documentation files.")

        generate_llms_full_txt(discovered_files, output_txt_path, repo_root)
        generate_llms_context_xml(discovered_files, output_xml_path, repo_root)
        print("Compilation complete successfully!")
    except Exception as e:
        print(f"Error during compilation: {e}")
        raise e

if __name__ == "__main__":
    main()

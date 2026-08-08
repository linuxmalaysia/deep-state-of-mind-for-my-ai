#!/usr/bin/env python3
"""
Sitemap Generator for Deep State of Mind (DSOM).

This script dynamically gathers all publishing URLs from:
1. GitHub Pages (parsed from MkDocs-generated site/sitemap.xml)
2. Read the Docs (derived from GitHub Pages URLs)
3. GitBook (parsed from SUMMARY.md and matched to valid repository files)

It outputs:
- sitemap.txt (plain text list of all URLs)
- sitemap.xml (standard unified XML sitemap)
- robots.txt (pointing to both sitemaps)

All generated files are written to the repository root, to the docs/ directory,
and directly to the built site/ directory to ensure seamless deployment and SEO indexation.
"""
import datetime
import os
import pathlib
import re
import subprocess
import urllib.parse
import xml.etree.ElementTree as ET

# Base URLs
GITHUB_PAGES_BASE = "https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/"
READTHEDOCS_BASE = "https://deep-state-of-mind-for-my-ai.readthedocs.io/en/latest/"
GITBOOK_BASE = "https://malaysia-open-source-community.gitbook.io/deep-state-of-mind-dsom-protocol-for-my-ai/"

def find_repo_root() -> pathlib.Path:
    """Locate and return the repository root containing the `.git` directory.
    
    Raises:
    	RuntimeError: If no repository root is found.
    """
    current = pathlib.Path(__file__).resolve().parent
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")

REPO_ROOT = find_repo_root()

def build_mkdocs():
    """
    Build the MkDocs site from the repository root.
    """
    print("Building MkDocs site to compile fresh sitemap source...")
    result = subprocess.run(
        ["uv", "run", "--with", "mkdocs-material", "mkdocs", "build"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True
    )
    print("MkDocs build complete.")

def parse_github_pages_urls() -> list[str]:
    """Extracts unique page URLs from the generated GitHub Pages sitemap.
    
    Returns:
    	list[str]: Sorted, deduplicated URLs found in the sitemap.
    
    Raises:
    	FileNotFoundError: If the generated sitemap does not exist.
    """
    sitemap_path = REPO_ROOT / "site" / "sitemap.xml"
    if not sitemap_path.exists():
        raise FileNotFoundError(f"MkDocs sitemap not found at {sitemap_path}. Build might have failed.")

    print(f"Parsing GitHub Pages URLs from {sitemap_path}...")
    tree = ET.parse(sitemap_path)
    root = tree.getroot()

    # Handle XML namespace
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = []
    for loc in root.findall('.//ns:loc', namespace):
        if loc.text:
            urls.append(loc.text.strip())

    print(f"Found {len(urls)} GitHub Pages URLs.")
    return sorted(list(set(urls)))

def generate_readthedocs_urls(gh_urls: list[str]) -> list[str]:
    """
    Convert GitHub Pages URLs to their corresponding Read the Docs URLs.
    
    Parameters:
        gh_urls (list[str]): GitHub Pages URLs to convert.
    
    Returns:
        list[str]: Sorted, deduplicated Read the Docs URLs.
    """
    print("Generating Read the Docs URLs...")
    rtd_urls = []
    for url in gh_urls:
        if url.startswith(GITHUB_PAGES_BASE):
            relative = url[len(GITHUB_PAGES_BASE):]
            # Read the Docs might trailing slash differently but keeping exact structure
            rtd_url = READTHEDOCS_BASE + relative
            rtd_urls.append(rtd_url)
    print(f"Generated {len(rtd_urls)} Read the Docs URLs.")
    return sorted(list(set(rtd_urls)))

def to_gitbook_slug(path_str: str) -> str:
    """
    Convert a repository Markdown path into a normalized GitBook slug.
    
    Parameters:
        path_str (str): Repository-relative Markdown path.
    
    Returns:
        str: GitBook slug, or an empty string for the README file.
    """
    if path_str.lower() == "readme.md":
        return ""

    # Strip .md extension
    if path_str.lower().endswith(".md"):
        path_str = path_str[:-3]

    parts = path_str.split('/')
    slug_parts = []
    for part in parts:
        part = part.lower()
        part = urllib.parse.unquote(part)
        # Replace non-alphanumeric (excluding hyphens/slashes/dots) with hyphens
        part = re.sub(r'[^a-z0-9_\-\.]', '-', part)
        part = re.sub(r'-+', '-', part)
        part = part.strip('-')
        slug_parts.append(part)

    return '/'.join(slug_parts)

def parse_gitbook_urls() -> list[str]:
    """
    Extract valid Markdown references from SUMMARY.md and convert them to GitBook URLs.
    
    Returns:
    	list[str]: Sorted, deduplicated GitBook URLs for existing referenced files.
    
    Raises:
    	FileNotFoundError: If SUMMARY.md does not exist.
    """
    summary_path = REPO_ROOT / "SUMMARY.md"
    if not summary_path.exists():
        raise FileNotFoundError(f"SUMMARY.md not found at {summary_path}")

    print(f"Parsing GitBook URLs from {summary_path}...")
    content = summary_path.read_text(encoding="utf-8")

    # Find all Markdown links
    # Matches [Anchor](path.md)
    matches = re.findall(r'\[[^\]]+\]\(([^)]+\.md)\)', content)

    gitbook_urls = []
    for raw_path in matches:
        # Decode path spaces/special characters
        decoded_path = urllib.parse.unquote(raw_path.strip())
        file_path = REPO_ROOT / decoded_path

        if not file_path.exists():
            print(f"WARNING: File referenced in SUMMARY.md does not exist: {decoded_path}")
            # Ensure "Make sure no broken links" constraint by checking and skipping or raising.
            # We want to be strict, but let's confirm if there are any actually missing files first.
            continue

        slug = to_gitbook_slug(raw_path.strip())
        if slug == "":
            url = GITBOOK_BASE
        else:
            url = GITBOOK_BASE + slug
        gitbook_urls.append(url)

    print(f"Found {len(gitbook_urls)} GitBook URLs.")
    return sorted(list(set(gitbook_urls)))

def main():
    # 1. Build MkDocs
    """
    Generate unified sitemap and robots files for all discovered site URLs.
    
    The generated files are written to the repository root and `docs/`, and to
    `site/` when that directory exists.
    """
    build_mkdocs()

    # 2. Get GitHub Pages URLs
    gh_urls = parse_github_pages_urls()

    # 3. Generate Read the Docs URLs
    rtd_urls = generate_readthedocs_urls(gh_urls)

    # 4. Parse GitBook URLs
    gb_urls = parse_gitbook_urls()

    # 5. Combine and deduplicate all URLs
    all_urls = sorted(list(set(gh_urls + rtd_urls + gb_urls)))
    print(f"Total unified URLs discovered: {len(all_urls)}")

    # 6. Generate sitemap.txt content
    txt_content = "\n".join(all_urls) + "\n"

    # 7. Generate sitemap.xml content
    today = datetime.date.today().isoformat()
    # In DSOM, the date anchor is set to 2026. Let's use 2026-08-08 or today's year normalized to 2026
    # if it's currently 2026, or use current system date.
    # To keep it consistent, let's use datetime.date.today().isoformat()

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for url in all_urls:
        xml_lines.append('    <url>')
        xml_lines.append(f'        <loc>{url}</loc>')
        xml_lines.append(f'        <lastmod>{today}</lastmod>')
        xml_lines.append('    </url>')
    xml_lines.append('</urlset>\n')
    xml_content = "\n".join(xml_lines)

    # 8. Generate robots.txt content
    robots_content = f"""User-agent: *
Allow: /

Sitemap: {GITHUB_PAGES_BASE}sitemap.xml
Sitemap: {READTHEDOCS_BASE}sitemap.xml
"""

    # 9. Define all target locations
    targets = {
        "sitemap.txt": txt_content,
        "sitemap.xml": xml_content,
        "robots.txt": robots_content
    }

    # Write to Root, docs/, and site/ (build output)
    for filename, content in targets.items():
        # Root
        root_path = REPO_ROOT / filename
        root_path.write_text(content, encoding="utf-8")
        print(f"Wrote {filename} to root directory.")

        # docs/
        docs_path = REPO_ROOT / "docs" / filename
        docs_path.write_text(content, encoding="utf-8")
        print(f"Wrote {filename} to docs/ directory.")

        # site/
        site_path = REPO_ROOT / "site" / filename
        if (REPO_ROOT / "site").exists():
            site_path.write_text(content, encoding="utf-8")
            print(f"Wrote {filename} to site/ directory.")

if __name__ == "__main__":
    main()

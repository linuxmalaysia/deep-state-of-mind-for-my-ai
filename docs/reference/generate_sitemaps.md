---
okf_version: 0.2
type: documentation
title: "Reference: generate_sitemaps.py"
timestamp: "2026-08-13T12:00:00Z"
topics: ["dsom", "reference", "sitemaps", "seo"]
resource: "/docs/reference/generate_sitemaps.md"
sources: [{author: Harisfazillah Jamel (LinuxMalaysia), id: dsom-core-spec, resource: /docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md,
  title: Deep State of Mind (DSOM) Governance Architecture, type: architecture_spec}, {author: Google Cloud Platform, id: google-okf-v02-spec, resource: 'https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md',
  title: Google Cloud Open Knowledge Format (OKF) v0.2 Specification, type: external_spec}]
spec_version: "0.2"
---
# generate_sitemaps.py reference

Dynamic, unified sitemap and search engine optimiser (SEO) asset generator.

## Description

The `generate_sitemaps.py` utility builds the MkDocs static site. It compiles URLs across **GitHub Pages**, **Read the Docs**, and **GitBook** and outputs sitemaps and robots rules.

## Script path

`tools/generate_sitemaps.py`

## CLI signature

```bash
uv run python tools/generate_sitemaps.py

```

## Inputs

- **site/sitemap.xml:** Compiled sitemap parsed to discover fresh GitHub Pages web paths.
- **SUMMARY.md:** GitBook navigation parsed to identify all valid internal markdown resources.

## Outputs

Unified assets exported to three targets: root directory `./`, `docs/`, and built `site/`:
- **sitemap.txt:** Plaintext listing of all consolidated indexing URLs.
- **sitemap.xml:** Standard XML sitemap with synchronised `<lastmod>` tags.
- **robots.txt:** Robot guidelines mapping rules pointing directly to the sitemaps.

## Dependencies

- **Python:** 3.12+ (managed through standard `uv` environment).
- **mkdocs-material:** Static site generator package.
- **pyyaml:** Standard YAML parser.

## Internal Python API

### `find_repo_root()`

Locates the repository root by detecting the nearest `.git` ancestor.
- **Returns:** `pathlib.Path` pointing to root.
- **Raises:** `RuntimeError` if `.git` cannot be resolved.

### `build_mkdocs()`

Triggers compilation of static HTML site files.
- **Command executed:** `uv run --with mkdocs-material mkdocs build`.

### `parse_github_pages_urls()`

Parses the generated `site/sitemap.xml` XML structure.
- **Returns:** Sorted list of GitHub Pages string URLs.

### `to_gitbook_slug(path_str)`

Converts raw Markdown file paths to URL-safe lower-case slugs.
- **Arguments:** `path_str` (string relative markdown file path).
- **Returns:** String normalised GitBook URL slug.


---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-14*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*

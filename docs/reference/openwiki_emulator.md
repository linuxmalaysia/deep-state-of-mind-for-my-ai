---
okf_version: 0.1
type: documentation
title: "Reference: openwiki_emulator.py"
timestamp: "2026-08-13T12:00:00Z"
topics: ["dsom", "reference", "openwiki", "emulator"]
---
# openwiki_emulator.py reference

Zero-binary, pure Python CLI tool emulating the OpenWiki documentation environment.

## Description

The `openwiki_emulator.py` script replaces external Node.js binaries and cloud APIs with localised, offline execution. It compiles 9 markdown wiki pages, repairs Mermaid schemas, and exports an interactive graph visualiser.

## Script path

`tools/openwiki_emulator.py`

## CLI options

```bash
# Initialize and compile the full OpenWiki workspace (default action)
uv run python tools/openwiki_emulator.py --init

# Retrieve recent Git changes and update context history
uv run python tools/openwiki_emulator.py --update

# Perform search against OpenWiki YAML metadata
uv run python tools/openwiki_emulator.py --search "ansible"

# Export a standalone offline HTML interactive knowledge graph
uv run python tools/openwiki_emulator.py --export-graph
```

## Inputs

- **Git status:** System porcelain variables used to determine modified workspace files.
- **Planned pages map:** Hardcoded schemas defining initial wiki content and layouts.

## Outputs

All workspace files created inside `./openwiki/`:
- **INSTRUCTIONS.md:** Standard CLI operating procedures and rules.
- **_skeleton.md:** Ranking matrices and structural subsystems mapping.
- **graph.html:** Interactive standalone knowledge visualization layout.
- **quickstart.md / architecture / automation / memory:** Structured markdown documents.
- **.last-update.json:** Dynamic JSON execution tracker log.

## Dependencies

- **Python:** 3.12+ (standard `uv` environment).
- **pyyaml:** YAML data loading engine.

## Internal Python API

### `validate_mermaid_diagram(code)`

Validates Mermaid diagram layout syntax, bracket matches, and unescaped quotes.
- **Arguments:** `code` (raw string of the diagram block).
- **Returns:** `(bool, reason)` tuple representing valid status and description.

### `process_markdown_file(filepath)`

Scans a markdown file, detects corrupted or plain code fences, and repairs them.
- **Arguments:** `filepath` (absolute target file `pathlib.Path`).
- **Mechanism:** Degrades blocks in place with errors; heals corrected blocks back to active schemas.

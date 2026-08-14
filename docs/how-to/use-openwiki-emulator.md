---
okf_version: 0.1
type: documentation
title: "How-To: Operate the OpenWiki Emulator"
timestamp: "2026-08-13T12:00:00Z"
topics: ["dsom", "how-to", "openwiki", "emulator"]
---
# Operate the OpenWiki emulator

This guide explains how to initialise, update, and query the local OpenWiki documentation and knowledge graph.

## Prerequisites

- **Python 3.12+** and **`uv`** must be configured.
- **`pyyaml`** dependency is required.

## Step 1: Initialise the wiki directory

Recompile standard directories, create index skeletons, self-heal Mermaid diagrams, and export standalone interactive HTML graphs:

```bash
uv run --with pyyaml python tools/openwiki_emulator.py --init
```

## Step 2: Query metadata from terminal

Use the search command to perform fast frontmatter variable checks on compiled wiki pages:

```bash
uv run --with pyyaml python tools/openwiki_emulator.py --search "ansible"
```

## Step 3: Sync changes from Git history

Before saving and finalizing work, pull updated Git changes into the wiki logs and refresh indices:

```bash
uv run --with pyyaml python tools/openwiki_emulator.py --update
```

## Step 4: Run diagram validation tests

Verify standard self-healing logic and schema parsing engines using unit tests:

```bash
uv run --with pyyaml --with pytest pytest tests/test_openwiki_emulator.py
```


---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-14*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*

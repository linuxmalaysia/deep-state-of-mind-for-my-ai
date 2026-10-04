---
okf_version: 0.2
type: documentation
title: "How-To: Check and Apply OKF Compliance"
timestamp: "2026-08-13T12:00:00Z"
topics: ["dsom", "how-to", "okf", "compliance"]
resource: "/docs/how-to/audit-and-apply-frontmatter.md"
sources: [{author: Harisfazillah Jamel (LinuxMalaysia), id: dsom-core-spec, resource: /docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md,
  title: Deep State of Mind (DSOM) Governance Architecture, type: architecture_spec}, {author: Google Cloud Platform, id: google-okf-v02-spec, resource: 'https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md',
  title: Google Cloud Open Knowledge Format (OKF) v0.2 Specification, type: external_spec}]
spec_version: "0.2"
---
# Check and apply OKF compliance

This guide explains how to audit, standardise, and auto-correct Markdown files to ensure compliance with the **Open Knowledge Format (OKF v0.1)**.

## Prerequisites

- **Python 3.12+** and **`uv`** must be installed on your environment.
- **`pyyaml`** dependency is required.

## Step 1: Scan and standardise directory frontmatter

Run the `apply_okf_frontmatter.py` tool pointing directly to your documentation folder. This script automatically injects the five required frontmatter variables (`okf_version`, `type`, `title`, `timestamp`, `topics`) and strips Byte Order Marks (BOM).

```bash
uv run --with pyyaml python tools/apply_okf_frontmatter.py docs/

```

## Step 2: Batch re-order metadata fields

To format skill schemas or re-align metadata ordering (placing `topics` immediately after `description` in skill documents), use the `refactor_okf.py` tool.

### Dry run check

Verify planned modifications without making changes on disk:

```bash
uv run --with pyyaml python tools/refactor_okf.py docs/ --dry-run

```

### In-place execution

Apply standard formatting and reordering rules atomically:

```bash
uv run --with pyyaml python tools/refactor_okf.py docs/

```

## Step 3: Verify the output

To confirm that the changes were executed successfully and no Byte Order Marks remain, use the standard test suite:

```bash
uv run --with pyyaml --with pytest pytest tests/test_okf_frontmatter_bom_reorder.py

```

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-14*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*

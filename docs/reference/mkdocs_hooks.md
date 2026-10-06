---
okf_version: 0.2
type: documentation
title: "Reference: mkdocs_hooks.py"
timestamp: "2026-08-13T12:00:00Z"
topics: ["dsom", "reference", "mkdocs", "hooks"]
resource: "/docs/reference/mkdocs_hooks.md"
sources: [{author: "Harisfazillah Jamel (LinuxMalaysia)", id: dsom-core-spec, resource: "/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md", title: "Deep State of Mind (DSOM) Governance Architecture", type: architecture_spec, url: "https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai/blob/main/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md"}, {author: Google Cloud Platform, id: google-okf-v02-spec, resource: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md", title: "Google Cloud Open Knowledge Format (OKF) v0.2 Specification", type: external_spec, url: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md"}]
status: stable
generated: {by: "agent/dsom-subagent-01", timestamp: "2026-08-13T12:00:00Z"}
stale_after: "2027-01-01"
spec_version: "0.2"
concept_id: mkdocs_hooks
---
# mkdocs_hooks.py reference

Custom MkDocs page compilation hook for relative Markdown URL rewriting.

## Description

The `mkdocs_hooks.py` script intercepts static pages during compilation. It strips unnecessary `docs/` prefixes and normalises repository-root relative paths (`../../` to `../`), ensuring links work seamlessly on both GitHub.com and built HTML servers.

## Script path

`tools/mkdocs_hooks.py`

## CLI integration

Automated by the static site compiler. Registered inside `mkdocs.yml`:

```yaml
hooks:
  - tools/mkdocs_hooks.py

```

## Functions

### `on_page_markdown(markdown, page, config, files)`

Interceptors registered by the MkDocs lifecycle.
- **Arguments:** `markdown` content (string), `page` metadata, `config` context, `files` collection.
- **Returns:** Modified Markdown string with rewritten relative URLs.

## Rewriting rules

- **External links:** Keeps `http://`, `https://`, `mailto:`, `ftp:`, and `#` anchor links unchanged.
- **`docs/` prefix:** Strips `docs/` from relative paths (e.g. `docs/governance/PROTOCOL.md` becomes `governance/PROTOCOL.md`).
- **`../../` prefix:** Normalises double-parent directories (e.g. `../../AGENTS.md` becomes `../AGENTS.md`).


---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-14*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*

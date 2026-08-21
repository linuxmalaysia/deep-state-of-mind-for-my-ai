---
okf_version: 0.2
type: documentation
title: "Open Knowledge Format (OKF) Adoption Guide: The Foundational Context Engine for DSOM"
timestamp: "2026-08-20T23:00:00Z"
topics: ["okf", "dsom", "documentation", "context-engineering", "progressive-disclosure", "llm-wiki"]
description: "The authoritative guide for human engineers and AI agents to understand, implement, and adopt the Open Knowledge Format (OKF v0.1 & v0.2) within the Deep State of Mind (DSOM) protocol."
resource: "file:///docs/OKF-ADOPTION-GUIDE.md"
sources: ["https://cloud.google.com/blog/products/databases/announcing-open-knowledge-format-for-gen-ai", ".agents/AGENTS.md"]
generated: "google-antigravity"
verified: true
status: "approved"
stale_after: "2027-08-20T00:00:00Z"
---

# 🌐 Open Knowledge Format (OKF) Adoption Guide: The Foundational Context Engine for DSOM

## Executive Summary & Core Concept

Introduced by Google Cloud’s Data Cloud team in June 2026, the **Open Knowledge Format (OKF)** is an open, vendor-neutral specification designed to resolve the fundamental "context problem" in autonomous AI agent systems.

Historically, AI agents struggle when deployed in real-world software and infrastructure engineering environments because institutional knowledge—such as system runbooks, database schemas, architectural decision records (ADRs), and operational playbooks—is fragmented across disparate wikis, databases, ticketing platforms, and code comments. Traditional Retrieval-Augmented Generation (RAG) attempts to bridge this gap by slicing raw text into floating-point vector embeddings. However, RAG is stateless, computationally expensive, subject to vector collision, and prone to severe attention dilution (the "lost-in-the-middle" phenomenon) within large language model (LLM) context windows.

OKF formalises the **"LLM-wiki" paradigm** into a standardised, Git-native representation. Rather than introducing proprietary runtimes, complex database schemas, or heavy binary SDKs, OKF represents curated organisational knowledge as a structured directory of UTF-8 Markdown files initialised with semantic YAML frontmatter.

---

## 🚀 Why OKF is the Core Engine that Makes DSOM Work & Fast

The **Deep State of Mind (DSOM)** protocol relies on OKF as its primary context engineering standard. OKF transforms passive documentation into an active, machine-readable **Spatial Memory Palace** (`.agents/brain/` and `.agents/skills/`), delivering four critical performance advantages:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                      Sovereign AI Workspace (DSOM)                      │
│                                                                         │
│  ┌───────────────────────┐                    ┌──────────────────────┐  │
│  │   Spatial Memory      │                    │  Agent Skill Library │  │
│  │   (.agents/brain/)    │                    │   (.agents/skills/)  │  │
│  │  YAML Frontmatter +   │                    │   YAML Frontmatter + │  │
│  │  Markdown Closets     │                    │   Executable SOPs    │  │
│  └───────────┬───────────┘                    └──────────┬───────────┘  │
│              │                                           │              │
│              └─────────────────────┬─────────────────────┘              │
│                                    ▼                                    │
│                    ┌───────────────────────────────┐                    │
│                    │     OKF Frontmatter Index     │                    │
│                    │    (okf_version, type, title, │                    │
│                    │     timestamp, topics, etc.)  │                    │
│                    └───────────────┬───────────────┘                    │
│                                    │                                    │
│       ┌────────────────────────────┼────────────────────────────┐       │
│       ▼                            ▼                            ▼       │
│  ┌───────────────┐          ┌───────────────┐          ┌───────────────┐│
│  │ Progressive   │          │ Zero-Loss     │          │ Multi-Agent   ││
│  │ Disclosure    │          │ Reanimation   │          │ MCP Server    ││
│  │ (~98% Token   │          │ (Instant      │          │ (FastMCP /    ││
│  │ Compression)  │          │ Re-alignment) │          │ OpenWiki)     ││
│  └───────────────┘          └───────────────┘          └───────────────┘│
└─────────────────────────────────────────────────────────────────────────┘
```

### 1. Project Target: 98%+ Token & Cost Compression Ratio
Loading raw source code, exhaustive database dumps, or thousands of lines of unformatted documentation into an LLM prompt consumes hundreds of thousands of context tokens, draining API budgets and degrading reasoning quality. In DSOM, OKF YAML frontmatter allows AI agents to scan lightweight metadata blocks (~50 tokens per file) to locate exact information before selectively reading deep content. As an engineering target, this compresses initial prompt overhead by over 98%.

### 2. Progressive Disclosure via Directory Index Routers
Instead of dumping an entire repository into active memory, OKF uses hierarchical `index.md` files at directory roots. An AI agent reads the root `index.md` first to build a topographical map of available domains, traversing deeper into specific concept files only when required for immediate execution.

### 3. Zero-Loss Persistent Memory & Instant Reanimation
By maintaining session walkthrough anchors (`task.md`, `walkthrough.md`, `palace_registry.md`) structured with OKF frontmatter, AI digital twins (such as Google Jules, Google Antigravity, Claude, and Copilot) reanimate instantly with full historical mental state across chat session resets or machine reboots.

### 4. The Artifact Pyramid & Zero-Cost Context Prediction
OKF knowledge bundles in DSOM stratify knowledge into an ontological pyramid:
* **Layer 1 (L1) - Strategic Synthesis:** High-level executive summaries and operational playbooks (for Orchestrator agents).
* **Layer 2 (L2) - Focused Analysis:** Deep domain-specific investigations and architecture maps (for Worker agents).
* **Layer 3 (L3) - Raw Dossiers:** Unaltered transcripts, raw telemetry, and code references (for Validator agents).

To enable zero-cost context prediction, every L1 and L2 document appends a structured `SOURCES` block at the bottom of its Markdown body, pairing Markdown links with single-line target descriptions. This allows agents to evaluate relevance without triggering additional filesystem reads.

---

## 📋 OKF Technical Specification & Conformance Rules

### OKF v0.1 Core Frontmatter Fields

Every non-reserved Markdown concept document inside an OKF knowledge bundle MUST begin with a valid YAML frontmatter block enclosed by triple dashes (`---`) at line 1, column 1. Note that DSOM enforces a specific OKF profile requiring mandatory `okf_version`, `type`, `title`, `timestamp`, and `topics` fields.

| Field | Type | Required in DSOM Profile? | Description / Example |
| :--- | :--- | :--- | :--- |
| `okf_version` | `float` / `string` | **Yes** | Specification version (e.g., `0.1` or `"0.1"`). |
| `type` | `string` | **Yes** | Semantic document category (`agent_skill`, `documentation`, `governance_protocol`, `architecture_concept`, `system_audit`). |
| `title` | `string` | **Yes** | Human- and machine-readable title of the document. |
| `timestamp` | `string` | **Yes** | ISO 8601 UTC timestamp of creation or last major revision (`"2026-08-20T23:00:00Z"`). |
| `topics` | `list[string]` | **Yes** | Array of lower-case semantic tags for zero-cost discovery (`["dsom", "okf", "governance"]`). |
| `description` | `string` | Optional | Concise 1-2 sentence summary used for semantic routing and LLM discovery. |
| `resource` | `string` | Optional | Canonical URI or file path identifier (`"file:///docs/OKF-ADOPTION-GUIDE.md"`). |

### Frontmatter Invariants & Formatting Rules

1. **Line 1 Column 1 Invariant:** The opening `---` fence MUST start at byte index 0 (no Byte Order Mark / BOM, no leading whitespace or newlines).
2. **Key Ordering & Field Placement:** The first three keys MUST always be `okf_version`, `type`, and `title`, followed by `timestamp`, `topics`, `description`, and `resource`. In skill files processed by compliance scripts, `topics` immediately follows `description` or `timestamp`.
3. **Quoting Rules for YAML Special Characters:** String values containing colons (`:`), brackets (`[`/`]`), braces (`{`/`}`), commas (`,`), emojis, or timestamps MUST be double-quoted (e.g. `title: "Open Knowledge Format (OKF) Guide"`).
4. **Preservation of Raw Timestamps:** Compliance tools like `tools/apply_okf_frontmatter.py` utilize PyYAML custom loaders (`CustomLoader`) to preserve raw string timestamps without converting them into native Python `datetime` objects.

### Reserved Filenames

The OKF specification reserves two explicit filenames at any hierarchical directory level:
* **`index.md`:** Serves as a directory router and progressive disclosure listing. It contains no frontmatter (except the bundle-root `index.md`, which MAY declare `okf_version: "0.1"`).
* **`log.md`:** Maintains a chronological ledger of updates organized in reverse-chronological order under ISO 8601 date headings (e.g., `## 2026-08-20`).

### OKF v0.2 Trust Signals & Provenance Profile

OKF v0.2 extends v0.1 by adding opt-in trust and provenance metadata fields in YAML frontmatter to allow autonomous agents to verify agent-generated content:
* `sources`: Array of origin URLs or relative paths (`["docs/governance/AI-MASTER-PROTOCOL.md"]`).
* `generated`: ISO 8601 timestamp or agent ID that generated the document.
* `verified`: Verification status (`true` / `false` / ISO timestamp).
* `status`: Lifecycle state (`draft`, `approved`, `deprecated`).
* `stale_after`: ISO 8601 date indicating when the context must be re-validated.

---

## 🛠️ Step-by-Step OKF Adoption Guide for Humans & AI Agents

Follow this 6-step SOP to adopt OKF across any new or existing codebase:

### Step 1: Establish Knowledge Bundle Structure
Organise knowledge assets into distinct, logical directories alongside source code:
```text
.agents/
├── brain/                   <-- Spatial Memory Palace (okf_version: 0.1)
│   ├── index.md             <-- Directory Router
│   ├── log.md               <-- Chronological Update Ledger
│   └── wings/               <-- Domain Closets
└── skills/                  <-- Executable Agent Capabilities (type: agent_skill)
    ├── index.md
    └── okf-frontmatter-injector/
        └── SKILL.md
```

### Step 2: Inject & Audit OKF Frontmatter
Run the automated compliance tool across your target documentation directory:
```bash
# Execute native Python OKF frontmatter injector
uv run python tools/apply_okf_frontmatter.py docs/

# Or invoke the agent skill script directly
python .agents/skills/okf-frontmatter-injector/scripts/apply_okf.py .
```

### Step 3: Implement Progressive Disclosure Directory Routers
Place an `index.md` file in each major subdirectory to list concept files and their descriptions:
```markdown
# Database Schemas Directory

* [orders.md](orders.md) - Orders table schema and relational joins.
* [customers.md](customers.md) - Customer profile definitions and GDPR compliance constraints.
```

### Step 4: Record Chronological Change History in `log.md`
When an AI agent or developer modifies knowledge nodes, append an entry to `log.md`:
```markdown
# Knowledge Bundle Change Log

## 2026-08-20
* **Updated:** `docs/OKF-ADOPTION-GUIDE.md` - Integrated deep research and OKF v0.2 trust signals.
```

### Step 5: Enforce OKF in CI/CD Workflows
Integrate automated OKF compliance testing into your GitHub Actions workflow (`.github/workflows/docs-ci.yml`):
```yaml
- name: Verify OKF Frontmatter Compliance
  run: |
    uv run python tools/apply_okf_frontmatter.py docs/
    git diff --exit-code -- docs/
```

### Step 6: Connect OKF to FastMCP & Native OpenWiki
Bridge your OKF knowledge graph directly to AI clients (Cursor, Claude Desktop, VSCode) via DSOM's FastMCP server:
```bash
# Start DSOM FastMCP Server
uv run tools/mcp/server.py

# Query OpenWiki Knowledge Graph
uv run python tools/openwiki_emulator.py --search "OKF"
```

---

## 💡 Concrete Code Examples & YAML Templates

### Example 1: OKF Agent Skill (`.agents/skills/audit-cluster/SKILL.md`)
```yaml
---
okf_version: 0.1
type: agent_skill
title: audit-cluster-health
timestamp: "2026-08-20T12:00:00Z"
description: "Executes cluster health diagnostics and extracts node telemetry."
topics: ["infrastructure", "telemetry", "health-check"]
resource: "file:///.agents/skills/audit-cluster/SKILL.md"
---

# 🔍 Cluster Health Audit Skill

## Instructions
1. Run diagnostic script: `tools/audit-pre-flight.sh`
2. Verify output and report status to user.
```

### Example 2: Spatial Memory Closet (`.agents/brain/wings/room_tooling/closet.md`)
```yaml
---
okf_version: 0.1
type: architecture_concept
title: "Room Tooling Memory Closet"
timestamp: "2026-08-20T14:30:00Z"
description: "Archived operational state for DSOM tooling scripts."
topics: ["tooling", "python", "automation", "memory-palace"]
resource: "file:///.agents/brain/wings/room_tooling/closet.md"
---

# Room Tooling Distillation
This closet tracks the execution parameters of `tools/openwiki_emulator.py` and `tools/generate_sitemaps.py`.
```

---

## 🧪 Verification & Testing

Verify that your repository maintains complete OKF compliance and zero broken links by running the full test suite and relative link validator:

```bash
# Run full pytest suite including OKF compliance tests
uv run --with pytest --with pyyaml --with mcp==1.2.1 --with fastmcp --with pydantic-settings python -m pytest

# Validate relative documentation links across Diátaxis docs
uv run python tools/check_docs_links.py
```

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-20*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*

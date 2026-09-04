---
okf_version: 0.2
type: "skill"
title: "Technical Ebook & Handbook Compiler (Pandoc / Print & Terminal Theme)"
timestamp: "2026-09-03T07:30:00Z"
description: "Compiles complete Diataxis documentation suites and source code repositories into publication-grade technical handbooks (PDF, standalone HTML, EPUB, ODT) using Pandoc and the Terminal & Cloud design framework."
topics: ["pandoc", "ebook", "pdf", "html", "epub", "terminal-theme"]
status: "stable"
stale_after: "2027-09-03"
sources:
  - id: "dsom_agents_rulebook"
    title: "The Core AI Rulebook (DSOM Rule 11 & Rule 22)"
    path: ".agents/AGENTS.md"
name: "dsom-technical-book-compiler"
---

# Technical Ebook & Handbook Compiler

**Purpose:** Standardizes the automated compilation of complex multi-part Diátaxis documentation palaces and complete source code directories into unified, publication-grade technical handbooks (PDF, HTML, EPUB, ODT) tailored for SysAdmins, DevOps Engineers, and SREs.

## Dual-Mode "Terminal & Cloud" Design System
1. **Interactive / Screen Mode:** Optional dark slate container (#0F172A) for code and off-white (#F8FAFC) reading background.
2. **Physical Print / PDF Handbook Mode (Zero Ink Waste):**
   - **Pure White Background:** `@page { background: #FFFFFF; }` and `body { background-color: #FFFFFF !important; }` to eliminate grayish tints and toner waste.
   - **Light Code Blocks:** Code containers use `#F8FAFC` light gray with `#CBD5E1` border, dark text (`#0F172A`), and high-contrast dark syntax highlighting (Pandoc `tango`). Black or solid dark containers are strictly forbidden.
   - **Light Pastel Callouts:** Soft pastel backgrounds (`#FEF2F2` for warnings, `#F0F9FF` for notes, `#F0FDF4` for tips) with colored left borders.
   - **Full Confidentiality Statement:** Must be written as `Private And Confidential (P&C)` (uppercase `PRIVATE AND CONFIDENTIAL (P&C)` in running headers).
   - **Attribution Standard:** Compilations must be credited as `Compile by: Harisfazillah Jamel`.

## Technical Execution Constraints
1. **Footer & Frontmatter Stripping:** Individual OKF frontmatter and DSOM signature footers must be stripped across all multi-document builds to prevent Pandoc YAML parser collisions (`Unknown alias`).
2. **Dynamic Backtick Fence Scaling:** When wrapping source code containing triple backticks (` ``` `), the enclosing fence must scale dynamically to 4 or 5 backticks (` ```` `).
3. **Mermaid HTML Unescaping Protocol:** Pandoc automatically escapes HTML entities inside `<pre class="mermaid"><code>` (`&quot;`, `&lt;br/&gt;`, `--&gt;`). The compilation pipeline must decode these entities before browser rendering to prevent Mermaid 10 syntax error bomb graphics.
4. **Standalone Cover Body Inclusion:** Never embed raw HTML covers inside Markdown files. Generate a standalone `cover.html` passed via `--include-before-body=cover.html`. Enforce `.cover-title { break-before: avoid !important; }` and `#title-block-header { display: none !important; }` to prevent cover fragmentation.
5. **Anti-Blank Page Discipline:** Never mix manual `<div class="page-break"></div>` tags with CSS `page-break-before: always;`.
6. **Headless Browser PDF Timeout:** Headless Chromium/Edge (`--headless=new --print-to-pdf`) renders CSS `@page` layouts, vector SVGs, and web fonts. A process timeout guardrail (45–60s) must be enforced.
7. **Mermaid Multi-Diagram Isolation Protocol:**
   - *Diagram-Scoped Namespace:* Prohibit reusing identical node IDs (e.g., `NODE1`, `CBE`, `PWP`) across diagrams. Prefix all node IDs with a unique diagram namespace (e.g., `TB_`, `PA_`, `PB_`, `PC_`) to prevent global symbol collisions.
   - *Sequential Headless DOM Replacement:* Headless Chromium renders in milliseconds, causing default `mermaid.run()` timestamp IDs (`Date.now()`) to collide and nest diagrams inside one container. Mandate sequential rendering via `mermaid.render(id, code)` with unique IDs (`diagram_svg_${i}`) replacing `<pre class="mermaid">` innerHTML sequentially.
8. **Soft-Path Link Resolution Mandate (3-Tier Normalisation):** The compilation pipeline must dynamically map all chapters (`#chap-{slug}`) and ingested code blocks (`#code-{slug}`) and rewrite all markdown links via a **3-tier normalisation pipeline**: (1) *Exact match* — look up the raw target in `link_map` as-is; (2) *Normalised match* — strip `file:///`, Windows drive letters (`D:/`, `C:/`), the project root prefix, and the `build/` intermediate directory prefix, then retry; (3) *Basename-only match* — strip all directory components and retry with the filename only (skipping external-scheme targets and rejecting ambiguous duplicate basenames). Pre-index basename-only keys into `link_map` before rewriting. Preserve `#fragment` suffixes across all tiers. Run a post-compile link audit asserting zero absolute path leaks (`D:/`, `C:/`, `file:///`, `build/` prefixes) survive in any PDF, HTML, EPUB, or ODT link target.
9. **Full-Spectrum Code Ingestion:** Ingest all production playbooks, Jinja2 templates, inventories, host/group variables, shell scripts, and candidate staging playbooks into dedicated book chapters to produce self-contained handbooks.
10. **Developer Commentary Extraction Protocol:** For every YAML playbook, shell script, or INI file ingested, extract the leading `#` comment block (all contiguous comment lines before the first YAML key, after the `---` fence) and render it as an HTML callout div above the code fence. Classify by keyword scan: comments containing `BUG`, `FIX`, `Confirmed`, `live`, `vendor`, `NEVER`, `destroy`, `destructive`, `ORA-\d+`, `crash`, `escalation`, or `hard way` render as `callout-warning` (⚠️ orange, label `Read Before Executing`); all others render as `callout-note` (💡 blue). Preserve original `#` lines inside the code fence unchanged. CSS must define `.callout-warning p`, `.callout-note p`, and `strong` selectors with explicit `padding: 12px 16px` and `page-break-inside: avoid` for clean print rendering.

## Execution Command
```bash
uv run python .agents/skills/dsom-technical-book-compiler/scripts/compile-book.py
```

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-09-03*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*

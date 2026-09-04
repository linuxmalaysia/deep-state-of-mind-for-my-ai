---
okf_version: 0.2
type: "governance"
title: "Technical Book Design & PDF Compilation Master Prompt Guide"
timestamp: "2026-09-04T21:15:00Z"
topics: ["pandoc", "pdf", "handbook", "prompt", "print-optimized", "mermaid", "ebook", "diataxis"]
description: "Master operational prompt and technical blueprint for compiling multi-file Markdown documentation suites into publication-grade, print-optimized PDF, HTML, EPUB, and ODT handbooks using Pandoc, Headless Chromium, and the Terminal & Cloud design framework."
status: "stable"
stale_after: "2027-09-04"
sources:
  - id: "dsom_agents_rulebook"
    title: "The Core AI Rulebook (DSOM Rule 11 & Rule 22)"
    path: ".agents/AGENTS.md"
  - id: "dsom_technical_book_compiler_skill"
    title: "Technical Ebook & Handbook Compiler Skill"
    path: ".agents/skills/dsom-technical-book-compiler/SKILL.md"
  - id: "build_mcmc_ansible_book_script"
    title: "MCMC Ansible Book Compiler Implementation"
    path: "tools/build_mcmc_ansible_book.py"
generated:
  by: "Antigravity Cognitive Digital Twin"
  timestamp: "2026-09-04T21:15:00Z"
verified:
  by: "Harisfazillah Jamel (LinuxMalaysia)"
  timestamp: "2026-09-04T21:15:00Z"
---

# Technical Book Design & PDF Compilation Master Prompt Guide

> **Document Type:** Governance Blueprint & Reusable AI Master Prompt
> **Classification:** Private And Confidential (P&C)
> **Attribution:** Compile by: Harisfazillah Jamel
> **Standard:** Terminal & Cloud Technical Ebook & Handbook Standard (DSOM Rule 11 & Rule 22)

---

## 1. Executive Overview & Dual Purpose

This document serves two complementary functions:
1. **The Reusable AI Master Prompt (Section 2):** A complete, drop-in system prompt that can be provided to any advanced AI coding assistant (Google Antigravity, Google Jules, Claude, Cursor, ChatGPT) to autonomously orchestrate, style, and compile an entire repository of multi-file Markdown (`.md`) documentation and source code into a publication-grade PDF handbook.
2. **The Architectural Blueprint & Engineering Field Manual (Sections 3–7):** An exhaustive technical record documenting the formatting standards, color palettes, typography pairings, CSS `@page` rules, and the **ten critical engineering hurdles** solved to eliminate syntax crashes, blank pages, link leaks, and ink waste during multi-format compilation (PDF, standalone HTML, EPUB 3, and styled ODT).
3. **The Embedded Skill SOP (Section 6):** The full operational specification of the `dsom-technical-book-compiler` skill, ensuring complete self-containment.

---

## 2. The Reusable AI Master Prompt

*Copy and paste the entire block below into your AI prompt window or agent instruction set:*

```markdown
You are a Principal Publication Systems Architect and Pandoc Book Engineering Specialist.
Your task is to take an entire repository of Markdown (.md) documents and source code trees, assemble them into a cohesive, publication-grade technical handbook, and compile them into a print-optimized PDF, standalone interactive HTML, EPUB 3, and styled OpenDocument Text (ODT).

### MANDATORY DESIGN & STYLING SPECIFICATIONS (TERMINAL & CLOUD STANDARD)

1. PRINT-OPTIMIZED PURE WHITE STANDARD (ZERO TONER WASTE):
   - For all PDF and print compilations, dark or black container backgrounds are STRICTLY FORBIDDEN.
   - Base Body Background: Pure White (#FFFFFF !important).
   - Code Blocks (Preformatted): Light Alabaster/Gray (#F8FAFC) with a subtle slate border (1px solid #CBD5E1), dark charcoal text (#0F172A), and high-contrast dark syntax highlighting (Pandoc 'tango' style: Keywords #1E40AF bold, Strings #047857, Comments #64748B italic, Numbers #B45309, Functions #6D28D9).
   - Callout & Alert Boxes: Light pastel containers with high-contrast colored left borders:
     * Critical Warnings & Cautions: Background #FEF2F2, Left Border 5px solid #DC2626, Border 1px solid #FCA5A5, Text #991B1B.
     * Operational Notes & Information: Background #F0F9FF, Left Border 5px solid #0284C7, Border 1px solid #BAE6FD, Text #075985.
     * Pro-Tips: Background #F0FDF4, Left Border 5px solid #16A34A, Border 1px solid #BBF7D0, Text #166534.
     * Chapter Executive Summaries: Background #F8FAFC, Border 1px solid #CBD5E1, Text #334155.

2. TYPOGRAPHY & VISUAL HIERARCHY:
   - Body Text: Clean sans-serif ('Inter', 'Plus Jakarta Sans', or system-ui fallback), 10pt, line-height 1.55, color #0F172A.
   - Code & Terminal Elements: Monospace font ('JetBrains Mono', 'Fira Code', or 'Consolas'), 8.5pt, line-height 1.4.
   - Headings:
     * Book Title (Cover): 22pt bold, Linux Blue (#1E3A8A).
     * Part Headers (H1 .part): 22pt bold, Linux Blue (#1E3A8A), shaded banner #F8FAFC with 8px solid #1E3A8A left bar, page-break-before: always.
     * Chapter Headers (H2): 16pt bold, Linux Blue (#1E3A8A), bottom border 1px solid #E2E8F0.
     * Section Headers (H3): 13pt bold, Deep Ubuntu (#77216F).
     * Sub-section Headers (H4): 11pt semibold, Deep Teal (#0D9488).

3. PAGE LAYOUT & RUNNING HEADERS/FOOTERS:
   - Page Size: A4 (margin: 20mm 15mm 20mm 15mm).
   - Running Header Top-Left: "<Book Title>" (Inter 8pt, #64748B).
   - Running Header Top-Right: "PRIVATE AND CONFIDENTIAL (P&C)" (Inter 8pt bold, #DC2626).
   - Running Footer Bottom-Left: "Compile by: Harisfazillah Jamel" (Inter 8pt, #64748B).
   - Running Footer Bottom-Right: "Page " counter(page) (Inter 8pt bold, #0F172A).

4. STANDALONE COVER PAGE (SINGLE PAGE FIT):
   - Passed to Pandoc via '--include-before-body=cover.html'.
   - Must fit entirely on Page 1 without spilling over.
   - Contain badges: Private And Confidential (P&C) (#FEE2E2), Technology badges (#EFF6FF), Tooling badges (#F0FDF4).
   - Metadata grid: 2-column key-value grid (Architect, Compiler, Audience, Classification, Covenant, Edition).
   - CSS Guard: Hide duplicate Pandoc title header (#title-block-header { display: none !important; }) and prevent cover title page break (.cover-title { break-before: avoid !important; }).

### NON-NEGOTIABLE ENGINEERING PIPELINE CONSTRAINTS

1. FRONTMATTER & FOOTER STRIPPING:
   - Systematically strip individual YAML frontmatter (lines between leading '---' fences) and individual document signature footers from every ingested .md file to prevent Pandoc YAML parser crashes ('Unknown alias').
   - Extract 'title' and 'description' from frontmatter: convert description into an executive summary callout box above the chapter body.

2. DYNAMIC BACKTICK SCALING:
   - When ingesting code files containing triple backticks (```), dynamically scale the outer markdown fence to 4 or 5 backticks (```` or `````) to prevent premature block closure.

3. ANTI-BLANK PAGE DISCIPLINE:
   - Never combine manual HTML page break tags ('<div class="page-break"></div>') with CSS 'page-break-before: always;'. Use CSS classes exclusively on H1/Part elements.

4. MERMAID MULTI-DIAGRAM ISOLATION PROTOCOL:
   - Diagram-Scoped Namespaces: Reusing identical node IDs (e.g. NODE1, DB, GATEWAY) across diagrams is strictly prohibited. Prefix all node IDs within each diagram with a unique diagram namespace (e.g. TB_, PA_, PB_, PC_) to eliminate global SVG node collisions.
   - Sequential DOM Replacement: Never rely on 'mermaid.run()' which causes millisecond timestamp collisions in headless Chromium. Render diagrams sequentially via 'mermaid.render("diagram_svg_" + i, code)' into unique containers.
   - Entity Unescaping Pipeline: Unescape '&quot;', '&lt;', '&gt;', '&amp;' inside '<pre class="mermaid">' blocks before rendering, and extract 'innerHTML' (not 'textContent') to preserve stacked card line breaks.
   - Balanced Flowchart Architecture: Prevent tall vertical flowchart towers (height > 600px) that cause blank page overflows. Split complex diagrams into balanced 2-column or orthogonal grid layouts.

5. SOFT-PATH INTERNAL LINK RESOLUTION MANDATE (3-TIER NORMALISATION):
   - Pre-index all chapters ('#chap-{slug}') and ingested code blocks ('#code-{slug}') into an internal anchor dictionary.
   - Rewrite all markdown links using a 3-tier normalisation lookup:
     * Tier 1 (Exact Match): Check raw relative path against dictionary.
     * Tier 2 (Normalised Match): Strip 'file:///', Windows drive letters ('C:/', 'D:/'), project root prefix, and 'build/' prefix, then check dictionary.
     * Tier 3 (Basename-Only Match): Strip all parent directories and check dictionary by filename only.
     * Preserve '#fragment' anchor jumps across all three tiers.
   - Post-Compile Audit: Assert zero absolute path leaks ('D:/', 'C:/', 'file:///') survive in compiled PDF/HTML links.

6. DEVELOPER COMMENTARY EXTRACTION PROTOCOL:
   - For every ingested Ansible playbook, shell script, or configuration file, parse the leading '#' comment block (contiguous comments before the first active code key).
   - Regex Keyword Scan: If comments contain keywords ('BUG', 'FIX', 'Confirmed', 'live', 'vendor', 'NEVER', 'destroy', 'destructive', 'ORA-\d+', 'crash', 'escalation', 'hard way'), render a ⚠️ orange warning callout ('callout-warning', 'Developer Commentary — Read Before Executing') ABOVE the code fence. Otherwise, render a 💡 blue note callout ('callout-note', 'Developer Commentary').
   - Keep the original '#' comments inside the code block intact.

7. MULTI-FORMAT COMPILATION SUITE:
   - Step 1: Standalone HTML with embedded Mermaid.js ESM and print CSS.
   - Step 2: Print-to-PDF via Headless Chromium/Edge with '--headless=new --run-all-compositor-stages-before-draw --virtual-time-budget=8000'.
   - Step 3: EPUB 3 with clean table of contents metadata.
   - Step 4: OpenDocument Text (ODT) with custom reference styles for Google Docs/LibreOffice collaboration.
```

---

## 3. Visual Design System: The "Terminal & Cloud" Framework

### 3.1 Color Palette & Contrast Economics

| Role | HEX Code | Print Rationale | CSS Class / Property |
| :--- | :--- | :--- | :--- |
| **Page Background** | `#FFFFFF` | Pure white. Eliminates background shading and toner waste. | `body { background-color: #FFFFFF !important; }` |
| **Body Text** | `#0F172A` | Deep charcoal slate. Maximum contrast against white without harsh black glare. | `color: #0F172A !important;` |
| **Primary Headings** | `#1E3A8A` | Linux Blue. Professional, authoritative enterprise header branding. | `h1, h2 { color: #1E3A8A; }` |
| **Secondary Headings**| `#77216F` | Deep Ubuntu Purple. High-visibility distinction for major subsections. | `h3 { color: #77216F; }` |
| **Tertiary Headings** | `#0D9488` | Deep Teal. Clear demarcator for low-level runbook procedures. | `h4 { color: #0D9488; }` |
| **Code Block Background** | `#F8FAFC` | Very light alabaster gray. Visually defines code boundaries without heavy ink deposit. | `div.sourceCode, pre.sourceCode { background-color: #F8FAFC !important; }` |
| **Code Block Border** | `#CBD5E1` | Slate border. Provides crisp, laser-printer-safe container edges. | `border: 1px solid #CBD5E1 !important;` |
| **Warning Callout** | `#FEF2F2` / `#DC2626` | Soft red pastel with intense dark red border and text. Immediate visual alert. | `.callout-warning` |
| **Note Callout** | `#F0F9FF` / `#0284C7` | Soft blue pastel with vivid blue border. High legibility for operational context. | `.callout-note` |
| **Tip Callout** | `#F0FDF4` / `#16A34A` | Soft green pastel with crisp green border. Architectural pro-tips. | `.callout-tip` |

### 3.2 Typography Pairing

- **Prose:** `font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;`
  *Characteristics:* Clean geometric sans-serif, high x-height, optimized for both 300 DPI print and high-res displays. Line height is fixed at `1.55` with `10pt` base size.
- **Code & Configurations:** `font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;`
  *Characteristics:* Distinct character shaping (disambiguating `0`/`O` and `1`/`l`/`I`), tabular numbers, ligature support. Sized at `8.5pt` with `1.4` line height.

### 3.3 Print Page Budget & Paging Rules (`@page`)

```css
@page {
    size: A4;
    margin: 20mm 15mm 20mm 15mm;
    background: #FFFFFF;
    @top-left {
        content: "MCMC Telecom Warning Automation Handbook";
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #64748B;
        font-weight: 500;
    }
    @top-right {
        content: "PRIVATE AND CONFIDENTIAL (P&C)";
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #DC2626;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    @bottom-left {
        content: "Compile by: Harisfazillah Jamel";
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #64748B;
    }
    @bottom-right {
        content: "Page " counter(page);
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #0F172A;
        font-weight: 600;
    }
}
```

---

## 4. The 10 Critical Engineering Hurdles Solved

### Hurdle 1: Pandoc YAML Parser Explosions (`Unknown alias`)
- **Failure Mode:** Stitched multi-document markdowns retain individual OKF frontmatter blocks (`--- ... ---`). Pandoc attempts to parse subsequent frontmatter blocks as YAML document streams, failing with `Unknown alias` or corrupted titles.
- **Solution:** A pre-processing function (`strip_frontmatter()`) strips leading YAML frontmatter while capturing `title` and `description` to create formatted chapter metadata banners (`.chapter-meta`).

### Hurdle 2: Nested Backtick Fence Collisions
- **Failure Mode:** Ingested markdown documents or playbook examples already contain triple backticks (```` ``` ````). If the master compiler wraps them in triple backticks, the code block prematurely terminates, leaking raw code into prose.
- **Solution:** Dynamic backtick scaling. The compiler scans the target code text; if triple backticks exist, it wraps the block in 4 backticks (```` ```` ````); if 4 exist, it scales to 5.

### Hurdle 3: Blank Overflow Pages & Cover Fragmentation
- **Failure Mode:** Manual page breaks (`<div class="page-break"></div>`) combined with CSS `page-break-before: always;` on H1 elements generate unwanted empty pages. Furthermore, default Pandoc title headers split the cover across Pages 1 and 2.
- **Solution:**
  1. Eliminate all manual page break divs.
  2. Generate a standalone `cover.html` passed via `--include-before-body=cover.html`.
  3. Enforce `#title-block-header { display: none !important; }` and `.cover-title { break-before: avoid !important; }`.
  4. Constrain cover page padding and metadata fonts so the entire cover fits inside Page 1.

### Hurdle 4: Mermaid 10 Syntax Bomb Graphics (HTML Escaping)
- **Failure Mode:** Pandoc automatically escapes HTML entities inside `<pre class="mermaid"><code>` (`&quot;`, `&lt;`, `&gt;`, `--&gt;`). When Mermaid.js runs, it encounters illegal characters, rendering a pink syntax error bomb icon.
- **Solution:** A dedicated post-pandoc HTML regex unescapes `&quot;`, `&lt;`, `&gt;`, `&amp;` and strips enclosing `<code>` tags before headless browser invocation.

### Hurdle 5: Mermaid Node Collision in Multi-Diagram Handbooks
- **Failure Mode:** Different diagrams reuse common node identifiers (e.g. `NODE1`, `DB`, `CBE`, `PWP`). Mermaid's internal parser merges identical IDs into the same global SVG graph, corrupting diagram topology.
- **Solution:** **Mermaid Multi-Diagram Isolation Protocol**. Every diagram must have unique diagram-scoped namespaces prefixed to all nodes (e.g., `TB_` for Master Architecture, `PA_` for Pattern A, `PB_` for Pattern B, `PC_` for Pattern C).

### Hurdle 6: Headless Chromium Millisecond Timestamp Collision
- **Failure Mode:** Headless Chromium renders all page scripts in milliseconds. Mermaid's default `mermaid.run()` uses `Date.now()` timestamp IDs, causing ID collisions that draw multiple diagrams inside the same container.
- **Solution:** Sequential DOM replacement. The browser script iterates over `document.querySelectorAll("pre.mermaid")` and calls `mermaid.render("diagram_svg_" + i, code)` sequentially, injecting the returned SVG directly into `el.innerHTML`.

### Hurdle 7: Tall Vertical Flowcharts Splitting Pages
- **Failure Mode:** Long linear flowcharts (height > 600px) split mid-node across physical page breaks, causing dangling connectors and unreadable diagrams.
- **Solution:**
  1. Re-architect flowcharts into balanced 2-column grids (e.g., Phase 1 vs Phase 2).
  2. Set `pre.mermaid svg { max-width: 100% !important; height: auto !important; }`.
  3. Extract `innerHTML` rather than `textContent` in the Mermaid pre-pass to preserve `<br/>` tags and card formatting.

### Hurdle 8: Broken Relative Links & Leaked Local Paths (`file:///`)
- **Failure Mode:** Ingested documentation contains relative links (`../how-to/deploy.md`) or absolute filesystem paths (`file:///D:/Users/...`), which break or leak workstation directories in the compiled PDF.
- **Solution:** **Soft-Path Link Resolution Mandate (3-Tier Normalisation Pipeline)**:
  1. Pre-index all chapters (`#chap-{slug}`) and code files (`#code-{slug}`) into an in-memory `link_map`.
  2. Normalize link targets across 3 tiers:
     - *Tier 1:* Exact match in `link_map`.
     - *Tier 2:* Strip `file:///`, Windows drive letters (`C:/`, `D:/`), root directory prefixes, and `build/` prefixes.
     - *Tier 3:* Basename-only fallback (`os.path.basename(target)`).
  3. Preserve `#fragment` anchor suffixes across all tiers.
  4. Run an automated post-assembly audit to verify zero absolute paths survive in PDF links.

### Hurdle 9: Critical Safety Warnings Hidden in Code Comments
- **Failure Mode:** Production playbooks contain vital operational warnings, vendor bug workarounds, and safety dispatches hidden in `#` comments that SysAdmins miss when skimming compiled books.
- **Solution:** **Developer Commentary Extraction Protocol**:
  1. Inspect the leading `#` comment block of every playbook, script, and configuration file.
  2. Scan for warning keywords (`BUG`, `FIX`, `Confirmed`, `live`, `vendor`, `NEVER`, `destroy`, `destructive`, `ORA-\d+`, `crash`, `escalation`).
  3. If keywords match, generate a **⚠️ orange warning callout** (`callout-warning`, "Developer Commentary — Read Before Executing") rendered **above** the code fence.
  4. If standard comments, render a **💡 blue note callout** (`callout-note`).
  5. Preserve the original `#` comments inside the code block intact.

### Hurdle 10: Headless Browser Print Timeouts & Compositor Stalls
- **Failure Mode:** Headless Chrome/Edge can hang indefinitely if web fonts or ESM modules fail to trigger draw completion, stalling CI/CD pipelines.
- **Solution:** Execute Chromium with strict flags:
  ```bash
  msedge.exe --headless=new --disable-gpu --run-all-compositor-stages-before-draw --virtual-time-budget=8000 --print-to-pdf=<out.pdf> <file_uri>
  ```
  Enforce a hard Python subprocess timeout (45–60s) to gracefully catch draw completion.

---

## 5. Multi-Format Compilation Commands

```bash
# 1. Compile Standalone Interactive HTML Ebook
pandoc build/book/master_book.md -o build/book/handbook.html \
  --standalone --toc --toc-depth=3 --number-sections \
  --include-before-body=build/book/cover.html \
  --css=build/book/terminal-theme.css \
  --highlight-style=tango \
  --metadata title="MCMC Cell Broadcast & Public Warning Automation Handbook" \
  --metadata author="Compile by: Harisfazillah Jamel" \
  --metadata date="September 2026" -V lang=en

# 2. Compile Publication-Grade PDF via Headless Chromium
msedge.exe --headless=new --disable-gpu \
  --run-all-compositor-stages-before-draw \
  --virtual-time-budget=8000 \
  --print-to-pdf=build/book/handbook.pdf \
  file:///D:/Users/LinuxMalaysia/Projects/cbc-mcmc/build/book/handbook.html

# 3. Compile EPUB 3 Ebook
pandoc build/book/master_book.md -o build/book/handbook.epub \
  -t epub3 --toc --toc-depth=3 \
  --css=build/book/terminal-theme.css \
  --metadata title="MCMC Cell Broadcast & Public Warning Automation Handbook" \
  --metadata author="Compile by: Harisfazillah Jamel" \
  --metadata publisher="SongketMail Sdn Bhd / Deep State of Mind (DSOM)"

# 4. Compile Styled OpenDocument Text (ODT) for Google Docs
pandoc build/book/master_book.md -o build/book/handbook.odt \
  --reference-doc=build/book/custom_reference.odt \
  --toc --toc-depth=3 \
  --metadata title="MCMC Cell Broadcast & Public Warning Automation Handbook" \
  --metadata author="Compile by: Harisfazillah Jamel"
```

---

## 6. Complete Embedded Skill: `dsom-technical-book-compiler`

Below is the full, unabridged operational specification of the `dsom-technical-book-compiler` skill:

```yaml
---
okf_version: "0.2"
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
1. **Footer & Frontmatter Stripping:** When assembling 100+ documents, individual OKF frontmatter and DSOM signature footers must be stripped to prevent Pandoc YAML parser collisions (`Unknown alias`).
2. **Dynamic Backtick Fence Scaling:** When wrapping source code containing triple backticks (` ``` `), the enclosing fence must scale dynamically to 4 or 5 backticks (` ```` `).
3. **Mermaid HTML Unescaping Protocol:** Pandoc automatically escapes HTML entities inside `<pre class="mermaid"><code>` (`&quot;`, `&lt;br/&gt;`, `--&gt;`). The compilation pipeline must decode these entities before browser rendering to prevent Mermaid 10 syntax error bomb graphics.
4. **Standalone Cover Body Inclusion:** Never embed raw HTML covers inside Markdown files. Generate a standalone `cover.html` passed via `--include-before-body=cover.html`. Enforce `.cover-title { break-before: avoid !important; }` and `#title-block-header { display: none !important; }` to prevent cover fragmentation.
5. **Anti-Blank Page Discipline:** Never mix manual `<div class="page-break"></div>` tags with CSS `page-break-before: always;`.
6. **Headless Browser PDF Timeout:** Headless Chromium/Edge (`--headless=new --print-to-pdf`) renders CSS `@page` layouts, vector SVGs, and web fonts. A process timeout guardrail (45–60s) must be enforced.
7. **Mermaid Multi-Diagram Isolation Protocol:**
   - *Diagram-Scoped Namespace:* Prohibit reusing identical node IDs (e.g., `NODE1`, `CBE`, `PWP`) across diagrams. Prefix all node IDs with a unique diagram namespace (e.g., `TB_`, `PA_`, `PB_`, `PC_`) to prevent global symbol collisions.
   - *Sequential Headless DOM Replacement:* Headless Chromium renders in milliseconds, causing default `mermaid.run()` timestamp IDs (`Date.now()`) to collide and nest diagrams inside one container. Mandate sequential rendering via `mermaid.render(id, code)` with unique IDs (`diagram_svg_${i}`) replacing `<pre class="mermaid">` innerHTML sequentially.
8. **Soft-Path Link Resolution Mandate (3-Tier Normalisation):** The compilation pipeline must dynamically map all chapters (`#chap-{slug}`) and ingested code blocks (`#code-{slug}`) and rewrite all markdown links via a **3-tier normalisation pipeline**: (1) *Exact match* — look up the raw target in `link_map` as-is; (2) *Normalised match* — strip `file:///`, Windows drive letters (`D:/`, `C:/`), the project root prefix, and the `build/` intermediate directory prefix, then retry; (3) *Basename-only match* — strip all directory components and retry with the filename only. Pre-index basename-only keys into `link_map` before rewriting. Preserve `#fragment` suffixes across all tiers. Run a post-compile link audit asserting zero absolute path leaks (`D:/`, `C:/`, `file:///`, `build/` prefixes) survive in any PDF/HTML link target.
9. **Full-Spectrum Code Ingestion:** Ingest all production playbooks, Jinja2 templates, inventories, host/group variables, shell scripts, and candidate staging playbooks into dedicated book chapters to produce self-contained handbooks.
10. **Developer Commentary Extraction Protocol:** For every YAML playbook, shell script, or INI file ingested, extract the leading `#` comment block (all contiguous comment lines before the first YAML key, after the `---` fence) and render it as an HTML callout div above the code fence. Classify by keyword scan: comments containing `BUG`, `FIX`, `Confirmed`, `live`, `vendor`, `NEVER`, `ORA-\d+`, `destroy`, `destructive`, `hard way`, or `escalation` render as `callout-warning` (⚠️ orange, label `Read Before Executing`); all others render as `callout-note` (💡 blue). Preserve original `#` lines inside the code fence unchanged. CSS must define `.callout-warning p`, `.callout-note p`, and `strong` selectors with explicit `padding: 12px 16px` and `page-break-inside: avoid` for clean print rendering.

## Execution Command
```bash
uv run python .agents/skills/dsom-technical-book-compiler/scripts/compile-book.py
```
```

---

## 7. Operational Checklist for AI Agents & Compilers

Before finalizing any compiled handbook, the AI agent must verify:
- [ ] **Pure White Audit:** No solid black terminal blocks exist in the compiled PDF.
- [ ] **Blank Page Audit:** Verified total page count has zero empty filler pages between chapters.
- [ ] **Mermaid Audit:** All diagrams render as clean vector SVGs with zero syntax error bomb icons.
- [ ] **Link Leak Audit:** Grep search the assembled HTML/PDF links for `file:///` or Windows drive letters (`D:/`, `C:/`) — result must be 0.
- [ ] **Commentary Audit:** Leading playbook dispatches are rendered as human-readable callouts above the code fences.
- [ ] **Confidentiality Audit:** Running headers state `PRIVATE AND CONFIDENTIAL (P&C)` and attribution reads `Compile by: Harisfazillah Jamel`.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-09-04*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | PRIVATE & CONFIDENTIAL (P&C) | All Rights Reserved*

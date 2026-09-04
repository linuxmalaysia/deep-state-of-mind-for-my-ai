---
okf_version: 0.2
type: "how-to"
title: "How to Produce a Project Technical Handbook: The AI Prompt Engineering & Skill Adoption Blueprint"
timestamp: "2026-09-05T05:00:00Z"
topics: ["pandoc", "pdf", "handbook", "prompt-engineering", "print-optimized", "diataxis", "gitops", "aiops", "transferable-skills"]
description: "Comprehensive operational handbook and transferable AI prompt library for analyzing code repositories, synthesizing Diataxis documentation, baking native vector diagrams, and compiling publication-grade print-ready handbooks (PDF, HTML, EPUB) using Pandoc and Headless Chromium."
status: "stable"
stale_after: "2027-09-05"
sources:
  - id: "dsom_agents_rulebook"
    title: "The Core AI Rulebook (DSOM Rule 11 & Rule 22)"
    path: ".agents/AGENTS.md"
  - id: "dsom_technical_book_compiler_skill"
    title: "Technical Ebook & Handbook Compiler Skill"
    path: ".agents/skills/dsom-technical-book-compiler/SKILL.md"
  - id: "technical_book_compiler_prompt_guide"
    title: "Technical Book Design & PDF Compilation Master Prompt Guide"
    path: "docs/governance/TECHNICAL-BOOK-DESIGN-AND-PDF-COMPILER-PROMPT-GUIDE.md"
---

# How to Produce a Project Technical Handbook: The AI Prompt Engineering & Skill Adoption Blueprint

> **Classification:** Technical Standard & Transferable Knowledge Base
> **Target Audience:** Lead Architects, DevOps/SRE Engineers, and Autonomous AI Coding Assistants
> **Standard:** Terminal & Cloud Technical Book Standard (DSOM Rule 11 & Rule 22)
> **Author & Lead Consultant:** Harisfazillah Jamel (LinuxMalaysia)
> **Compiled By:** Antigravity Cognitive Digital Twin

---

## 1. Executive Overview & Transferability Mandate

Modern software, DevOps, and infrastructure projects frequently suffer from **fragmented documentation**. Architectural intent is split across READMEs, tribal chat logs, wiki pages, runbooks, and inline source code comments. When teams need to present their systems for audits, client handovers, team onboarding, or management reviews, they lack a single, authoritative, publication-grade volume.

This guide provides a **100% transferable blueprint** that enables any engineering repository—whether built on Ansible, Terraform, Kubernetes, Python, Go, or Cloud Native architectures—to synthesize its entire codebase and documentation into a cohesive, print-optimized technical book (PDF, interactive HTML, and EPUB 3).

### What This Blueprint Provides:
1. **The Prompt Transformation Matrix:** All conversational prompts typically asked by human leads, rewritten into high-fidelity, optimized master prompts that any AI agent can execute without ambiguity.
2. **The 6-Phase Engineering Pipeline:** Discovery, visual modeling, Diataxis ingestion, narrative storytelling, print formatting, and multi-format compilation.
3. **The 17 Core Compilation Invariants:** Solutions to every major compilation hurdle (syntax crashes, dark container ink waste, missing covers, unrendered Mermaid blocks, unparsed callout alerts, and browser process timeouts).
4. **Drop-in Reusable Skill Specification:** An autonomous skill definition that can be copied directly into `.agents/skills/` of any target repository.

---

## 2. The Prompt Transformation Matrix: From Conversational Ask to Production AI Master Prompts

When humans communicate with AI assistants during technical book compilation, their initial requests are often short and intuitive. However, generic AI assistants often misinterpret these asks—generating dark code blocks, omitting cover pages, hardcoding narrative text into compiler scripts, or failing to render diagrams.

Below is the complete **Before & After Matrix**, translating conversational requests into robust, constraint-enforced AI master prompts.

---

### Prompt 1: Project Discovery & Architectural Modeling

#### Conversational Human Ask:
> *"I need you to produce a book for this project. Start with understanding the project by understanding the ansible playbook and documents that can be related to the ansible playbook. Make sure we have diagram of flow of works and flow of how ansible work."*

#### Production-Grade AI Master Prompt:
```markdown
You are a Principal Technical Author and Systems Architect. Your mission is to analyze this repository and assemble an authoritative, publication-grade Technical Handbook.

PHASE 1: REPOSITORY DISCOVERY & TAXONOMY
1. Scan the repository inventory, orchestration playbooks/manifests, roles, configuration templates, and documentation suites.
2. Catalog all operational components into logical tiers (e.g., Command Centres, Orchestration Bridges, Persistence Fabrics, Telemetry Ingestion Workers).
3. Map every production playbook/code file to its corresponding documentation, runbooks, and Root Cause Analysis (RCA) reports.

PHASE 2: ARCHITECTURAL VISUAL MODELING
Construct two comprehensive architectural flowcharts:
1. The End-to-End Command Highway: Visualizing the multi-tier flow of code from local development and GitOps remotes to target nodes.
2. The Orchestration Execution Engine: Visualizing how automation tasks inspect hardware, apply declarative baselines, enforce zero-trust security, and verify system state.

OUTPUT REQUIREMENTS:
- Structure the book into clear, hierarchical Parts and Chapters following the Diataxis framework.
- Ensure every code artifact has a dedicated sub-chapter accompanied by developer operational context and architectural rationale.
```

---

### Prompt 2: Resolving Diagram Failures (Mermaid to Native SVG)

#### Conversational Human Ask:
> *"The diagram is not showing in the book."*

#### Production-Grade AI Master Prompt:
```markdown
You are a Graphics & Headless Browser Print Specialist. The Mermaid diagrams in our compiled HTML/PDF are failing to render or displaying syntax error graphics.

ROOT CAUSE ANALYSIS:
1. Headless Chrome/Edge print engines capture DOM snapshots in milliseconds, outrunning asynchronous client-side Mermaid JavaScript CDN libraries.
2. Pandoc wraps `<pre class="mermaid">` blocks in `<code>` tags and escapes HTML arrows (`-->` becomes `--&gt;`), corrupting Mermaid syntax.

REMEDIATION MANDATE (NATIVE VECTOR SVG PRE-RENDERING):
1. Eliminate client-side Mermaid JavaScript rendering entirely for PDF production.
2. Author a standalone Python script (e.g., `tools/bake_native_svg.py`) that pre-renders or directly substitutes Mermaid code blocks with clean, styled, inline vector `<svg>` markup.
3. Ensure SVG elements include viewBox definitions, drop-shadow filters, high-contrast text labels (using 'Inter' or system sans-serif), and responsive container wrappers (`<div class="mermaid-svg-container">`).
4. Execute this transformation directly on the generated `handbook.html` prior to launching the headless browser PDF print step.
```

---

### Prompt 3: Diátaxis Documentation Enrichment & Ingestion

#### Conversational Human Ask:
> *"Add into our books, content from md documents that is related to each of our ansible playbooks. Enrich our book."*

#### Production-Grade AI Master Prompt:
```markdown
You are a Technical Documentation Compiler. Your task is to enrich every playbook chapter in the Technical Handbook by dynamically ingesting its accompanying operational runbooks, explanations, and incident reports.

MANDATORY INGESTION & SANITIZATION RULES:
1. Frontmatter & Signature Stripping: Parse each ingested markdown file and strip all YAML metadata fences (`--- ... ---`) and document signature footers (`*Maintained by...*`) to prevent Pandoc parser collisions (`Unknown alias`).
2. Heading Level Offsetting: Apply a dynamic heading level offset (+2 levels: `#` becomes `###`, `##` becomes `####`) to ensure ingested document headings nest cleanly beneath the parent Chapter title in the Table of Contents.
3. Markdown Horizontal Rule Sanitization: Replace all internal standalone horizontal rules (`\n---\n`) with triple asterisks (`\n***\n`) to prevent Pandoc from falsely interpreting them as YAML metadata blocks.
4. Operational Provenance Banner: Inject an audit pill above each ingested document:
   `<div class="doc-provenance"><strong>Operational Reference Guide:</strong> <code>path/to/file.md</code></div>`
5. Developer Commentary Extraction: Scan the leading comment block of each code file for keywords (BUG, FIX, WARNING, CRITICAL, NEVER, escalation). Render matches as high-visibility callouts (`callout-warning` or `callout-note`) above the code fence.
```

---

### Prompt 4: The Narrative Epic (Heart, Soul, and Sovereign Blood)

#### Conversational Human Ask:
> *"I need a chapter that's like a story, all about this project and infra from start to end, how it can be built, deployed, and operated. Highlight the use of ansible + semaphoreui + gitea as GitOps, and AIOps with human in the loop. Add about deep state of mind (DSOM) of My AI as the AI memory and brain. This chapter is not technical; it is about the heart, soul, and blood of this project."*

#### Production-Grade AI Master Prompt:
```markdown
You are a Principal Technical Biographer and Systems Philosopher. Author an evocative, inspiring narrative chapter titled:
"# Prologue: The Story of <Project Name> — Heart, Soul, and Sovereign Blood {.unnumbered}"

NARRATIVE STRUCTURE & THEMES:
1. The Spark in the Dark (Why This Fabric Was Born):
   - Paint the operational reality: telemetry deluge, memory exhaustion, swap death spirals, and the painful loss of context when engineers step away from the terminal.
2. The Trinity of Motion (GitOps, The Control Node, and The Hand):
   - Explain how Git serves as the immutable source of truth, Semaphore UI acts as the scheduled heartbeat, and Ansible operates as the indomitable physical hand shaping the infrastructure.
3. The Mind in the Machine (Deep State of Mind & AIOps):
   - Address the fatal flaw of Large Language Models: Context Decay (cognitive amnesia).
   - Chronicle the creation of the Sovereign Markdown Palace (`.agents/brain/`, `palace_registry.md`, Start-of-Day reanimation, and End-of-Day hibernation), preserving unbroken historical context across operational shifts.
4. The Sacred Balance (AIOps with Human-in-the-Loop):
   - Reject blind, dangerous auto-remediation.
   - Embed the Sovereign AIOps Integration Loop (ASCII architectural diagram): AI proposes remediation -> Sovereign Human verifies and commits -> Ansible executes -> AI audits and records memory.
   - Articulate the Three Laws of the Twin: Advisory over Execution, Logic over Operation, and Partnership through Environmental Awareness.
5. From Raw Metal to Living Shield:
   - Walk through the 5 foundational phases from genesis virtual machine bootstrapping to hardened security baselines, rootless container pods, threat analytics, and continuous Day-2 operations.
6. The Heart, Soul, and Blood:
   - Close with the philosophical trifecta: Sovereignty, Discipline, and Human-AI Symbiosis.
```

---

### Prompt 5: Clean Architecture Separation (Standalone Markdown Document)

#### Conversational Human Ask:
> *"I need the story to be in its own md file."*

#### Production-Grade AI Master Prompt:
```markdown
You are a Clean Architecture and Diataxis Specialist. Refactor the narrative story chapter out of inline Python script strings into a dedicated, reusable documentation artifact.

IMPLEMENTATION STEPS:
1. Author the file `docs/explanation/THE-STORY-OF-<PROJECT>.md` with complete OKF v0.2 YAML frontmatter (`type: documentation`, `title: ...`).
2. Embed the complete narrative text, ASCII loop diagram, and formal DSOM signature footer.
3. Register the new document in `SUMMARY.md` under the `explanation` quadrant to ensure GitBook/MkDocs navigation indexing.
4. Update the book compiler script (`tools/build_book.py`) to dynamically ingest this document using `ingest_doc_file("docs/explanation/THE-STORY-OF-<PROJECT>.md", heading_offset=0, show_provenance=False)` directly into the book's Prologue.
```

---

### Prompt 6: Print-Optimized Formatting Restoration (Zero Toner Waste & Cover Injection)

#### Conversational Human Ask:
> *"What happened to my book? We lost the formatting. No cover, black background? That needs to be checked again."*

#### Production-Grade AI Master Prompt:
```markdown
You are a Print Production Engineer and CSS Specialist. Diagnose and fix the visual formatting regressions in our compiled PDF and HTML handbook.

SYMPTOMS TO REMEDY:
1. Missing Cover Page: Re-inject `--include-before-body=build/book/cover.html` in the Pandoc build chain. Ensure `.cover-page` in CSS declares `break-after: page; min-height: 250mm;` so the cover fills Page 1 completely and cleanly page-breaks before the Table of Contents.
2. Black Background Code Blocks: Replace dark syntax highlighting (e.g. `--syntax-highlighting=espresso`) with `--syntax-highlighting=tango`. Ensure CSS enforces `pre, code, div.sourceCode { background-color: #F8FAFC !important; border: 1px solid #CBD5E1 !important; color: #0F172A !important; }` to eliminate toner waste.
3. External CSS Linking Failures: Prevent headless browser path resolution failures by reading `terminal-theme.css` and inlining the complete stylesheet directly into `<style>` inside `<head>` of the HTML before PDF generation.
4. Raw GitHub Alert Syntax: Detect all `> [!NOTE]`, `> [!WARNING]`, `> [!TIP]`, `> [!IMPORTANT]`, and `> [!CAUTION]` syntax in ingested markdown files and transform them into styled pastel HTML callout cards (`<div class="callout callout-note"><strong>💡 Note</strong><p>...</p></div>`).
5. Asynchronous Process Premature Exit: When compiling via Microsoft Edge on Windows PowerShell, execute with `Start-Process -FilePath $edge -ArgumentList ... -Wait` using an isolated user profile (`--user-data-dir`) to ensure the process does not terminate before the PDF file buffer is completely written.
```

---

## 3. The 17 Non-Negotiable Technical Book Compilation Invariants

Any automated compilation pipeline must adhere to these 17 strict invariants:

| # | Invariant Name | Failure Mode Addressed | Architectural Rule |
| :--- | :--- | :--- | :--- |
| **1** | **Pure White Standard** | Dark gray backgrounds waste ink and look muddy | Force `@page { background: #FFFFFF; }` and `body { background-color: #FFFFFF !important; }`. |
| **2** | **Light Alabaster Code** | Solid black terminal containers waste ink | Code containers must use `#F8FAFC` background with `#CBD5E1` border and dark charcoal text `#0F172A`. |
| **3** | **Syntax Theme (`tango`)** | Dark themes (`espresso`, `zenburn`) force black code backgrounds | Strictly enforce `--syntax-highlighting=tango` for light-background compatibility. |
| **4** | **Standalone Cover Injection** | Raw Markdown covers break page layout and spill over | Author `cover.html` and inject via `--include-before-body=cover.html`. |
| **5** | **Cover Single-Page Fit** | Cover content spilling into Table of Contents | Enforce `.cover-page { break-after: page; min-height: 250mm; height: 100%; display: flex; flex-direction: column; justify-content: space-between; }`. |
| **6** | **Frontmatter Stripping** | Pandoc crashes with `Unknown alias` error | Strip `--- ... ---` blocks from all ingested markdown files before concatenation. |
| **7** | **Horizontal Rule Sanitization** | `\n---\n` parsed by Pandoc as YAML start | Regex replace `\n---\n` with `\n***\n` in all ingested content. |
| **8** | **GitHub Alert Card Conversion** | `> [!NOTE]` renders as unstyled plain text | Programmatically transform into `<div class="callout callout-note"><strong>💡 Note</strong><p>...</p></div>`. |
| **9** | **Self-Contained Embedded CSS** | Headless browsers fail to resolve relative CSS links | Read `terminal-theme.css` and inject directly into `<style>` inside `<head>`. |
| **10** | **Dynamic Backtick Scaling** | Triple backticks inside code blocks close outer fence | Count max backticks in code and scale outer fence to N+1 (e.g. ` ```` `). |
| **11** | **Heading Offset (+2)** | Embedded guide titles collide with Book H1/H2 | Dynamically increment heading level (`#` to `###`, `##` to `####`). |
| **12** | **Native Vector SVG Baking** | Client-side Mermaid race conditions in headless PDF | Pre-render diagrams to `<svg>` and inject into HTML before headless PDF execution. |
| **13** | **Mermaid Namespace Isolation** | Global node ID collisions across multiple diagrams | Prefix node IDs with unique namespace prefixes (`TB_`, `AN_`, `TH_`). |
| **14** | **Pandoc Code-Tag Wrapping** | Pandoc wraps `<pre class="mermaid"><code>` and escapes HTML | SVG replacement regexes must match both standard and `<code>`-wrapped pre blocks and unescape arrows (`--&gt;`). |
| **15** | **Windows Isolated Browser Profile** | Edge crashes or hangs if user desktop instances are running | Launch Edge with `--user-data-dir="$env:TEMP/edge-pdf-$(Get-Random)"`. |
| **16** | **Synchronous Edge Execution** | PowerShell returns before Edge finishes writing PDF | Always use `Start-Process -FilePath $edge -ArgumentList ... -Wait`. |
| **17** | **Provenance Audit Banners** | Loss of traceability for ingested runbooks | Inject `<div class="doc-provenance">` detailing the repository source path. |

---

## 4. Reusable Project Book Assembler Template (`tools/build_project_book.py`)

Below is the clean, modular Python assembler that can be copied directly into any repository:
```python
#!/usr/bin/env python3
"""
Universal Technical Handbook Assembler & Multi-Format Compiler
Standard: Terminal & Cloud Standard (DSOM Rule 11 & Rule 22)
"""

import os
import re
import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path(".").resolve()
BUILD_DIR = ROOT_DIR / "build" / "book"
BUILD_DIR.mkdir(parents=True, exist_ok=True)

MASTER_MD = BUILD_DIR / "master_book.md"
COVER_HTML = BUILD_DIR / "cover.html"
THEME_CSS = BUILD_DIR / "terminal-theme.css"
HANDBOOK_HTML = BUILD_DIR / "handbook.html"
HANDBOOK_PDF = BUILD_DIR / "handbook.pdf"
HANDBOOK_EPUB = BUILD_DIR / "handbook.epub"

WARNING_KEYWORDS = re.compile(
    r"\b(BUG|FIX|Confirmed|live|vendor|NEVER|destroy|destructive|ORA-\d+|crash|escalation|hard way|WARNING|CAUTION|CRITICAL)\b",
    re.IGNORECASE
)

def strip_frontmatter_and_footer(content: str) -> str:
    lines = content.splitlines()
    if lines and lines[0].strip() == "---":
        end_idx = -1
        for idx in range(1, len(lines)):
            if lines[idx].strip() == "---":
                end_idx = idx
                break
        if end_idx != -1:
            content = "\n".join(lines[end_idx+1:])
    content = re.sub(r"\n---\s*\n\*.*", "", content, flags=re.DOTALL)
    content = re.sub(r"\n---\n", "\n***\n", content)
    return content.strip()

def convert_github_alerts(text: str) -> str:
    alert_types = "NOTE|TIP|WARNING|IMPORTANT|CAUTION|SUCCESS"
    pattern = re.compile(
        r"^>\s*(?:\*\*)?\[!(" + alert_types + r")\]"
        + r"\s*" + r"(?:\*\*)?(?:[ \t]*(.*))?\n((?:^>.*$\n?)*)",
        re.MULTILINE
    )
    def replacer(match):
        alert_type = match.group(1).upper()
        first_line = match.group(2) or ""
        raw_body = match.group(3) or ""
        lines = []
        if first_line.strip():
            lines.append(first_line.strip())
        for line in raw_body.splitlines():
            clean_line = re.sub(r"^>\s?", "", line)
            lines.append(clean_line)
        body = "\n".join(lines).strip()

        if alert_type in ("WARNING", "CAUTION", "IMPORTANT"):
            css_class = "callout callout-warning"
            icon = "⚠️" if alert_type != "CAUTION" else "🛑"
            title = alert_type.capitalize()
        elif alert_type in ("TIP", "SUCCESS"):
            css_class = "callout callout-tip"
            icon = "💡" if alert_type == "TIP" else "✅"
            title = alert_type.capitalize()
        else:
            css_class = "callout callout-note"
            icon = "💡"
            title = "Note"

        return f'\n<div class="{css_class}">\n<strong>{icon} {title}</strong>\n\n{body}\n</div>\n\n'

    return pattern.sub(replacer, text)

def scale_backticks(code_text: str) -> tuple[str, str]:
    max_ticks = 0
    matches = re.findall(r"(`{3,})", code_text)
    for m in matches:
        if len(m) > max_ticks:
            max_ticks = len(m)
    fence = "`" * max(3, max_ticks + 1)
    return fence, fence

def extract_commentary(code_text: str, lang: str = "yaml"):
    lines = code_text.splitlines()
    comment_lines = []
    start_idx = 1 if lines and lines[0].strip() == "---" else 0
    for i in range(start_idx, len(lines)):
        l = lines[i]
        stripped = l.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            comment_lines.append(stripped.lstrip("#").strip())
        else:
            break
    if not comment_lines:
        return None
    comment_text = " ".join(comment_lines)
    is_warning = bool(WARNING_KEYWORDS.search(comment_text))
    callout_class = "callout callout-warning" if is_warning else "callout callout-note"
    callout_title = "Developer Commentary — Read Before Executing" if is_warning else "Developer Operational Context"
    callout_icon = "⚠️" if is_warning else "💡"
    body = "\n".join(f"> {cl}" for cl in comment_lines[:15])
    return f'<div class="{callout_class}">\n<strong>{callout_icon} {callout_title}</strong>\n\n{body}\n</div>\n'

def ingest_code_file(file_path: Path, lang: str, title: str, anchor: str) -> str:
    if not file_path.exists():
        return f"\n*File not found: {file_path}*\n"
    content = file_path.read_text(encoding="utf-8", errors="replace")
    callout = extract_commentary(content, lang)
    fence_start, fence_end = scale_backticks(content)
    md_parts = [f"\n<a id=\"{anchor}\"></a>\n### {title}\n"]
    md_parts.append(f"**Source File:** `{file_path.relative_to(ROOT_DIR).as_posix()}`\n")
    if callout:
        md_parts.append(callout)
    md_parts.append(f"{fence_start}{lang}\n{content.strip()}\n{fence_end}\n")
    return "\n".join(md_parts)

def ingest_doc_file(rel_path: str, heading_offset: int = 1, show_provenance: bool = True) -> str:
    file_path = ROOT_DIR / rel_path
    if not file_path.exists():
        return f"\n*Documentation file not found: {rel_path}*\n"
    raw = file_path.read_text(encoding="utf-8", errors="replace")
    clean = strip_frontmatter_and_footer(raw)
    clean = convert_github_alerts(clean)

    out = []
    for line in clean.splitlines():
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            lvl = min(len(m.group(1)) + heading_offset, 6)
            hashes = "#" * lvl
            title = m.group(2)
            out.append(f"{hashes} {title}")
        else:
            out.append(line)

    header = f'\n<div class="doc-provenance"><strong>Operational Reference Guide:</strong> <code>{rel_path}</code></div>\n' if show_provenance else "\n"
    return header + "\n".join(out) + "\n"

def build_master_book():
    print("Assembling master book markdown...")
    parts = []

    # 1. Book Executive Overview
    parts.append("""# Executive Overview {.unnumbered}
> **Classification:** Private And Confidential (P&C)
> **Compiled By:** Autonomous Cognitive Twin
> **Standard:** Terminal & Cloud Technical Handbook Standard
""")

    # 2. Prologue Story (Dynamically Ingested from Standalone File)
    story_path = "docs/explanation/THE-STORY-OF-PROJECT.md"
    if (ROOT_DIR / story_path).exists():
        parts.append(ingest_doc_file(story_path, heading_offset=0, show_provenance=False))

    # 3. Dynamic Chapters and Code Ingestion
    # Add your project-specific parts and chapters here...

    full_text = "\n\n".join(parts)
    MASTER_MD.write_text(full_text, encoding="utf-8")
    print(f"Master markdown written: {MASTER_MD} ({len(full_text):,} bytes)")

if __name__ == "__main__":
    build_master_book()
```

---

## 5. Standalone Reusable Skill Specification (`project-technical-book-compiler`)

To adopt this capability in another repository, copy the specification below into `.agents/skills/project-technical-book-compiler/SKILL.md`:

```yaml
---
okf_version: "0.2"
type: "skill"
title: "Project Technical Book & Handbook Compiler"
timestamp: "2026-09-05T00:00:00Z"
description: "Autonomously synthesizes repository code, Diataxis documentation, and system telemetry into publication-grade print-ready PDF, standalone HTML, and EPUB handbooks using Pandoc, Headless Chromium, and the Terminal & Cloud design framework."
topics: ["pandoc", "pdf", "html", "epub", "print-optimized", "diataxis", "handbook"]
status: "stable"
stale_after: "2027-09-05"
name: "project-technical-book-compiler"
---

# Project Technical Book & Handbook Compiler

## Purpose
Standardises the automated assembly, styling, and multi-format compilation of entire project repositories into unified, publication-grade engineering handbooks.

## Execution Commands

### 1. Build Master Markdown
```bash
uv run python tools/build_project_book.py
```

### 2. Compile Standalone Interactive HTML (Pandoc 3.x)
```powershell
pandoc build/book/master_book.md -o build/book/handbook.html `
  --standalone --toc --toc-depth=3 --number-sections `
  --include-before-body=build/book/cover.html `
  --css=terminal-theme.css `
  --syntax-highlighting=tango `
  --metadata title="Project Technical Handbook" `
  --metadata author="Lead Architect" `
  --metadata date="September 2026" -V lang=en
```

### 3. Bake Native Vector SVGs & Inline Theme CSS
```bash
uv run python tools/bake_native_svg.py
```

### 4. Compile Publication-Grade PDF (Headless Chromium / Edge)
```powershell
$tmpProfile = "$env:TEMP\edge-pdf-profile-$(Get-Random)"
Start-Process -FilePath "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" `
  -ArgumentList "--headless=new", "--disable-gpu", "--run-all-compositor-stages-before-draw", `
  "--no-pdf-header-footer", "--print-to-pdf=d:\path\to\build\book\handbook.pdf", `
  "--user-data-dir=$tmpProfile", "file:///d:/path/to/build/book/handbook.html" -Wait
Remove-Item -Recurse -Force $tmpProfile -ErrorAction SilentlyContinue
```

### 5. Compile EPUB 3 Ebook
```powershell
pandoc build/book/master_book.md -o build/book/handbook.epub `
  -t epub3 --toc --toc-depth=3 `
  --css=build/book/terminal-theme.css `
  --metadata title="Project Technical Handbook"
```
```

---

## 6. Operational Checklist & Quality Assurance

Before delivering any compiled handbook to stakeholders, execute this audit checklist:

- [ ] **Cover Page Audit:** Page 1 renders as a full-page bordered card with P&C badges and metadata table; breaks cleanly before Table of Contents.
- [ ] **Zero Toner Waste Audit:** All code containers have `#F8FAFC` light gray backgrounds with dark charcoal text and `tango` syntax colors. Zero black terminal boxes exist.
- [ ] **Callout Card Audit:** All operational notes, warnings, and tips render as styled pastel cards with icons (`💡 Note`, `⚠️ Warning`, `💡 Tip`). Zero raw `[!NOTE]` markdown syntax leaks survive.
- [ ] **Vector Diagram Audit:** All architecture and workflow diagrams render as crisp, scalable vector SVGs directly inline.
- [ ] **Inline CSS Audit:** CSS is embedded directly into `<style>` inside `<head>` to prevent external relative link breakage.
- [ ] **Soft-Path Link Audit:** All internal cross-references point to clean `#chap-...` or `#code-...` fragments without surviving absolute filesystem paths (`file:///` or drive letters).
- [ ] **Pagination Audit:** Verified zero empty filler pages exist between chapters.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-09-05*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*

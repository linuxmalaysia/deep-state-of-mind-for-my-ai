---
okf_version: 0.1
type: agent_skill
title: "📄 DOCX Document Processor Skill"
timestamp: "2026-09-02T12:00:00Z"
description: "Comprehensive document creation, editing, and analysis for .docx Word files with support for tracked changes, comments, formatting preservation, and text extraction."
topics: ["docx", "word", "document-processing", "pandoc", "dsom"]
name: docx
---
# 📄 DOCX Document Processor Skill (`docx`)

## Purpose
The `docx` skill enables AI agents and engineers to create, edit, analyse, and convert `.docx` Microsoft Word documents. It maintains structural formatting, handles tracked changes and comments in collaborative workflows, and extracts text or converts documents to portable formats like Markdown using Pandoc.

---

## When to Use This Skill

- Creating new Word documents (`.docx`) programmatically for reports, proposals, or formal briefs.
- Editing existing Word documents while preserving tracked changes, redlining, and reviewer comments.
- Converting `.docx` files to clean Markdown for context inspection or ingesting into the Sovereign Markdown Palace.
- Converting Markdown proposals into formatted Word documents.

---

## Workflows & Tools

### 1. Document Creation & Manipulation
- Use Node.js libraries (`docx`, `docx-templates`) or Python packages (`python-docx`) to generate structured documents.
- Use native DSOM helpers (e.g. `node-proposal-formatter` or `proposal-docx-formatter`) when building formal proposals.

### 2. Text Extraction & Inspection
- Convert `.docx` to Markdown via Pandoc:
  ```bash
  pandoc input.docx -f docx -t markdown -o output.md
  ```
- Use `markitdown` when batch converting office files (`.docx`, `.xlsx`, `.pptx`) into context sheets.

### 3. Redlining & Tracked Changes Workflow
- Preserve author comments, revision markup, and tracked changes in legal, academic, or business documents.
- Avoid flattening or dropping reviewer metadata when updating existing files.

---

## Security & Safety Instructions

- **No Privilege Escalation**: Never execute commands requiring elevated administrative rights (`sudo`) when processing user-uploaded documents.
- **Report Conversion Loss**: When converting complex Word documents to Markdown, explicitly report any flattened nested tables, stripped headers, or unhandled inline media.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-09-02*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*

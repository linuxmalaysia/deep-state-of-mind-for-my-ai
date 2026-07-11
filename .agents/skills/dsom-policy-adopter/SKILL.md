---
okf_version: 0.1
type: skill
title: "DSOM Policy Adopter"
name: "dsom-policy-adopter"
description: "Automatically ingests an external research paper or policy document (PDF/Markdown) and formally integrates it into the DSOM framework governance and core rules."
timestamp: 2026-07-11T23:19:45Z
---
# DSOM Policy Adopter Skill

**Purpose**: To seamlessly ingest external architectural or governance documents and integrate them into the DSOM repository strictly adhering to the Triple-Ledger Synchronization Mandate and Core Rules.

## Prerequisites
- The user has provided an absolute path to a document (e.g., PDF or Markdown).
- If the document is a PDF, the AI should use the iew_file or pdf-text-extractor tool to read the contents first.

## Execution Workflow

1. **Ingest & Extract**
   - Read the provided document in its entirety.
   - Extract the core architectural principles, rules, and actionable constraints that apply to the DSOM ecosystem.

2. **Draft Governance Document**
   - Create a dedicated, highly-structured Markdown file in the docs/governance/ directory.
   - The file must contain OKF v0.1 YAML frontmatter (with okf_version, 	ype: documentation, 	itle, and 	imestamp).
   - Format the document strictly following the Generative Engine Optimization (GEO) standard: Authoritative tone, verifiable statistics/quotes, H2 user-centric headings, and 200-400 word chunks.

3. **Core Engine Injection (AGENTS.md)**
   - Distill the most critical, actionable constraints from the new policy.
   - Inject these constraints directly as a new numbered Core Rule into .agents/AGENTS.md. Be extremely precise; do not bloat the file.

4. **Triple-Ledger Synchronization**
   - **README.md**: Add a link to the new docs/governance/ file in the "Key Documents" table with a short emoji-prefixed description.
   - **CHANGELOG.md**: Add an entry under ## [Unreleased] describing the new governance policy and rule addition.
   - **HISTORY.md**: Append a new entry to the universal ledger detailing the architectural integration and the exact files modified.

5. **Defensive GitOps (Commit & Push)**
   - Run git pull --rebase origin main to ensure sync.
   - Add all changed files: git add docs/governance/... .agents/AGENTS.md README.md CHANGELOG.md HISTORY.md
   - Commit with an atomic, conventional commit message (e.g., docs(governance): adopt [Policy Name]).
   - Push to all active remotes (e.g., GitHub and GitLab).

6. **Closure & Walkthrough**
   - Report the successful adoption to the user, highlighting the exact architectural changes made.


---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-11*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*

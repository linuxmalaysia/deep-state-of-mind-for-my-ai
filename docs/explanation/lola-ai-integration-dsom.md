---
okf_version: 0.2
type: explanation
title: "Lola AI Package Manager Integration in Deep State of Mind (DSOM)"
timestamp: "2026-09-06T00:00:00Z"
topics: ["lola-ai", "package-manager", "dsom", "air-gapped", "sovereign"]
resource: "/docs/explanation/lola-ai-integration-dsom.md"
sources: [{id: dsom-core-spec, title: "Deep State of Mind (DSOM) Governance Architecture", resource: "/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md", url: "https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai/blob/main/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md", type: architecture_spec, author: "Harisfazillah Jamel (LinuxMalaysia)"}, {id: google-okf-v02-spec, title: "Google Cloud Open Knowledge Format (OKF) v0.2 Specification", resource: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md", url: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md", type: external_spec, author: Google Cloud Platform}]
status: stable
generated: {by: Google Jules, timestamp: "2026-09-06T00:00:00Z"}
stale_after: "2027-10-01"
spec_version: "0.2"
concept_id: lola_ai_integration_dsom
description: "Comprehensive 4W1H architectural guide on integrating Lola AI package manager into the Deep State of Mind framework for sovereign, air-gapped skill distribution."
---
# Lola AI Package Manager Integration in Deep State of Mind (DSOM)

## 1. Executive Overview & 4W1H Architecture

This document presents the architectural framework and operational SOP for adopting Lola (`lola-ai`) within the Deep State of Mind (DSOM) AI orchestration system.

### 4W1H Framework Breakdown

- **WHAT (Definition & Analogy):**
  Lola (`lola-ai`) is an open-source declarative package manager and synchronization engine designed specifically for AI agent skills and context packages. If an agent skill is an RPM package, Lola is the DNF package manager. It allows skills to be packaged as portable, version-controlled, dual-compliant filesystem bundles anchored by `SKILL.md`.

- **WHY (Strategic Rationale & Sovereignty):**
  To enable seamless portability, versioning, and distribution of agent capabilities across heterogeneous execution environments (e.g., local control nodes, telecommunication bastions, enterprise clouds) without introducing hard dependencies on external SaaS registries, internet access, or WAN endpoints. This preserves 100% operational sovereignty and air-gapped readiness under DSOM Rule 16 and Rule 27.

- **WHO (Target Audience & Governance):**
  System Architects, GitOps Engineers, Ansible Automation Engineers, and AI Agents (e.g., Google Jules, Google Antigravity) operating under the DSOM Protocol.

- **WHERE (Location & File Anchors):**
  Declared globally at the repository root via `.lola-req` and locally vendored under `.agents/skills/<skill-name>/`. Automated deployment is orchestrated via `playbooks/install.yml`.

- **HOW (Implementation & Synchronization SOP):**
  - **Packaging:** Skills are organised into standardised directory structures (`SKILL.md`, `scripts/`, `references/`, `tests/`) with dual-compliant metadata (Lola + OKF v0.2).
  - **Script Hermeticity:** Python helper scripts embed PEP 723 inline script metadata (`# /// script ...`) for self-contained `uv run` execution.
  - **Requirements Declaration:** `.lola-req` enumerates all in-repo skills as locally vendored packages with optional sovereign Git remote fallbacks.
  - **Idempotent Air-Gapped Sync:** Ansible (`playbooks/install.yml`) and shell scripts check for `lola` CLI presence (`which lola`) before executing `lola sync`. If absent or offline, sync is skipped gracefully, falling back to local vendored skills.

---

## 2. Dual-Compliant Metadata Standard (Lola + OKF v0.2)

Every skill package in `.agents/skills/<skill-name>/SKILL.md` implements a unified frontmatter combining Lola package manager attributes with OKF v0.2 trust pillars:

```yaml
---
name: <skill-name>
version: 1.0.0
description: "<Precise capability description and functional trigger>"
author: "Harisfazillah Jamel (LinuxMalaysia)"
license: "GPL-3.0-or-later"
# OKF v0.2 / DSOM Core Metadata
okf_version: "0.2"
type: "skill"
topics: ["<topic1>", "<topic2>"]
status: "stable"
stale_after: "2027-10-01"
---
```

---

## 3. Standard Skill Package Directory Layout

All skills adhere to the following directory structure:

```
.agents/skills/<skill-name>/
├── SKILL.md              # Primary specification & prompt instructions
├── scripts/              # Executable helpers, Python scripts (with PEP 723)
├── references/           # Templates, guidelines, CSS, schemas
└── tests/                # Smoke tests or verification scripts
```

---

## 4. Declarative Repository Manifest (`.lola-req`)

The root `.lola-req` manifest configures local vendored skill resolution with one module reference per line (`lola-ai>=0.1.0` CLI format):

```
# Declarative Lola Package Specification (.lola-req)
# Lola CLI Minimum Version Supported: lola-ai>=0.1.0

.agents/skills/agent-plugin-packager
.agents/skills/council-of-high-intelligence
```

---

## 5. Air-Gapped Idempotent Automation Snippets

### Ansible Playbook (`playbooks/install.yml`)

```yaml
- name: "DSOM Framework & Lola AI Package Sync"
  hosts: localhost
  connection: local
  gather_facts: false

  tasks:
    - name: "Lola | Check if lola CLI is present on control node"
      ansible.builtin.command: "which lola"
      register: lola_check
      changed_when: false
      failed_when: false

    - name: "Lola | Execute lola sync against .lola-req (if lola is installed)"
      ansible.builtin.command: "lola sync"
      args:
        chdir: "{{ playbook_dir }}/.."
      register: lola_sync_output
      changed_when: "lola_sync_output.rc == 0 and ('Synchronized' in lola_sync_output.stdout or 'Installed' in lola_sync_output.stdout)"
      when: lola_check.rc == 0
      failed_when: false

    - name: "Lola | Report Lola AI Package Manager status"
      ansible.builtin.debug:
        msg: >
          {{
            'Lola CLI detected. Executed lola sync against .lola-req successfully.'
            if (lola_check.rc == 0 and lola_sync_output is defined and lola_sync_output.rc == 0)
            else ('Lola sync failed (exit code ' ~ (lola_sync_output.rc | default('unknown')) ~ '). Falling back to local vendored skills in .agents/skills/.')
            if (lola_check.rc == 0 and lola_sync_output is defined and lola_sync_output.rc != 0)
            else 'Lola CLI not detected or air-gapped environment. Using local vendored skills in .agents/skills/.'
          }}
```

### POSIX Shell Script Snippet

```sh
#!/bin/sh
# Idempotent Air-Gapped Lola Sync Wrapper
if command -v lola >/dev/null 2>&1; then
    echo "[INFO] Lola CLI detected. Syncing declarative requirements (.lola-req)..."
    lola sync || echo "[WARN] Lola sync completed with non-zero status; proceeding with local vendored skills."
else
    echo "[INFO] Lola CLI not found. Falling back to local vendored skills under .agents/skills/."
fi
```

---

## 6. Complete Skill Package Summary Matrix (46 Skills)

| Skill Name | Version | Local Path | Status | Operational Capability |
| :--- | :--- | :--- | :--- | :--- |
| `agent-plugin-packager` | `1.0.0` | `.agents/skills/agent-plugin-packager` | `stable` | Packages, validates, and scaffolds DSOM skills and FastMCP servers into porta... |
| `architecture-decision-records` | `1.0.0` | `.agents/skills/architecture-decision-records` | `stable` | Writes and maintains Architecture Decision Records (ADRs) following standard ... |
| `changelog-automation` | `1.0.0` | `.agents/skills/changelog-automation` | `stable` | Automates changelog generation from commits, pull requests, and release notes... |
| `context7-indexer` | `1.0.0` | `.agents/skills/context7-indexer` | `stable` | Governs the use of Context7 for indexing the Sovereign Markdown Palace and re... |
| `council-of-high-intelligence` | `1.0.0` | `.agents/skills/council-of-high-intelligence` | `stable` | Executes a multi-perspective deliberation protocol using specialised AI domai... |
| `cross-platform-translator` | `1.0.0` | `.agents/skills/cross-platform-translator` | `stable` | Analyses a Windows PowerShell (.ps1) or Linux Bash (.sh) script and automatic... |
| `docs-review` | `1.0.0` | `.agents/skills/docs-review` | `stable` | Facilitates systematic review of documentation changes, pull requests, and di... |
| `docs-write` | `1.0.0` | `.agents/skills/docs-write` | `stable` | Assists users in creating and editing documentation that adheres to a clear, ... |
| `docstring` | `1.0.0` | `.agents/skills/docstring` | `stable` | Provides a structured approach for writing precise, maintainer-focussed Pytho... |
| `docx` | `1.0.0` | `.agents/skills/docx` | `stable` | Comprehensive document creation, editing, and analysis for .docx Word files w... |
| `dsom-bootstrap` | `1.0.0` | `.agents/skills/dsom-bootstrap` | `stable` | Executes the DSOM bootstrapping process for a new or existing project by read... |
| `dsom-knowledge-ingester` | `1.0.0` | `.agents/skills/dsom-knowledge-ingester` | `stable` | Executes the Knowledge Ingestion protocol (/learn) inspired by the LLM WIKI c... |
| `dsom-policy-adopter` | `1.0.0` | `.agents/skills/dsom-policy-adopter` | `stable` | Automatically ingests an external research paper or policy document (PDF/Mark... |
| `dsom-project-cloner` | `1.0.0` | `.agents/skills/dsom-project-cloner` | `stable` | Scaffolds a new DSOM project by copying the Sovereign Engine, Universal Gatew... |
| `dsom-release-manager` | `1.0.0` | `.agents/skills/dsom-release-manager` | `stable` | Cuts a formal DSOM release, updates ledgers, tags the repository, and deploys... |
| `dsom-signature-injector` | `1.0.0` | `.agents/skills/dsom-signature-injector` | `stable` | Automatically injects the standard DSOM ownership, timestamp, and GPL v3.0 li... |
| `dsom-state-sync` | `1.0.0` | `.agents/skills/dsom-state-sync` | `stable` | Executes Semantic Compaction locally by analyzing a Git diff and updating cur... |
| `dsom-technical-book-compiler` | `1.0.0` | `.agents/skills/dsom-technical-book-compiler` | `stable` | Compiles complete Diataxis documentation suites and source code repositories ... |
| `dsom-token-calculator` | `1.0.0` | `.agents/skills/dsom-token-calculator` | `stable` | Calculates token counts via tiktoken in isolated uv Python runspaces. |
| `eod-palace-sync` | `1.0.0` | `.agents/skills/eod-palace-sync` | `stable` | The Hibernation (End of Day) ritual to externalise memory into the Palace and... |
| `forensic-log-audit` | `1.0.0` | `.agents/skills/forensic-log-audit` | `stable` | Scrapes raw JSONL transcripts to recover exact commands from historical conve... |
| `git-commit-resolver` | `1.0.0` | `.agents/skills/git-commit-resolver` | `stable` | Automatically resolves invalid or orphaned Git commit IDs referenced in the A... |
| `git-history-scrubber` | `1.0.0` | `.agents/skills/git-history-scrubber` | `stable` | Safely purges sensitive data (IPs, credentials) from Git history using git-fi... |
| `github-actions-snyk-scanner` | `1.0.0` | `.agents/skills/github-actions-snyk-scanner` | `stable` | Sets up a proven Snyk dependency vulnerability scan workflow for DSOM GitHub ... |
| `hyperparameter-tuning-expert` | `1.0.0` | `.agents/skills/hyperparameter-tuning-expert` | `stable` | Analyses, optimises, and debugs learning rates and hyperparameters in deep le... |
| `initialize-gitops` | `1.0.0` | `.agents/skills/initialize-gitops` | `stable` | Establishes the foundational GitOps repository, configures the .gitignore, an... |
| `jules-antigravity-sync` | `1.0.0` | `.agents/skills/jules-antigravity-sync` | `stable` | Procedural SOP for synchronising cognitive context, rule alignment, and histo... |
| `knowledge-base-templates` | `1.0.0` | `.agents/skills/knowledge-base-templates` | `stable` | Provides reusable templates and structural frameworks for generating comprehe... |
| `latex-proposal-compiler` | `1.0.0` | `.agents/skills/latex-proposal-compiler` | `stable` | Compiles a markdown proposal document into a professionally formatted PDF usi... |
| `mintlify-docs-compiler` | `1.0.0` | `.agents/skills/mintlify-docs-compiler` | `stable` | Compiles Sovereign Markdown Palace documents into Mintlify MDX trees and sync... |
| `node-proposal-formatter` | `1.0.0` | `.agents/skills/node-proposal-formatter` | `stable` | Compiles a markdown proposal document into a professionally formatted DOCX fi... |
| `node-slide-generator` | `1.0.0` | `.agents/skills/node-slide-generator` | `stable` | Generates a PowerPoint presentation from a markdown outline using Node.js and... |
| `odp-slide-generator` | `1.0.0` | `.agents/skills/odp-slide-generator` | `stable` | Generates highly styled 3-column Corporate Presentation slides (PPTX/ODP form... |
| `okf-frontmatter-injector` | `1.0.0` | `.agents/skills/okf-frontmatter-injector` | `stable` | Scans a target directory and automatically injects OKF (v0.1/v0.2) YAML front... |
| `okf-v02-adoption-engineer` | `1.2.0` | `.agents/skills/okf-v02-adoption-engineer` | `stable` | Seamlessly converts, validates, and enforces OKF v0.2 standards across worksp... |
| `openapi-spec-generation` | `1.0.0` | `.agents/skills/openapi-spec-generation` | `stable` | Generates, validates, and maintains OpenAPI 3.1+ specifications from code pat... |
| `openwiki-compiler` | `1.0.0` | `.agents/skills/openwiki-compiler` | `stable` | Procedural SOP for executing the native Python OpenWiki Emulator to compile, ... |
| `palace-auditor` | `1.0.0` | `.agents/skills/palace-auditor` | `stable` | A diagnostic skill that crawls the workspace to verify index.md links, identi... |
| `pdf-text-extractor` | `1.0.0` | `.agents/skills/pdf-text-extractor` | `stable` | Safely download external PDF files and extract their text content using curl ... |
| `persona-injector` | `1.0.0` | `.agents/skills/persona-injector` | `stable` | Guides a user to define their Sovereign Persona and safely injects it into th... |
| `proposal-docx-formatter` | `1.0.0` | `.agents/skills/proposal-docx-formatter` | `stable` | Compiles a markdown proposal document into a professionally formatted DOCX fi... |
| `publish-to-blogger` | `1.0.0` | `.agents/skills/publish-to-blogger` | `stable` | Converts a markdown artefact into a clean HTML format suitable for publishing... |
| `render-deployment` | `1.0.0` | `.agents/skills/render-deployment` | `stable` | Configures and manages Render.com deployments via native Free Static Site pat... |
| `sitemap-seo-generator` | `1.0.0` | `.agents/skills/sitemap-seo-generator` | `stable` | Configures and manages sitemap and robots.txt generation to optimize SEO inde... |
| `sod-palace-sync` | `1.0.0` | `.agents/skills/sod-palace-sync` | `stable` | The Reanimation (Start of Day) ritual to load the workspace context and estab... |
| `ssh-passwordless-setup` | `1.0.0` | `.agents/skills/ssh-passwordless-setup` | `stable` | Orchestrates SSH jump configurations for Linux servers. |

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-09-06*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*

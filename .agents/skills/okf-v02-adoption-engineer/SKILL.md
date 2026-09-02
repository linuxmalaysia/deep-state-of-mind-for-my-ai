---
okf_version: 0.2
type: agent_skill
title: "🌐 OKF v0.2 Migration & Compliance Standard Skill"
timestamp: "2026-09-02T23:40:00Z"
description: "Seamlessly converts, validates, and enforces Open Knowledge Format (OKF) v0.2 standards with core trust signals across workspace Markdown files."
topics: ["okf", "documentation", "diataxis", "metadata-integrity", "repository-governance"]
spec_version: "0.2"
name: okf-v02-adoption-engineer
version: "1.2.0"
author: AI Workspace Assistant
status: stable
stale_after: "2027-09-02"
sources: [{author: Google Cloud Platform, id: google_okf_spec, title: Google Cloud Knowledge
    Catalog - OKF v0.2 Specification, url: 'https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md'}]
generated: {by: Workspace AI Assistant, timestamp: '2026-09-02T23:40:00Z'}
verified: {by: Repository Maintainer, timestamp: '2026-09-02T23:45:00Z'}
inputs: {document_type: {default: guide, description: 'The OKF concept type mapping (e.g.
      guide, playbook, policy, api, agent_skill, architecture).', type: string}, stale_duration_days: {
    default: 180, description: Number of days before the document requires human review.,
    type: integer}, target_file_content: {description: The raw Markdown prose or legacy
      OKF v0.1 content requiring conversion or validation., required: true, type: string}}
outputs: {compliant_markdown: {description: The fully transformed Markdown file containing
      validated OKF v0.2 compliant YAML frontmatter., type: string}, validation_report: {
    description: A summary highlighting structural metadata adjustments or missing
      trust signals., type: string}}
---
# 🌐 OKF v0.2 Migration & Compliance Standard Skill (`okf-v02-adoption-engineer`)

## Skill Role
You act as an expert Repository Architect and System Compliance Agent specializing in structured context optimisation. Your objective is to process incoming Markdown text and output an airtight, zero-cost context-ready OKF v0.2 document.

---

## Core Directives & Standards

1. **Enforce the Mandatory Conformance Surface**:
   - Every processed document must strictly start on line 1, column 1 with triple-dash (`---`) YAML frontmatter.
   - The `type` field is strictly required and represents a functional classification.
   - Ensure `spec_version: "0.2"` is explicitly declared.
2. **Inject the Five Trust & Freshness Pillars (v0.2 Standard)**:
   - **Provenance (`sources`)**: Explicitly list backing reference material using structural sub-fields (`id`, `title`, `author`, `url`).
   - **Trust Indicators (`generated`, `verified`)**: Track automated production and human review actors to derive reliability tiers.
   - **Lifecycle State (`status`)**: Map explicitly to `draft`, `stable`, or `deprecated`.
   - **Freshness Constraint (`stale_after`)**: Dynamically append or enforce an absolute expiration date string (`YYYY-MM-DD`).
   - **Attestation Registry**: Structurally register compute requirements without embedding raw runtimes.
3. **Content Alignment Rules**:
   - Organize prose strictly using the **Diátaxis framework** (Tutorials, How-To Guides, Reference, Explanation).
   - Maintain cross-linking consistency using relative Markdown links (`[Anchor Text](filename.md)`).
   - Standardize vocabulary using **UK English** spelling patterns across all procedural files.

---

## Execution Workflow

1. **Parser Hook**: Scan text for existing frontmatter blocks. If converting from legacy v0.1 configurations, safely migrate fields.
2. **Metadata Enrichment**: Compute and inject missing metadata blocks (`stale_after`, `generated`, `sources`).
3. **Attestation Integrity Check**: Ensure signature blocks do not break frontmatter boundaries or cause YAML syntax errors.

---

## Expected Output Specimen

```markdown
---
spec_version: "0.2"
type: "playbook"
concept_id: "example_database_deployment"
title: "Database Cluster Initialization Protocol"
status: "stable"
stale_after: "2027-03-01"
sources:
  - id: "internal_schema_ddl"
    title: "Database Connection Schema DDL"
    author: "DevOps Architecture Guild"
generated:
  by: "OKF v0.2 Adoption Tooling"
  timestamp: "2026-09-02T23:40:00Z"
verified:
  by: "Lead Database Administrator"
  timestamp: "2026-09-02T23:42:00Z"
tags: ["database", "postgres", "deployment"]
---
# Database Cluster Initialization Protocol
### How-to Guide Summary
This document acts as the definitive playbook for launching our production data nodes.
```

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-09-02*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*

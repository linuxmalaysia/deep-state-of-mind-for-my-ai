---
okf_version: 0.1
type: agent_skill
title: "📚 Knowledge Base Templates Skill"
timestamp: "2026-09-02T12:00:00Z"
description: "Provides reusable templates and structural frameworks for generating comprehensive internal wikis, concept maps, and module documentation across single projects and monorepos."
topics: ["knowledge-base", "wiki", "templates", "documentation-structure", "dsom"]
name: knowledge-base-templates
---
# 📚 Knowledge Base Templates Skill (`knowledge-base-templates`)

## Purpose
The `knowledge-base-templates` skill provides reusable templates and structural guidelines for establishing and maintaining codebase knowledge bases, internal wikis, concept maps, and module documentation. It enforces ownership, pruning, and structured categorization across single-project and monorepo architectures.

---

## Core Principles: Ownership, Pruning & Diátaxis

1. **A Knowledge Base Needs Ownership & Pruning**:
   - Every KB document must designate an owner or maintainer team and specify a review cadence or `stale_after` date.
   - Routinely prune, archive, or delete stale or duplicate pages to prevent knowledge decay.
2. **Diátaxis Quadrant Separation**:
   - Categorize wiki pages into distinct quadrants:
     - **Tutorials**: Step-by-step learning paths for onboarding.
     - **How-To Guides**: Goal-focussed instructions for completing specific operational tasks.
     - **Reference**: Technical specifications, parameter dictionaries, and architectural diagrams.
     - **Explanation**: In-depth theoretical discussions, design rationale, and background context.

---

## Standard Template Schemas

### 1. Architecture & Module Overview Template
- **Title & Purpose**: High-level summary of the subsystem or module.
- **Component Diagram**: Mermaid flowchart or sequence diagram.
- **Key File Maps**: Table listing primary source files and their responsibilities.
- **Operational Dependencies**: Upstream services and downstream consumers.

### 2. Operational Runbook Template
- **Overview & Severity**: Impact summary and alert thresholds.
- **Prerequisites**: Access levels, tools, and CLI requirements.
- **Step-by-Step Remediation**: Sequential recovery instructions.
- **Verification**: Commands to confirm resolution.

---

## When to Use This Skill

- Setting up an internal repository wiki or knowledge base structure.
- Creating onboarding guides, architecture maps, or troubleshooting runbooks.
- Organizing monorepo documentation to maintain cross-module consistency.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-09-02*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*

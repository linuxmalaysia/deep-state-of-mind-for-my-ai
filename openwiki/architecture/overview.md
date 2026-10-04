---
okf_version: 0.2
type: documentation
title: "DSOM Scope & Three-Pillar Operational Model"
timestamp: "2026-09-20T03:29:08Z"
topics: ["openwiki", "architecture", "overview", "pillars"]
resource: "/openwiki/architecture/overview.md"
sources: [{author: Harisfazillah Jamel (LinuxMalaysia), id: dsom-core-spec, resource: /docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md,
  title: Deep State of Mind (DSOM) Governance Architecture, type: architecture_spec}, {author: Google Cloud Platform, id: google-okf-v02-spec, resource: 'https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md',
  title: Google Cloud Open Knowledge Format (OKF) v0.2 Specification, type: external_spec}]
spec_version: "0.2"
description: "DSOM scope, three-pillar operating model, component boundaries, and authoritative sources."
---
# DSOM Scope & Three-Pillar Operational Model

The **Deep State of Mind (DSOM)** protocol is a metacognitive governance framework designed to establish absolute operational alignment, digital sovereignty, and persistent context continuity between human operators and AI agents.

## 🏛️ The Three-Pillar Operating Model

The architecture of DSOM is structured around three foundational pillars:

```mermaid
flowchart TD
    GOV["Pillar 1: Metacognitive Governance<br/>Constitutional AGENTS.md Laws"] --> MEM["Pillar 2: Spatial Memory<br/>Brain & Palace"]
    GOV --> EXEC["Pillar 3: Absolute Execution<br/>Ansible & Tools"]
    MEM <--> EXEC
```

1. **Pillar 1: Metacognitive Governance (The Mind):**
   - Established by the master constitution under `.agents/AGENTS.md`.
   - Governs AI self-reflection, behaviour guidelines, token budgeting, and the 27 operational rules.

2. **Pillar 2: Spatial Memory (The Palace):**
   - Co-located in `.agents/brain/` and compiled inside the `docs/` Palace.
   - Prevents context decay across ephemeral chat session boundaries through structured daily reanimation and hibernation rituals.

3. **Pillar 3: Absolute Execution (The Body):**
   - Implemented via declarative automation (Ansible baseline) and idempotent operational wrappers (`tools/`).
   - Ensures that all technical instructions translate directly to deterministic local environment actions.

## 🧱 Component Boundaries & Authoritative Sources

- **Authoritative Source of Truth:** The active repository files and Git history.
- **Cognitive Control Plane:** The `.agents/` folder, which is strictly managed and preserved across sessions.
- **External Public Interfaces:** Render blueprints, Read the Docs configuration, and GitHub Actions CD pipelines.

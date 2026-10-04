---
okf_version: 0.2
type: architecture_concept
title: Clean Architecture
timestamp: "2026-06-19T14:00:00Z"
topics: ["dsom", "brain", "concept"]
resource: "/.agents/brain/wings/wing_dsom_core/hall_facts/room_clean_architecture/closet.md"
sources: [{author: Harisfazillah Jamel (LinuxMalaysia), id: dsom-core-spec, resource: /docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md,
  title: Deep State of Mind (DSOM) Governance Architecture, type: architecture_spec}, {author: Google Cloud Platform, id: google-okf-v02-spec, resource: 'https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md',
  title: Google Cloud Open Knowledge Format (OKF) v0.2 Specification, type: external_spec}]
spec_version: "0.2"
description: Distilled knowledge for Clean Architecture
---
# 🚪 Closet: Room Clean Architecture (The Skeleton)

This closet contains the **distilled architectural truths** for the **DSOM** framework. It enforces the **Inward Dependency Rule** and ensures **Sovereign Portability**.

---

## 🏛️ Layered Separation (Concentric Circles)

1. **Entities (Sovereign Core):** Pure domain logic (e.g., `SitemapNode`). No external awareness.
2. **Use Cases (Interactors):** Orchestration and data flow logic.
3. **Interface Adapters:** Translators (JSON builders, CLI controllers).
4. **Frameworks & Drivers (The Edge):** Volatile tools: Podman, RHEL, SQL, Ansible Playbooks.

---

## ⚖️ The Dependency Law
*   **Source code dependencies MUST only point inwards.** 
*   Outer layers (Drivers) can touch Inner layers (Entities), but **Entities NEVER know about the Drivers**.
*   This ensures that the project remains portable: we can swap Podman for Kubernetes or Python for Node.js without touching the **Entity Truth**.

---

## 🔗 Retrieval Reference (The Drawer)
- **Primary Drawer:** [walkthrough.md:L161-174](file:///d:/Users/LinuxMalaysia/Projects/deep-state-of-mind-for-my-ai/.agents/brain/walkthrough.md#L161-L174)
- **Detailed Design:** [walkthrough.md:L225-L230](file:///d:/Users/LinuxMalaysia/Projects/deep-state-of-mind-for-my-ai/.agents/brain/walkthrough.md#L225-L230)

---
*Last Refined: 2026-04-08 | Hall: hall_facts | Wing: wing_dsom_core*

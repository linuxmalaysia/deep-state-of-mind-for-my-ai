---
okf_version: 0.1
type: documentation
title: "Explanation: Diátaxis Framework Adoption"
timestamp: "2026-08-13T12:00:00Z"
topics: ["dsom", "explanation", "diataxis", "documentation"]
---
# Diátaxis framework adoption in DSOM

An architectural overview explaining the adoption, structure, and benefits of the Diátaxis documentation framework in the DSOM project.

## What is Diátaxis?

The **Diátaxis Framework** is a systematic approach to technical documentation. It categorises files based on their purpose and user intent, separating content into four distinct quadrants:

```text
               USER INTENT
        Learning        Practical
      +---------------+---------------+
      |   TUTORIALS   | HOW-TO GUIDES |
Acq.  |  (Learning-   |  (Problem-    |
      |   oriented)   |   oriented)   |
      +---------------+---------------+
      |  EXPLANATION  |   REFERENCE   |
Und.  |  (Concept-    |  (Information-|
      |   oriented)   |   oriented)   |
      +---------------+---------------+

```

## Why adopt Diátaxis in DSOM?

Historically, AI agent tool documentation was mixed with procedural runbooks. This led to high cognitive load and excessive token consumption.

Adopting Diátaxis provides three main benefits:
- **Reduces token costs:** Separate reference files allow AI agents to fetch precise factual details without reading conversational or tutorial text.
- **Speeds up onboarding:** Human developers can follow step-by-step lessons without getting bogged down in low-level arguments.
- **Clarifies purpose:** Developers and writers know exactly where a new document belongs based on the user's intent.

## Quadrant mappings in DSOM

Our documentation Palace is structured cleanly inside `docs/` using the four Diátaxis folders:

1. **Tutorials (`docs/tutorials/`):**
   - Guided learning lessons for beginners.
   - Example: [Getting Started with DSOM Tools](../tutorials/getting-started.md).

2. **How-To Guides (`docs/how-to/`):**
   - Goal-oriented, step-by-step instructions for specific real-world tasks.
   - Example: [Run the FastMCP Server](../how-to/run-fastmcp-server.md).

3. **Reference (`docs/reference/`):**
   - Factual description, API signatures, and configurations for all 8 Python scripts.
   - Example: [apply_okf_frontmatter.py Reference](../reference/apply_okf_frontmatter.md).

4. **Explanation (`docs/explanation/`):**
   - Context, architecture, and design rationale behind our components.
   - Example: [OpenWiki & FastMCP Architecture](openwiki-mcp-architecture.md).

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-14*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*

---
okf_version: 0.1
type: agent_skill
title: "✍️ Documentation Writer Skill"
timestamp: "2026-09-02T12:00:00Z"
description: "Assists users in creating and editing documentation that adheres to a clear, conversational, and user-focussed writing style with reader intent."
topics: ["documentation", "writing", "markdown", "technical-writing", "dsom"]
name: docs-write
---
# ✍️ Documentation Writer Skill (`docs-write`)

## Purpose

The `docs-write` skill assists users and AI agents in creating and editing documentation that adheres to a clear, conversational, and user-focussed writing style. It addresses common challenges faced by technical writers and engineers when conveying complex technical information in an accessible manner, ensuring documentation is engaging, structured, and easy to navigate.

---

## Key Principles & Reader Intent

1. **Ask Who the Reader Is**: Identify the target audience (new user needing orientation, developer integrating an API, or engineer debugging operational context) before drafting.
2. **Focus on Audience Needs**: Prefer active voice, precise nouns, concrete examples, and predictable structure over decorative writing.
3. **Inspect Real Context**: Always inspect product behaviour, source code paths, existing documentation, and release notes rather than inventing plausible prose.
4. **Mark Unverified Claims**: Clearly flag any detail that could not be verified directly against source code or test execution.

---

## When to Use This Skill

- Drafting new technical guides, tutorials, or reference documents in Markdown or MDX.
- Updating existing documentation pages to reflect recent software releases or UI/API changes.
- Standardising writing style and tone across project documentation repositories.

---

## Writing & Editing Process

### Step 1: Identify Reader Intent & Inputs

Confirm inputs before writing:
- Targeted reader persona and level of expertise.
- Exact code paths, CLI commands, or API parameters.
- Existing documentation pages affected by the change.

### Step 2: Drafting

- Use active voice and simple, direct UK English prose.
- Present instructions as explicit commands.
- Include concrete code or CLI examples with realistic outputs.

### Step 3: Formatting & Structure

- Structure material following the **Diátaxis framework** (Tutorial, How-To Guide, Reference, or Explanation).
- Maintain clear, descriptive heading hierarchies (MD022/MD031 compliant with blank lines around headings and fenced code blocks).
- Avoid vague headings like "Overview" or "Miscellaneous". Use action-oriented titles.

---

## Common Pitfalls to Avoid

- **Overly formal or bureaucratic tone**: Keep language conversational and direct.
- **Non-functional code examples**: Ensure code snippets and commands are tested and syntax-valid.
- **Speculative prose**: Never guess parameter defaults or response fields; verify with source files.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-09-02*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*

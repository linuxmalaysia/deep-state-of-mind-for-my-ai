---
okf_version: 0.1
type: agent_skill
title: "🏛️ Architecture Decision Records Skill"
timestamp: "2026-09-02T12:00:00Z"
description: "Writes and maintains Architecture Decision Records (ADRs) following standard MADR formats to document significant technical choices, tradeoffs, and consequences."
topics: ["adr", "architecture", "decision-records", "madr", "dsom"]
name: architecture-decision-records
---
# 🏛️ Architecture Decision Records Skill (`architecture-decision-records`)

## Purpose
The `architecture-decision-records` skill provides a structured framework for documenting significant technical decisions through Architecture Decision Records (ADRs). It captures the context, rationale, trade-offs, and consequences behind architectural choices, ensuring historical clarity and facilitating decision reviews.

---

## When to Write an ADR

Write an ADR when making significant architectural or technological choices, such as:
- Selecting or replacing a database technology, framework, or message broker.
- Adopting a new system-wide security, deployment, or state synchronization pattern.
- Making trade-offs between latency, consistency, complexity, and operational cost.

*Do NOT write an ADR for*: Minor dependency version bumps, bug fixes, or localised code refactorings.

---

## Standard ADR Format (MADR Schema)

```markdown
# [Short Title of Solved Problem and Decision]

* Status: [proposed | accepted | rejected | deprecated | superseded by ADR-XXXX]
* Deciders: [List of stakeholders involved]
* Date: YYYY-MM-DD

## Context and Problem Statement
Describe the technical context and the specific problem requiring a decision.

## Decision Drivers
* Driver 1 (e.g. Latency requirements)
* Driver 2 (e.g. License compatibility)

## Considered Options
* Option 1: Description
* Option 2: Description

## Decision Outcome
Chosen option: **[Option 1]**, because [summary of primary justification].

### Positive Consequences
* Consequence 1
* Consequence 2

### Negative Consequences / Trade-offs
* Consequence 1

## Pros and Cons of Options

### Option 1
* Good, because [argument]
* Bad, because [argument]

### Option 2
* Good, because [argument]
* Bad, because [argument]
```

---

## Best Practices

- **Durable Explanation**: Focus on *why* the decision was made given the constraints at the time.
- **Explicit Triggers**: State what conditions or metrics would prompt the team to revisit the decision in the future.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-09-02*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*

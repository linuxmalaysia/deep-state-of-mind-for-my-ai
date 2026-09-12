---
okf_version: 0.2
type: explanation
title: "Attested Computations in Open Knowledge Format (OKF v0.2): Ensuring Verifiable AI Knowledge"
timestamp: "2026-09-06T12:00:00Z"
topics: ["okf", "attested-computation", "data-governance", "ai-agents", "verification", "dsom"]
spec_version: "0.2"
concept_id: attested_computations_okf
status: stable
stale_after: "2027-03-06"
description: "Explores Attested Computations in OKF v0.2, bridging metrics definitions and runnable queries so AI agents and consumers can mechanically verify AI-generated insights."
sources: [{author: RedLineSoft AI Engineering Blog, id: redlinesoft_okf_attested_computations,
  title: 'Attested Computations in Open Knowledge Format (OKF): Ensuring Verifiable
    AI Knowledge', url: 'https://blog.redlinesoft.net/posts/attested-computations-in-open-knowledge-format/'}, {author: Google Cloud Platform, id: google_okf_spec, title: Open Knowledge Format
    (OKF) Specification v0.2, url: 'https://cloud.google.com/blog/products/databases/announcing-open-knowledge-format-for-gen-ai'}]
generated: {by: Google Jules, timestamp: '2026-09-06T12:00:00Z'}
verified: {by: DSOM Protocol Guild, timestamp: '2026-09-06T12:00:00Z'}
---
# 🔐 Attested Computations in Open Knowledge Format (OKF v0.2): Ensuring Verifiable AI Knowledge

## Overview & Foundational Challenge

When AI agents answer complex analytical questions—such as calculating fiscal revenue, cluster bandwidth utilization, or gross profit—knowing what a metric means is only half the battle. In production AI environments, human operators and automated governance gates must also guarantee that the resulting figure was produced using the exact, sanctioned computation rather than agent improvisation or hallucinated query execution.

In Open Knowledge Format (OKF) v0.2, this challenge is solved through **Attested Computations** (`type: Attested Computation`).

Rather than embedding raw SQL queries, shell commands, or Python execution scripts directly inside narrative documentation or relying on black-box LLM SQL generation, OKF separates the semantic definition of a concept from its execution and attestation contract.

---

## What is an Attested Computation?

An Attested Computation is a standalone, first-class OKF concept (`type: Attested Computation`) that carries a sanctioned, deterministic way to compute a value. It specifies everything required for execution and mechanical verification:

````yaml
---
okf_version: 0.2
spec_version: "0.2"
concept_id: "revenue_for_fiscal_year"
type: "Attested Computation"
title: "Revenue for fiscal year"
timestamp: "2026-06-25T09:00:00Z"
topics: ["revenue", "bigquery", "attested-computation", "finance"]
description: "Recognized revenue for a fiscal year, per Finance's definition."
status: "stable"
stale_after: "2026-09-23"
runtime: "bigquery"
parameters:
  - name: "year"
    type: "integer"
    required: true
executor:
  resource: "references/skills/run-on-bq.md"
  receipt: ["job_id", "executed_sql", "result"]
attester:
  resource: "references/attesters/sql-equality.py"
generated:
  by: "reference_agent/gemini-2.5-pro"
  timestamp: "2026-06-20T22:53:05Z"
verified:
  by: "human:ahormati"
  timestamp: "2026-06-25T09:00:00Z"
sources:
  - id: "rev-policy"
    title: "Revenue recognition policy"
    author: "Finance Guild"
    url: "https://wiki.acme.internal/finance/revenue-recognition"
---

# Computation

```sql
SELECT SUM(amount) AS revenue
FROM finance.recognized_revenue
WHERE fiscal_year = @year
```

The computation binds only the declared `parameters`, per the recognition policy.[^rev-policy]

[^rev-policy]: Revenue recognition policy
````

---

## Core Principles & Design Benefits

### 1. Runtime Binding
The `runtime` property (e.g. `bigquery`, `postgres`, `dbt`, `python`, `bash`) defines precisely how parameters are bound and interpreted. Autonomous agents supply valid values for declared parameters without modifying the underlying query string.

### 2. Reusability Across the Workspace
A single sanctioned Attested Computation can back multiple metrics, dashboards, AI agent toolcalls, and operational playbooks across the organisation.

### 3. Independent Trust Signals
Each computation maintains its own `verified`, `stale_after`, and `attester` metadata fields. This ensures individual metrics verify independently and automatically expire when underlying business policies or schemas evolve.

---

## Contract Structure & Key Components

1. **`runtime`**: Identifies the execution environment (`bigquery`, `postgres`, `dbt`, `python`, `bash`).
2. **`parameters`**: Typed, named variables the AI agent is permitted to supply. Agents MUST NOT alter the underlying computation query itself.
3. **`executor`**: Defines execution instructions (`resource`) and required evidence elements returned in the receipt (`receipt`).
4. **`attester`**: Points to deterministic (no-LLM) code that inspects the execution receipt and returns an unambiguous pass/fail attestation verdict.

---

## The 6-Step Mechanical Execution & Attestation Lifecycle

The OKF specification separates specification from runtime execution in 6 deterministic steps:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│              Attested Computation Execution Lifecycle                  │
│                                                                         │
│  ┌────────────┐     ┌────────────┐     ┌────────────────┐               │
│  │ 1. Discover│ ──> │  2. Load   │ ──> │ 3. Parameterize│               │
│  └────────────┘     └────────────┘     └───────┬────────┘               │
│                                                │                        │
│                                                ▼                        │
│  ┌────────────┐     ┌────────────┐     ┌────────────────┐               │
│  │  6. Gate   │ <── │ 5. Attest  │ <── │   4. Execute   │               │
│  └────────────┘     └────────────┘     └────────────────┘               │
└─────────────────────────────────────────────────────────────────────────┘
```

1. **Discover:** Agents locate the computation via `type: Attested Computation` or via links from narrative metric docs.
2. **Load:** The agent reads the frontmatter contract and computation block.
3. **Parameterize:** The agent supplies valid values for declared parameters (e.g., `year: 2026`).
4. **Execute:** The executor runs the bound computation and returns an evidence receipt (e.g., job ID, executed query, and result payload).
5. **Attest:** The agent or system runs the deterministic attester script over the receipt to verify that the query executed matched the sanctioned computation without unauthorized modifications.
6. **Gate:** The governance system surfaces the verified result or blocks stale/failing computations.

---

## Verification vs. Attestation

It is crucial to distinguish between doc-level verification and runtime attestation:

* **Doc-Level Verification (`verified`):** Confirms that the metric definition matches business policy (stored in the document bundle, updated periodically during human or automated audits).
* **Runtime Attestation (`attester`):** Confirms that a specific runtime execution produced the value correctly (per-call, un-stored receipt evaluation executed by deterministic code).

---

## Conclusion & Impact on DSOM v0.2

Attested Computations in OKF v0.2 transform AI-driven analytics and operational telemetry from a "trust me" black box into a verifiable, deterministic science. By establishing clear contracts between definitions, parameters, executors, and deterministic attesters, organisations deploying DSOM digital twins can operate autonomous agents with absolute confidence in data integrity.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-09-06*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*

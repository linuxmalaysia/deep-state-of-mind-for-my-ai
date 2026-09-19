---
okf_version: 0.2
type: agent_skill
title: Council of High Intelligence Multi-Agent Consensus Engine
timestamp: "2026-09-19T00:00:00Z"
description: "Executes a multi-perspective deliberation protocol using specialized AI domain personas (Domain Experts, Security Auditor, Systems Architect, Pragmatist) to review complex architectural decisions, evaluate trade-offs, and synthesize unified consensus decisions."
topics: ["council", "multi-agent", "consensus", "deliberation", "antigravity"]
name: council-of-high-intelligence
spec_version: "0.2"
status: stable
stale_after: "2027-01-01"
sources: [{author: 0xnyk, id: council_repo, title: Council of High Intelligence, url: 'https://github.com/0xnyk/council-of-high-intelligence'}]
generated: {by: Google Jules & Antigravity, timestamp: '2026-09-19T00:00:00Z'}
allowed_tools: ["file_system_write", "file_system_read", "bash"]
tags: ["council", "multi-agent", "consensus", "deliberation", "antigravity"]
---
# Skill: Council of High Intelligence Multi-Agent Consensus Engine

## 1. Overview & Capability Scope
The **Council of High Intelligence** skill orchestrates a structured, multi-persona deliberation workflow. Instead of relying on a single AI persona's output, this skill simulates a panel of specialized domain experts who independently evaluate a prompt, debate trade-offs, perform cross-examination, and reach a unified, resilient consensus decision.

<Image src="image_agent_tag_3439772652216829028" alt="Multi-agent collaboration ecosystem workflow steps including Planning, Routing, Execution, Validation, and Optimisation" caption="Five-stage multi-agent deliberation framework" />

---

## 2. Council Persona Definitions
When activated, the agent impersonates or delegates to four distinct council members (or the full 18-member panel depending on execution mode):

1. **The Senior Systems Architect:** Focuses on scalability, HA-readiness, data flows, zero-global state patterns, and long-term technical debt.
2. **The Chief Security Officer (CSO):** Focuses on Fine-Grained Access Control (FGAC), attack vectors, zero-trust boundaries, credential management, and compliance.
3. **The Pragmatic Staff Engineer:** Focuses on implementation velocity, developer experience, operational overhead, dependencies, and immediate business value.
4. **The Domain Specialist:** Tailored dynamically to the prompt (e.g., Data Engineer, ML Ops Lead, Database Administrator).

---

## 3. Activation Criteria & Triggers
Trigger this skill automatically whenever a user request or issue requires multi-faceted analysis or high-stakes decision-making:

- **Architectural Decision Records (ADRs):** Major structural refactoring, database migrations, or framework replacements.
- **Security & Infrastructure Audits:** Evaluating trade-offs between speed, security, and infrastructure complexity.
- **Conflicting Requirements:** Problems where performance, cost, and developer experience strongly compete.
- **Explicit Invocations:** Requests containing phrases like `"run council review"`, `"evaluate across personas"`, or `"deliberate architectural choices"`.

---

## 4. Attested Computations & Deliberation Protocol

In accordance with OKF v0.2 Attested Computations (`type: Attested Computation`), council deliberations bridge definition contracts and execution contracts through runtime bindings, parameters, and deterministic attesters across a 6-step lifecycle (Discover, Load, Parameterize, Execute, Attest, Gate).

<Sequence>
  <Step title="Phase 1: Independent Assessment" subtitle="Isolated evaluation without bias">
    Deconstruct the user prompt into domain-specific sub-questions. Each council persona evaluates the prompt in isolation and records their independent position, key risks, and recommendations.
  </Step>

  <Step title="Phase 2: Debate & Cross-Examination" subtitle="Challenging assumptions and trade-offs">
    Compare the four persona assessments. Identify contradictions (e.g., Security vs. Velocity) and explicitly debate edge cases, security vulnerabilities, and operational costs using evidence labeling (`FACT`, `INFERENCE`, `ASSUMPTION`, `UNKNOWN`).
  </Step>

  <Step title="Phase 3: Consensus Synthesis" subtitle="Merging perspectives into a single decision">
    Reconcile opposing views using a weighted consensus model. Where trade-offs exist, document the compromise, explicit non-goals, and mitigation strategies.
  </Step>

  <Step title="Phase 4: Artifact Generation & Attestation" subtitle="Persisting the Council decision">
    Write the final Council Decision Record into a Markdown artifact inside the repository workspace (e.g., `docs/decisions/` or PR notes) and record cryptographic attestation proofs.
  </Step>
</Sequence>

---

## 5. Mandatory Artifact Output Structure

Every Council execution must write its findings using the following compact structure:

```markdown
# Council Decision Record (CDR)

## 1. Executive Summary
Brief summary of the issue and the final unified decision reached by the Council.

## 2. Persona Perspectives Matrix

| Persona | Primary Stance | Key Recommendation | Critical Risk Flagged |
| :--- | :--- | :--- | :--- |
| **Systems Architect** | ... | ... | ... |
| **Chief Security Officer** | ... | ... | ... |
| **Pragmatic Engineer** | ... | ... | ... |
| **Domain Specialist** | ... | ... | ... |

## 3. Deliberation & Trade-off Debate
- **Security vs. Velocity:** Detail how opposing priorities were reconciled.
- **Architecture vs. Cost:** Detail infrastructure budget and maintenance compromises.

## 4. Final Council Verdict & Action Plan
1. **Immediate Step:** Concrete action 1.
2. **Mitigation Strategy:** How identified risks will be neutralized.
```

---

## 6. System Constraints & Guardrails

* **No Sycophancy:** Personas must not prematurely agree with each other; tension during Phase 2 is mandatory.
* **Compact Frontmatter:** Any YAML arrays (`tags: ["a", "b"]`) **MUST** use compact single-line syntax per AGENTS.md rules.
* **Traceability:** Every final recommendation must cite which persona originated or advocated for it.
* **Attestation Binding:** Execution contracts must verify evidence classification tags before committing decision records to the repository ledger.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-09-19*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*

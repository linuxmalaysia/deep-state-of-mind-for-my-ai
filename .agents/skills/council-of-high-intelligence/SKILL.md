---
name: council-of-high-intelligence
version: "1.1.0"
description: "Executes a multi-perspective deliberation protocol using specialised AI domain personas (Domain Experts, Security Auditor, Systems Architect, Pragmatist, Sovereign FOSS Architect) to review complex architectural decisions, evaluate trade-offs, and synthesize unified consensus decisions."
topics: ["council", "multi-agent", "consensus", "deliberation", "antigravity"]
author: "Harisfazillah Jamel (LinuxMalaysia)"
license: "GPL-3.0-or-later"
okf_version: 0.2
type: agent_skill
status: stable
stale_after: "2027-01-01"
title: Council of High Intelligence Multi-Agent Consensus Engine
timestamp: "2026-11-01T00:08:30Z"
resource: "/.agents/skills/council-of-high-intelligence/SKILL.md"
sources: [{author: 0xnyk, id: council_repo, resource: "https://github.com/0xnyk/council-of-high-intelligence", title: Council of High Intelligence, url: "https://github.com/0xnyk/council-of-high-intelligence"}, {author: "Harisfazillah Jamel (LinuxMalaysia)", id: council_persona_harisfazillah, resource: "docs/reference/COUNCIL-PERSONA-HARISFAZILLAH-JAMEL.md", title: "Council Persona Specification: Harisfazillah Jamel", url: "https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai/blob/main/docs/reference/COUNCIL-PERSONA-HARISFAZILLAH-JAMEL.md"}]
generated: {by: "Google Jules & Antigravity", timestamp: "2026-11-01T00:08:30Z"}
spec_version: "0.2"
allowed_tools: ["file_system_write", "file_system_read", "bash"]
tags: ["council", "multi-agent", "consensus", "deliberation", "antigravity"]
---
# Skill: Council of High Intelligence Multi-Agent Consensus Engine

## 1. Overview & Capability Scope

The **Council of High Intelligence** skill orchestrates a structured, multi-persona deliberation workflow. Instead of relying on a single AI persona's output, this skill simulates a panel of specialised domain experts who independently evaluate a prompt, debate trade-offs, perform cross-examination, and reach a unified, resilient consensus decision.

<Image src="image_agent_tag_3439772652216829028" alt="Multi-agent collaboration ecosystem workflow steps including Planning, Routing, Execution, Validation, and Optimisation" caption="Five-stage multi-agent deliberation framework" />

---

## 2. Council Persona Definitions & Member Roster

### Member Roster

The council integrates established analytical thinkers alongside sovereign infrastructure architects:

- `aristotle`: Categories & formal structure
- `socrates`: Dialectical assumption testing
- `sun-tzu`: Positioning & terrain
- `lovelace`: Mathematical purity & formal systems
- `aurelius`: Moral cost & duty
- `machiavelli`: Realpolitik & power dynamics
- `lao-tzu`: Emergence & non-action
- `feynman`: Empirical debugging & plain clarity
- `torvalds`: Shipping & pragmatic code maintainability
- `musashi`: Decisive execution & timing
- `watts`: Reframing & double binds
- `karpathy`: Empirical ML behaviour & developer ergonomics
- `sutskever`: Scaling laws & frontier AI safety
- `kahneman`: Bias & heuristic detection
- `meadows`: Feedback loops & systems leverage
- `munger`: Mental model lattices & inversion
- `taleb`: Antifragility & tail risk
- `rams`: User clarity & essentialism
- `harisfazillah`: Sovereign FOSS systems architecture, digital sovereignty, enterprise Linux HA, and COO realism

### Primary Operational Personas

When activated in default or focused modes, the agent impersonates or delegates to core council roles:

1. **The Senior Systems Architect:** Focuses on scalability, HA-readiness, data flows, zero-global state patterns, and long-term technical debt.
2. **The Chief Security Officer (CSO):** Focuses on Fine-Grained Access Control (FGAC), attack vectors, zero-trust boundaries, credential management, and compliance.
3. **The Pragmatic Staff Engineer:** Focuses on implementation velocity, developer experience, operational overhead, dependencies, and immediate business value.
4. **The Domain Specialist:** Tailored dynamically to the prompt (e.g., Data Engineer, ML Ops Lead, Database Administrator).
5. **The Sovereign FOSS Systems Architect (`harisfazillah` / LinuxMalaysia):** Focuses on digital sovereignty, vendor de-risking, POSIX compliance, open-source high-availability clustering, DevSecOps reality, and calibrated 5-year TCO.

---

## 3. Deliberation Modes, Domain Triads & Profiles

### Deliberation Modes
- **Full Mode (`--full`):** Multi-phase adversarial protocol across all roster members.
- **Quick Mode (`--quick`):** Rapid 3-phase restate-analyse-stance sequence without explicit cross-examination round.
- **Duo Mode (`--duo`):** Direct 2-member dialectic highlighting core polarity tensions.
- **Triad Mode (`--triad <domain>`):** Domain-specific 3-member panels.

### Custom Domain Triads

| Triad Domain | Members | Strategic Focus |
| :--- | :--- | :--- |
| `sovereignty` | `harisfazillah`, `torvalds`, `taleb` | Sovereign autonomy, open standards, and antifragile self-hosting. |
| `enterprise-infrastructure` | `harisfazillah`, `torvalds`, `munger` | Production maintainability, hardware economics, and inversion. |
| `public-sector-tech` | `harisfazillah`, `machiavelli`, `meadows` | Statutory compliance, institutional power, and systemic feedback loops. |
| `architecture` | `harisfazillah`, `aristotle`, `feynman` | Systematic classification, empirical validation, and modular decoupling. |
| `security` | `CSO`, `Systems Architect`, `harisfazillah` | Zero-trust boundaries, defense-in-depth, and digital sovereignty. |

### Deliberation Profiles
- `classic`: Balanced architectural assessment and historical mental models.
- `exploration-orthogonal`: Divergent perspectives testing radical assumptions (`harisfazillah` included).
- `execution-lean`: Pragmatic, shipping-focused velocity with strict operational maintainability (`harisfazillah` included).

---

## 4. Activation Criteria & Triggers

Trigger this skill automatically whenever a user request or issue requires multi-faceted analysis or high-stakes decision-making:

- **Architectural Decision Records (ADRs):** Major structural refactoring, database migrations, or framework replacements.
- **Security & Infrastructure Audits:** Evaluating trade-offs between speed, security, and infrastructure complexity.
- **Conflicting Requirements:** Problems where performance, cost, and developer experience strongly compete.
- **Explicit Invocations:** Requests containing phrases like `"run council review"`, `"evaluate across personas"`, or `"deliberate architectural choices"`.

---

## 5. Attested Computations & Deliberation Protocol

In accordance with OKF v0.2 Attested Computations (`type: Attested Computation`), council deliberations bridge definition contracts and execution contracts through runtime bindings, parameters, and deterministic attesters across a 6-step lifecycle (Discover, Load, Parameterize, Execute, Attest, Gate).

<Sequence>
  <Step title="Phase 1: Independent Assessment" subtitle="Isolated evaluation without bias">
    Deconstruct the user prompt into domain-specific sub-questions. Each council persona evaluates the prompt in isolation and records their independent position, key risks, and recommendations.
  </Step>

  <Step title="Phase 2: Debate & Cross-Examination" subtitle="Challenging assumptions and trade-offs">
    Compare persona assessments. Identify contradictions (e.g., Security vs. Velocity, Proprietary SaaS vs. Sovereign On-Prem) and explicitly debate edge cases using evidence labeling (`FACT`, `INFERENCE`, `ASSUMPTION`, `UNKNOWN`).
  </Step>

  <Step title="Phase 3: Consensus Synthesis" subtitle="Merging perspectives into a single decision">
    Reconcile opposing views using a weighted consensus model across personas. Where trade-offs exist, document the compromise, explicit non-goals, and mitigation strategies.
  </Step>

  <Step title="Phase 4: Artifact Generation & Attestation" subtitle="Persisting the Council decision">
    Write the final Council Decision Record into a Markdown artifact inside the repository workspace (e.g., `docs/decisions/` or PR notes) with valid OKF v0.2 frontmatter and cryptographic attestation proofs.
  </Step>
</Sequence>

---

## 6. Mandatory Artifact Output Structure

Every Council execution must write its findings using the following compact structure with valid OKF frontmatter:

```markdown
---
okf_version: 0.2
type: documentation
title: "Council Decision Record: <Topic>"
timestamp: "<ISO_8601_TIMESTAMP>"
topics: ["council", "decision", "architecture"]
spec_version: "0.2"
---

# Council Decision Record (CDR)

## 1. Executive Summary
Brief summary of the issue and the final unified decision reached by the Council.

## 2. Persona Perspectives Matrix

| Persona | Primary Stance | Key Recommendation | Critical Risk Flagged |
| :--- | :--- | :--- | :--- |
| **Systems Architect** | ... | ... | ... |
| **Chief Security Officer** | ... | ... | ... |
| **Pragmatic Engineer** | ... | ... | ... |
| **Sovereign FOSS Architect** | ... | ... | ... |
| **Domain Specialist** | ... | ... | ... |

## 3. Deliberation & Trade-off Debate
- **Security vs. Velocity:** Detail how opposing priorities were reconciled.
- **Sovereignty vs. Cloud Lock-in:** Detail data sovereignty and long-term TCO trade-offs.
- **Architecture vs. Cost:** Detail infrastructure budget and maintenance compromises.

## 4. Final Council Verdict & Action Plan
1. **Immediate Step:** Concrete action 1.
2. **Mitigation Strategy:** How identified risks will be neutralized.
```

---

## 7. System Constraints & Guardrails

* **No Sycophancy:** Personas must not prematurely agree with each other; tension during Phase 2 is mandatory.
* **Compact Frontmatter:** Any YAML arrays (`tags: ["a", "b"]`) **MUST** use compact single-line syntax per AGENTS.md rules.
* **Traceability:** Every final recommendation must cite which persona originated or advocated for it.
* **Attestation Binding:** Execution contracts must verify evidence classification tags before committing decision records to the repository ledger.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-11-01*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*

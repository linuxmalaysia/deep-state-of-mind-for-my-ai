---
okf_version: 0.2
type: governance_proposal
title: "Council of High Intelligence: DSOM Adoption Proposal & Architectural Design"
timestamp: "2026-09-19T00:00:00Z"
topics: ["dsom", "governance", "council-of-intelligence", "deliberation", "multi-agent", "tri-phasic-mind", "attested-computations"]
spec_version: "0.2"
description: "Architectural blueprint and governance proposal for adopting the 18-member Council of High Intelligence multi-perspective deliberation framework into the DSOM engine."
resource: "file:///docs/governance/COUNCIL-OF-HIGH-INTELLIGENCE-DSOM-ADOPTION-PROPOSAL.md"
status: stable
stale_after: "2027-09-19"
sources: [{author: 0xnyk, id: council_repo, title: Council of High Intelligence, url: 'https://github.com/0xnyk/council-of-high-intelligence'}, {author: Redlinesoft, id: attested_computations_post, title: Attested Computations
    in Open Knowledge Format, url: 'https://blog.redlinesoft.net/posts/attested-computations-in-open-knowledge-format/'}]
generated: {by: Google Jules & Antigravity, timestamp: '2026-09-19T00:00:00Z'}
---
# 🏛️ Council of High Intelligence: DSOM Adoption Proposal & Architectural Design

> **Entry Point 24:** This document serves as the Master Governance Proposal for adopting structured multi-perspective deliberation into the Deep State of Mind (DSOM) framework. See [START-HERE.md](../../START-HERE.md) for the master onboarding roadmap.

---

## Executive Summary & Feasibility Affirmation

### "Can we adopt this into DSOM?"

**Yes, unequivocally.** Adopting the **Council of High Intelligence** framework ([`0xnyk/council-of-high-intelligence`](https://github.com/0xnyk/council-of-high-intelligence)) into Deep State of Mind (DSOM) is not only feasible, but represents a natural evolutionary step for DSOM's **Metacognition & Guardrails Subsystem** and **Tri-Phasic Mind Architecture**.

While single-model outputs often suffer from overconfident hallucinations, vendor bias, and single-lens anchoring, DSOM is built on digital sovereignty, structured metacognition, and Git-native auditability. Incorporating an **18-member persona deliberation council** directly enhances DSOM's decision boundary for high-stakes architectural choices, infrastructure migrations, security posture reviews, and strategic trade-offs.

Furthermore, under **OKF v0.2**, council deliberations incorporate **Attested Computations** (`type: Attested Computation`), bridging definition and execution contracts via runtime bindings, parameters, and deterministic attesters across a 6-step lifecycle (Discover, Load, Parameterize, Execute, Attest, Gate).

---

## 1. Deconstruction of Council of High Intelligence

The **Council of High Intelligence** is an open-source decision-making framework designed to replace single-model reasoning with structured, multi-perspective deliberation across multi-LLM provider backends.

```text
+-----------------------------------------------------------------------------------+
|                        COUNCIL OF HIGH INTELLIGENCE                               |
|                                                                                   |
|  +------------------+   +-----------------------+   +--------------------------+  |
|  | Phase 1: Blind   |   | Phase 2: Cross-       |   | Phase 3: Final Stance    |  |
|  | Analysis         |-->| Examination & Dissent |-->| & Domain-Weighted Tally  |  |
|  +------------------+   +-----------------------+   +--------------------------+  |
|                                                                  |                |
|                                                                  v                |
|                                                     +--------------------------+  |
|                                                     | Phase 4: Verdict         |  |
|                                                     | Blueprint & Attestation  |  |
|                                                     | Ledger Entry             |  |
|                                                     +--------------------------+  |
+-----------------------------------------------------------------------------------+
```

### 1.1 The 18 Analytical Persona Lenses

Rather than broad impersonation, personas serve as grounded analytical instruments with specific methods, counterweights, and blind spots:

| Member Persona | Primary Analytical Lens | Counterweight Lens | Key Operational Method |
| :--- | :--- | :--- | :--- |
| **Aristotle** | Categories & Formal Structure | Lao Tzu (Emergence) | Systematic classification & syllogism |
| **Socrates** | Premise & Assumption Destruction | Richard Feynman (First Principles) | Dialectic questioning & elenchus |
| **Sun Tzu** | Terrain, Positioning & Strategy | Marcus Aurelius (Moral Cost) | Strategic leverage & risk minimization |
| **Ada Lovelace** | Formal Systems & Abstraction | Machiavelli (Informal Power) | Mathematical limits & structural purity |
| **Marcus Aurelius** | Resilience, Duty & Moral Clarity | Sun Tzu (External Competition) | Stoic locus of control & duty |
| **Machiavelli** | Incentives, Power & Realpolitik | Ada Lovelace (Formal Consistency) | Unvarnished incentive analysis |
| **Lao Tzu** | Non-action, Emergence & Flow | Aristotle (Explicit Categories) | Frictionless systems & subtle dynamics |
| **Richard Feynman** | Empirical Debugging & Clarity | Socrates (Premise Questioning) | Plain explanation & physics-first principles |
| **Linus Torvalds** | Shipping, Pragmatism & Code Maintainability | Donella Meadows (System Dynamics) | Practical maintainability & pragmatic execution |
| **Miyamoto Musashi** | Timing, Precision & Decisive Action | Linus Torvalds (Early Action) | Timing, readiness & ruthless focus |
| **Alan Watts** | Reframing & False Dichotomies | Linus Torvalds (Concrete Code) | Unmasking false premises & double binds |
| **Andrej Karpathy** | Empirical ML Behaviour & Iteration | Ilya Sutskever (Frontier Safety) | Observation-driven empirical validation |
| **Ilya Sutskever** | Scaling Laws & Frontier AI Safety | Andrej Karpathy (Smooth Trends) | Tail risks in AI scaling & safety boundaries |
| **Daniel Kahneman** | Cognitive Bias & Heuristics | Richard Feynman (Causal Logic) | System 1 vs. System 2 bias detection |
| **Donella Meadows** | Feedback Loops & System Interventions | Linus Torvalds (Local Fixes) | Leverage points & systemic root causes |
| **Charlie Munger** | Inversion & Mental Model Lattices | Aristotle (Single Classification) | Latticework inversion & multi-disciplinary fit |
| **Nassim Taleb** | Antifragility, Tail Risk & Asymmetry | Andrej Karpathy (Empirical Trends) | Convex payoff analysis & fragility tests |
| **Dieter Rams** | User Clarity, Essentialism & Restraint | Ada Lovelace (Formal Abstraction) | Less, but better; clutter removal |

### 1.2 Deliberation Modes & Domain Triads

To balance decision depth against latency and token consumption, the framework provides four modes:

1. **Full Mode (`--full`)**: 4-phase adversarial protocol across all 18 members. Reserved for high-stakes, irreversible architectural choices.
2. **Quick Mode (`--quick`)**: Rapid 3-phase restate-analyze-stance sequence without an explicit cross-examination round.
3. **Duo Mode (`--duo`)**: Direct 2-member dialectic highlighting one core tension (e.g. `Torvalds` vs. `Meadows`).
4. **Triad Mode (`--triad <domain>`)**: Specialized 3-member sub-panels routed dynamically across 17 domain presets:
   - `architecture`, `strategy`, `ethics`, `debugging`, `risk`, `shipping`, `product`, `founder`, `ai`, `ai-product`, `ai-safety`, `decision`, `systems`, `uncertainty`, `design`, `economics`, `bias`.

### 1.3 Protocol Protections & Output Standards

- **Blind First Phase**: Members evaluate the problem independently to eliminate first-speaker bias and groupthink anchoring.
- **Forced Dissent & Cross-Examination**: Protocol checks look for premature agreement, repeated claims, and unsupported confidence.
- **Evidence Labeling Standard**:
  - `FACT`: Direct evidence present in codebase or verified data.
  - `INFERENCE`: Deductive conclusion following from facts.
  - `ASSUMPTION`: Required premise currently unverified.
  - `UNKNOWN`: Missing information that could alter the verdict.
- **Decision Field Notes**: Mandatory pre-deliberation document separating knowns, assumptions, and reversibility boundaries before convening personas.
- **Verdict Blueprint**: Output leads with unresolved questions, followed by recommendations, kill criteria, acceptable compromises, and concrete next actions.
- **Outcome Ledger Checkpoint**: Post-decision predictions are recorded with review dates to audit outcome validity (`confirmed`, `revised`, `reversed`, `inconclusive`).
- **Multi-Provider Seat Routing**: Seats are assigned across available CLI backends (Claude Code, OpenAI Codex, Gemini CLI, Ollama, NVIDIA NIM, Cursor) so opposing polarities do not reside on the same model family.

---

## 2. Deep State of Mind (DSOM) Integration Architecture

Integrating the Council framework into DSOM harmonises multi-perspective deliberation with DSOM's core pillars:

```text
+-----------------------------------------------------------------------------------+
|                        DSOM TRI-PHASIC MIND INTEGRATION                           |
|                                                                                   |
|  +---------------------------+   +---------------------------+                    |
|  | Active State (MCP Server) |-->| Fast Triad Queries &      |                    |
|  | (Target Latency < 50ms)   |   | Quick Decision Prompts    |                    |
|  +---------------------------+   +---------------------------+                    |
|                                                |                                  |
|                                                v                                  |
|  +---------------------------+   +---------------------------+                    |
|  | Twilight State            |-->| Linter, Token Gate &      |                    |
|  | (Verification & Audits)   |   | Pre-Commit Interception   |                    |
|  +---------------------------+   +---------------------------+                    |
|                                                |                                  |
|                                                v                                  |
|  +---------------------------+   +---------------------------+                    |
|  | Deep State                |-->| Full 18-Member Deliberation|                    |
|  | (EOD Consolidation)       |   | & Outcome Ledger Sync     |                    |
|  +---------------------------+   +---------------------------+                    |
+-----------------------------------------------------------------------------------+
```

### 2.1 Alignment with the Tri-Phasic Mind & Attested Computations

1. **Active State (MCP & Quick Query)**:
   - Plans exposure of lightweight `run_council` tool capabilities (supporting `--triad <domain>` and `--duo` parameters) via FastMCP (`tools/mcp/server.py`). Target latency for local `search_palace` dispatches is under 50ms for standard local payloads.
   - Allows AI IDEs (Cursor, Claude Desktop, Jules) to execute rapid multi-angle sanity checks during active coding sessions.
2. **Twilight State (Safety & Verification)**:
   - Intercepts council executions via DSOM Guardrails & Byte-Capped Execution framework to prevent token runaway.
   - Enforces evidence labeling (`FACT`, `INFERENCE`, `ASSUMPTION`, `UNKNOWN`) before accepting conclusions.
3. **Deep State (EOD Consolidation & Universal Ledger)**:
   - Synthesises Full Council verdicts into spatial brain state files (`.agents/brain/task.md` and `.agents/brain/walkthrough.md`).
   - Records universal audit trail milestones in project ledgers (`HISTORY.md`, `CHANGELOG.md`, `README.md`).

### 2.2 Adopted DSOM Skill Component (`.agents/skills/council-of-high-intelligence/SKILL.md`)

An OKF v0.2 compliant execution manual is established under `.agents/skills/council-of-high-intelligence/SKILL.md`:

```yaml
---
okf_version: 0.2
type: agent_skill
title: "Council of High Intelligence Multi-Agent Consensus Engine"
timestamp: "2026-09-19T00:00:00Z"
description: "Executes a multi-perspective deliberation protocol using specialised AI domain personas..."
topics: ["council", "multi-agent", "consensus", "deliberation", "antigravity"]
name: council-of-high-intelligence
spec_version: "0.2"
status: stable
stale_after: "2027-01-01"
---
```

### 2.3 Planned Zero-Binary Python Emulator (`tools/council_emulator.py`)

In compliance with **Rule 27 (Native OpenWiki Emulator & Zero-Binary Mandate)**, DSOM plans to implement a native, zero-dependency Python utility `tools/council_emulator.py`:

- **Pure Python Execution**: Runs via `uv run python tools/council_emulator.py` without requiring external Node.js packages or UAC elevation.
- **Provider Auto-Detection**: Checks local CLI tools (`gemini`, `codex`, `ollama`) and API keys (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`, `NVIDIA_API_KEY`).
- **Proposed CLI Invocations**:
  ```bash
  # Run a full 18-member council deliberation
  uv run python tools/council_emulator.py --full "Should we migrate from REST to FastMCP?"

  # Run a domain triad deliberation
  uv run python tools/council_emulator.py --triad architecture "Should we adopt Quadlets or Ansible?"

  # Run a two-member dialectic
  uv run python tools/council_emulator.py --duo torvalds meadows "Is this abstraction layer worth maintaining?"
  ```

### 2.4 Proposed FastMCP Server Tool Binding (`tools/mcp/server.py`)

The Council engine is planned for direct exposure as an MCP tool in `tools/mcp/server.py`:

```python
@mcp.tool()
def run_council(question: str, mode: str = "quick", triad: str = None, members: str = None) -> str:
    """Executes multi-perspective AI deliberation using Council of High Intelligence personas."""
    # Invokes internal Council Deliberation Engine
```

### 2.5 Spatial Memory & Ledger Sync

1. **Decision Field Notes**: Saved under `.agents/brain/council_field_notes_<timestamp>.md`.
2. **Verdict Blueprints**: Saved under `docs/governance/council_verdict_<timestamp>.md` or recorded in `.agents/brain/walkthrough.md`.
3. **Outcome Ledger**: Tracked in `HISTORY.md` and checked at scheduled EOD review dates.

---

## 3. Token Efficiency, Trade-Offs & Mitigation Strategies

Running 18 distinct persona evaluations across multiple LLM calls introduces significant context and token overhead. DSOM mitigates this through three token-conservation layers:

| Challenge / Risk | Impact | DSOM Mitigation Mechanism |
| :--- | :--- | :--- |
| **Token Inflation (18x Overhead)** | Heavy prompt token consumption in `--full` mode | Default to `--triad <domain>` (3 members) for daily development; limit `--full` to major architecture decision records (ADRs). |
| **Local Latency** | Sequential LLM API calls delay execution | Asynchronous concurrency via Python `asyncio` across multi-provider endpoints + local Ollama acceleration. |
| **Vendor Anchoring** | Single model provider dominates both sides | Multi-provider routing splits polarity pairs across distinct LLM families (Claude vs. Gemini vs. OpenAI). |
| **Context Window Rot** | Verbose raw discussion clutters chat context | Summary compaction via proposed `tools/council_emulator.py` returning only the structured Verdict Blueprint to the active agent window. |

---

## 4. Implementation Roadmap & Discussion Points

```text
+-----------------------------------------------------------------------------------+
|                            IMPLEMENTATION ROADMAP                                 |
|                                                                                   |
|  Phase 1: Governance & Proposal Review [COMPLETED]                                |
|  - Approve architectural design & DSOM integration strategy.                      |
|                                                                                   |
|  Phase 2: Antigravity Skill Specification [COMPLETED]                             |
|  - Create `.agents/skills/council-of-high-intelligence/SKILL.md`.                 |
|                                                                                   |
|  Phase 3: Native Python Engine Development [PLANNED]                              |
|  - Implement `tools/council_emulator.py` zero-dependency runner.                  |
|                                                                                   |
|  Phase 4: FastMCP & OpenWiki Integration [PLANNED]                                |
|  - Add `run_council` tool to `tools/mcp/server.py`.                              |
|  - Integrate Council verdicts into OpenWiki knowledge graph.                      |
|                                                                                   |
|  Phase 5: Unit Testing & CI Verification [PLANNED]                                |
|  - Add test suite `tests/test_council_emulator.py`.                               |
|  - Verify navigation, links, and OKF frontmatter compliance.                      |
+-----------------------------------------------------------------------------------+
```

---

*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-09-19*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*

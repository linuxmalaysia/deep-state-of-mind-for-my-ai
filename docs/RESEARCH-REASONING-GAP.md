# 🧩 The Reasoning Gap: What DSOM Solves and What It Doesn't

> *"The reasoning, the tradeoffs, the 'we tried X and it failed because Y' — all trapped in chat windows that evaporate when the session ends."*
> — MemPalace research, 2025

**Document Type:** Research Finding | **Status:** Open Gap — Partially Mitigated
**Date Identified:** 2026-04-08 | **Protocol Version:** DSOM v6.1 + Palace v1.0

---

## 📊 The Scale of the Problem

Six months of daily AI use produces approximately **19.5 million tokens** of conversation. That includes every decision, every debugging session, every architecture debate. All of it trapped in chat windows.

| Approach | Tokens Loaded Per Session | Annual Cost Estimate |
|---|---|---|
| Paste everything | 19.5M — exceeds all context windows | Impossible |
| LLM summaries | ~650K | ~$507/yr |
| MemPalace wake-up | ~170 tokens | ~$0.70/yr |
| MemPalace + 5 searches | ~13,500 tokens | ~$10/yr |
| **DSOM Palace (our approach)** | **~1,500–3,000 tokens** | **~$1–3/yr** |

Source: MemPalace research (2025). DSOM cost estimates based on Palace Registry + 2–3 closets.

---

## ✅ What DSOM Solves Well

DSOM with the Sovereign Markdown Palace addresses the **cost and state persistence problem** effectively:

### State Persistence

- `task.md` — What we are working on right now (Present)
- `walkthrough.md` — Full session history with Mental Anchors (Past)
- `implementation_plan.md` — Project roadmap (Future)
- `palace_registry.md` — Spatial index loaded at every SOD

### Cost Efficiency

Our Palace Registry + relevant closets loads **~1,500–3,000 tokens** per session — in the same cost class as MemPalace, achieved through structured Markdown hierarchy rather than vector embeddings.

### Fact Retrieval

Each `closet.md` is a distilled, high-density summary. Instead of scanning 300+ lines of session logs, the AI walks to the relevant Room and reads a 40–80 line summary.

### Git Persistence

Every state change is committed to Git. The project state cannot be lost — it is version-controlled, multi-machine synced, and provider-agnostic.

---

## ⚠️ The Identified Gap: Live Reasoning Capture

### What the Gap Is

DSOM does **not** automatically capture the *reasoning* behind decisions. It captures outcomes — what was decided, what was built, what changed. It does not capture:

- ❌ **Why** a decision was made
- ❌ **What alternatives were considered and rejected**
- ❌ **The conversation thread** that produced the reasoning
- ❌ **"We tried X and it failed because Y"** — unless manually committed

### Why It Matters

Decisions made today become constraints six months from now. If the reasoning is lost:

- A future session may propose the same failed approach again.
- The AI has no way to explain *why* the current architecture is the way it is.
- New team members (human or AI) cannot understand the tradeoff history.

### Example Scenario

```
Session Day 1:
  Human: "Why are we using Macvlan instead of bridge networking?"
  AI: "Because Elasticsearch nodes needed their own routable IPs for 
       cluster discovery. Bridge networking caused split-brain under 
       load. We tested this in Phase 42 and it failed with 3 nodes."

Session Day 180 (new AI, same repo):
  Human: "Why are we using Macvlan?"
  AI: "I don't know. The config shows Macvlan but there's no reasoning 
       documented. Do you want to reconsider?"
```

The outcome (Macvlan config) is in Git. The *reasoning* is gone.

---

## 🔬 Architectural Comparison

| Dimension | MemPalace | DSOM Palace |
|---|---|---|
| **Retrieval mechanism** | Vector embeddings + semantic search | Structured Markdown + walking |
| **Capture method** | Automated (conversation → embeddings) | Manual curation + Git commit |
| **Reasoning capture** | Automatic (if conversation is indexed) | Manual (requires intentional `walkthrough.md` entry) |
| **Ownership** | Depends on the MemPalace service | 100% sovereign — your Git repo |
| **Cost** | ~$10/yr for search | ~$1–3/yr for Palace walk |
| **Offline capability** | No (requires embedding API) | Yes (plain Markdown + Git) |
| **Vendor dependency** | Yes | None |
| **Fidelity of old reasoning** | High (verbatim if indexed) | Varies (depends on what was written) |

**Conclusion:** DSOM wins on sovereignty, cost, and ownership. MemPalace wins on automated reasoning capture. The gap is real but addressable without sacrificing sovereignty.

---

## 🔧 Current Mitigation: Hibernation Notes

The existing EOD ritual includes the **Hibernation Notes export prompt**, which asks the AI to dump its full in-session memory before the session ends:

```
"List every memory you have stored about our progress and our chats of 
this project... Cover: reasoning, tradeoffs, what failed and why..."
```

**Limitation:** This relies on the AI's **in-session memory at that moment**. If the session was long, context was refreshed mid-session, or the AI forgot earlier reasoning, the export is incomplete.

Hibernation Notes mitigate the gap — they do not close it.

---

## 💡 Recommended Practice: The Decision Log Protocol

### The Principle

**Capture reasoning in the moment, not at EOD.** At every significant architectural decision, constraint, or failure, immediately ask the AI to log it:

### The Command

```
"Log this decision to walkthrough.md:
 Decision: [what was decided]
 Alternatives: [what was rejected]
 Reason: [why this and not that]
 Context: [what would make us revisit this]"
```

### Example

```
"Log this decision to walkthrough.md:
 Decision: Macvlan networking for Elasticsearch nodes
 Alternatives: Bridge networking (tested Phase 42), Host networking (security risk)
 Reason: Nodes need routable IPs for cluster discovery. Bridge caused split-brain 
          under 3-node load test on 2026-03-15.
 Context: Revisit if we move to Kubernetes (CNI handles this differently)."
```

This entry lands in Git **during the session**, not hours later in a summary that may lose fidelity.

### When to Trigger a Decision Log

- Any time you say "we'll use X instead of Y"
- Any time a test fails and you pivot approach
- Any time you override an AI recommendation
- Any time you establish a constraint that will affect future sessions

---

## 🗺️ Future Consideration: Semantic Search for DSOM

If the DSOM community grows and the reasoning backlog becomes deep, a sovereign semantic search layer could be added **without breaking the Plain Markdown Mandate**:

- Tool: `ripgrep` (already used) for keyword search across all closets
- Upgrade: A local embedding model (e.g., via Ollama) to add vector search on top of the existing Markdown files
- The Markdown files remain the source of truth — the embeddings are a search index only

This would close the gap entirely while maintaining full sovereignty and zero vendor dependency.

---

## 📋 Gap Status Summary

| Gap | Status | Mitigation |
|---|---|---|
| State persistence | ✅ Solved | `walkthrough.md` + Git |
| Cost/token efficiency | ✅ Solved | Palace Registry + closets |
| Fact retrieval | ✅ Solved | Walk Palace → closet.md |
| Outcome capture | ✅ Solved | Git commit history + `palace-sync` |
| **Live reasoning capture** | **⚠️ Partially mitigated** | **Hibernation Notes + Decision Log Protocol** |
| Semantic search | 🔵 Future | Planned: local Ollama embeddings |

---

## 🔗 Related Documents

| Document | Relevance |
|---|---|
| [`docs/PALACE-BUILD-STORY.md`](PALACE-BUILD-STORY.md) | Why the Palace was built |
| [`docs/DIGITAL-SOVEREIGNTY-OPERATIONAL-MODEL-PALACE.md`](DIGITAL-SOVEREIGNTY-OPERATIONAL-MODEL-PALACE.md) | Full Palace specification |
| [`docs/EOD-RITUAL.md`](EOD-RITUAL.md) | Hibernation Notes export protocol |
| [`docs/HOWTO-PALACE-ONBOARDING.md`](HOWTO-PALACE-ONBOARDING.md) | Palace usage guide |

---
*Research finding documented: 2026-04-08*
*Identified by: Harisfazillah Jamel (LinuxMalaysia) in session with Google Antigravity*
*Inspired by: MemPalace research (andrewyng/mempalace)*
*Protocol: DSOM v6.1 + Palace v1.0*

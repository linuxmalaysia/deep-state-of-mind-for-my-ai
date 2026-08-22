# Deep State of Mind (DSOM) Instructions for Claude Code & Claude Desktop

> **ATTENTION CLAUDE:** This repository is governed by the **Deep State of Mind (DSOM)** framework.

## 1. 🛑 Genesis Boot Sequence
Upon initialisation, orient yourself by consulting these files:
1. `.agents/AGENTS.md` — The 29 Constitutional Laws & Persona Matrix.
2. `.agents/brain/task.md` — Active session task list.
3. `.agents/brain/walkthrough.md` — Session history & Mental Anchors.
4. `START-HERE.md` — Master onboarding map with 19 entry points.

## 2. ⚖️ Core Execution Constraints
- **Python uv Mandate:** Execute all Python tooling via `uv run` (e.g. `uv run pytest`, `uv run tools/...`).
- **Atomic Commits:** Discrete semantic commits grouped by logical task boundaries.
- **UK English:** Use British English for all code documentation, comments, and commit messages.
- **Episodic Memory:** Always emit a `[DSOM EPISODIC RECORD]` summary block upon completing complex tasks.

<!-- OPENWIKI:START -->

## OpenWiki

This repository has a generated `openwiki/` evidence index. It is optional just-in-time context, not required startup reading.

- Treat source code and tests as authoritative. A brief's unknowns and review items are verification gaps, not automatic requirements.
- Prefer the narrowest quiet validation that proves the changed behaviour. Preserve complete failure output.

The scheduled OpenWiki GitHub Actions workflow refreshes the repository wiki. Do not hand-edit generated OpenWiki pages unless explicitly asked; prefer updating source code/docs and letting OpenWiki regenerate.
 
 <!-- OPENWIKI:END -->
+
+<!-- dts:start -->
+
+## Output Standard (DTS 0.1)
+
+Governs every English word this agent writes for engineers and agents: replies in conversation, docs, code comments, commit and PR bodies, checklists, error strings, CLI help, tool descriptions, and agent prompts.
+
+Out of scope: any other language, fiction, persuasive or brand copy, and long-form argument such as a thesis, paper, essay, or legal text, where hedging and long linked sentences are part of the job. An overlay below this block says which of your own rules covers those.
+
+Override, per file: `<!-- dts:core -->` keeps the core and drops the sentence caps, the modal limit, and the bullets rule. `<!-- dts:off -->` disables everything. A project memory file and any text outside this block outrank these rules.
+
+- Compression removes filler, never content. Every fact the reader needs to act survives. When keeping a fact costs another sentence, write the sentence. Being complete is never a reason to hedge. An uncertain fact is stated as unconfirmed, never as `may`.
+- Protected content survives every cut: caveats, security constraints, edge cases, scope limits, and version requirements. These are never filler.
+- Answer first. No preamble, no restatement of the request, no closing recap.
+- One idea per sentence. At most 15 words for an instruction, 20 for an explanation. Shorter is always better. Split a longer thought into two sentences. Never drop the tail of it.
+- Name who does the thing, and use the plain present tense. Write an instruction as a command. Never `has been` / `have been`.
+- Modals: `can`, `will`, `must` only. Never `should` / `would` / `may` / `might` / `could`.
+- Bullets and tables for anything enumerable. Never a prose list. No semicolons. Open each item with the thing it names, never with the same verb repeated down the list.
+- Stop a list when the next row adds nothing the reader will act on. Never pad to look thorough. Never truncate mid-row. Past ten rows, the question probably needs splitting.
+- One word, one meaning. The word is fixed, never picked fresh each time: `fetch` (network), `read` (disk), `modify`, `create`, `remove`, `run`, `directory`, `function`.
+- Three words get swapped most often. Pick one and never use the others: `check` never verify/confirm/validate/ensure. `error` never failure/issue/problem. `config` never configuration/settings/options. Exempt: verbatim code identifiers, and terms with a distinct technical sense.
+- Ban: simply, just, easily, seamless, robust, powerful, comprehensive, crucial, vital, essential, leverage, utilize, delve, "it is worth noting", "that said". No hedge stacks — state the fact, or state that it is unconfirmed.
+- Prefer the plain word. Keep a technical term only when it is exact and the reader already uses it. A word that signals expertise and nothing else goes.
+- State the point straight. No analogy, no clever one-liner, no `not X, but Y`. A sentence the reader must read twice has failed, however short it is.
+- Reproduce code, paths, commands, identifiers, and error strings verbatim. Never paraphrase or re-case them.
+- Never re-output unchanged code. Edit an existing file in place — never rewrite it whole for a partial change. Never print back a file you just edited.
+- Brevity governs prose ONLY. Code in an edit must be complete — never `// ... existing code` or a stub placeholder.
+- An artifact with a required shape keeps every part. An error message names what failed, the exact input, and the next action.
+<!-- dts:end -->


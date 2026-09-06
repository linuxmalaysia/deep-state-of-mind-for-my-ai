---
okf_version: 0.2
spec_version: "0.2"
type: agent_skill
concept_id: "dsom_knowledge_ingester"
title: "📥 DSOM Knowledge Ingester Skill"
status: "stable"
stale_after: "2027-03-06"
timestamp: "2026-08-25T18:52:00Z"
description: "Executes the Knowledge Ingestion protocol (/learn) inspired by the LLM WIKI concept."
topics: ["knowledge", "ingestion", "okf", "palace", "markdown"]
sources:
  - id: "okf_v02_spec"
    title: "Open Knowledge Format (OKF) v0.2 Specification"
    author: "Google Cloud Platform & DSOM Protocol Guild"
    url: "https://cloud.google.com/blog/products/data-analytics/okf-v0-2-adds-trust-signals"
generated:
  by: "DSOM Knowledge Ingestion Agent v1.0"
  timestamp: "2026-08-25T18:52:00Z"
name: dsom-knowledge-ingester
---
## 📥 DSOM Knowledge Ingester Skill

### SYSTEM PROTOCOL: Knowledge Ingestion Command (`/learn`)

#### Role & Objective

You are an advanced Knowledge Ingestion Agent operating within a structured GitOps/AIOps ecosystem.
Your objective is to intercept the user command format `/learn [Topic, URL, or Context]` and transform
that raw information into a highly optimised, context-ready Open Knowledge Format (OKF) v0.2 Markdown document.

---

#### Trigger & Scope

- **Activation Command:** Whenever the user inputs text starting with `/learn`, suspend general conversational behaviour.
- **Target Action:** Parse the provided URL, text string, or referenced documentation in `raw_sources/` or
  external inputs, extract core architectural technical truths, and generate a new `.md` file in the repository.

---

#### 1. Structural Frontmatter Mandate (OKF v0.2)

The generated file MUST begin strictly on Line 1, Column 1 with a triple-dash (`---`) YAML frontmatter block.
You must populate the **Five Trust & Freshness Pillars**:

- **spec_version:** Explicitly set to `"0.2"`.
- **type:** Define the functional classification (e.g., `"tutorial"`, `"how-to"`, `"reference"`, `"explanation"`).
- **concept_id:** Define a concise, snake_case identifier for the concept.
- **title:** A concise, clear title.
- **status:** Explicitly set to `"stable"` or `"draft"`.
- **stale_after:** Calculate and append an absolute expiration date string (`YYYY-MM-DD`),
  typically set to 6 months from the current processing timestamp.
- **sources:** Structurally list the source material provided in the `/learn` trigger using sub-fields
  (`id`, `title`, `author`, `url`).
- **generated:** Structurally record automated production metadata
  (`by: [Agent Name]`, `timestamp: [ISO 8601 UTC string]`).

##### Example Frontmatter Structure

```yaml
---
okf_version: 0.2
spec_version: "0.2"
type: "how-to"
concept_id: "ingested_topic_name"
title: "Ingested Topic Technical Protocol"
status: "stable"
stale_after: "2027-03-06"
sources:
  - id: "source_context_1"
    title: "Raw Context Title"
    author: "User Provided / External"
    url: "https://example.com"
generated:
  by: "DSOM Ingestion Agent v1.0"
  timestamp: "2026-09-06T18:52:00Z"
---
```

---

#### 2. Content Alignment Rules (Diátaxis Framework)

Organise the body of the prose strictly adhering to one of the four Diátaxis quadrants based on the query type:

1. **Tutorial:** Learning-oriented, step-by-step guidance for beginners.
2. **How-To Guide:** Goal-oriented, practical steps to solve a specific problem.
3. **Reference:** Information-oriented, technical descriptions, schemas, and API definitions.
4. **Explanation:** Understanding-oriented, high-level architectural concepts and design choices.

Ensure vocabulary patterns adhere strictly to **UK English** spelling
(e.g., *optimise*, *organise*, *centring*, *behaviour*).

---

<!-- markdownlint-disable MD013 -->
#### 3. Workspace Quality Enforcement (`markdownlint-cli`)

Before presenting the generated knowledge asset or finalising the file write, you MUST execute quality assurance checks:

1. Programmatically invoke `npx --no-install markdownlint-cli --fix <filename.md>` to resolve auto-formattable style errors.
2. Ensure that the document successfully passes all rules permitted by the local `.markdownlint.json` configuration file.
3. Verify that the frontmatter block does not trigger errors by keeping the file starting cleanly with `---` on line 1.
4. Execute `uv run python tools/apply_okf_frontmatter.py --require-okf-v02 <directory>` to normalise metadata and reject newly synthesised Markdown documents unless `okf_version`, `spec_version`, `concept_id`, `status`, `stale_after`, `sources`, and `generated` contain valid OKF v0.2 values.
5. Run `uv run .agents/skills/dsom-signature-injector/scripts/inject.py <directory>` to append standard GPL v3.0 ownership signatures.
4. Execute `uv run python tools/apply_okf_frontmatter.py <directory>` to verify and inject OKF v0.2 frontmatter headers into all newly synthesised Markdown documents.
5. Run `python .agents/skills/dsom-signature-injector/scripts/inject.py <directory>` to append standard GPL v3.0 ownership signatures.
<!-- markdownlint-enable MD013 -->

---

#### 4. Ledger & Index Updates

- Add the new file to `SUMMARY.md` and `mkdocs.yml` (Dual Documentation Sync).
- Add the new file to `.agents/brain/palace_registry.md`.
- Update `CHANGELOG.md` and `HISTORY.md` to note the new knowledge ingestion.

---

#### Final Output Delivery

Once validation is clean, save the file to the designated path and output a summary response to the user confirming:

- The path of the newly compiled OKF v0.2 document.
- A concise summary of the ingested material.
- The computed `stale_after` date and trust attributes.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-09-06*
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-20*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai)*
*GNU General Public License v3.0*

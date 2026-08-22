---
okf_version: 0.2
type: governance
title: "Mintlify One-Way Docs Sync & Safety Guards Specification"
timestamp: "2026-08-22T22:42:00Z"
sources:
  - title: "Mintlify Documentation"
    url: "https://mintlify.com/docs"
  - file:///scripts/sync_docs.py
  - file:///tools/build_mintlify_mdx.py
  - file:///.github/workflows/sync-docs.yml
generated: "human-and-ai"
verified: "verified"
status: "authoritative"
stale_after: "2027-08-22T22:42:00Z"
topics: ["mintlify", "sync", "governance", "mdx", "safety-guards", "gitops"]
description: "Master governance specification for automated Markdown-to-MDX compilation and deterministic one-way sync to Mintlify downstream repositories under 5 non-negotiable safety guards."
---

# Mintlify One-Way Docs Sync & Safety Guards Specification

> **Entry Point 21:** This document governs the automated compilation of standard Markdown documents in `docs/` and skills in `.agents/skills/` into Mintlify MDX (`docs-source/`) and their deterministic, one-way synchronization to downstream docs repositories (e.g. `linuxmalaysia/my-knowledge-brain`) powering [harisfazillah.mintlify.site](https://harisfazillah.mintlify.site).

---

## 1. Architectural Philosophy & Zero-Bloat Invariant

In modern multi-agent systems and sovereign software engineering, documentation must maintain a single authoritative source of truth. Authoring documentation directly inside hosted CMS tools, web editors, or downstream deployment repositories creates context drift, merge conflicts, and accidental knowledge destruction.

The **Deep State of Mind (DSOM)** protocol resolves this through **Automated MD-to-MDX Compilation** and **One-Way GitOps Synchronization**:

```text
┌────────────────────────────────────────────────────────────┐
│ Sovereign Source of Truth: docs/ & .agents/skills/         │
└───────────────────────────┬────────────────────────────────┘
                            │ (python tools/build_mintlify_mdx.py)
                            ▼
┌────────────────────────────────────────────────────────────┐
│ Intermediate Compiled Tree: docs-source/ + docs.json       │
└───────────────────────────┬────────────────────────────────┘
                            │ (python scripts/sync_docs.py)
                            ▼ (5 Non-Negotiable Safety Guards A–E)
┌────────────────────────────────────────────────────────────┐
│ Downstream Deployment: linuxmalaysia/my-knowledge-brain    │
└───────────────────────────┬────────────────────────────────┘
                            │ (Mintlify Auto-Build)
                            ▼
┌────────────────────────────────────────────────────────────┐
│ Public Portal: https://harisfazillah.mintlify.site         │
└───────────────────────────┬────────────────────────────────┘
```

---

## 2. The 5 Non-Negotiable Safety Guards (A–E)

The sync pipeline (`scripts/sync_docs.py`) executes five sequential verification gates. If **any** guard fails, the process immediately exits non-zero before touching the downstream repository:

| Guard | Gate Name | Validation Invariant | Destruction Prevented |
|:---|:---|:---|:---|
| **A** | **Source & JSON Integrity** | Asserts `docs-source/` exists and `docs.json` parses as valid JSON. | Prevents running against deleted or renamed folders. |
| **B** | **Minimum File Count Floor** | Asserts count of `.mdx` files meets or exceeds `MIN_MDX_FILES` (default `5`). | Prevents empty or half-populated source from wiping downstream. |
| **C** | **Navigation Route Integrity** | Validates that every page referenced in `docs.json` exists on disk as a `.mdx` file. | Prevents broken navigation links and 404 page errors. |
| **D** | **Diff Preview & Deletion Cap** | Computes added/modified/deleted diff against downstream tree. Fails if deletions exceed `MAX_DELETIONS` (default `10`). | Prevents accidental bulk mass-deletions unless `ALLOW_LARGE_DELETIONS=true`. |
| **E** | **Dry-Run Preview Mode** | Supports `--dry-run` and `DRY_RUN=true`. Runs Guards A–D and logs the exact diff without modifying Git. | Allows human and AI to safely audit changes prior to production sync. |

---

## 3. Reusable Implementation Prompt for Any AI Coding Assistant

To instantiate this identical architecture on any other repository or client project, provide the following prompt to an AI coding assistant (Google Antigravity, Claude Code, Cursor, GitHub Copilot):

```text
Set up an automated Markdown-to-MDX compiler and a hardened one-way docs sync pipeline between two GitHub repositories with 5 strict safety guards so an empty or partial source can NEVER destroy the downstream Mintlify docs repo.

REPOS & CONFIGURATION
- App repo (source of truth, where we work): <OWNER>/<APP_REPO>
- Docs repo (Mintlify deployment, downstream): <OWNER>/<DOCS_REPO>
- Mintlify live URL / subdomain:               <SUBDOMAIN>.mintlify.site
- Branch on both repos:                        main
- Native source folder in app repo:            docs/
- Compiled target folder in app repo:          docs-source/
- Target in downstream docs repo:              repo root

GOAL
1. Treat docs/ (standard Markdown .md) as the single source of truth.
2. Automatically compile docs/ into Mintlify MDX format under docs-source/ (with valid frontmatter and auto-generated docs.json).
3. Safely sync docs-source/ into <OWNER>/<DOCS_REPO> root on push to main or manual dispatch, protected by 5 non-negotiable safety guards (Guards A–E).

DELIVERABLES TO CREATE

1. tools/build_mintlify_mdx.py:
   - Traverses docs/ and skills/ to discover all .md files.
   - Extracts OKF / standard YAML frontmatter (title, description, topics).
   - Generates corresponding .mdx files in docs-source/.
   - Dynamically builds docs-source/docs.json with proper navigation tabs and groups matching the project structure.

2. Seed docs-source/:
   - Run tools/build_mintlify_mdx.py once to populate docs-source/ with all initial .mdx files and docs.json.

3. scripts/sync_docs.py:
   Implement the 5 strict safety guards. Any failed guard must exit non-zero BEFORE touching the downstream repo:
   - Guard A (Source & JSON Integrity):
     Fail if docs-source/ does not exist or docs-source/docs.json is missing/invalid JSON.
   - Guard B (Minimum File Count Floor):
     Count .mdx files under docs-source/. Fail if count is below MIN_MDX_FILES (default 5).
   - Guard C (Navigation Integrity):
     Walk docs.json navigation. Assert that every referenced page has a matching docs-source/<path>.mdx file. Fail if any are missing.
   - Guard D (Diff Preview & Deletion Cap):
     Clone downstream repo into a temp directory using DOCS_REPO_TOKEN. Compute file diff (added/modified/deleted). Fail if deleted files exceed MAX_DELETIONS (default 10) unless ALLOW_LARGE_DELETIONS=true is set.
   - Guard E (Dry-Run Mode):
     Support --dry-run flag and DRY_RUN=true env var. Preview the plan without committing or pushing.

   Sync execution (only after all guards pass):
   - Wipe downstream working tree (preserve .git).
   - Copy docs-source/ into it.
   - git config user.name "Docs Sync Bot" and user.email "bot@<SUBDOMAIN>.mintlify.site".
   - Stage changes (git add -A). If clean, exit 0.
   - Commit: "Sync docs from app repo @ <short-sha>".
   - Push to main. Never force-push.

4. .github/workflows/sync-docs.yml:
   - Triggers on push to main touching docs/**, docs-source/**, tools/build_mintlify_mdx.py, or scripts/sync_docs.py.
   - Exposes workflow_dispatch with inputs: dry_run (default true), allow_large_deletions (default false), min_mdx_files (default "5"), max_deletions (default "10").
   - Runs on ubuntu-latest, Python 3.11+.
   - Step 1: Run `python tools/build_mintlify_mdx.py`.
   - Step 2: Run `python scripts/sync_docs.py`.
   - Injects secrets.DOCS_REPO_TOKEN.

5. Rule & Governance Documentation:
   - Document Rule: "Mintlify One-Way Docs Sync & Safety Guards Mandate" in AGENTS.md.
   - In downstream repo README.md, state clearly: "Auto-synced from <APP_REPO>/docs-source/. Do NOT edit here or via Mintlify web editor."

6. Automated Tests:
   - tests/test_mintlify_mdx_builder.py: Validate frontmatter conversion, MD-to-MDX text generation, and docs.json assembly.
   - tests/test_sync_docs.py: Validate Guards A through E.

CONSTRAINTS & RULES
- One-way sync only. Never configure two-way sync.
- Use Fine-Grained Personal Access Token (PAT) with Read & Write access to <OWNER>/<DOCS_REPO> only.
- UTF-8 console encoding safe (no raw unhandled unicode errors on Windows/Linux).
- Never force-push.
```

---

## 4. Setup & Operational Runbook

### Step 1: Create Fine-Grained Personal Access Token (PAT)
1. On GitHub, navigate to **Settings** -> **Developer settings** -> **Personal access tokens** -> **Fine-grained tokens**.
2. Set **Repository access** to `Only select repositories` -> select `<OWNER>/<DOCS_REPO>`.
3. Set **Permissions** -> **Repository permissions** -> **Contents**: `Read and write`.
4. Generate the token.

### Step 2: Configure Repository Secret
1. In the source repository, go to **Settings** -> **Secrets and variables** -> **Actions**.
2. Click **New repository secret**.
3. Name: `DOCS_REPO_TOKEN`.
4. Value: `<fine-grained-pat>`.

### Step 3: Local Dry-Run Testing
Before pushing major documentation reorganizations, verify the sync locally:
```powershell
python tools/build_mintlify_mdx.py
python scripts/sync_docs.py --dry-run
```

### Step 4: Disaster Recovery & Rollback
If an errant commit is pushed downstream:
```bash
git clone https://github.com/<OWNER>/<DOCS_REPO>.git
cd <DOCS_REPO>
git log --oneline -n 5
git revert <bad-commit-sha>
git push origin main
```
Fix the source issue in `docs/` in the main repo and re-run dry-run before pushing.

---

## SOURCES
- [tools/build_mintlify_mdx.py](file:///tools/build_mintlify_mdx.py): Automated MD-to-MDX compiler and `docs.json` tree generator.
- [scripts/sync_docs.py](file:///scripts/sync_docs.py): Hardened sync script enforcing Guards A–E.
- [.github/workflows/sync-docs.yml](file:///.github/workflows/sync-docs.yml): Automated GitHub Actions deployment pipeline.
- [Mintlify Official Documentation](https://mintlify.com/docs): Reference specification for Mintlify docs hosting and MDX components.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-22*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*

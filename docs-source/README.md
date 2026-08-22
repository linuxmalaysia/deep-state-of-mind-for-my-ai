# my-knowledge-brain Docs Repo

This repository (`linuxmalaysia/my-knowledge-brain`) is the **Mintlify docs deployment source** for [harisfazillah.mintlify.app](https://harisfazillah.mintlify.app).

> ⚠️ **Do not edit files in this repo directly.** ⚠️ **Do not edit in the Mintlify web editor.** This repo is auto-synced one-way from `linuxmalaysia/deep-state-of-mind-for-my-ai` under `docs-source/`. Any manual change here will be overwritten on the next sync.

## Where to edit docs

Edit docs in the app repo: [**linuxmalaysia/deep-state-of-mind-for-my-ai**](https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai) under the `docs-source/` folder.

On every push to `main` that touches `docs-source/**`, a GitHub Actions workflow runs safety guards, then copies the contents into this repo and pushes to `main` here. Mintlify then rebuilds automatically.

```text
linuxmalaysia/deep-state-of-mind-for-my-ai (app repo, source of truth)
  └── docs-source/                    ← edit here
       ├── *.mdx
       ├── docs.json
       ├── images/
       └── ...
  └── scripts/sync_docs.py
  └── .github/workflows/sync-docs.yml
  └── AGENTS.md

     ↓ (on push to main, paths: docs-source/**)
     ↓ (guards A–E must pass)

linuxmalaysia/my-knowledge-brain (this repo, auto-synced, DO NOT EDIT)
  └── *.mdx
  └── docs.json

     ↓ (Mintlify GitHub app watches main)

https://harisfazillah.mintlify.app
```

## Safety guards

The sync script (`scripts/sync_docs.py` in the app repo) runs these guards **before** touching this repo. Any failed guard exits non-zero and no changes are pushed.

| Guard | Prevents |
| --- | --- |
| **A — Source exists** | Sync running against a missing/renamed folder or invalid `docs.json`. |
| **B — Minimum file count** | Empty or half-populated `docs-source/` wiping this repo. Floor via `MIN_MDX_FILES` (default 5). |
| **C — Navigation integrity** | Broken links, empty groups, missing pages. Every path in `docs.json` navigation must have a matching `.mdx`. |
| **D — Deletion cap** | Mass-delete accidents. Fails if deletions exceed `MAX_DELETIONS` (default 10) unless `ALLOW_LARGE_DELETIONS=true`. |
| **E — Dry-run** | Preview the plan (add/modify/delete lists) without pushing. Enable via `--dry-run` or `DRY_RUN=true`. |

## Rules

- ❌ Do NOT edit files in this repo (`my-knowledge-brain`) directly
- ❌ Do NOT edit in the Mintlify web editor (changes will be overwritten)
- ❌ Do NOT disable guards to "make it work" — fix `docs-source/` instead
- ❌ Do NOT force-push to this repo
- ✅ Only edit `docs-source/` in `linuxmalaysia/deep-state-of-mind-for-my-ai`
- ✅ Always run the workflow with `dry_run=true` first, review the diff, then run with `dry_run=false`
- ✅ Push to `main` in the app repo → guards run → auto-sync → Mintlify rebuild

## Setup checklist

### ✅ Done

- Mintlify deployment `harisfazillah` created
- Git source connected: `linuxmalaysia/my-knowledge-brain` on `main`
- Live site: [https://harisfazillah.mintlify.app](https://harisfazillah.mintlify.app)

### ⬜ To do (in app repo `linuxmalaysia/deep-state-of-mind-for-my-ai`)

1. **Seed `docs-source/`** with the current contents of this repo (clone this repo, copy every file including `docs.json`, all `.mdx`, images, `logo/`, `favicon.svg`, `.mintignore`). Verify with a recursive diff — `docs-source/` and this repo's root must be identical before the first sync.
2. **Add `scripts/sync_docs.py`** implementing guards A–E (see the "Sync script" section below).
3. **Add `.github/workflows/sync-docs.yml`** with the `push` trigger and a `workflow_dispatch` trigger exposing `dry_run`, `allow_large_deletions`, `min_mdx_files`, `max_deletions` inputs.
4. **Add `AGENTS.md`** in the app repo instructing humans and AI agents to edit only under `docs-source/`, never in this repo or the Mintlify web editor, and to always run a dry-run first.
5. **Create a fine-grained Personal Access Token:**
   - Repository access: `linuxmalaysia/my-knowledge-brain` only
   - Permissions: **Contents: Read and write**
   - Do NOT use a classic token.
6. **Add the token as repository secret** `DOCS_REPO_TOKEN` in the app repo.
7. **Run the workflow manually with `dry_run=true`** and review the add/modify/delete lists.
8. **Run again with `dry_run=false`** to perform the first real sync.
9. **Enable branch protection** on `main` in this repo, allowing pushes only from the sync bot / PAT owner.

## Sync script

`scripts/sync_docs.py` in the app repo must:

- Read `DOCS_REPO_TOKEN` from env.
- Read `MIN_MDX_FILES` (default `5`), `MAX_DELETIONS` (default `10`), `ALLOW_LARGE_DELETIONS` (default `false`), `DRY_RUN` (default `false`) from env. Support `--dry-run` flag.
- Run guards A–E in order and exit non-zero on any failure, before touching this repo:
  - **A**: fail if `docs-source/` missing or `docs-source/docs.json` missing/invalid JSON.
  - **B**: count `.mdx` files under `docs-source/`; fail if below `MIN_MDX_FILES`. Print the count.
  - **C**: parse `docs.json`, walk both `navigation.tabs[].groups[].pages` and `navigation.groups[].pages` (support nested groups), assert `docs-source/<page>.mdx` exists for every referenced path. Fail with the list of missing files. Warn (do not fail) on orphan `.mdx` files not referenced in navigation.
  - **D**: clone this repo to a temp dir with `DOCS_REPO_TOKEN`, compute file-level diff (`files_added`, `files_modified`, `files_deleted`), print counts and lists, fail if `len(files_deleted) > MAX_DELETIONS` unless `ALLOW_LARGE_DELETIONS=true`.
  - **E**: if dry-run, print the plan and exit 0 without commit/push.
- Only after all guards pass: wipe the working tree (keep `.git`), copy `docs-source/` into it, `git add -A`, exit 0 if no staged changes, commit `Sync docs from app repo @ <short-sha>`, push to `main`. Never force-push.
- Configure git user `Docs Sync Bot <bot@harisfazillah.com>`.
- Print a final summary: files added / modified / deleted / total copied.

## Workflow

`.github/workflows/sync-docs.yml` in the app repo must:

- Trigger on `push` to `main` with `paths: [docs-source/**]`.
- Also expose `workflow_dispatch` with inputs:
  - `dry_run` (boolean, default `true`)
  - `allow_large_deletions` (boolean, default `false`)
  - `min_mdx_files` (string, default `"5"`)
  - `max_deletions` (string, default `"10"`)
- Ubuntu-latest, Python 3.11.
- Run `scripts/sync_docs.py`, passing `DOCS_REPO_TOKEN` from secrets and the four inputs above as env vars (with sensible defaults on `push` events).
- On failure, print a clear message pointing at the failed guard.

## Recovery procedure

If this repo is ever wiped or corrupted by a bad sync:

```bash
git clone https://github.com/linuxmalaysia/my-knowledge-brain.git
cd my-knowledge-brain
git log --oneline
git revert <bad-sync-sha>
git push origin main
```

Then fix `docs-source/` in `linuxmalaysia/deep-state-of-mind-for-my-ai` and re-run the sync workflow with `dry_run=true` before pushing for real.

## Local preview (in app repo)

```bash
cd docs-source
npm i -g mint
mint dev
```

Preview at [http://localhost:3000](http://localhost:3000).

Also run a dry-run of the sync before committing:

```bash
DOCS_REPO_TOKEN=<pat> python scripts/sync_docs.py --dry-run
```

## Resources

- [Mintlify documentation](https://mintlify.com/docs)
- [Live site](https://harisfazillah.mintlify.app)
- [App repo (edit docs here)](https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai)
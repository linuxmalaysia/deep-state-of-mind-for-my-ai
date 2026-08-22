# Instructions for AI agents and humans

This repository (`linuxmalaysia/my-knowledge-brain`) is the **downstream Mintlify docs deployment repo** for [harisfazillah.mintlify.app](https://harisfazillah.mintlify.app). It is **auto-synced one-way** from `linuxmalaysia/deep-state-of-mind-for-my-ai` under `docs-source/`.

## Hard rules

- ❌ **Do NOT edit any file in this repo directly.** Every file here is overwritten on the next sync.
- ❌ **Do NOT edit in the Mintlify web editor.** Same reason.
- ❌ **Do NOT open PRs against this repo** with docs changes. Open them against the app repo instead.
- ❌ **Do NOT force-push.** The sync bot never force-pushes; neither should anyone else.
- ❌ **Do NOT disable or bypass the sync guards** in the app repo. If a guard fails, fix `docs-source/`, not the guard.

## Where to make changes

All docs edits happen in the app repo:

- Repo: [`linuxmalaysia/deep-state-of-mind-for-my-ai`](https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai)
- Folder: `docs-source/`
- Files: `.mdx` pages, `docs.json`, images, logo, favicon, `.mintignore`

The app repo also contains:

- `scripts/sync_docs.py` — the sync script with safety guards A–E.
- `.github/workflows/sync-docs.yml` — the workflow that runs on push to `main` touching `docs-source/**`, and on manual `workflow_dispatch`.
- `AGENTS.md` — full agent instructions for the app repo.

## Required workflow for any docs change

1. Branch from `main` in the app repo.
2. Edit files under `docs-source/`.
3. If you add or rename a page in `docs.json` navigation, the matching `.mdx` file must exist under `docs-source/` **in the same commit**. Guard C fails otherwise.
4. Run `scripts/sync_docs.py --dry-run` locally (or trigger the workflow with `dry_run=true`) and review the add/modify/delete lists.
5. Open a PR against the app repo `main`.
6. After merge, the sync workflow runs guards A–E and pushes to this repo. Mintlify rebuilds.

## If this repo looks broken

Do not try to fix it here. Follow the recovery procedure in `README.md`: revert the bad sync commit, fix `docs-source/` in the app repo, and re-run the workflow in dry-run first.

## Summary

- Source of truth: `linuxmalaysia/deep-state-of-mind-for-my-ai` → `docs-source/`
- This repo: read-only artifact of the sync pipeline
- Web editor: disabled by policy
- Sync: one-way, guarded, never force-pushed
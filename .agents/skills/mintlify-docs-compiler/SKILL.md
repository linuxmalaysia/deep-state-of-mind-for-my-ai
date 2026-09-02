---
okf_version: 0.2
type: skill_sop
title: "Mintlify MDX Compiler & One-Way Sync"
timestamp: "2026-08-23T06:57:00Z"
description: "Compiles Sovereign Markdown Palace documents into Mintlify MDX trees and syncs to downstream docs repository under 5 strict safety guards."
topics: ["mintlify", "docs", "sync", "mdx", "safety-guards", "user-manual-style"]
sources: [{title: Mintlify Documentation, url: 'https://mintlify.com/docs'}, "file:///tools/build_mintlify_mdx.py", "file:///scripts/sync_docs.py", "file:///.github/workflows/sync-docs.yml"]
generated: human-and-ai
verified: verified
status: authoritative
stale_after: "2027-08-23T06:57:00Z"
name: mintlify-docs-compiler
---
# Mintlify MDX Compiler & One-Way Sync

This skill automates compiling standard Markdown documents in `docs/` and skills in `.agents/skills/` into Mintlify-compliant MDX (`docs-source/`) and executing a one-way synchronization pipeline to the downstream deployment repository (`linuxmalaysia/my-knowledge-brain`) serving `https://harisfazillah.mintlify.site`.

## User Manual Site Style Standards

The compiler (`tools/build_mintlify_mdx.py`) and any manual MDX authoring must follow these formatting rules:

### 1. Frontmatter Requirements
Every generated `.mdx` file must contain valid YAML frontmatter:
```yaml
---
title: "<50-60 char SEO title, unique across the site>"
sidebarTitle: "<1-3 word Title Case label>"
description: "<130-155 chars, unique, adds information beyond title>"
---
```
- **`sidebarTitle`**: Mandatory and short (1-3 words). Never put the full SEO title in the sidebar. Never repeat the product name.
- **First Paragraph**: Must be plain prose (no JSX components, no code fences) naming the feature and stating what the page covers.
- **Punctuation**: No em dashes (`—`) or en dashes (`–`) as punctuation in prose. Use commas, colons, parentheses, or split sentences.

### 2. Information Architecture (`docs.json`)
- `navigation` must be an object with tabs (≤ 2-3 tabs), ≤ 4-5 groups per tab, and ≥ 2 pages per group.
- Page paths must be extensionless with no leading slash (e.g. `rituals/start-of-day`).
- `index.mdx` is the landing page using `<CardGroup>` and `<Steps>` without raw HTML or inline CSS.

### 3. Mintlify Ignore Rules (`docs-source/.mintignore`)
Must explicitly ignore non-public assets:
```text
AGENTS.md
AGENTS-PROMPT.md
drafts/
*.draft.mdx
```

## The 5 Safety Guards (A-E)

| Guard | Validation Target | Failure Consequence |
|:---|:---|:---|
| **Guard A** | Source directory `docs-source/` exists and `docs.json` is valid JSON. | Immediate abort before contacting remote repository. |
| **Guard B** | Count of `.mdx` files exceeds minimum floor (`MIN_MDX_FILES`, default `5`). | Prevents empty or partial source from wiping downstream docs. |
| **Guard C** | Every navigation path in `docs.json` has a corresponding `.mdx` file. | Fails fast on broken links or missing page files. |
| **Guard D** | File deletions do not exceed cap (`MAX_DELETIONS`, default `10`). | Blocks mass-deletion accidents unless `ALLOW_LARGE_DELETIONS=true`. |
| **Guard E** | Dry-run execution (`--dry-run` or `DRY_RUN=true`). | Previews planned additions/modifications/deletions without touching Git. |

## Step-by-Step Execution Workflow

### Step 1: Compile Markdown to Mintlify MDX
When documents in `docs/` or skills in `.agents/skills/` are created or updated, run the compiler:
```powershell
python tools/build_mintlify_mdx.py
```

### Step 2: Validate with Local Dry-Run
Run the sync script in dry-run mode to verify all 5 guards and review the diff plan:
```powershell
python scripts/sync_docs.py --dry-run
```

### Step 3: Automated Push to Production
Push changes to `main`:
```powershell
git add docs/ docs-source/ .agents/skills/
git commit -m "docs: update sovereign guides and regenerate mdx tree"
git push origin main
```
The GitHub Actions workflow `.github/workflows/sync-docs.yml` triggers automatically, executes the compiler, runs Guards A-E, and updates `my-knowledge-brain` using `Docs Sync Bot <bot@harisfazillah.com>`.

## Recovery Procedure
If the downstream repository is corrupted by an unintended push:
```bash
git clone https://github.com/linuxmalaysia/my-knowledge-brain.git
cd my-knowledge-brain
git log --oneline -n 5
git revert <bad-commit-sha>
git push origin main
```
Then resolve the discrepancy in `deep-state-of-mind-for-my-ai` under `docs/` and re-run `python scripts/sync_docs.py --dry-run`.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-23*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*

# 🚪 Closet: Room Tooling (The Workshop)

This closet documents the **Sovereign Toolchain** — all scripts that operationalize the DSOM protocol on Linux and Windows.

---

## 🛠️ Tool Inventory & Evolution

| Tool | Current Version | Platform | Purpose |
|---|---|---|---|
| `reanimate.sh/.ps1` | v2.2 / v2.0 | Bash/PS | Generates SOD manifest including Palace Registry [14] |
| `hibernation.sh/.ps1` | v2.1 / v2.0 | Bash/PS | EOD Sovereign Save with Palace Spatial Reflection |
| `palace-sync.sh/.ps1` | v1.0 | Bash/PS | Maps git commits → Palace Rooms, generates proposals |
| `reanimate-claude.sh/.ps1` | v2.0 | Bash/PS | 9-section manifest for Claude.ai handover |
| `audit-pre-flight.sh/.ps1` | v5.0 | Bash/PS | Pre-session environment integrity check |
| `git-ritual.sh/.ps1` | v1.0 | Bash/PS | SOD/EOD atomic commit helper |
| `check-usage.sh` / `CheckUsage.ps1` | v8.6 | Bash/PS | Token usage estimator with age column |
| `privacy-guardian.sh/.ps1` | v1.0 | Bash/PS | Blocks secrets/PII from manifests |
| `init-brain.sh/.ps1` | v1.0 | Bash/PS | Initialises `.agent/brain/` scaffold |
| `template-reset.sh/.ps1` | v1.0 | Bash/PS | Project scaffolding reset |
| `build_sovereign_book.sh` | v3.11 | Bash | LuaLaTeX PDF generator for the Sovereign Brain |
| `setup-dsom-control-node.sh` | v1.0 | Bash | Linux control node provisioner |

## 🗝️ Key Design Laws
- **No blind `git add .`** — All tools use selective staging (`git add -u`).
- **Bash-first:** Every tool has a Linux bash version. PowerShell provides Windows parity.
- **Palace-aware (v2.1+):** `hibernation.sh` triggers `palace-sync.sh` before the Sovereign Save.
- **`set -euo pipefail`** enforced in all bash scripts since v6.1.

## 📅 Evolution Timeline
- `2026-01-07`: `init-brain.sh`, `audit-pre-flight.sh`, `reanimate.sh` v1.4 initialised.
- `2026-01-08`: `privacy-guardian.sh`, `template-reset.sh` added.
- `2026-01-11`: Claude.ai support via `reanimate-claude.sh`.
- `2026-01-16`: Full Windows PowerShell parity for all tools. `set -e` injected. `hibernation.sh` v1.0.
- `2026-03-09`: `git-ritual.sh/.ps1` added. `audit-pre-flight` v5.0.
- `2026-03-10`: `CheckUsage.ps1` v8.0→v8.6 — age column, accurate token estimate, ASCII-safe.
- `2026-03-24`: `check-usage.sh` bash version added.
- `2026-03-29`: `hibernation.sh/.ps1` → v2.0, `reanimate.sh/.ps1` → v2.1/v2.0, `reanimate-claude` → v2.0.
- `2026-04-08`: `palace-sync.sh/.ps1` v1.0 created. `hibernation.sh` → v2.1, `reanimate.sh` → v2.2.

---
## 🔗 Retrieval Reference
- **Tooling History in Drawer:** [CHANGELOG.md](file:///d:/Users/LinuxMalaysia/Projects/deep-state-of-mind-for-my-ai/CHANGELOG.md)
- **Backfill Proposal:** `.agent/brain/palace_update_proposal_2026-04-08_1214.md`

---
*Last Refined: 2026-04-08 | Backfill: Full History | Hall: hall_facts | Wing: wing_dsom_core*

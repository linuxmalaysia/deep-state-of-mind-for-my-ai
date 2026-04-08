# HOWTO: palace-sync — Kingdom Spatial Mapping

# docs/tools/HOWTO-PALACE-SYNC.md

> **Standard: DSOM For My AI Protocol v6.1 | Palace v1.0 | Core Engine**
> **Tools:** `palace-sync.ps1`, `palace-sync.sh`
> **Platforms:** Windows Native (T1), Linux/WSL2 (T2)

---

## 1. Purpose

`palace-sync` is the **Spatial Parser** of the Sovereign Markdown Palace. It bridges the gap between raw Git commits and high-density cognitive closets. By analyzing the path of changed files in git, it automatically maps updates to the correct "Room" in the Palace hierarchy.

**Use it to:**
- Automatically categorize git history since the last sync.
- Generate a **Palace Update Proposal** for AI review.
- Perform a full-history backfill to populate a new Palace from scratch.
- Maintain the spatial integrity of the `wings/` directory.

**Location:** 
- `tools/palace-sync.ps1` (Windows)
- `tools/palace-sync.sh` (Linux/WSL2)

---

## 2. Prerequisites

| Requirement | Minimum | Notes |
|:---|:---|:---|
| Protocol Level | Palace v1.0 | Requires the `wings/` directory structure. |
| Sync Marker | `.palace-sync-marker` | Automatically created to track the last sync date. |
| Closets | `closet.md` | Rooms must have a closet file to receive updates. |

---

## 3. Usage

### 3.1 Incremental Sync (EOD Fashion)

```powershell
.\tools\palace-sync.ps1
```

```bash
bash tools/palace-sync.sh
```

Analyzes commits since the date stored in `.palace-sync-marker`. Used during every End-of-Day ritual.

### 3.2 Full History Backfill

```powershell
.\tools\palace-sync.ps1 -Backfill
```

```bash
bash tools/palace-sync.sh --backfill
```

Scans the **entire git history** from the first commit. Essential for onboarding an existing repository into the Palace architecture.

---

## 4. Reading the Output & Status Codes

| Label | Meaning | Action |
|:---|:---|:---|
| `✅ No new commits` | The Palace is already up to date. | None needed. |
| `📝 Building Proposal` | Mapping detected changes. | Wait for the generator to finish. |
| `📄 File: palace_update_proposal...` | Success. | Share this file with the AI for closet updates. |

---

## 5. Implementation Logic (Path Mapping)

The tool uses regex patterns to map files to Rooms:

| Path | Wing | Hall | Room |
|:---|:---|:---|:---|
| `playbooks/`, `roles/` | `wing_dsom_core` | `hall_events` | `room_sovereign_fabric` |
| `.agent/brain/` | `wing_dsom_core` | `hall_events` | `room_brain_artifacts` |
| `tools/` | `wing_dsom_core` | `hall_facts` | `room_tooling` |
| `docs/` | `wing_dsom_core` | `hall_facts` | `room_dsom_protocol` |
| `CHANGELOG.md` | `wing_dsom_core` | `hall_events` | `room_ledger` |

---

## 6. Related Documents

| Document | Purpose |
|:---|:---|
| [`docs/HOWTO-PALACE-ONBOARDING.md`](../HOWTO-PALACE-ONBOARDING.md) | Guide for first-time Palace setup. |
| [`docs/MIRROR-OF-KNOWLEDGE.md`](../MIRROR-OF-KNOWLEDGE.md) | Understanding the underlying memory theory. |

---

*Standard: DSOM For My AI Protocol v6.1 | Palace v1.0 | Harisfazillah Jamel*
*Document Version: v1.0 | Created: 2026-04-08*

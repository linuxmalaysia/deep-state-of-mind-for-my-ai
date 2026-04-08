# HOWTO: reanimate — AI Context Handshake

# docs/tools/HOWTO-REANIMATE.md

> **Standard: DSOM For My AI Protocol v6.1 | Context Engineering**
> **Tools:** `reanimate.ps1`, `reanimate.sh`
> **Platforms:** Windows Native (T1), Linux/WSL2 (T2)

---

## 1. Purpose

`reanimate` is the **Context Assembler** of the DSOM framework. It solves the "Memory Decay" problem in AI sessions by aggregating all critical project artifacts—task lists, walkthroughs, identity protocols, and environment maps—into a single, dense manifest file.

**Use it to:**
- Generate a `sod_manifest_YYYY-MM-DD.txt` for starting a new AI session.
- Inject manual state (EOD summaries or Master Prompts) into the reanimation chain.
- Provide the AI with an immediate "High-Resolution" map of the project state.
- Ensure the AI adheres to the Sovereign Constitution from Minute 1.

**Location:** 
- `tools/reanimate.ps1` (Windows)
- `tools/reanimate.sh` (Linux/WSL2)

---

## 2. Prerequisites

| Requirement | Minimum | Notes |
|:---|:---|:---|
| Brain Artifacts | `task.md`, `walkthrough.md` | Core state files must exist in `.agent/brain/`. |
| Identity Doc | `docs/AI-COGNITIVE-TWIN-PROTOCOL.md` | Defines "Who" the AI is for this project. |
| Topology | `inventory/hosts.yml` | Ingests the server/container map. |

---

## 3. Usage

### 3.1 Standard Reanimation

```powershell
# Windows (T1)
.\tools\reanimate.ps1
```

```bash
# WSL2 / Linux (T2)
bash tools/reanimate.sh
```

### 3.2 Interactive Injection

Upon running, the tool will ask:
`Do you have a manual EOD Summary or Master Prompt addition? (y/N)`

- **If No (Default):** It builds the manifest from the static Git artifacts.
- **If Yes:** It opens a multi-line input buffer. Paste your "Hibernation Notes" or custom instructions here. Type `EOF` (Windows) or `Ctrl+D` (Linux) to save.

---

## 4. Reading the Output & Status Codes

| Label | Meaning | Action |
|:---|:---|:---|
| `[WARNING]` | Missing brain artifact. | Run `init-brain` if first-time setup. |
| `[OK]` | Manifest generated. | Upload the file to your AI now. |

---

## 5. The Cognitive Handshake

After generating the manifest, upload `sod_manifest_YYYY-MM-DD.txt` to your AI and use the following phrase:

> *"Initialise DSOM Protocol v6.1. Read the uploaded manifest. Summarise the Mental Anchor and confirm the 4-Tier environment map. State: 'Sovereign State Synchronised' when ready."*

---

## 6. Related Documents

| Document | Purpose |
|:---|:---|
| [`docs/SOD-RITUAL.md`](../SOD-RITUAL.md) | The Ritual utilizing this manifest. |
| [`docs/REANIMATION-PROMPT-TEMPLATE.md`](../REANIMATION-PROMPT-TEMPLATE.md) | Backup prompt strategies. |
| [`HOWTO-INIT-BRAIN.md`](HOWTO-INIT-BRAIN.md) | Setup the files reanimate needs to read. |

---

*Standard: DSOM For My AI Protocol v6.1 | Harisfazillah Jamel | LinuxMalaysia*
*Document Version: v1.0 | Created: 2026-04-08*

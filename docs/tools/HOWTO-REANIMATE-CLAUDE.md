# HOWTO: reanimate-claude — Anthropic Context Injection

# docs/tools/HOWTO-REANIMATE-CLAUDE.md

> **Standard: DSOM For My AI Protocol v6.1 | Claude AI Integration**
> **Tools:** `reanimate-claude.ps1`, `reanimate-claude.sh`
> **Platforms:** Windows Native (T1), Linux/WSL2 (T2)

---

## 1. Purpose

`reanimate-claude` is a specialized variant of the reanimation tool optimized for **Anthropic Claude**. Unlike the standard reanimate tool which generates a raw `.txt` log, this tool produces a targeted `DSOM-CLAUDE-INIT.md` file designed to be uploaded directly into a **Claude Project Knowledge Base**.

**Use it to:**
- Populate a Claude Project with the latest Sovereign context.
- Bridge the "Memory Gap" between different Claude sessions.
- Ingest a comprehensive "Identity Manifest" into the Claude latent space.
- Ensure strict adherence to the **Sovereign Constitution** on the Anthropic platform.

**Location:** 
- `tools/reanimate-claude.ps1` (Windows)
- `tools/reanimate-claude.sh` (Linux/WSL2)

---

## 2. Prerequisites

| Requirement | Minimum | Notes |
|:---|:---|:---|
| Project Platform | Claude.ai | Specifically for "Projects" feature. |
| Identity Doc | `docs/AI-COGNITIVE-TWIN-PROTOCOL.md` | Required for the 4-Tier map. |
| Structure | `wings/` (Optional) | Can ingest Palace spatial metadata. |

---

## 3. Usage

```powershell
# Windows (T1)
.\tools\reanimate-claude.ps1
```

```bash
# WSL2 / Linux (T2)
bash tools/reanimate-claude.sh
```

The script generates a file named **`DSOM-CLAUDE-INIT.md`** in the project root.

---

## 4. Operation Workflow

1. Run the script on your T1 or T2 node.
2. Run `tools/privacy-guardian` to ensure no environment secrets are in the manifest.
3. Open your project on **Claude.ai**.
4. Go to **"Project Knowledge"** and upload `DSOM-CLAUDE-INIT.md`.
5. Start a new chat and perform the **Cognitive Handshake**.

---

## 5. The Claude Handshake

After uploading the manifest, use this prompt in your first Claude interaction:

> *"Initialise DSOM Protocol v6.1. Read the uploaded manifest. Summarise the current Mental Anchor from .agent/brain/walkthrough.md. Confirm the 4-Tier environment map from AI-COGNITIVE-TWIN-PROTOCOL.md. State: 'Sovereign State Synchronised' when ready."*

---

## 6. Related Documents

| Document | Purpose |
|:---|:---|
| [`docs/CLAUDE-SETUP.md`](../docs/CLAUDE-SETUP.md) | Full Anthropic Claude setup guide. |
| [`HOWTO-REANIMATE.md`](HOWTO-REANIMATE.md) | Standard reanimation for other models (Gemini, GPT). |
| [`HOWTO-PRIVACY-GUARDIAN.md`](HOWTO-PRIVACY-GUARDIAN.md) | Mandatory security scan before upload. |

---

*Standard: DSOM For My AI Protocol v6.1 | Harisfazillah Jamel | LinuxMalaysia*
*Document Version: v1.0 | Created: 2026-04-08*

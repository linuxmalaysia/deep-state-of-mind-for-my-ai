# HOWTO: privacy-guardian — Data Masking Defense

# docs/tools/HOWTO-PRIVACY-GUARDIAN.md

> **Standard: DSOM For My AI Protocol v6.1 | Secret Management**
> **Tools:** `privacy-guardian.ps1`, `privacy-guardian.sh`, `playbooks/dsom/privacy-scan.yml`
> **Platforms:** Windows Native (T1), Linux/WSL2 (T2)

---

## 1. Purpose

`privacy-guardian` is the **Security Sentinel** of the DSOM ecosystem. Before any context manifest is shared with an external LLM (Gemini, Claude, GPT), this tool scans the file for common sensitive data patterns to prevent accidental data leaks or credential exposure.

**Use it to detect:**
- **Network Leaks:** Plaintext IPv4 addresses.
- **Identity Leaks:** Email addresses and local user home paths (e.g., `C:\Users\Admin`).
- **Cloud Secrets:** AWS Access Keys, Google API Keys, GitHub Tokens, OpenAI Secrets, Slack Tokens.
- **Cryption Leaks:** PEM-formatted Private Keys.

**Location:** 
- `tools/privacy-guardian.ps1` (Windows)
- `tools/privacy-guardian.sh` (Linux/WSL2)
- `playbooks/dsom/privacy-scan.yml` (Ansible)

---

## 2. Prerequisites

| Requirement | Minimum | Notes |
|:---|:---|:---|
| Target File | `sod_manifest_*.txt` | Scans the today's manifest by default. |
| Tooling | Regex | Uses native grep (Linux) or Select-String (Windows). |

---

## 3. Usage

### 3.1 Standard Scanning

```powershell
# Windows (T1)
.\tools\privacy-guardian.ps1
```

```bash
# WSL2 / Linux (T2)
bash tools/privacy-guardian.sh
```

### 3.2 Ansible Sweep

```bash
ansible-playbook playbooks/dsom/privacy-scan.yml
```

---

## 4. Scan Patterns

The tool utilizes a library of high-fidelity regex patterns:

| Pattern Type | Scope |
|:---|:---|
| **IPv4** | `([0-9]{1,3}\.){3}[0-9]{1,3}` |
| **GitHub** | `ghp_...` (Tokens) |
| **Google** | `AIza...` (API Keys) |
| **OpenAI** | `sk-...` (API Keys) |
| **Private Keys** | `-----BEGIN ... PRIVATE KEY-----` |

---

## 5. Reading the Output & Status Codes

| Label | Meaning | Action Needed |
|:---|:---|:---|
| `✅ SCAN COMPLETE` | No generic leaks found. | Safe to upload to AI. |
| `⚠️  POTENTIAL LEAK` | Found a match at a specific line. | **REDACT** the manifest manually before upload. |
| `❌ SCAN FAILED` | Security risk confirmed. | DO NOT UPLOAD. Fix the source file or mask the manifest. |

---

## 6. Security Advisory

> [!IMPORTANT]
> This tool is a **Heuristic Scanner**. It detects *patterns*, not every possible secret. 
> 
> - **Always** perform a quick manual scroll-through of your manifest before uploading. 
> - **Never** upload raw `.env` files or `vault/secrets.yml` to an external AI chat.
> - Utilize the [Atomic Git Hygiene](file:///docs/AI-MASTER-PROTOCOL.md) rule to ensure secrets never even enter your git history.

---

## 7. Related Documents

| Document | Purpose |
|:---|:---|
| [`HOWTO-REANIMATE.md`](HOWTO-REANIMATE.md) | Generator of the file this tool scans. |
| [`docs/REANIMATION-PROMPT-TEMPLATE.md`](../docs/REANIMATION-PROMPT-TEMPLATE.md) | Where the manifest is ultimately used. |

---

*Standard: DSOM For My AI Protocol v6.1 | Harisfazillah Jamel | LinuxMalaysia*
*Document Version: v1.0 | Created: 2026-04-08*

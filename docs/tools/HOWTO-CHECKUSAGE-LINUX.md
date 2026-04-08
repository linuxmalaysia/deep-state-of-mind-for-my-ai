# HOWTO: check-usage.sh — Antigravity Session Monitor (Linux)

# docs/tools/HOWTO-CHECKUSAGE-LINUX.md

> **Standard: DSOM For My AI Protocol v6.1 | Context Monitoring**
> **Tool:** `tools/check-usage.sh` | **Version:** v8.6 | **Platform:** Linux / WSL2 (T2)

---

## 1. Purpose

`check-usage.sh` is the **Bash port** of the Sovereign Session Monitor. It reads the `.pb` conversation context files stored by Antigravity in the Linux `$HOME` directory and provides real-time health metrics.

**Use it to:**
- Monitor the context growth of your active Linux-based AI sessions.
- Identified "Dormant" sessions taking up disk space in WSL.
- Forecast API rate limit risks based on **Velocity** (MB/min growth).
- Maintain a stable, high-density development environment on Tier 2 nodes.

**Location:** `tools/check-usage.sh`
**Monitors:** `$HOME/.gemini/antigravity/conversations/*.pb`

---

## 2. Prerequisites

| Requirement | Minimum | Notes |
|:---|:---|:---|
| Operating System | Linux / WSL2 | T2 environment. |
| Shell | Bash 4.0+ | Uses associative arrays. |
| Dependencies | `bc`, `stat` | Required for size and math calculations. |

---

## 3. Usage

### 3.1 Snaphost (Run Once)

```bash
bash tools/check-usage.sh
```

### 3.2 Live Monitor (Loop Mode)

```bash
bash tools/check-usage.sh --loop
```

Refreshes every 60 seconds with a countdown pulse bar.

### 3.3 Full Syntax

```bash
bash tools/check-usage.sh [options]

Options:
  -l, --loop              Live monitor mode
  -i, --interval SECS     Refresh interval [default: 60]
  -w, --threshold MB      WARNING threshold [default: 20]
  -c, --critical MB       CRITICAL threshold [default: 50]
  -n, --top N             Show only top N sessions
  --no-pulse              Suppress the progress bar
```

---

## 4. Reading the Output & Status Codes

| Label | Meaning | Action |
|:---|:---|:---|
| `[>>]` | **Active Session** | Your most recently updated chat. |
| `[ACT]` | **Actively Growing** | Session is currently receiving new context. |
| `[WRN]` | Exceeds `THRESHOLD_MB` | Approaching large context; prepare for sync. |
| `[CRT]` | **LIMIT RISK** | Context is very large; expect AI latency or "decay". |
| `[ZZZ]` | **Dormant** | No activity for >4 hours. |

---

## 5. Token Estimation

The tool uses the standard DSOM 6.1 tokenization heuristic:
`1 MB ≈ 62,500 tokens`

This assumes an average of 4 characters per token across a binary `.pb` payload.

---

## 6. Integration with the Daily Rituals

Run this tool on your WSL2 node during the **Start-of-Day Ritual** to ensure that your T2 context isn't fragmented or bloated before beginning Ansible operations. If your active session is marked `[CRT]`, consider starting a fresh "Project" session.

---

## 7. Related Documents

| Document | Purpose |
|:---|:---|
| [`HOWTO-CHECKUSAGE.md`](HOWTO-CHECKUSAGE.md) | The native Windows PowerShell version of this tool. |
| [`docs/SOD-RITUAL.md`](../docs/SOD-RITUAL.md) | Where monitoring fits in the daily lifecycle. |

---

*Standard: DSOM For My AI Protocol v6.1 | Harisfazillah Jamel | LinuxMalaysia*
*Document Version: v1.0 | Created: 2026-04-08*

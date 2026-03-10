# HOWTO: CheckUsage.ps1 — Antigravity Session Monitor
# docs/tools/HOWTO-CHECKUSAGE.md

> **Standard: DSOM For My AI Protocol v6.1 | GitOps · AIOps · Ansible**
> **Tool:** `tools/CheckUsage.ps1` | **Version:** v8.6 | **Platform:** Windows PowerShell (T1)

---

## 1. Purpose

`CheckUsage.ps1` is the **Sovereign Session Monitor** for the Antigravity AI assistant. It reads the `.pb` conversation context files stored locally by Antigravity and displays real-time health metrics for each session — size, estimated token usage, growth velocity, age, and status.

**Use it to:**
- Know when your current session is approaching the context limit
- Identify dormant old sessions consuming disk space
- Detect burst rate spikes that may trigger API rate limits (RPM)
- Keep a live health dashboard open in a side terminal during active work

**Location:** `tools/CheckUsage.ps1`
**Monitors:** `C:\Users\[you]\.gemini\antigravity\conversations\*.pb`

---

## 2. Prerequisites

| Requirement | Minimum | Notes |
|:---|:---|:---|
| Operating System | Windows 10/11 | T1 environment |
| PowerShell | 5.1+ | Built into Windows |
| Execution Policy | `RemoteSigned` (CurrentUser) | Set once — see §3 |
| Antigravity | Any version | `.pb` files must exist |

---

## 3. First-Time Setup (Run Once)

Open PowerShell and run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

This allows locally written scripts to run. It only affects your user account. You will not need to run this again.

**Verify:**
```powershell
Get-ExecutionPolicy -Scope CurrentUser
# Expected: RemoteSigned
```

---

## 4. Usage

### 4.1 Run Once (Snapshot)

```powershell
.\tools\CheckUsage.ps1
```

Displays the current state of all sessions and exits. A usage tip is shown at the bottom.

### 4.2 Live Monitor (Loop Mode)

```powershell
.\tools\CheckUsage.ps1 -Loop
```

Refreshes every 60 seconds. Shows a countdown bar between refreshes. Press **Ctrl+C** to stop.

### 4.3 Full Syntax

```powershell
.\tools\CheckUsage.ps1 [options]

Options:
  -Loop    (-l)           Live monitor mode (repeats every IntervalSeconds)
  -IntervalSeconds (-i)   Refresh interval in seconds         [default: 60]
  -ThresholdMB     (-w)   MB size to trigger WARNING status   [default: 20]
  -CriticalMB      (-c)   MB size to trigger LIMIT RISK       [default: 50]
  -DormantHours    (-d)   Hours idle before DORMANT status    [default: 4]
  -Top             (-n)   Show only top N sessions            [default: all]
  -NoPulse                Suppress countdown bar in loop mode
  -Help            (-h)   Show the full help screen
```

### 4.4 Examples

```powershell
# Snapshot — run once and exit
.\tools\CheckUsage.ps1

# Live monitor with default 60s refresh
.\tools\CheckUsage.ps1 -Loop

# Live monitor with 30s refresh (short alias)
.\tools\CheckUsage.ps1 -l -i 30

# Top 5 largest sessions only
.\tools\CheckUsage.ps1 -Top 5

# Tighter thresholds — warn at 10MB, critical at 25MB
.\tools\CheckUsage.ps1 -ThresholdMB 10 -CriticalMB 25

# Live monitor for large projects, suppress countdown bar
.\tools\CheckUsage.ps1 -Loop -NoPulse -CriticalMB 80

# Show full help screen
.\tools\CheckUsage.ps1 -Help
```

---

## 5. Reading the Output

### 5.1 Column Reference

| Column | Description |
|:---|:---|
| **Session** | Shortened session UUID (first 8 chars + `...`) |
| **Size(MB)** | Raw file size of the `.pb` context file |
| **Tokens(Est)** | Estimated token count (`Size × 62,500 tokens/MB`) |
| **Velocity** | Size change since last refresh in loop mode (`+X.XX MB`) |
| **Age** | Time since last activity (`just now`, `Xm`, `Xh`, `Xd`, `Xw`) |
| **Last Active** | Timestamp of last write (`MM-DD HH:mm`) |
| **Status** | Health label — see §5.2 |

### 5.2 Status Labels

| Label | Colour | Meaning | Action |
|:---|:---|:---|:---|
| `[>>]` | — | **Current session** (most recently modified) | Your active chat |
| `[OK ]` | Green | Nominal — healthy size and recent activity | None needed |
| `[ACT]` | Cyan | **Actively growing** this refresh cycle | Normal during use |
| `[WRN]` | Yellow | Exceeds `ThresholdMB` (default 20 MB) | Monitor closely |
| `[CRT]` | Red | **LIMIT RISK** — exceeds `CriticalMB` (default 50 MB) | Consider starting a new session |
| `[RPM]` | Magenta | High burst velocity (>2 MB/interval) | Possible rate limit approaching |
| `[ZZZ]` | Dark Grey | **Dormant** — no activity for `DormantHours` (default 4h) | Safe to ignore |

### 5.3 Summary Footer

```
Sessions (26 total)  |  Total: 354.97 MB  |  Est Tokens: 22,185,625  |  WARN: 9  |  CRIT: 0
Token basis: 1 MB ~ 62,500 tokens (4 chars/token avg)
```

- **Total MB** — total disk used by all `.pb` files
- **Est Tokens** — aggregate estimated token count across all sessions
- **WARN / CRIT** — count of sessions in warning or critical state

---

## 6. Token Estimation Methodology

The tool estimates tokens using:

```
1 MB  =  ~250,000 characters  (binary file, predominantly text)
1 token ≈ 4 characters         (Gemini / GPT average)
∴ 1 MB ≈ 62,500 tokens
```

This is more accurate than the commonly cited 50,000 tokens/MB. Actual token count varies by content type (code is denser than prose).

**Interpret estimates as a guide, not an exact count.** Use the `[WRN]` and `[CRT]` thresholds relative to your observed model behaviour.

---

## 7. Troubleshooting

### Script will not run — Execution Policy error

```
CheckUsage.ps1 cannot be loaded because running scripts is disabled on this system.
```

**Fix:** Run once in PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Unknown parameter error

```
[ERROR] Unknown parameter(s): -Loops
```

**Cause:** Typo in the parameter name.
**Fix:** Run `.\tools\CheckUsage.ps1 -Help` to see all valid options.

---

### No .pb files found

```
No .pb conversation files found.
```

**Cause:** Antigravity has not yet created any conversation context files, or the path is wrong.
**Check:** Verify the path exists: `C:\Users\[you]\.gemini\antigravity\conversations\`

---

### Loop mode exits immediately

Ensure you are using `-Loop` (not `-Loops` or `-loop`). The `-l` short alias also works.

---

## 8. Integration with DSOM SOD Ritual

As part of the **Start-of-Day Ritual** (`docs/SOD-RITUAL.md` Step 1), run the snapshot to verify the current session health before starting work:

```powershell
# SOD check — confirm current session is Nominal
.\tools\CheckUsage.ps1

# If current session is [CRT], start a new Antigravity chat and reanimate
# See: docs/REANIMATION-PROMPT-TEMPLATE.md → Prompt 2
```

If the current session exceeds `CriticalMB`, begin a new Antigravity conversation and use the **SOD Reanimation Prompt** to restore context.

---

## 9. Related Documents

| Document | Purpose |
|:---|:---|
| [`docs/SOD-RITUAL.md`](../SOD-RITUAL.md) | Start-of-Day Ritual — includes session health check |
| [`docs/EOD-RITUAL.md`](../EOD-RITUAL.md) | End-of-Day Ritual — Hibernation Notes export |
| [`docs/REANIMATION-PROMPT-TEMPLATE.md`](../REANIMATION-PROMPT-TEMPLATE.md) | AI prompts for new session reanimation |
| [`tools/audit-pre-flight.sh`](../../tools/audit-pre-flight.sh) | Full 5-check workspace audit (Linux/WSL2) |
| [`tools/audit-pre-flight.ps1`](../../tools/audit-pre-flight.ps1) | Full 5-check workspace audit (Windows) |

---

*Standard: DSOM For My AI Protocol v6.1 | Harisfazillah Jamel | LinuxMalaysia*
*Tool Version: v8.6 | Document Version: v1.0 | Created: 2026-03-10*

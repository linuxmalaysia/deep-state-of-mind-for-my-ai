<#
.SYNOPSIS
    Antigravity Token & Quota Monitor (v8.1 ASCII-Safe)
.DESCRIPTION
    Real-time monitor for Gemini Pro / Antigravity conversation context files (.pb).
    Detects Context Limits, Rate Limits (RPM/TPM), session age, velocity spikes,
    and highlights the current active session with a [>>] CURRENT marker.

    Token estimation: 1 MB ~ 62,500 tokens (4 chars/token average,
    1 MB = ~250,000 chars -> 250,000 / 4 = 62,500 tokens).

.PARAMETER Loop
    If set, refreshes every N seconds (default 60). Press Ctrl+C to stop.
.PARAMETER IntervalSeconds
    Refresh interval in seconds when -Loop is active. Default: 60.
.PARAMETER ThresholdMB
    Size in MB to trigger a WARNING status. Default: 20 MB.
.PARAMETER CriticalMB
    Size in MB to trigger a LIMIT RISK status. Default: 50 MB.
.PARAMETER DormantHours
    Hours of inactivity before a session is marked DORMANT. Default: 4 hours.
.PARAMETER Top
    Show only the top N sessions by size. Default: 0 (show all).
.PARAMETER NoPulse
    Suppress the countdown timer during loop mode.

.EXAMPLE
    # Run once (snapshot)
    .\CheckUsage.ps1

    # Real-time monitor, refresh every 30s
    .\CheckUsage.ps1 -Loop -IntervalSeconds 30

    # Show only top 5 largest sessions
    .\CheckUsage.ps1 -Top 5

    # Aggressive thresholds
    .\CheckUsage.ps1 -Loop -ThresholdMB 10 -CriticalMB 30

.NOTES
    Author:  DSOM For My AI Protocol v6.1
    Partner: Harisfazillah Jamel (LinuxMalaysia)
    Version: v8.1 (ASCII-Safe)
    License: GNU GPL v3.0
#>

param (
    [Switch]$Loop,
    [int]$IntervalSeconds  = 60,
    [int]$ThresholdMB      = 20,
    [int]$CriticalMB       = 50,
    [int]$DormantHours     = 4,
    [int]$Top              = 0,
    [Switch]$NoPulse
)

# ── Constants ──────────────────────────────────────────────────────────────────
$CONVERSATION_PATH = "$HOME\.gemini\antigravity\conversations\"
$TOKENS_PER_MB     = 62500   # 1 MB ~ 62,500 tokens (4 chars/token, 1MB = 250k chars)
$VELOCITY_RPM_RISK = 2.0     # MB delta per interval that signals burst risk
$VERSION           = "v8.1"
$HR                = "-" * 108

# ── State ─────────────────────────────────────────────────────────────────────
$PreviousState = @{}   # SessionID -> SizeMB at last refresh

# ── Helper: Format age as human-readable string ────────────────────────────────
function Format-Age {
    param([datetime]$LastWrite)
    $age = (Get-Date) - $LastWrite
    if     ($age.TotalMinutes -lt 1)  { return "just now" }
    elseif ($age.TotalMinutes -lt 60) { return "{0}m ago"  -f [int]$age.TotalMinutes }
    elseif ($age.TotalHours   -lt 24) { return "{0}h ago"  -f [int]$age.TotalHours }
    elseif ($age.TotalDays    -lt 7)  { return "{0}d ago"  -f [int]$age.TotalDays }
    else                              { return "{0}w ago"  -f [int]($age.TotalDays / 7) }
}

# ── Helper: Shorten a UUID-style session ID ────────────────────────────────────
function Format-ShortID {
    param([string]$ID)
    if ($ID.Length -ge 8) { return $ID.Substring(0, 8) + "..." }
    return $ID
}

# ── Main display function ──────────────────────────────────────────────────────
function Show-Usage {
    Clear-Host
    $now = Get-Date

    # ── Title bar ──────────────────────────────────────────────────────────────
    Write-Host ""
    Write-Host ("  [DSOM] Antigravity Sovereign Monitor [{0}]" -f $VERSION) -ForegroundColor Cyan
    Write-Host ("  Time: {0}  |  Path: {1}" -f $now.ToString("yyyy-MM-dd HH:mm:ss"), $CONVERSATION_PATH) -ForegroundColor DarkGray
    if ($Loop) {
        Write-Host ("  Mode: LIVE PULSE (loop)  |  Thresholds: WARN={0}MB  CRIT={1}MB  DORMANT={2}h  |  Ctrl+C to stop" -f $ThresholdMB, $CriticalMB, $DormantHours) -ForegroundColor DarkGray
    } else {
        Write-Host ("  Mode: SNAPSHOT  |  Thresholds: WARN={0}MB  CRIT={1}MB  DORMANT={2}h" -f $ThresholdMB, $CriticalMB, $DormantHours) -ForegroundColor DarkGray
    }
    Write-Host ""

    if (-not (Test-Path $CONVERSATION_PATH)) {
        Write-Host ("  [ERROR] Directory not found: {0}" -f $CONVERSATION_PATH) -ForegroundColor Red
        return
    }

    $files = Get-ChildItem -Path $CONVERSATION_PATH -Filter *.pb -ErrorAction SilentlyContinue

    if (-not $files -or $files.Count -eq 0) {
        Write-Host "  No conversation files (.pb) found." -ForegroundColor Yellow
        return
    }

    # ── Identify current active session (most recently modified) ───────────────
    $latestFile = $files | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    $latestID   = $latestFile.BaseName

    # ── Build data rows ────────────────────────────────────────────────────────
    $rows = $files | ForEach-Object {
        $sizeMB     = [math]::Round($_.Length / 1MB, 2)
        $prevSize   = if ($PreviousState.ContainsKey($_.BaseName)) { $PreviousState[$_.BaseName] } else { $sizeMB }
        $delta      = [math]::Round($sizeMB - $prevSize, 2)

        # Update state for next refresh
        $PreviousState[$_.BaseName] = $sizeMB

        [PSCustomObject]@{
            SessionID    = $_.BaseName
            ShortID      = Format-ShortID $_.BaseName
            SizeMB       = $sizeMB
            EstTokens    = [int]($sizeMB * $TOKENS_PER_MB)
            LastWrite    = $_.LastWriteTime
            LastWriteStr = $_.LastWriteTime.ToString("MM-dd HH:mm")
            Age          = Format-Age $_.LastWriteTime
            AgeHours     = ((Get-Date) - $_.LastWriteTime).TotalHours
            Delta        = $delta
            IsCurrent    = ($_.BaseName -eq $latestID)
        }
    } | Sort-Object SizeMB -Descending

    # ── Apply Top filter ───────────────────────────────────────────────────────
    if ($Top -gt 0) { $rows = $rows | Select-Object -First $Top }

    # ── Column header ──────────────────────────────────────────────────────────
    Write-Host ("  {0}" -f $HR) -ForegroundColor DarkGray
    Write-Host ("  {0,-15} {1,10} {2,13} {3,11} {4,-10} {5,-16} {6}" -f `
        "Session", "Size (MB)", "Tokens (Est)", "Velocity", "Age", "Last Active", "Status") -ForegroundColor Gray
    Write-Host ("  {0}" -f $HR) -ForegroundColor DarkGray

    # ── Data rows ─────────────────────────────────────────────────────────────
    $totalMB     = 0
    $totalTokens = 0
    $warnCount   = 0
    $critCount   = 0

    foreach ($row in $rows) {
        $totalMB     += $row.SizeMB
        $totalTokens += $row.EstTokens

        # Velocity string
        $deltaStr = "         -"
        if ($row.Delta -gt 0) { $deltaStr = "+{0:N2} MB" -f $row.Delta }
        elseif ($row.Delta -lt 0) { $deltaStr = "{0:N2} MB" -f $row.Delta }

        # Default status
        $status = "[OK ] Nominal"
        $color  = "Green"
        $marker = "    "

        if ($row.IsCurrent) { $marker = "[>>]" }

        if ($row.Delta -gt $VELOCITY_RPM_RISK) {
            $status = "[RPM] RISK - High Burst"
            $color  = "Magenta"
            $warnCount++
        } elseif ($row.Delta -gt 0) {
            $status = "[ACT] Active (+{0:N2}MB)" -f $row.Delta
            $color  = "Cyan"
        } elseif ($row.SizeMB -gt $CriticalMB) {
            $status = "[CRT] LIMIT RISK - Pause use"
            $color  = "Red"
            $critCount++
        } elseif ($row.SizeMB -gt $ThresholdMB) {
            $status = "[WRN] Warning (>{0}MB)" -f $ThresholdMB
            $color  = "Yellow"
            $warnCount++
        } elseif ($row.AgeHours -gt $DormantHours -and -not $row.IsCurrent) {
            $status = "[ZZZ] Dormant"
            $color  = "DarkGray"
        } else {
            $status = "[OK ] Nominal"
            $color  = "Green"
        }

        $displayID = "{0} {1}" -f $marker, $row.ShortID

        Write-Host ("  {0,-15} {1,10:N2} {2,13:N0} {3,11} {4,-10} {5,-16} {6}" -f `
            $displayID, $row.SizeMB, $row.EstTokens, $deltaStr, $row.Age, $row.LastWriteStr, $status) `
            -ForegroundColor $color
    }

    # ── Summary footer ─────────────────────────────────────────────────────────
    Write-Host ("  {0}" -f $HR) -ForegroundColor DarkGray

    $totalSessions  = $rows.Count
    $shownLabel     = if ($Top -gt 0 -and $Top -lt $files.Count) { " (top {0} of {1})" -f $Top, $files.Count } else { " ({0} total)" -f $totalSessions }

    Write-Host ("  Sessions{0}  |  Total: {1:N2} MB  |  Est Tokens: {2:N0}  |  WARN: {3}  |  CRIT: {4}" -f `
        $shownLabel, $totalMB, $totalTokens, $warnCount, $critCount) -ForegroundColor DarkGray

    Write-Host ("  Token basis: 1 MB ~ {0:N0} tokens (4 chars/token avg)" -f $TOKENS_PER_MB) -ForegroundColor DarkGray
    Write-Host ""

    # ── Countdown (loop mode only) ────────────────────────────────────────────
    if ($Loop -and -not $NoPulse) {
        Write-Host ("  --- Quota Heartbeat (next refresh in {0}s) ---" -f $IntervalSeconds) -ForegroundColor DarkGray
        for ($i = $IntervalSeconds; $i -gt 0; $i--) {
            $filled  = [int]($i / $IntervalSeconds * 20)
            $bar     = ("#" * $filled) + ("." * (20 - $filled))
            $pct     = [int]($i / $IntervalSeconds * 100)
            Write-Host ("`r  [{0}] {1,3}%  {2,3}s remaining  " -f $bar, $pct, $i) -NoNewline -ForegroundColor DarkCyan
            Start-Sleep -Seconds 1
        }
        Write-Host ("`r" + (" " * 55)) -NoNewline   # clear progress line
    }
}

# ── Entry point ────────────────────────────────────────────────────────────────
if ($Loop) {
    try {
        while ($true) { Show-Usage }
    } catch {
        Write-Host "`n  Monitor stopped." -ForegroundColor Gray
    }
} else {
    Show-Usage
}

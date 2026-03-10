<#
.SYNOPSIS
    Antigravity Token & Quota Monitor (v8.4)
.DESCRIPTION
    Real-time monitor for Gemini Pro / Antigravity conversation context files (.pb).
    Shows size, estimated tokens, velocity, age, and status for each session.
    Marks the most recently active session with [>>].

    Token estimate: 1 MB ~ 62,500 tokens (4 chars/token avg, 1MB = 250k chars).

.PARAMETER Loop
    If set, refreshes continuously. Press Ctrl+C to stop.
.PARAMETER IntervalSeconds
    Refresh interval in seconds (Loop mode). Default: 60.
.PARAMETER ThresholdMB
    MB threshold for WARNING status. Default: 20.
.PARAMETER CriticalMB
    MB threshold for LIMIT RISK status. Default: 50.
.PARAMETER DormantHours
    Hours of inactivity before session is DORMANT. Default: 4.
.PARAMETER Top
    Show only top N sessions by size. Default: 0 (all).
.PARAMETER NoPulse
    Suppress countdown in loop mode.

.EXAMPLE
    .\CheckUsage.ps1
    .\CheckUsage.ps1 -Loop
    .\CheckUsage.ps1 -Loop -IntervalSeconds 30
    .\CheckUsage.ps1 -Top 10 -ThresholdMB 10 -CriticalMB 30

.NOTES
    Author:  DSOM For My AI Protocol v6.1
    Partner: Harisfazillah Jamel (LinuxMalaysia)
    Version: v8.4
    License: GNU GPL v3.0
#>

[CmdletBinding()]
param (
    [Switch]$Loop,
    [int]$IntervalSeconds = 60,
    [int]$ThresholdMB     = 20,
    [int]$CriticalMB      = 50,
    [int]$DormantHours    = 4,
    [int]$Top             = 0,
    [Switch]$NoPulse
)

$CONVERSATION_PATH = "$HOME\.gemini\antigravity\conversations\"
$TOKENS_PER_MB     = 62500
$VERSION           = "v8.4"
$PreviousState     = @{}

function Get-AgeLabel {
    param([datetime]$T)
    $age = (Get-Date) - $T
    if     ($age.TotalMinutes -lt 1)  { return "just now" }
    elseif ($age.TotalMinutes -lt 60) { return ([string][int]$age.TotalMinutes) + "m ago" }
    elseif ($age.TotalHours   -lt 24) { return ([string][int]$age.TotalHours)   + "h ago" }
    elseif ($age.TotalDays    -lt 7)  { return ([string][int]$age.TotalDays)    + "d ago" }
    else                              { return ([string][int]($age.TotalDays/7)) + "w ago" }
}

function Show-Monitor {
    Clear-Host
    $now = Get-Date
    Write-Host ""
    Write-Host ("  [DSOM Sovereign Monitor {0}]  {1}" -f $VERSION, $now.ToString("yyyy-MM-dd HH:mm:ss")) -ForegroundColor Cyan
    Write-Host ("  Path: {0}" -f $CONVERSATION_PATH) -ForegroundColor DarkGray
    Write-Host ("  Thresholds: WARN={0}MB  CRIT={1}MB  DORMANT={2}h" -f $ThresholdMB, $CriticalMB, $DormantHours) -ForegroundColor DarkGray
    Write-Host ""

    if (-not (Test-Path $CONVERSATION_PATH)) {
        Write-Host "  [ERROR] Path not found: $CONVERSATION_PATH" -ForegroundColor Red
        return
    }

    $files = @(Get-ChildItem -Path $CONVERSATION_PATH -Filter "*.pb" -ErrorAction SilentlyContinue)

    if ($files.Count -eq 0) {
        Write-Host "  No .pb conversation files found." -ForegroundColor Yellow
        return
    }

    # Find most recently modified
    $latestID = ($files | Sort-Object LastWriteTime -Descending | Select-Object -First 1).BaseName

    # Build rows array
    $rows = @()
    foreach ($f in $files) {
        $sizeMB   = [math]::Round($f.Length / 1MB, 2)
        $prevSize = if ($PreviousState.ContainsKey($f.BaseName)) { $PreviousState[$f.BaseName] } else { $sizeMB }
        $delta    = [math]::Round($sizeMB - $prevSize, 2)
        $PreviousState[$f.BaseName] = $sizeMB

        $shortID  = if ($f.BaseName.Length -ge 8) { $f.BaseName.Substring(0,8) + "..." } else { $f.BaseName }
        $ageHours = ((Get-Date) - $f.LastWriteTime).TotalHours

        $rows += [PSCustomObject]@{
            ID        = $f.BaseName
            ShortID   = $shortID
            SizeMB    = $sizeMB
            Tokens    = [int]($sizeMB * $TOKENS_PER_MB)
            Age       = Get-AgeLabel $f.LastWriteTime
            AgeHours  = $ageHours
            LastStr   = $f.LastWriteTime.ToString("MM-dd HH:mm")
            Delta     = $delta
            IsCurrent = ($f.BaseName -eq $latestID)
        }
    }

    # Sort by size descending
    $rows = $rows | Sort-Object SizeMB -Descending

    # Apply Top filter
    if ($Top -gt 0) {
        $rows = $rows | Select-Object -First $Top
    }

    # Header
    $sep = "-" * 110
    Write-Host ("  " + $sep) -ForegroundColor DarkGray
    Write-Host ("  {0,-16} {1,10} {2,13} {3,11} {4,-10} {5,-16} {6}" -f `
        "Session", "Size(MB)", "Tokens(Est)", "Velocity", "Age", "Last Active", "Status") -ForegroundColor Gray
    Write-Host ("  " + $sep) -ForegroundColor DarkGray

    $totalMB     = 0.0
    $totalTokens = 0
    $warnCount   = 0
    $critCount   = 0

    foreach ($row in $rows) {
        $totalMB     += $row.SizeMB
        $totalTokens += $row.Tokens

        $velStr = "         -"
        if ($row.Delta -gt 0) { $velStr = "+" + ("{0:N2}" -f $row.Delta) + " MB" }
        if ($row.Delta -lt 0) { $velStr = ("{0:N2}" -f $row.Delta) + " MB" }

        $marker = "    "
        if ($row.IsCurrent) { $marker = "[>>]" }

        $status = "[OK ] Nominal"
        $color  = "Green"

        if ($row.Delta -gt 2.0) {
            $status = "[RPM] RISK - High Burst"
            $color  = "Magenta"
            $warnCount++
        } elseif ($row.Delta -gt 0) {
            $status = "[ACT] Active +" + ("{0:N2}" -f $row.Delta) + "MB"
            $color  = "Cyan"
        } elseif ($row.SizeMB -gt $CriticalMB) {
            $status = "[CRT] LIMIT RISK - Pause"
            $color  = "Red"
            $critCount++
        } elseif ($row.SizeMB -gt $ThresholdMB) {
            $status = "[WRN] Warning >" + $ThresholdMB + "MB"
            $color  = "Yellow"
            $warnCount++
        } elseif ($row.AgeHours -gt $DormantHours -and -not $row.IsCurrent) {
            $status = "[ZZZ] Dormant"
            $color  = "DarkGray"
        }

        $displayID = $marker + " " + $row.ShortID
        Write-Host ("  {0,-16} {1,10:N2} {2,13:N0} {3,11} {4,-10} {5,-16} {6}" -f `
            $displayID, $row.SizeMB, $row.Tokens, $velStr, $row.Age, $row.LastStr, $status) `
            -ForegroundColor $color
    }

    # Footer
    Write-Host ("  " + $sep) -ForegroundColor DarkGray

    $shownNote = if ($Top -gt 0 -and $Top -lt $files.Count) {
        " (top {0} of {1})" -f $Top, $files.Count
    } else {
        " ({0} total)" -f $rows.Count
    }

    Write-Host ("  Sessions{0}  |  Total: {1:N2} MB  |  Est Tokens: {2:N0}  |  WARN: {3}  |  CRIT: {4}" -f `
        $shownNote, $totalMB, $totalTokens, $warnCount, $critCount) -ForegroundColor DarkGray
    Write-Host ("  Token basis: 1 MB ~ {0:N0} tokens (4 chars/token avg)" -f $TOKENS_PER_MB) -ForegroundColor DarkGray
    Write-Host ""
}

# Entry point
if ($Loop) {
    try {
        while ($true) {
            Show-Monitor

            # Countdown lives here — $Loop, $NoPulse, $IntervalSeconds are all in script scope
            if (-not $NoPulse) {
                Write-Host ("  --- Next refresh in {0}s (Ctrl+C to stop) ---" -f $IntervalSeconds) -ForegroundColor DarkGray
                for ($i = $IntervalSeconds; $i -gt 0; $i--) {
                    $filled = [int]($i / $IntervalSeconds * 20)
                    $bar    = ("#" * $filled) + ("." * (20 - $filled))
                    $pct    = [int]($i / $IntervalSeconds * 100)
                    Write-Host ("`r  [{0}] {1,3}%  {2,3}s remaining  " -f $bar, $pct, $i) -NoNewline -ForegroundColor DarkCyan
                    Start-Sleep -Seconds 1
                }
                Write-Host ("`r" + (" " * 55) + "`r") -NoNewline
            } else {
                Start-Sleep -Seconds $IntervalSeconds
            }
        }
    } catch {
        Write-Host "`n  Monitor stopped." -ForegroundColor Gray
    }
} else {
    Show-Monitor
}

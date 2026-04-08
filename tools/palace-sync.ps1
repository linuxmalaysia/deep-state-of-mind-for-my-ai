<#
.SYNOPSIS
    DSOM Palace Sync Tool v1.0 (PowerShell)

.DESCRIPTION
    Reads the git commit history and generates a Palace Update Proposal —
    a structured Markdown file mapping each commit to the relevant Palace Room.
    The AI then reviews this proposal and updates the corresponding closet.md files.

    Modes:
      Default (EOD Batch): Reads commits since the last sync marker.
      -Backfill           : Reads the FULL git history from day zero.

.PARAMETER Backfill
    Switch to enable full history backfill mode.

.EXAMPLE
    .\tools\palace-sync.ps1              # EOD batch sync
    .\tools\palace-sync.ps1 -Backfill    # Full history backfill

.NOTES
    Author:  Harisfazillah Jamel (LinuxMalaysia)
    Partner: Generated with assistance from Google Antigravity
    Version: v1.0
    License: GNU GPL v3.0 or later
#>

[CmdletBinding()]
param(
    [switch]$Backfill
)

$ErrorActionPreference = "Stop"
$VERSION = "v1.0"
$MODE = if ($Backfill) { "BACKFILL" } else { "EOD" }

# --- Setup ---
try {
    $RepoRoot = (git rev-parse --show-toplevel 2>$null).Trim()
} catch { $RepoRoot = $null }

if (-not $RepoRoot) {
    Write-Host "  [ERROR] Not in a Git repository." -ForegroundColor Red
    exit 1
}

$BrainDir      = Join-Path $RepoRoot ".agent" "brain"
$PalaceDir     = Join-Path $BrainDir "wings"
$Registry      = Join-Path $BrainDir "palace_registry.md"
$MarkerFile    = Join-Path $BrainDir ".palace-sync-marker"
$DateStamp     = Get-Date -Format "yyyy-MM-dd"
$TimeStamp     = Get-Date -Format "yyyy-MM-dd_HHmm"
$ProposalFile  = Join-Path $BrainDir "palace_update_proposal_${TimeStamp}.md"

Write-Host ""
Write-Host "  ======================================================================" -ForegroundColor Cyan
Write-Host "  🏛️ DSOM Palace Sync Tool — $VERSION" -ForegroundColor Cyan
Write-Host "  Mode: $MODE" -ForegroundColor Cyan
Write-Host "  Date: $DateStamp" -ForegroundColor Cyan
Write-Host "  ======================================================================" -ForegroundColor Cyan
Write-Host ""

# --- Path-to-Room Mapping ---
function Get-PalaceRoom {
    param([string]$FilePath)

    if ($FilePath -match "^(playbooks|inventory|roles|vault)/") {
        return @{ Wing="wing_dsom_core"; Hall="hall_events"; Room="room_sovereign_fabric" }
    }
    if ($FilePath -match "^\.agent/brain/") {
        return @{ Wing="wing_dsom_core"; Hall="hall_events"; Room="room_brain_artifacts" }
    }
    if ($FilePath -match "^tools/") {
        return @{ Wing="wing_dsom_core"; Hall="hall_facts"; Room="room_tooling" }
    }
    if ($FilePath -match "^docs/AI-MASTER-PROTOCOL|^docs/OPERATIONAL") {
        return @{ Wing="wing_dsom_core"; Hall="hall_facts"; Room="room_dsom_protocol" }
    }
    if ($FilePath -match "^(CHANGELOG|HISTORY)\.md$") {
        return @{ Wing="wing_dsom_core"; Hall="hall_events"; Room="room_ledger" }
    }
    if ($FilePath -match "^(README|SUMMARY|mkdocs)") {
        return @{ Wing="wing_dsom_core"; Hall="hall_facts"; Room="room_dsom_protocol" }
    }
    if ($FilePath -match "^docs/") {
        return @{ Wing="wing_dsom_core"; Hall="hall_facts"; Room="room_dsom_protocol" }
    }
    return @{ Wing="wing_dsom_core"; Hall="hall_discoveries"; Room="room_uncategorised" }
}

# --- Determine git log range ---
$GitSinceArg = ""
$SinceLabel  = ""

if ($MODE -eq "BACKFILL") {
    Write-Host "  📚 Backfill mode: scanning FULL git history..." -ForegroundColor Yellow
    $SinceLabel = "the beginning of the project"
} else {
    if (Test-Path $MarkerFile) {
        $LastSync   = (Get-Content $MarkerFile -Raw).Trim()
        Write-Host "  🔍 EOD mode: scanning commits since last sync ($LastSync)..." -ForegroundColor Yellow
        $GitSinceArg = "--after=$LastSync"
        $SinceLabel  = $LastSync
    } else {
        Write-Host "  ⚠️  No sync marker found. Running full scan for first-time setup..." -ForegroundColor Yellow
        $SinceLabel = "the beginning (first run)"
    }
}

Write-Host ""

# --- Collect commits ---
$GitArgs = @("log", "--pretty=format:%H|%as|%s", "--name-only", "--diff-filter=ACMR")
if ($GitSinceArg) { $GitArgs += $GitSinceArg }
$CommitLog = git -C $RepoRoot @GitArgs 2>$null

if (-not $CommitLog) {
    Write-Host "  ✅ No new commits to process since $SinceLabel." -ForegroundColor Green
    $DateStamp | Out-File -FilePath $MarkerFile -Encoding UTF8
    exit 0
}

Write-Host "  📝 Building Palace Update Proposal..." -ForegroundColor Cyan

# --- Build proposal header ---
$ProposalLines = [System.Collections.Generic.List[string]]::new()
$ProposalLines.Add("# 🏛️ Palace Update Proposal")
$ProposalLines.Add("")
$ProposalLines.Add("> **Generated:** $TimeStamp  ")
$ProposalLines.Add("> **Mode:** $MODE  ")
$ProposalLines.Add("> **Scope:** Commits since $SinceLabel  ")
$ProposalLines.Add("> **Status:** PENDING AI REVIEW — Do not commit until closets are updated.")
$ProposalLines.Add("")
$ProposalLines.Add("---")
$ProposalLines.Add("")
$ProposalLines.Add("## 📋 Instructions for AI")
$ProposalLines.Add("")
$ProposalLines.Add("For each entry below:")
$ProposalLines.Add("1. Read the **Commit Subject** and **Files Changed**.")
$ProposalLines.Add("2. Navigate to the **Target Closet** path listed.")
$ProposalLines.Add("3. Add a concise, high-density entry to that closet's knowledge summary.")
$ProposalLines.Add("4. Cross-link back to this proposal file's date for audit trail.")
$ProposalLines.Add("5. Update ``palace_registry.md`` if a new Room was created.")
$ProposalLines.Add("")
$ProposalLines.Add("---")
$ProposalLines.Add("")

# --- Parse commits ---
$RoomGroups = @{}
$CurrentHash = ""
$CurrentDate = ""
$CurrentMsg  = ""
$CurrentFiles = [System.Collections.Generic.List[string]]::new()

function Process-Commit {
    if (-not $script:CurrentHash) { return }

    $SeenRooms = @{}
    foreach ($f in $script:CurrentFiles) {
        $Mapping  = Get-PalaceRoom -FilePath $f
        $RoomKey  = "$($Mapping.Wing)/$($Mapping.Hall)/$($Mapping.Room)"

        if (-not $script:RoomGroups.ContainsKey($RoomKey)) {
            $script:RoomGroups[$RoomKey] = [System.Collections.Generic.List[string]]::new()
        }

        if (-not $SeenRooms.ContainsKey($RoomKey)) {
            $SeenRooms[$RoomKey] = $true
            $ClosetPath = "wings/$($Mapping.Wing)/$($Mapping.Hall)/$($Mapping.Room)/closet.md"
            $script:RoomGroups[$RoomKey].Add("### ``$($script:CurrentHash.Substring(0,7))`` — $($script:CurrentDate)")
            $script:RoomGroups[$RoomKey].Add("**Subject:** $($script:CurrentMsg)")
            $script:RoomGroups[$RoomKey].Add("**Files:** ``$f``")
            $script:RoomGroups[$RoomKey].Add("**Target Closet:** ``.agent/brain/$ClosetPath``")
            $script:RoomGroups[$RoomKey].Add("")
        } else {
            # Append file to existing entry
            $last = $script:RoomGroups[$RoomKey].Count - 1
            # Find the Files line and append
            for ($i = $script:RoomGroups[$RoomKey].Count - 1; $i -ge 0; $i--) {
                if ($script:RoomGroups[$RoomKey][$i] -match "^\*\*Files:\*\*") {
                    $script:RoomGroups[$RoomKey][$i] += " ``$f``"
                    break
                }
            }
        }
    }
}

foreach ($line in $CommitLog) {
    if ($line -match "^([0-9a-f]{40})\|(\d{4}-\d{2}-\d{2})\|(.+)$") {
        Process-Commit
        $CurrentHash  = $Matches[1]
        $CurrentDate  = $Matches[2]
        $CurrentMsg   = $Matches[3]
        $CurrentFiles = [System.Collections.Generic.List[string]]::new()
    } elseif ($line.Trim() -ne "") {
        $CurrentFiles.Add($line.Trim())
    }
}
Process-Commit

# --- Append grouped rooms to proposal ---
if ($RoomGroups.Count -eq 0) {
    $ProposalLines.Add("*(No file changes detected in the commit range.)*")
} else {
    foreach ($RoomKey in ($RoomGroups.Keys | Sort-Object)) {
        $Parts = $RoomKey.Split("/")
        $ProposalLines.Add("## 🚪 Room: ``$($Parts[2])``")
        $ProposalLines.Add("> **Wing:** ``$($Parts[0])`` | **Hall:** ``$($Parts[1])``")
        $ProposalLines.Add("")
        foreach ($entry in $RoomGroups[$RoomKey]) {
            $ProposalLines.Add($entry)
        }
        $ProposalLines.Add("---")
        $ProposalLines.Add("")
    }
}

# --- Post-review checklist ---
$ProposalLines.Add("")
$ProposalLines.Add("## ✅ Post-Review Checklist")
$ProposalLines.Add("")
$ProposalLines.Add("- [ ] All closets updated with new knowledge")
$ProposalLines.Add("- [ ] ``palace_registry.md`` updated if new Rooms were created")
$ProposalLines.Add("- [ ] This proposal file committed to Git alongside closet updates")
$ProposalLines.Add("")
$ProposalLines.Add("---")
$ProposalLines.Add("*Generated by palace-sync.ps1 $VERSION | DSOM Protocol v6.1*")

# --- Write proposal file ---
($ProposalLines -join "`n") | Out-File -FilePath $ProposalFile -Encoding UTF8

# --- Update sync marker ---
$DateStamp | Out-File -FilePath $MarkerFile -Encoding UTF8

# --- Summary ---
Write-Host ""
Write-Host "  ======================================================================" -ForegroundColor Green
Write-Host "  ✅ Palace Update Proposal generated." -ForegroundColor Green
Write-Host "  ======================================================================" -ForegroundColor Green
Write-Host "  📄 File:  $(Split-Path $ProposalFile -Leaf)" -ForegroundColor Green
Write-Host "  🚪 Rooms: $($RoomGroups.Count) Rooms affected" -ForegroundColor Green
Write-Host "  📍 Path:  $ProposalFile" -ForegroundColor Green
Write-Host ""
Write-Host "  NEXT STEP: Ask your AI to review this proposal and update" -ForegroundColor Cyan
Write-Host "  the corresponding closet.md files in .agent/brain/wings/" -ForegroundColor Cyan
Write-Host "  ======================================================================" -ForegroundColor Green
Write-Host ""

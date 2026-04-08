<#
.SYNOPSIS
    DSOM End-of-Day (EOD) — Palace Edition
    Automates the EOD ritual natively on Windows (T1).
    - Runs Palace Sync to generate the update proposal
    - Validates brain artifacts (walkthrough anchor + task progress)
    - Stages and commits brain artifacts + Palace files
    - Pushes to origin/main

    The closet editing step (review & update palace_update_proposal) remains
    a human+AI step. This playbook commits AFTER that review is done (or before if skipping review).

.EXAMPLE
    .\tools\eod-palace.ps1

.NOTES
    Author:  Harisfazillah Jamel (LinuxMalaysia)
    Version: v1.0 | 2026-04-08
#>

$ErrorActionPreference = "Stop"

try {
    $RepoRoot = (git rev-parse --show-toplevel 2>$null).Trim()
} catch { exit 1 }

$DateStamp = Get-Date -Format "yyyy-MM-dd"
$TimeStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$BrainDir = Join-Path $RepoRoot ".agent" "brain"
$TaskFile = Join-Path $BrainDir "task.md"
$WalkthroughFile = Join-Path $BrainDir "walkthrough.md"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  DSOM EOD RITUAL — PALACE EDITION v1.0" -ForegroundColor Cyan
Write-Host "  $TimeStamp" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# Step 1: Validate Brain Artifacts
Write-Host ""
Write-Host "  [1/6] Validate task.md exists and has completed tasks..." -ForegroundColor Yellow
if (-not (Test-Path $TaskFile)) { Write-Host "    [FAIL] task.md not found" -ForegroundColor Red; exit 1 }
$TaskCompleted = (Select-String -Path $TaskFile -Pattern "\[x\]" -AllMatches).Matches.Count
if ($TaskCompleted -eq 0) { Write-Host "    [FAIL] No completed tasks found in task.md" -ForegroundColor Red; exit 1 }
Write-Host "    [OK] task.md: $TaskCompleted completed tasks found." -ForegroundColor Green

Write-Host "  [1/6] Validate walkthrough.md has today's anchor..." -ForegroundColor Yellow
if (-not (Test-Path $WalkthroughFile)) { Write-Host "    [FAIL] walkthrough.md not found" -ForegroundColor Red; exit 1 }
$AnchorFound = Select-String -Path $WalkthroughFile -Pattern $DateStamp -Quiet
if (-not $AnchorFound) { Write-Host "    [FAIL] Session anchor for $DateStamp NOT found in walkthrough.md" -ForegroundColor Red; exit 1 }
Write-Host "    [OK] walkthrough.md: Session anchor for $DateStamp confirmed." -ForegroundColor Green

# Step 2: Palace Sync
Write-Host ""
Write-Host "  [2/6] Run Palace Sync (generate update proposal)..." -ForegroundColor Yellow
& .\tools\palace-sync.ps1

# Step 3: Show Dirty Files
Write-Host ""
Write-Host "  [3/6] Review uncommitted changes..." -ForegroundColor Yellow
$DirtyFilesRaw = git status --short 2>&1
$DirtyFiles = if ($null -ne $DirtyFilesRaw) { ($DirtyFilesRaw -join "`n").Trim() } else { "" }
if ([string]::IsNullOrWhiteSpace($DirtyFiles)) {
    Write-Host "    (working tree clean)" -ForegroundColor DarkGray
} else {
    Write-Host $DirtyFiles -ForegroundColor Gray
}

# Step 4: Stage
Write-Host ""
Write-Host "  [4/6] Stage brain artifacts & updated tracking files..." -ForegroundColor Yellow
git add $TaskFile
git add $WalkthroughFile
$PalaceRegistry = Join-Path $BrainDir "palace_registry.md"
if (Test-Path $PalaceRegistry) { git add $PalaceRegistry }
$WingsDir = Join-Path $BrainDir "wings"
if (Test-Path $WingsDir) { git add "$WingsDir/" }
git add -u

# Step 5: Commit
Write-Host ""
Write-Host "  [5/6] Commit staged changes..." -ForegroundColor Yellow
$StagedFilesRaw = git diff --cached --name-only 2>&1
$StagedFiles = if ($null -ne $StagedFilesRaw) { ($StagedFilesRaw -join "`n").Trim() } else { "" }
if (-not [string]::IsNullOrWhiteSpace($StagedFiles)) {
    git commit -m "chore(eod): Palace sync + sovereign save $DateStamp [Native EOD Palace v1.0]"
} else {
    Write-Host "    (nothing new to commit — working tree already clean)" -ForegroundColor DarkGray
}

# Step 6: Push
Write-Host ""
Write-Host "  [6/6] Push to origin/main..." -ForegroundColor Yellow
git push origin main

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "  SLEEP WELL, ARCHITECT. YOUR SOVEREIGN STATE IS SAVED." -ForegroundColor Green
Write-Host "" -ForegroundColor Green
Write-Host "  Palace sync committed. State pushed to origin." -ForegroundColor Green
Write-Host "" -ForegroundColor Green
Write-Host "  REMAINING HUMAN STEPS:" -ForegroundColor Cyan
Write-Host "  - Review the latest palace_update_proposal_$DateStamp.md with your AI" -ForegroundColor Cyan
Write-Host "  - Update relevant closets in .agent/brain/wings/" -ForegroundColor Cyan
Write-Host "  - Commit closet updates: git add .agent/brain/ && git commit" -ForegroundColor Cyan
Write-Host "" -ForegroundColor Cyan
Write-Host "  Resume tomorrow with:" -ForegroundColor Cyan
Write-Host "    .\tools\sod-palace.ps1" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Green

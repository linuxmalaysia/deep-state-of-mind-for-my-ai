<#
.SYNOPSIS
    DSOM Checkpoint Ritual v1.0 (PowerShell)

.DESCRIPTION
    Automates a mid-day continuous integration save:
      - Generates the Palace Update Proposal without stopping
      - Mechanically splits commits (tracked vs untracked limits risk)
      - Pushes immediately to origin

.EXAMPLE
    .\tools\checkpoint.ps1

.NOTES
    Author:  Harisfazillah Jamel (LinuxMalaysia)
    Version: v1.0 
#>

$ErrorActionPreference = "Stop"

$DateStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  DSOM MID-DAY CHECKPOINT RITUAL — PALACE EDITION" -ForegroundColor Cyan
Write-Host "  $DateStamp" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "  [1/4] Generating Palace Update Proposal..." -ForegroundColor Yellow
try {
    .\tools\palace-sync.ps1
} catch {
    Write-Host "  [WARNING] palace-sync.ps1 failed to generate proposal." -ForegroundColor Magenta
}

Write-Host ""
Write-Host "  [2/4] Stage / Commit tracked modifications..." -ForegroundColor Yellow
$TrackedChanges = (git diff --name-only).Trim()
if (-not [string]::IsNullOrWhiteSpace($TrackedChanges)) {
    git add -u
    git commit -m "chore(checkpoint): modified tracked files [$DateStamp]"
    Write-Host "    -> Committed tracked modifications." -ForegroundColor Green
} else {
    Write-Host "    -> No tracked modifications to commit." -ForegroundColor DarkGray
}

Write-Host ""
Write-Host "  [3/4] Stage / Commit newly added untracked files..." -ForegroundColor Yellow
$UntrackedFiles = (git ls-files --others --exclude-standard).Trim()
if (-not [string]::IsNullOrWhiteSpace($UntrackedFiles)) {
    git add .
    git commit -m "chore(checkpoint): untracked new files [$DateStamp]"
    Write-Host "    -> Committed untracked configurations." -ForegroundColor Green
} else {
    Write-Host "    -> No untracked files to commit." -ForegroundColor DarkGray
}

Write-Host ""
Write-Host "  [4/4] Pushing to origin/main..." -ForegroundColor Yellow
git push origin main

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "  ✅ MID-DAY CHECKPOINT SAVED" -ForegroundColor Green
Write-Host "" -ForegroundColor Green
Write-Host "  Tracked and untracked files have been compartmentalised and pushed." -ForegroundColor Green
Write-Host "  Palace update proposal generated (ready for EOD review later today)." -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green

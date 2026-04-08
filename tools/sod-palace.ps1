<#
.SYNOPSIS
    DSOM Start-of-Day (SOD) — Palace Edition
    Automates the mechanical SOD ritual natively on Windows (T1).
    The AI handshake (manifest upload) remains a manual human step.

.EXAMPLE
    .\tools\sod-palace.ps1

.NOTES
    Author:  Harisfazillah Jamel (LinuxMalaysia)
    Version: v1.0 | 2026-04-08
#>

$ErrorActionPreference = "Stop"

try {
    $RepoRoot = (git rev-parse --show-toplevel 2>$null).Trim()
} catch { 
    Write-Host "  [ERROR] Not in a git repository." -ForegroundColor Red
    exit 1 
}

$DateStamp = Get-Date -Format "yyyy-MM-dd"
$TimeStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$BrainDir = Join-Path $RepoRoot ".agent" "brain"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  DSOM SOD RITUAL — PALACE EDITION v1.0" -ForegroundColor Cyan
Write-Host "  $TimeStamp" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "  [1/4] Git pull (rebase) from origin/main..." -ForegroundColor Yellow
$gitPull = git pull --rebase origin main 2>&1
Write-Host ($gitPull -join "`n")

Write-Host ""
Write-Host "  [2/4] Run Pre-Flight Audit..." -ForegroundColor Yellow
# Run without stopping script if audit fails (so user sees output)
& .\tools\audit-pre-flight.ps1

Write-Host ""
Write-Host "  [3/4] Verify Palace Registry exists..." -ForegroundColor Yellow
$PalaceRegistry = Join-Path $BrainDir "palace_registry.md"
if (Test-Path $PalaceRegistry) {
    Write-Host "  [OK] Palace Registry found — AI will receive Section [14] at handshake." -ForegroundColor Green
} else {
    Write-Host "  [WARN] Palace Registry missing — run: .\tools\palace-sync.ps1 -Backfill" -ForegroundColor Magenta
}

Write-Host ""
Write-Host "  [4/4] Generate Reanimation Manifest (Palace-aware)..." -ForegroundColor Yellow
& .\tools\reanimate.ps1

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "  SOD MECHANICAL STEPS COMPLETE" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "  NEXT — MANUAL STEP (cannot be automated):" -ForegroundColor Cyan
Write-Host "  1. Upload the highest numbered sod_manifest_$DateStamp*.txt to your AI" -ForegroundColor Cyan
Write-Host "  2. Say to the AI:" -ForegroundColor Cyan
Write-Host "     'Initialise DSOM Protocol v6.1 + Palace v1.0." -ForegroundColor Cyan
Write-Host "      Read the manifest. Walk the Palace Registry in Section [14]." -ForegroundColor Cyan
Write-Host "      State: Sovereign State Synchronised when ready.'" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Palace Registry loaded in Section [14] — AI has spatial awareness." -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Green

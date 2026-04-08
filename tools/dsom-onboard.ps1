<#
.SYNOPSIS
    DSOM Framework Onboarding Bootstrap Script
.DESCRIPTION
    Downloads and executes the Ansible playbook to structure the target repository.
#>

$ErrorActionPreference = "Stop"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "      🚀 DSOM Framework Onboarding Initiated" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Verify git repository
try {
    $isGitRepo = git rev-parse --is-inside-work-tree 2>&1
    if ("$isGitRepo" -ne "true") { Throw }
} catch {
    Write-Host "ERROR: You must run this script from inside a git repository." -ForegroundColor Red
    exit 1
}

# Determine dates and temporary names
$Timestamp = Get-Date -Format "yyyy-MM-dd"
$TimeSuffix = Get-Date -Format "HHmmss"
$TmpBranch = "dsom-onboarding-$Timestamp-$TimeSuffix"

Write-Host "[1/4] Checking dependencies..." -ForegroundColor Yellow
$AnsibleCommand = "wsl"
$AnsibleArgs = "ansible-playbook"
$hasWsl = Get-Command wsl -ErrorAction SilentlyContinue
if (-not $hasWsl) {
    Write-Host "ERROR: WSL is required to run ansible-playbook on Windows." -ForegroundColor Red
    exit 1
}

Write-Host "[2/4] Creating temporary branch: $TmpBranch" -ForegroundColor Yellow
$gitDiff = git diff-index --quiet HEAD -- 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: You have uncommitted changes. Stashing them..." -ForegroundColor Magenta
    git stash
}
git checkout -b "$TmpBranch"

Write-Host "[3/4] Downloading DSOM Onboarding Playbook..." -ForegroundColor Yellow
$PlaybookDir = Join-Path $env:TEMP "dsom-onboard-$Timestamp-$(Get-Random)"
New-Item -ItemType Directory -Force -Path $PlaybookDir | Out-Null
$PlaybookFile = Join-Path $PlaybookDir "onboard-dsom.yml"

$Url = "https://raw.githubusercontent.com/linuxmalaysia/deep-state-of-mind-for-my-ai/main/playbooks/dsom/onboard-dsom.yml"
Invoke-WebRequest -Uri $Url -OutFile $PlaybookFile

Write-Host "[4/4] Executing Ansible Playbook..." -ForegroundColor Yellow
$env:ANSIBLE_NOCOWS = "1"
# Convert Windows path to WSL path for ansible-playbook
$PlaybookFileWsl = (wsl wslpath -u "'$PlaybookFile'").Trim()

wsl ansible-playbook $PlaybookFileWsl -e "timestamp=$Timestamp"

Write-Host "`nCleaning up Playbook..." -ForegroundColor Gray
Remove-Item -Recurse -Force $PlaybookDir

Write-Host "============================================================" -ForegroundColor Green
Write-Host "      ✅ DSOM Onboarding Architecture Synchronized" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "ACTION REQUIRED:" -ForegroundColor Cyan
Write-Host "----------------"
Write-Host "1. We have fetched all required DSOM tools, playbooks, and docs into this branch ($TmpBranch)."
Write-Host "2. Any existing files that collided with DSOM files have been safely kept. The incoming DSOM files were renamed to include '$Timestamp' in their names."
Write-Host "3. Please review the changes using 'git status'."
Write-Host "4. Commit the changes: git add . && git commit -m 'chore: onboard DSOM framework'"
Write-Host "5. Merge into your main working branch to finalize the setup."
Write-Host ""

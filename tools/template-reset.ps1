<#
.SYNOPSIS
    DSOM Template Reset Tool (V1.0)
    
.DESCRIPTION
    Prepares a DSOM clone for a new project. It purges old Git history and 
    resets brain artifacts to a "Golden Image" state.
    
.AUTHOR
    Harisfazillah Jamel (LinuxMalaysia)
    
.LICENSE
    GNU GPL v3.0 or later
#>

$ErrorActionPreference = "Stop"

# Colors
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"

# 1. Setup Variables
try {
    $RepoRoot = git rev-parse --show-toplevel 2>$null
} catch {
    $RepoRoot = $null
}

if (-not $RepoRoot) {
    Write-Host "❌ Error: Not in a Git repository." -ForegroundColor $Red
    exit 1
}

Write-Host "⚠️  WARNING: This will reset brain files and remove Git history." -ForegroundColor $Yellow
$Confirm = Read-Host "Are you sure you want to proceed? (y/N)"

if ($Confirm -notmatch "^[yY]") {
    Write-Host "Operation cancelled."
    exit 0
}

# 2. Purge Git History
Write-Host "🧹 Removing old Git history..." -ForegroundColor $Yellow
$GitDir = Join-Path $RepoRoot ".git"

if (Test-Path $GitDir) {
    Remove-Item -Path $GitDir -Recurse -Force | Out-Null
}

Set-Location $RepoRoot
git init
Write-Host "Git initialized."

# 3. Reset Brain Artifacts
$BrainDir = Join-Path $RepoRoot ".agent" "brain"
if (-not (Test-Path $BrainDir)) {
    New-Item -ItemType Directory -Path $BrainDir -Force | Out-Null
}

Write-Host "🧠 Resetting Brain Artifacts..." -ForegroundColor $Cyan

# Reset Task.md
$TaskContent = @"
# 🎯 Current Task: Project Initialization
- [ ] Define initial architectural goals.
- [ ] Update implementation_plan.md with the new vision.
- [ ] Run tools/reanimate.ps1 for the first handshake.
"@
Set-Content -Path (Join-Path $BrainDir "task.md") -Value $TaskContent -Encoding UTF8

# Reset Walkthrough.md
$DateToday = Get-Date -Format "yyyy-MM-dd"
$WalkthroughContent = @"
# 🏁 DSOM Project Walkthrough & Session Log

## 📜 Historical Context
This project is derived from the DSOM Template.

## 🏁 Session Anchor: $DateToday (Initialization)
- **Accomplished:** Project cloned and reset using template-reset.ps1.
- **Current State:** New project logic initialized.
- **Mental Anchor:** Ready for the first Architectural Handshake.
"@
Set-Content -Path (Join-Path $BrainDir "walkthrough.md") -Value $WalkthroughContent -Encoding UTF8

# Reset Implementation Plan
$PlanContent = @"
# 🗺️ New Project Implementation Plan
- [ ] Phase 1: Requirement Analysis
- [ ] Phase 2: Core Logic Development
"@
Set-Content -Path (Join-Path $BrainDir "implementation_plan.md") -Value $PlanContent -Encoding UTF8

Write-Host "✅ Template Reset Complete." -ForegroundColor $Green
Write-Host "👉 Next steps: Update README.md and run 'git add .' to start your new history." -ForegroundColor $Yellow

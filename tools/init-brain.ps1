<#
.SYNOPSIS
    DSOM Brain Initializer (V4.1 - Root Aware)
    
.DESCRIPTION
    Safely initializes the Deep State of Mind (DSOM) directory and artifacts 
    at the repository root to ensure cognitive continuity for AI agents.
    
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
$Cyan = "Cyan"

# Find the Git root directory
try {
    $RootDir = git rev-parse --show-toplevel 2>$null
} catch {
    $RootDir = $null
}

if (-not $RootDir) {
    Write-Host "[ERROR] This directory is not a Git repository." -ForegroundColor $Red
    Write-Host "Please run 'git init' first." -ForegroundColor $Yellow
    exit 1
}

$BrainDir = Join-Path $RootDir ".agent" "brain"
Write-Host "Targeting DSOM Root: $RootDir" -ForegroundColor $Cyan

# 1. Create Directory Structure
if (-not (Test-Path $BrainDir)) {
    New-Item -ItemType Directory -Path $BrainDir -Force | Out-Null
    Write-Host "[NEW] Created directory: $BrainDir" -ForegroundColor $Green
} else {
    Write-Host "[SKIP] Directory $BrainDir already exists." -ForegroundColor $Yellow
}

# 2. Define Files and Content
$Files = @{
    "task.md" = "# 🎯 Current Task`n`n- [ ] Task 1: Initialize project`n- [ ] Task 2: Sync state with AI"
    "walkthrough.md" = "# 🏁 Walkthrough`n`n## Session Log`n- Project initialized using DSOM Protocol v4.1."
    "implementation_plan.md" = "# 🗺️ Implementation Plan`n`n## Phase 1: Infrastructure`n- [x] Brain artifacts deployment`n- [ ] Project logic hardening"
    "DSOM_TEMPLATE.md" = "# 🧠 Deep State Walkthrough Template`n`n## 🏗️ 1. The Architectural `"Why`"`n`n## 🛠️ 2. Implementation Logic`n`n## 🏁 3. Mental Anchor"
}

# 3. Create Files Safely
foreach ($FileName in $Files.Keys) {
    $TargetPath = Join-Path $BrainDir $FileName
    if (-not (Test-Path $TargetPath)) {
        # Using Set-Content with UTF8 encoding for cross-platform compatibility
        Set-Content -Path $TargetPath -Value $Files[$FileName] -Encoding UTF8
        Write-Host "[NEW] Created file: $TargetPath" -ForegroundColor $Green
    } else {
        Write-Host "[SKIP] File $TargetPath already exists." -ForegroundColor $Yellow
    }
}

Write-Host "==================================================" -ForegroundColor $Cyan
Write-Host "DSOM Brain is Ready. Open Source Sovereignty Secured." -ForegroundColor $Green
Write-Host "==================================================" -ForegroundColor $Cyan

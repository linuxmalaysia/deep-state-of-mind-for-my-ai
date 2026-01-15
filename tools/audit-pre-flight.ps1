<#
.SYNOPSIS
    Universal DSOM Audit Pre-Flight (V4.1 - Root Aware)
    
.DESCRIPTION
    Enforces synchronization between the physical environment, Git state, 
    and the AI's "External Brain" before starting a development session.
    
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
    Write-Host "[ERROR] Audit failed: Not a git repository." -ForegroundColor $Red
    exit 1
}

$BrainDir = Join-Path $RootDir ".agent" "brain"

Write-Host "==================================================" -ForegroundColor $Cyan
Write-Host "   DEEP STATE OF MIND (DSOM) INTELLIGENCE AUDIT   " -ForegroundColor $Cyan
Write-Host "   Project Root: $RootDir" -ForegroundColor $Cyan
Write-Host "==================================================" -ForegroundColor $Cyan

# 1. BRAIN CHECK
Write-Host "Step 1: Checking AI Brain Artifacts..." -ForegroundColor $Yellow
$RequiredFiles = @("task.md", "walkthrough.md")

foreach ($file in $RequiredFiles) {
    $FilePath = Join-Path $BrainDir $file
    if (-not (Test-Path $FilePath)) {
        Write-Host "[ERROR] Missing Brain Artifact: $FilePath" -ForegroundColor $Red
        Write-Host "Hint: Run .\tools\init-brain.ps1 to restore artifacts." -ForegroundColor $Yellow
        exit 1
    }
}
Write-Host "[PASS] AI Brain artifacts are present." -ForegroundColor $Green

# 2. GIT DRIFT CHECK
Write-Host "`nStep 2: Checking Version Control Sync..." -ForegroundColor $Yellow
git -C "$RootDir" fetch origin *> $null

try {
    $Local = git -C "$RootDir" rev-parse @
    $Remote = git -C "$RootDir" rev-parse @{u} 2>$null
} catch {
    $Remote = $null
}

if (-not $Remote) {
    Write-Host "[SKIP] No upstream found. Working in local mode." -ForegroundColor $Yellow
} elseif ($Local -ne $Remote) {
    Write-Host "[WARNING] Git Drift detected! Local and Remote are out of sync." -ForegroundColor $Red
    Write-Host "Please run 'git pull' to align your state." -ForegroundColor $Yellow
} else {
    Write-Host "[PASS] Git state is synchronized." -ForegroundColor $Green
}

# 3. ENVIRONMENT DISCOVERY
Write-Host "`nStep 3: Discovering Language Environment..." -ForegroundColor $Yellow
if (Test-Path (Join-Path $RootDir "composer.json")) {
    Write-Host "[DETECTED] PHP Project." -ForegroundColor $Cyan
    php -v | Select-Object -First 1
} elseif (Test-Path (Join-Path $RootDir "package.json")) {
    Write-Host "[DETECTED] Node.js Project." -ForegroundColor $Cyan
    node -v
} elseif ((Test-Path (Join-Path $RootDir "requirements.txt")) -or (Test-Path (Join-Path $RootDir "pyproject.toml"))) {
    Write-Host "[DETECTED] Python Project." -ForegroundColor $Cyan
    python --version
} else {
    Write-Host "[NOTICE] Universal project detected (No standard manifest)." -ForegroundColor $Yellow
}

# 4. PROTOCOL GOVERNANCE
Write-Host "`nStep 4: Checking Governance Documents..." -ForegroundColor $Yellow
if ((Test-Path (Join-Path $RootDir "docs\AI-MASTER-PROTOCOL.md")) -or (Test-Path (Join-Path $RootDir "README.md"))) {
    Write-Host "[PASS] Project documentation found." -ForegroundColor $Green
} else {
    Write-Host "[WARNING] No Master Protocol or README found." -ForegroundColor $Red
}

Write-Host "`n==================================================" -ForegroundColor $Green
Write-Host "   AUDIT COMPLETE: DSOM SECURED & READY FOR FLOW  " -ForegroundColor $Green
Write-Host "==================================================" -ForegroundColor $Green

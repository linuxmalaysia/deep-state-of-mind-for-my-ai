<#
.SYNOPSIS
    Universal DSOM Audit Pre-Flight (V5.0 - GitOps + AIOps + Ansible)
    
.DESCRIPTION
    Enforces synchronization between the physical environment, Git state,
    the AI's "External Brain", Cognitive Twin Protocol, and the Ansible
    baseline before starting a development session.
    
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
    $Local = git -C "$RootDir" rev-parse "@"
    $Remote = git -C "$RootDir" rev-parse "@{u}" 2>$null
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

# 4. COGNITIVE TWIN PROTOCOL CHECK
Write-Host "`nStep 4: Checking Cognitive Twin Protocol..." -ForegroundColor $Yellow
$TwinProtocol = Join-Path $RootDir "docs\AI-COGNITIVE-TWIN-PROTOCOL.md"
if (Test-Path $TwinProtocol) {
    $Content = Get-Content $TwinProtocol -Raw
    if ($Content -match '\[YOUR_PROJECT_NAME\]') {
        Write-Host "[WARNING] AI-COGNITIVE-TWIN-PROTOCOL.md has unfilled [PLACEHOLDER] values." -ForegroundColor $Yellow
        Write-Host "          Fill in all [YOUR_*] fields to configure the Cognitive Twin." -ForegroundColor $Yellow
    } else {
        Write-Host "[PASS] AI-COGNITIVE-TWIN-PROTOCOL.md exists and appears configured." -ForegroundColor $Green
    }
} else {
    Write-Host "[WARNING] docs/AI-COGNITIVE-TWIN-PROTOCOL.md is MISSING." -ForegroundColor $Red
    Write-Host "          Copy from the DSOM skeleton and fill in your project details." -ForegroundColor $Yellow
}

# 5. ANSIBLE BASELINE CHECK
Write-Host "`nStep 5: Checking Ansible Baseline..." -ForegroundColor $Yellow
$AnsibleCmd = Get-Command ansible -ErrorAction SilentlyContinue
if (-not $AnsibleCmd) {
    Write-Host "[SKIP] Ansible not found — skipping Ansible checks (non-infra project or setup pending)." -ForegroundColor $Yellow
} else {
    $AnsibleVer = (ansible --version)[0]
    Write-Host "[OK] $AnsibleVer" -ForegroundColor $Green
    if (Test-Path (Join-Path $RootDir "inventory\hosts.yml")) {
        Write-Host "[OK] inventory/hosts.yml exists." -ForegroundColor $Green
    } else {
        Write-Host "[WARN] inventory/hosts.yml missing. See HOWTO-SETUP-ANSIBLE-BASELINE.md." -ForegroundColor $Yellow
    }
    if (Test-Path (Join-Path $RootDir "ansible.cfg")) {
        Write-Host "[OK] ansible.cfg exists." -ForegroundColor $Green
    } else {
        Write-Host "[WARN] ansible.cfg missing." -ForegroundColor $Yellow
    }
}

Write-Host "`n==================================================" -ForegroundColor $Green
Write-Host "   AUDIT COMPLETE: DSOM SECURED & READY FOR FLOW  " -ForegroundColor $Green
Write-Host "   Protocol v5.0 | GitOps · AIOps · Ansible        " -ForegroundColor $Green
Write-Host "==================================================" -ForegroundColor $Green

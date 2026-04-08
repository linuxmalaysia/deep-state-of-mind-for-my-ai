<#
.SYNOPSIS
    DSOM Reanimation Manifest Generator (v2.1 - GitOps + AIOps + Ansible + Palace)

.DESCRIPTION
    Aggregates ALL core DSOM artifacts including Cognitive Twin Protocol and
    Ansible inventory. Features an interactive multi-line input for EOD summaries.
    Generates a sod_manifest_YYYY-MM-DD.txt for AI session reanimation.

.EXAMPLE
    .\tools\reanimate.ps1
    Upload the resulting sod_manifest_*.txt in your AI session.

.NOTES
    Author:  Harisfazillah Jamel (LinuxMalaysia)
    Partner: Generated with assistance from Google Antigravity
    Version: v2.1
    License: GNU GPL v3.0 or later
#>

$ErrorActionPreference = "Stop"
$VERSION = "v2.1"

# 1. Setup Variables
try {
    $RepoRoot = (git rev-parse --show-toplevel 2>$null).Trim()
} catch {
    $RepoRoot = $null
}

if (-not $RepoRoot) {
    Write-Error "[ERROR] Not in a Git repository. Run from the project root."
    exit 1
}

$DateStamp  = Get-Date -Format "yyyy-MM-dd"
$OutputFile = Join-Path $RepoRoot "sod_manifest_$DateStamp.txt"
$BrainDir   = Join-Path $RepoRoot ".agent" "brain"
$DocsDir    = Join-Path $RepoRoot "docs"
$ReadmeFile = Join-Path $RepoRoot "README.md"
$InvFile    = Join-Path $RepoRoot "inventory" "hosts.yml"

Write-Host ""
Write-Host "  [DSOM] Reanimation Manifest Generator $VERSION" -ForegroundColor Cyan
Write-Host "  Output: sod_manifest_$DateStamp.txt" -ForegroundColor Cyan
Write-Host ""

# 2. Validate required brain files
$Missing = $false
foreach ($f in @("task.md", "walkthrough.md")) {
    $p = Join-Path $BrainDir $f
    if (-not (Test-Path $p)) {
        Write-Host "  [WARNING] Missing brain artifact: $p" -ForegroundColor Yellow
        $Missing = $true
    }
}
if ($Missing) {
    Write-Host "  Hint: Run .\tools\init-brain.ps1 to initialise brain artifacts." -ForegroundColor Yellow
    Write-Host ""
}

# 3. Interactive Input
Write-Host "----------------------------------------------------------------------"
Write-Host "  DSOM Manual State Injection"
Write-Host "----------------------------------------------------------------------"

$Choice = "n"
# Check if running in an interactive session
if ([Environment]::UserInteractive) {
    try {
        $Choice = Read-Host "  Do you have a manual EOD Summary or Master Prompt addition? (y/N)"
    } catch {
        $Choice = "n"
    }
} else {
    Write-Host "  [INFO] Non-interactive session detected. Skipping manual input."
}

$ManualInput = ""
if ($Choice -match "^[yY]") {
    Write-Host ""
    Write-Host "  PASTE/TYPE YOUR CONTENT BELOW:"
    Write-Host "----------------------------------------------------------------------"
    Write-Host "  [INSTRUCTION]: Type 'EOF' on a new line and press ENTER to save."
    Write-Host "----------------------------------------------------------------------"

    $InputLines = [System.Collections.Generic.List[string]]::new()
    while ($true) {
        $Line = Read-Host
        if ($Line -eq "EOF") { break }
        $InputLines.Add($Line)
    }
    $ManualInput = $InputLines -join "`n"
    Write-Host "----------------------------------------------------------------------"
    Write-Host "  Input captured successfully." -ForegroundColor Green
}

# 4. Helper — safe read file
function Get-FileSafe {
    param([string]$Path, [string]$Fallback = "[MISSING] File not found: $Path")
    if (Test-Path $Path) { return (Get-Content $Path -Raw -Encoding UTF8) }
    return $Fallback
}

function Get-FileHeadSafe {
    param([string]$Path, [int]$Lines = 60, [string]$Fallback = "[MISSING] File not found: $Path")
    if (Test-Path $Path) {
        $content = (Get-Content $Path -Encoding UTF8 | Select-Object -First $Lines) -join "`n"
        return "$content`n`n... (see full doc: $Path)"
    }
    return $Fallback
}

# 5. Define the Gathering Logic
function New-Manifest {
    $DateNow = Get-Date
    $Lines   = [System.Collections.Generic.List[string]]::new()

    $Lines.Add("======================================================================")
    $Lines.Add("DSOM START OF DAY REANIMATION MANIFEST - $VERSION")
    $Lines.Add("Generated on: $DateNow")
    $Lines.Add("Project Root: $RepoRoot")
    $Lines.Add("======================================================================")
    $Lines.Add("")
    $Lines.Add("------------------------------------------------------------")
    $Lines.Add(" REANIMATING: Deep State of Mind (DSOM) For My AI Protocol")
    $Lines.Add(" NODE: $env:COMPUTERNAME | USER: $env:USERNAME")
    $Lines.Add("------------------------------------------------------------")
    $Lines.Add("")
    $Lines.Add("## CRISP STRATEGY MANDATE")
    $Lines.Add("- **C**ontext Awareness: Read brain artifacts first.")
    $Lines.Add("- **R**eview and Record: Commit atomic changes; update walkthrough.md.")
    $Lines.Add("- **I**teration: Incremental progress; no monolithic refactors.")
    $Lines.Add("- **S**ingle-purpose: Focus on one sub-task at a time.")
    $Lines.Add("- **P**artnership: AI acts as a Senior Architect Digital Twin.")
    $Lines.Add("")

    # Sunday Audit Check
    if ($DateNow.DayOfWeek -eq 'Sunday') {
        $Lines.Add("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        $Lines.Add("SUNDAY AUDIT PROTOCOL ACTIVE")
        $Lines.Add("   Today is Sunday. You MUST perform the Weekly Human Refresh.")
        $Lines.Add("   Refer to task.md -> 'Sunday Audit Protocol' for the checklist.")
        $Lines.Add("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        $Lines.Add("")
    }

    # Manual Injection
    if (-not [string]::IsNullOrWhiteSpace($ManualInput)) {
        $Lines.Add("### [0] MANUAL STATE INJECTION (Last Session EOD/Master Prompt)")
        $Lines.Add($ManualInput)
        $Lines.Add("`n---`n")
    }

    $Lines.Add("### [1] PROJECT README (Identity and Overview)")
    $Lines.Add((Get-FileSafe $ReadmeFile "README.md not found."))
    $Lines.Add("`n---`n")

    $Lines.Add("### [2] SYSTEM TELEMETRY (Physical Constraints)")
    $Lines.Add("- **OS:** $env:OS")
    $Lines.Add("- **Architecture:** $env:PROCESSOR_ARCHITECTURE")
    $Lines.Add("- **Host:** $env:COMPUTERNAME")
    $Lines.Add("- **User:** $env:USERNAME")
    $Lines.Add("- **Date:** $DateNow")
    $Lines.Add("`n---`n")

    $Lines.Add("### [3] MASTER PROTOCOL (The Constitution)")
    $Lines.Add((Get-FileSafe "$DocsDir\AI-MASTER-PROTOCOL.md"))
    $Lines.Add("`n---`n")

    $Lines.Add("### [4] COGNITIVE TWIN PROTOCOL (Project Identity Card)")
    $Lines.Add((Get-FileSafe "$DocsDir\AI-COGNITIVE-TWIN-PROTOCOL.md" `
        "[MISSING] docs/AI-COGNITIVE-TWIN-PROTOCOL.md not found. Run HOWTO-ADOPT-DSOM.md."))
    $Lines.Add("`n---`n")

    $Lines.Add("### [5] CURRENT TASK (The Cutting Edge)")
    $Lines.Add((Get-FileSafe "$BrainDir\task.md"))
    $Lines.Add("`n---`n")

    $Lines.Add("### [6] FULL WALKTHROUGH (The Complete Narrative History)")
    $Lines.Add((Get-FileSafe "$BrainDir\walkthrough.md"))
    $Lines.Add("`n---`n")

    $Lines.Add("### [7] IMPLEMENTATION PLAN (The Roadmap)")
    $Lines.Add((Get-FileSafe "$BrainDir\implementation_plan.md"))
    $Lines.Add("`n---`n")

    $Lines.Add("### [8] PROJECT STRUCTURE (The Spatial Map)")
    $Lines.Add("Files in repository:")
    try {
        $tree = git ls-tree -r HEAD --name-only 2>&1
        foreach ($f in $tree) { $Lines.Add("  - $f") }
    } catch {
        $Lines.Add("[SKIP] git ls-tree failed.")
    }
    $Lines.Add("`n---`n")

    $Lines.Add("### [9] GIT HISTORY")
    $Lines.Add("#### Recent Activity (Last 48 Hours)")
    try {
        $recent = git log --since="48 hours ago" --pretty=format:"%h - %an (%ar): %s" 2>&1
        $Lines.Add($recent -join "`n")
    } catch { $Lines.Add("[SKIP] git log failed.") }
    $Lines.Add("")
    $Lines.Add("#### Context (Last 30 Commits)")
    try {
        $logEntries = git log -n 30 --pretty=format:"%h - %an (%ar): %s" 2>&1
        $Lines.Add($logEntries -join "`n")
    } catch { $Lines.Add("[SKIP] git log failed.") }
    $Lines.Add("`n---`n")

    $Lines.Add("### [10] SOD RITUAL (Cognitive Handshake - Summary)")
    $Lines.Add((Get-FileHeadSafe "$DocsDir\SOD-RITUAL.md"))
    $Lines.Add("`n---`n")

    $Lines.Add("### [11] RITUAL OF TRANSITION (Cross-AI Handover - Summary)")
    $Lines.Add((Get-FileHeadSafe "$DocsDir\RITUAL-OF-TRANSITION.md"))
    $Lines.Add("`n---`n")

    $Lines.Add("### [12] ANSIBLE INVENTORY (Node Topology)")
    if (Test-Path $InvFile) {
        $Lines.Add("WARNING: This file may contain hostnames/IPs. Run privacy-guardian.ps1 before sharing.")
        $Lines.Add((Get-Content $InvFile -Raw -Encoding UTF8))
    } else {
        $Lines.Add("[SKIP] inventory/hosts.yml not found (non-infra project or Ansible not yet configured).")
    }
    $Lines.Add("`n---`n")

    $Lines.Add("### [13] GITOPS STRATEGY (Three-Pillar Doctrine Summary)")
    $Lines.Add((Get-FileHeadSafe "$DocsDir\GITOPS-AIOPS-ANSIBLE-STRATEGY.md" 60 "[SKIP] GITOPS-AIOPS-ANSIBLE-STRATEGY.md not found."))
    $Lines.Add("`n---`n")

    $Lines.Add("### [14] PALACE REGISTRY (Spatial Knowledge Map)")
    $PalaceRegistry = Join-Path $BrainDir "palace_registry.md"
    if (Test-Path $PalaceRegistry) {
        $Lines.Add((Get-Content $PalaceRegistry -Raw -Encoding UTF8))
        $Lines.Add("")
        $Lines.Add("PALACE WALKING INSTRUCTION:")
        $Lines.Add("  1. Identify relevant Wings and Rooms from the registry above.")
        $Lines.Add("  2. Read the closet.md in each relevant Room for instant context.")
        $Lines.Add("  3. Only drill into walkthrough.md if the closet is insufficient.")
    } else {
        $Lines.Add("[SKIP] palace_registry.md not found. Run: .\tools\palace-sync.ps1 -Backfill")
    }
    $Lines.Add("`n---`n")

    $Lines.Add("======================================================================")
    $Lines.Add("MANIFEST COMPLETE - DSOM For My AI Protocol v6.1 + Palace v1.0")
    $Lines.Add("======================================================================")
    $Lines.Add("")
    $Lines.Add("Handshake: Ask the AI:")
    $Lines.Add('  "Summarise the current Mental Anchor from .agent/brain/walkthrough.md.')
    $Lines.Add('   Confirm the 4-Tier environment. State: Sovereign State Synchronised when ready."')
    $Lines.Add("")
    $Lines.Add("REMINDER: Upload this manifest file as part of your Start of Day (SOD).")

    # Return all lines as a single string
    return ($Lines -join "`n")
}

# 6. Execute and Capture (fix double-output bug from v1.5)
$ManifestContent = New-Manifest
$ManifestContent | Out-File -FilePath $OutputFile -Encoding UTF8
Write-Host $ManifestContent

Write-Host ""
Write-Host "  [OK] Manifest saved to: $OutputFile" -ForegroundColor Green
Write-Host "  [!]  REMINDER: Run .\tools\privacy-guardian.ps1 before sharing." -ForegroundColor Yellow
Write-Host ""

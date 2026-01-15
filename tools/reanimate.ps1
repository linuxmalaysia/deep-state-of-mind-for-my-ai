<#
.SYNOPSIS
    DSOM Reanimation Manifest Generator (V1.5)
    
.DESCRIPTION
    Aggregates ALL core DSOM artifacts. Features an interactive multi-line 
    input for EOD summaries.
    
.AUTHOR
    Harisfazillah Jamel (LinuxMalaysia)
    
.LICENSE
    GNU GPL v3.0 or later
#>

$ErrorActionPreference = "Stop"

# 1. Setup Variables
try {
    $RepoRoot = git rev-parse --show-toplevel 2>$null
} catch {
    $RepoRoot = $null
}

if (-not $RepoRoot) {
    Write-Error "Error: Not in a Git repository."
    exit 1
}

$DateStamp = Get-Date -Format "yyyy-MM-dd"
$OutputFile = Join-Path $RepoRoot "sod_manifest_$DateStamp.txt"
$BrainDir = Join-Path $RepoRoot ".agent" "brain"
$DocsDir = Join-Path $RepoRoot "docs"
$ReadmeFile = Join-Path $RepoRoot "README.md"

# 2. Interactive Input
Write-Host "----------------------------------------------------------------------"
Write-Host "🧠 DSOM Manual State Injection"
Write-Host "----------------------------------------------------------------------"

$Choice = Read-Host "❓ Do you have a manual EOD Summary or Master Prompt addition? (y/N)"
$ManualInput = ""

if ($Choice -match "^[yY]") {
    Write-Host "`n📝 PASTE/TYPE YOUR CONTENT BELOW:"
    Write-Host "----------------------------------------------------------------------"
    Write-Host "👉 [INSTRUCTION]: Type 'EOF' on a new line and press ENTER to save."
    Write-Host "----------------------------------------------------------------------"
    
    $InputLines = @()
    while ($true) {
        $Line = Read-Host
        if ($Line -eq "EOF") { break }
        $InputLines += $Line
    }
    $ManualInput = $InputLines -join "`n"
    
    Write-Host "----------------------------------------------------------------------"
    Write-Host "✅ Input captured successfully."
}

# 3. Define the Gathering Logic
function Generate-Manifest {
    $DateNow = Get-Date
    
    Write-Output "======================================================================"
    Write-Output "🚀 DSOM START OF DAY REANIMATION MANIFEST"
    Write-Output "Generated on: $DateNow"
    Write-Output "Project Root: $RepoRoot"
    Write-Output "======================================================================"
    Write-Output ""
    
    Write-Output "------------------------------------------------------------"
    Write-Output " 🧠 REANIMATING: Deep State of Mind (DSOM) For My AI Protocol"
    Write-Output " 📍 NODE: $env:COMPUTERNAME | USER: $env:USERNAME"
    Write-Output "------------------------------------------------------------"
    Write-Output ""
    Write-Output "## 🛡️ CRISP STRATEGY MANDATE"
    Write-Output "- **C**ontext Awareness: Read brain artifacts first."
    Write-Output "- **R**eview & Record: Commit atomic changes; update walkthrough.md."
    Write-Output "- **I**teration: Incremental progress; no monolithic refactors."
    Write-Output "- **S**ingle-purpose: Focus on one sub-task at a time."
    Write-Output "- **P**artnership: AI acts as a Senior Architect Digital Twin."
    Write-Output ""

    # Sunday Audit Check
    if ($DateNow.DayOfWeek -eq 'Sunday') {
        Write-Output "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        Write-Output "🚨 SUNDAY AUDIT PROTOCOL ACTIVE"
        Write-Output "   Today is Sunday. You MUST perform the Weekly Human Refresh."
        Write-Output "   Refer to task.md -> 'Sunday Audit Protocol' for the checklist."
        Write-Output "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        Write-Output ""
    }

    if (-not [string]::IsNullOrWhiteSpace($ManualInput)) {
        Write-Output "### [0] MANUAL STATE INJECTION (Last Session EOD/Master Prompt)"
        Write-Output $ManualInput
        Write-Output "`n---`n"
    }

    Write-Output "### [1] PROJECT README (Identity & Overview)"
    if (Test-Path $ReadmeFile) { Get-Content $ReadmeFile -Raw -Encoding UTF8 } else { Write-Output "README.md not found." }
    Write-Output "`n---`n"

    Write-Output "### [2] SYSTEM TELEMETRY (Physical Constraints)"
    Write-Output "- **OS:** $env:OS"
    Write-Output "- **Architecture:** $env:PROCESSOR_ARCHITECTURE"
    Write-Output "- **Date:** $DateNow"
    Write-Output "`n---`n"

    Write-Output "### [3] MASTER PROTOCOL (The Constitution)"
    if (Test-Path "$DocsDir\AI-MASTER-PROTOCOL.md") { Get-Content "$DocsDir\AI-MASTER-PROTOCOL.md" -Raw -Encoding UTF8 }
    Write-Output "`n---`n"

    Write-Output "### [4] CURRENT TASK (The Cutting Edge)"
    if (Test-Path "$BrainDir\task.md") { Get-Content "$BrainDir\task.md" -Raw -Encoding UTF8 }
    Write-Output "`n---`n"

    Write-Output "### [5] FULL WALKTHROUGH (The Complete Narrative History)"
    if (Test-Path "$BrainDir\walkthrough.md") { Get-Content "$BrainDir\walkthrough.md" -Raw -Encoding UTF8 }
    Write-Output "`n---`n"

    Write-Output "### [6] IMPLEMENTATION PLAN (The Roadmap)"
    if (Test-Path "$BrainDir\implementation_plan.md") { Get-Content "$BrainDir\implementation_plan.md" -Raw -Encoding UTF8 }
    Write-Output "`n---`n"

    Write-Output "### [7] PROJECT STRUCTURE (The Spatial Map)"
    Write-Output "Files in repository (rel to root):"
    git ls-tree -r HEAD --name-only | ForEach-Object { Write-Output "  - $_" }
    Write-Output "`n---`n"

    Write-Output "### [8] GIT HISTORY (Last 30 Atomic Commits)"
    git log -n 30 --pretty=format:"%h - %an (%ar): %s"
    Write-Output "`n`n---`n"

    Write-Output "### [9] RITUAL OF TRANSITION (Operational Guidance)"
    if (Test-Path "$DocsDir\RITUAL-OF-TRANSITION.md") { Get-Content "$DocsDir\RITUAL-OF-TRANSITION.md" -Raw -Encoding UTF8 }
    
    Write-Output ""
    Write-Output "======================================================================"
    Write-Output "🏁 MANIFEST COMPLETE"
    Write-Output "======================================================================"
    Write-Output ""
    Write-Output "Handshake: Ask the AI: `"Summarize the current Mental Anchor after you have read the file uploaded`""
    Write-Output ""
    Write-Output "⚠️  REMINDER: Upload this manifest file as part of your Start of Day (SOD)."
}

# 4. Execute and Capture
$ManifestContent = Generate-Manifest
$ManifestContent | Out-File -FilePath $OutputFile -Encoding UTF8
$ManifestContent # Print to screen as well

Write-Host "`n📝 Manifest saved to: $OutputFile" -ForegroundColor Cyan
Write-Host "🛡️  REMINDER: Run tools/privacy-guardian.ps1 before sharing this manifest." -ForegroundColor Yellow

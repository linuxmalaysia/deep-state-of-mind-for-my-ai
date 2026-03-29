<#
.SYNOPSIS
    DSOM Claude Reanimation Generator (v2.0 - GitOps + AIOps + Ansible)

.DESCRIPTION
    Generates a targeted context file (DSOM-CLAUDE-INIT.md) for upload to
    Claude.ai Project Knowledge Base. This file contains the full DSOM
    Cognitive Twin context including: Sovereign Constitution, Brain Artifacts,
    4-Tier Environment Map, Ansible Inventory, and GitOps Strategy.

.EXAMPLE
    .\tools\reanimate-claude.ps1
    Then upload the resulting DSOM-CLAUDE-INIT.md to your Claude Project.

.NOTES
    Author:  Harisfazillah Jamel (LinuxMalaysia)
    Partner: Generated with assistance from Google Antigravity
    Version: v2.0
    License: GNU GPL v3.0 or later
#>

$ErrorActionPreference = "Stop"
$Output      = "DSOM-CLAUDE-INIT.md"
$DocsDir     = "docs"
$BrainDir    = ".agent\brain"
$InventoryDir = "inventory"
$VERSION     = "v2.0"

Write-Host ""
Write-Host "  [DSOM] Claude Reanimation Generator $VERSION" -ForegroundColor Cyan
Write-Host "  Generating: $Output" -ForegroundColor Cyan
Write-Host ""

# Validate required brain files
$MissingFiles = @()
foreach ($f in @("task.md", "walkthrough.md")) {
    if (-not (Test-Path "$BrainDir\$f")) {
        Write-Host "  [WARNING] Missing brain artifact: $BrainDir\$f" -ForegroundColor Yellow
        $MissingFiles += $f
    }
}
if ($MissingFiles.Count -gt 0) {
    Write-Host "  Hint: Run .\tools\init-brain.ps1 to initialise brain artifacts." -ForegroundColor Yellow
    Write-Host ""
}

# Helper to safely read a file or return a fallback message
function Get-FileOrFallback {
    param([string]$Path, [string]$Fallback = "[MISSING] File not found: $Path")
    if (Test-Path $Path) {
        return (Get-Content $Path -Raw -Encoding UTF8)
    }
    return $Fallback
}

$Lines = [System.Collections.Generic.List[string]]::new()

$Lines.Add("# $(([char]0x1F9E0)) DSOM CLAUDE INITIALIZATION MANIFEST")
$Lines.Add("# Standard: DSOM For My AI Protocol v6.1")
$Lines.Add("# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')")
$Lines.Add("")
$Lines.Add("> **PURPOSE:** Upload this file to your Claude Project Knowledge Base.")
$Lines.Add("> It contains your full Cognitive Digital Twin context. After uploading,")
$Lines.Add("> use the SOD Handshake prompt in docs/CLAUDE-SETUP.md to reanimate.")
$Lines.Add("")
$Lines.Add("---")

# --- Section 1: Sovereign Constitution ---
$Lines.Add("")
$Lines.Add("## $(([char]0x2696))$(([char]0xFE0F)) [1] SOVEREIGN CONSTITUTION (The Law)")
$Lines.Add("")
$masterProtocol = Get-FileOrFallback "$DocsDir\AI-MASTER-PROTOCOL.md" `
    "[MISSING] docs/AI-MASTER-PROTOCOL.md`nFallback Laws:`n1. Zero-Global Pattern`n2. Sovereign Portability`n3. HA-Ready`n4. Atomic Git Hygiene`n5. Pedagogical Logic`n6. GitOps Rule`n7. Ansible-First Execution"
$Lines.Add($masterProtocol)
$Lines.Add("")
$Lines.Add("---")

# --- Section 2: Cognitive Twin Protocol ---
$Lines.Add("")
$Lines.Add("## $(([char]0x1F5FA))$(([char]0xFE0F)) [2] COGNITIVE TWIN PROTOCOL (Project Identity Card)")
$Lines.Add("")
$Lines.Add($(Get-FileOrFallback "$DocsDir\AI-COGNITIVE-TWIN-PROTOCOL.md"))
$Lines.Add("")
$Lines.Add("---")

# --- Section 3: Current Task ---
$Lines.Add("")
$Lines.Add("## $(([char]0x1F3AF)) [3] CURRENT TASK (What to do NOW)")
$Lines.Add("")
$Lines.Add($(Get-FileOrFallback "$BrainDir\task.md"))
$Lines.Add("")
$Lines.Add("---")

# --- Section 4: Mental Anchor / Walkthrough ---
$Lines.Add("")
$Lines.Add("## $(([char]0x1F3C1)) [4] MENTAL ANCHOR - WALKTHROUGH (The History)")
$Lines.Add("")
$Lines.Add($(Get-FileOrFallback "$BrainDir\walkthrough.md"))
$Lines.Add("")
$Lines.Add("---")

# --- Section 5: Implementation Plan ---
$Lines.Add("")
$Lines.Add("## $(([char]0x1F5FA))$(([char]0xFE0F)) [5] IMPLEMENTATION PLAN (The Roadmap)")
$Lines.Add("")
$Lines.Add($(Get-FileOrFallback "$BrainDir\implementation_plan.md"))
$Lines.Add("")
$Lines.Add("---")

# --- Section 6: Git History ---
$Lines.Add("")
$Lines.Add("## $(([char]0x1F4DC)) [6] GIT HISTORY (Recent Activity)")
$Lines.Add("")
$Lines.Add("### Last 30 Commits")
try {
    $gitLog = git log -n 30 --pretty=format:"%h - %an (%ar): %s" 2>&1
    $Lines.Add($gitLog -join "`n")
} catch {
    $Lines.Add("[SKIP] git log failed — not a Git repository or no commits.")
}
$Lines.Add("")
$Lines.Add("---")

# --- Section 7: Project Structure ---
$Lines.Add("")
$Lines.Add("## $(([char]0x1F5C2))$(([char]0xFE0F)) [7] PROJECT STRUCTURE")
$Lines.Add("")
try {
    $tree = git ls-tree -r HEAD --name-only 2>&1
    foreach ($file in $tree) { $Lines.Add("  - $file") }
} catch {
    $Lines.Add("[SKIP] git ls-tree failed.")
}
$Lines.Add("")
$Lines.Add("---")

# --- Section 8: Ansible Inventory ---
$Lines.Add("")
$Lines.Add("## $(([char]0x2699))$(([char]0xFE0F)) [8] ANSIBLE INVENTORY (Node Topology)")
$Lines.Add("")
$hostsFile = "$InventoryDir\hosts.yml"
if (Test-Path $hostsFile) {
    $Lines.Add("WARNING: This file may contain hostnames/IPs. Run privacy-guardian.ps1 before sharing.")
    $Lines.Add("")
    $Lines.Add($(Get-Content $hostsFile -Raw -Encoding UTF8))
} else {
    $Lines.Add("[SKIP] inventory/hosts.yml not found (non-infra project or Ansible not yet configured).")
}
$Lines.Add("")
$Lines.Add("---")

# --- Section 9: GitOps Strategy ---
$Lines.Add("")
$Lines.Add("## $(([char]0x1F531)) [9] GITOPS STRATEGY (Three-Pillar Doctrine)")
$Lines.Add("")
$gitopsFile = "$DocsDir\GITOPS-AIOPS-ANSIBLE-STRATEGY.md"
if (Test-Path $gitopsFile) {
    $gitopsContent = (Get-Content $gitopsFile -Encoding UTF8 | Select-Object -First 60) -join "`n"
    $Lines.Add($gitopsContent)
    $Lines.Add("")
    $Lines.Add("... (see full doc: docs/GITOPS-AIOPS-ANSIBLE-STRATEGY.md)")
} else {
    $Lines.Add("[SKIP] GITOPS-AIOPS-ANSIBLE-STRATEGY.md not found.")
}
$Lines.Add("")
$Lines.Add("---")

# --- Footer ---
$Lines.Add("")
$Lines.Add("## $(([char]0x2705)) UPLOAD INSTRUCTIONS")
$Lines.Add("")
$Lines.Add("1. Upload this file (DSOM-CLAUDE-INIT.md) to your Claude Project Knowledge Base.")
$Lines.Add("2. Start a new Claude conversation and use the SOD Handshake prompt:")
$Lines.Add("")
$Lines.Add('   > "Initialise DSOM Protocol v6.1. Read the uploaded manifest.')
$Lines.Add('   > Summarise the current Mental Anchor from .agent/brain/walkthrough.md.')
$Lines.Add('   > Confirm the 4-Tier environment map from AI-COGNITIVE-TWIN-PROTOCOL.md.')
$Lines.Add('   > State: Sovereign State Synchronised when ready."')
$Lines.Add("")
$Lines.Add("See: docs/CLAUDE-SETUP.md for the full ritual.")
$Lines.Add("")
$Lines.Add("======================================================================")
$Lines.Add("MANIFEST COMPLETE - DSOM For My AI Protocol v6.1")
$Lines.Add("======================================================================")

# Write to file
$Lines | Out-File -FilePath $Output -Encoding UTF8

Write-Host "  [OK] Manifest saved to: $Output" -ForegroundColor Green
Write-Host "  [!]  REMINDER: Run .\tools\privacy-guardian.ps1 before uploading." -ForegroundColor Yellow
Write-Host ""
Write-Host "  Next step: Upload DSOM-CLAUDE-INIT.md to Claude Project Knowledge Base." -ForegroundColor Cyan
Write-Host "  Then follow the SOD ritual in docs/CLAUDE-SETUP.md." -ForegroundColor Cyan
Write-Host ""

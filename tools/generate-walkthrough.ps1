# ==============================================================================
# 📝 DSOM Session Scribe (Walkthrough Generator) - PowerShell Edition
# ==============================================================================
$ErrorActionPreference = "Stop"

$RepoRoot = git rev-parse --show-toplevel
$Today = Get-Date -Format "yyyy-MM-dd"

Write-Host "🔍 Harvesting Session Data for $Today..."

# 1. Harvest Git Data
$Commits = git log --since="today" --pretty=format:"    - %s" --reverse | Select-String -Pattern "chore(hibernation)" -NotMatch

# 2. Harvest Task Data
$TaskFile = "$RepoRoot\.agent\brain\task.md"
if (Test-Path $TaskFile) {
    $Tasks = Select-String -Path $TaskFile -Pattern "\[x\].*\(SELESAI\)"
} else {
    $Tasks = "    - No tasks marked as SELESAI found."
}

# 3. Generate Output
Write-Host ""
Write-Host "## 🏁 Session Anchor: $Today (Auto-Generated)"
Write-Host "- **Accomplished:**"
if ($Tasks) { foreach ($t in $Tasks) { Write-Host "$($t.Line)" } }
if ($Commits) { foreach ($c in $Commits) { Write-Host "$c" } }
Write-Host "- **Current State:** [UPDATE ME]"
Write-Host "- **Mental Anchor:** [UPDATE ME]"
Write-Host ""

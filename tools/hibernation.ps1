<#
.SYNOPSIS
    DSOM Hibernation Sequence (End-of-Day)
    
.DESCRIPTION
    Safeguards the project state before the human sleeps. Checks artifacts, 
    summarizes commits, and pushes to remote.
#>

$ErrorActionPreference = "Stop"

# 1. Setup
try {
    $RepoRoot = git rev-parse --show-toplevel 2>$null
} catch {
    $RepoRoot = $null
}

if (-not $RepoRoot) {
    Write-Error "❌ Error: Not in a Git repository."
    exit 1
}

$BrainDir = Join-Path $RepoRoot ".agent" "brain"
$TaskFile = Join-Path $BrainDir "task.md"
$WalkthroughFile = Join-Path $BrainDir "walkthrough.md"
$DateStamp = Get-Date -Format "yyyy-MM-dd"

# 2. Safety Checks
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "🌙 DSOM HIBERNATION SEQUENCE INITIATED"
Write-Host "======================================================================"
Write-Host ""

# Check Task List Status
Write-Host "🔍 Checking Task List..." -ForegroundColor Yellow
$TaskContent = Get-Content $TaskFile -Raw
if ($TaskContent -match "\[x\]") {
    Write-Host "✅ Progress detected in task.md." -ForegroundColor Green
} else {
    Write-Host "⚠️  WARNING: No completed tasks found in task.md today. Did you forget to update it?" -ForegroundColor Red
}

# Check Walkthrough Status
Write-Host "`n🔍 Checking Session Anchor..." -ForegroundColor Yellow
$WalkthroughContent = Get-Content $WalkthroughFile -Raw
if ($WalkthroughContent -match $DateStamp) {
    Write-Host "✅ Session Anchor for today found in walkthrough.md." -ForegroundColor Green
} else {
    Write-Host "❌ CRITICAL: No Session Anchor for $DateStamp found in walkthrough.md!" -ForegroundColor Red
    Write-Host "   You MUST summarize your work before sleeping." -ForegroundColor Red
}

# 3. Context Summary
Write-Host "`n----------------------------------------------------------------------"
Write-Host "📅 SESSION SUMMARY (What we did)"
Write-Host "----------------------------------------------------------------------"
# Show last 5 commits for context
git log -n 5 --pretty=format:"%h - %s (%ar)"
Write-Host "`n----------------------------------------------------------------------"

# 4. Next Steps Generator
Write-Host "`n🔮 NEXT STEPS (For Tomorrow)" -ForegroundColor Magenta
Write-Host "----------------------------------------------------------------------"
Select-String -Path $TaskFile -Pattern "\[ \]" | Select-Object -First 5 -ExpandProperty Line
Write-Host "----------------------------------------------------------------------"

# 5. Final Confirmation
Write-Host "`n😴 Are you ready to hibernate? (This will push all changes to GitHub)" -ForegroundColor Cyan
$Confirm = Read-Host "Confirm (y/N)"

if ($Confirm -match "^[yY]") {
    Write-Host "`n🚀 Committing context..." -ForegroundColor Green
    git add .
    git commit -m "chore(hibernation): End-of-Day safe shutdown $DateStamp"
    git push origin main
    Write-Host "`n✅ SLEEP WELL, ARCHITECT. YOUR STATE IS SAVED." -ForegroundColor Green
} else {
    Write-Host "`n🛑 Hibernation aborted. Stay awake." -ForegroundColor Red
}

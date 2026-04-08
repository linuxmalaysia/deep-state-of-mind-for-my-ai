<#
.SYNOPSIS
    DSOM End-of-Day (EOD) — Palace Edition
    Automates the EOD ritual natively on Windows (T1).
    - Runs Palace Sync to generate the update proposal
    - Validates brain artifacts (walkthrough anchor + task progress)
    - Stages and commits brain artifacts + Palace files
    - Pushes to origin/main

    The closet editing step (review & update palace_update_proposal) remains
    a human+AI step. This playbook commits AFTER that review is done (or before if skipping review).

.EXAMPLE
    .\tools\eod-palace.ps1

.NOTES
    Author:  Harisfazillah Jamel (LinuxMalaysia)
    Version: v1.0 | 2026-04-08
#>

$ErrorActionPreference = "Stop"

try {
    $RepoRoot = (git rev-parse --show-toplevel 2>$null).Trim()
} catch { exit 1 }

$DateStamp = Get-Date -Format "yyyy-MM-dd"
$TimeStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$BrainDir = Join-Path $RepoRoot ".agent" "brain"
$TaskFile = Join-Path $BrainDir "task.md"
$WalkthroughFile = Join-Path $BrainDir "walkthrough.md"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  DSOM EOD RITUAL — PALACE EDITION v1.0" -ForegroundColor Cyan
Write-Host "  $TimeStamp" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# Step 1: Validate Brain Artifacts
Write-Host ""
Write-Host "  [1/6] Validate task.md exists and has completed tasks..." -ForegroundColor Yellow
if (-not (Test-Path $TaskFile)) { Write-Host "    [FAIL] task.md not found" -ForegroundColor Red; exit 1 }
$TaskCompleted = (Select-String -Path $TaskFile -Pattern "\[x\]" -AllMatches).Matches.Count
if ($TaskCompleted -eq 0) { Write-Host "    [FAIL] No completed tasks found in task.md" -ForegroundColor Red; exit 1 }
Write-Host "    [OK] task.md: $TaskCompleted completed tasks found." -ForegroundColor Green

Write-Host "  [1/6] Validate walkthrough.md has today's anchor..." -ForegroundColor Yellow
if (-not (Test-Path $WalkthroughFile)) { Write-Host "    [FAIL] walkthrough.md not found" -ForegroundColor Red; exit 1 }
$AnchorFound = Select-String -Path $WalkthroughFile -Pattern $DateStamp -Quiet
if (-not $AnchorFound) { Write-Host "    [FAIL] Session anchor for $DateStamp NOT found in walkthrough.md" -ForegroundColor Red; exit 1 }
Write-Host "    [OK] walkthrough.md: Session anchor for $DateStamp confirmed." -ForegroundColor Green

# Step 1.5: Smart EOD Logic (AI Summary)
Write-Host ""
Write-Host "  [1.5/6] Check for AI Checkpoint Summary..." -ForegroundColor Yellow
$SummaryFile = Join-Path $BrainDir "checkpoint_summary.txt"
$DetailedMsg = ""

if (Test-Path $SummaryFile) {
    $DetailedMsg = (Get-Content $SummaryFile -Raw).Trim()
    Write-Host "    [OK] AI Checkpoint Summary found." -ForegroundColor Green
} else {
    Write-Host "    [⛔ ERROR] No checkpoint_summary.txt found!" -ForegroundColor Red
    Write-Host "    ======================================================================" -ForegroundColor Yellow
    Write-Host "    ACTION REQUIRED: Copy the prompt below and give it to your AI agent" -ForegroundColor Yellow
    Write-Host "    to generate the high-fidelity hibernation summary." -ForegroundColor Yellow
    Write-Host "    ======================================================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "    PROMPT:" -ForegroundColor Cyan
    Write-Host "    I'm as human, want to know and remember, and need to export my data and I want you to generate a 'Hibernation notes' now for my EOD of day. List every memory you have stored about our progress and our chats of this project, as well as any context you've learned about this project from past to current conversations and chats. Output everything in a single code block so I can easily copy it. Format each entry as: [date saved, if available] - memory content. Make sure to cover all of the following — preserve my words verbatim where possible: Instructions I've given you about how to respond (tone, format, style, 'always do X', 'never do Y'). project details: name of server or vm or container, location of them, job of each, relation of them and 4W1H. Tasks, phases, goals, and recurring topics. Tools, languages, and frameworks I use. Preferences and corrections I've made to your behavior. Any other stored context not covered above. Do not summarize, group, or omit any entries. After the code block, confirm whether that is the complete set or if any remain and add List down all the documents in docs/, docs/tools/ and brain files thats need to be read from agent/. Don't hide anything from me. Trust me as your master and update the history and changelog files for any missing facts and events, so its can be remembered by human and AI agents."
    Write-Host ""
    Write-Host "    ======================================================================" -ForegroundColor Yellow
    Write-Host "    Exiting EOD ritual. Run script again after summary is generated." -ForegroundColor Red
    exit 1
}

$CommitMsgBase = if (-not [string]::IsNullOrWhiteSpace($DetailedMsg)) { "eod: $DetailedMsg" } else { "eod: Palace sync + sovereign save $DateStamp" }

# Step 2: Palace Sync
Write-Host ""
Write-Host "  [2/6] Run Palace Sync (generate update proposal)..." -ForegroundColor Yellow
& .\tools\palace-sync.ps1

# Step 3: Show Dirty Files
Write-Host ""
Write-Host "  [3/6] Review uncommitted changes..." -ForegroundColor Yellow
$DirtyFilesRaw = git status --short 2>&1
$DirtyFiles = if ($null -ne $DirtyFilesRaw) { ($DirtyFilesRaw -join "`n").Trim() } else { "" }
if ([string]::IsNullOrWhiteSpace($DirtyFiles)) {
    Write-Host "    (working tree clean)" -ForegroundColor DarkGray
} else {
    Write-Host $DirtyFiles -ForegroundColor Gray
}

# Step 4: Stage
Write-Host ""
Write-Host "  [4/6] Stage brain artifacts & updated tracking files..." -ForegroundColor Yellow
git add $TaskFile
git add $WalkthroughFile
$PalaceRegistry = Join-Path $BrainDir "palace_registry.md"
if (Test-Path $PalaceRegistry) { git add $PalaceRegistry }
$WingsDir = Join-Path $BrainDir "wings"
if (Test-Path $WingsDir) { git add "$WingsDir/" }
git add $SummaryFile
git add -u

# Step 5: Commit
Write-Host ""
Write-Host "  [5/6] Commit staged changes..." -ForegroundColor Yellow
$StagedFilesRaw = git diff --cached --name-only 2>&1
$StagedFiles = if ($null -ne $StagedFilesRaw) { ($StagedFilesRaw -join "`n").Trim() } else { "" }
if (-not [string]::IsNullOrWhiteSpace($StagedFiles)) {
    git commit -m "chore($CommitMsgBase) [$TimeStamp]"
} else {
    Write-Host "    (nothing new to commit — working tree already clean)" -ForegroundColor DarkGray
}

# Step 6: Push
Write-Host ""
Write-Host "  [6/6] Push to origin/main..." -ForegroundColor Yellow
git push origin main

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "  SLEEP WELL, ARCHITECT. YOUR SOVEREIGN STATE IS SAVED." -ForegroundColor Green
Write-Host ""
Write-Host "  Palace sync committed. State pushed to origin." -ForegroundColor Green
Write-Host ""
Write-Host "  [NEXT STEP] Sync your AI agent's session state by copying this prompt:" -ForegroundColor Cyan
Write-Host "  ----------------------------------------------------------------------" -ForegroundColor Gray
Write-Host "  The EOD ritual [$TimeStamp] has been successfully pushed to origin/main." -ForegroundColor White
Write-Host "  Update .agent/brain/checkpoint_summary.txt: archive all completed items," -ForegroundColor White
Write-Host "  note the final EOD commit hash, and prepare the 'Mental Anchor' for" -ForegroundColor White
Write-Host "  tomorrow morning's Start-of-Day. What is the final EOD report?" -ForegroundColor White
Write-Host "  ----------------------------------------------------------------------" -ForegroundColor Gray
Write-Host ""
Write-Host "  REMAINING HUMAN STEPS:" -ForegroundColor Cyan
Write-Host "  - Review the latest palace_update_proposal_$DateStamp.md with your AI" -ForegroundColor Cyan
Write-Host "  - Update relevant closets in .agent/brain/wings/" -ForegroundColor Cyan
Write-Host "  - Commit closet updates: git add .agent/brain/ && git commit" -ForegroundColor Cyan
Write-Host "" -ForegroundColor Cyan
Write-Host "  Resume tomorrow with:" -ForegroundColor Cyan
Write-Host "    .\tools\sod-palace.ps1" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Green

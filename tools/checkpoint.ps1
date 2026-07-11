<#
.SYNOPSIS
    Deep State of Mind (DSOM) For My AI Protocol
.NOTES
    Author    : Harisfazillah Jamel (LinuxMalaysia)
    Timestamp : 2026-07-12
    License   : GNU General Public License v3.0
    Standard  : UK English | DBP-standard Bahasa Melayu Malaysia (Piawai)
#>
<#
.SYNOPSIS
    DSOM Checkpoint Ritual v1.0 (PowerShell)

.DESCRIPTION
    Automates a mid-day continuous integration save:
      - Generates the Palace Update Proposal without stopping
      - Mechanically splits commits (tracked vs untracked limits risk)
      - Pushes immediately to origin

.EXAMPLE
    .\tools\checkpoint.ps1

.NOTES
    Author:  Harisfazillah Jamel (LinuxMalaysia)
    Version: v1.0 
#>

$ErrorActionPreference = "Stop"

$DateStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# --- Setup Paths ---
try {
    $RepoRoot = (git rev-parse --show-toplevel 2>$null).Trim()
} catch { $RepoRoot = $null }

if (-not $RepoRoot) {
    Write-Host "  [ERROR] Not in a Git repository." -ForegroundColor Red
    exit 1
}

$BrainDir = Join-Path $RepoRoot ".agents\brain"
# ------------------

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  DSOM MID-DAY CHECKPOINT RITUAL — PALACE EDITION" -ForegroundColor Cyan
Write-Host "  $DateStamp" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# --- Setup Paths ---
try {
    $RepoRoot = (git rev-parse --show-toplevel 2>$null).Trim()
} catch { $RepoRoot = $null }

if (-not $RepoRoot) {
    Write-Host "  [ERROR] Not in a Git repository." -ForegroundColor Red
    exit 1
}

$BrainDir = Join-Path $RepoRoot ".agents" "brain"
# ------------------

Write-Host "  [1/4] Generating Palace Update Proposal..." -ForegroundColor Yellow
try {
    .\tools\palace-sync.ps1
} catch {
    Write-Host "  [WARNING] palace-sync.ps1 failed to generate proposal." -ForegroundColor Magenta
}

# --- SMART CHECKPOINT LOGIC ---
$SummaryFile = Join-Path $BrainDir "checkpoint_summary.txt"
$DetailedMsg = ""

if (Test-Path $SummaryFile) {
    $DetailedMsg = (Get-Content $SummaryFile -Raw).Trim()
    Write-Host "  [OK] AI Checkpoint Summary found." -ForegroundColor Green
} else {
    Write-Host "  [⛔ ERROR] No checkpoint_summary.txt found!" -ForegroundColor Red
    Write-Host "  ======================================================================" -ForegroundColor Yellow
    Write-Host "  ACTION REQUIRED: Copy the prompt below and give it to your AI agent" -ForegroundColor Yellow
    Write-Host "  to generate the high-fidelity checkpoint summary." -ForegroundColor Yellow
    Write-Host "  ======================================================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  PROMPT:" -ForegroundColor Cyan
    Write-Host "  I'm as human, want to know and remember, and need to export my data and I want you to generate a 'Hibernation notes' now for my EOD of day. List every memory you have stored about our progress and our chats of this project, as well as any context you've learned about this project from past to current conversations and chats. Output everything in a single code block so I can easily copy it. Format each entry as: [date saved, if available] - memory content. Make sure to cover all of the following — preserve my words verbatim where possible: Instructions I've given you about how to respond (tone, format, style, 'always do X', 'never do Y'). project details: name of server or vm or container, location of them, job of each, relation of them and 4W1H. Tasks, phases, goals, and recurring topics. Tools, languages, and frameworks I use. Preferences and corrections I've made to your behavior. Any other stored context not covered above. Do not summarize, group, or omit any entries. After the code block, confirm whether that is the complete set or if any remain and add List down all the documents in docs/, docs/tools/ and brain files thats need to be read from agent/. Don't hide anything from me. Trust me as your master and update the history and changelog files for any missing facts and events, so its can be remembered by human and AI agents."
    Write-Host ""
    Write-Host "  ======================================================================" -ForegroundColor Yellow
    Write-Host "  Exiting checkpoint. Run script again after summary is generated." -ForegroundColor Red
    exit 1
}

$CommitMsgBase = if (-not [string]::IsNullOrWhiteSpace($DetailedMsg)) { "checkpoint: $DetailedMsg" } else { "checkpoint: generic save" }
# ------------------------------

Write-Host ""
Write-Host "  [2/4] Stage / Commit tracked modifications..." -ForegroundColor Yellow
$TrackedChangesRaw = git diff --name-only 2>&1
$TrackedChanges = if ($null -ne $TrackedChangesRaw) { ($TrackedChangesRaw -join "`n").Trim() } else { "" }
if (-not [string]::IsNullOrWhiteSpace($TrackedChanges)) {
    git add -u
    git commit -m "chore($CommitMsgBase) [$DateStamp]"
    Write-Host "    -> Committed tracked modifications." -ForegroundColor Green
} else {
    Write-Host "    -> No tracked modifications to commit." -ForegroundColor DarkGray
}

Write-Host ""
Write-Host "  [3/4] Stage / Commit newly added untracked files..." -ForegroundColor Yellow
$UntrackedFilesRaw = git ls-files --others --exclude-standard 2>&1
$UntrackedFiles = if ($null -ne $UntrackedFilesRaw) { ($UntrackedFilesRaw -join "`n").Trim() } else { "" }
if (-not [string]::IsNullOrWhiteSpace($UntrackedFiles)) {
    git add .
    git commit -m "chore($CommitMsgBase - untracked) [$DateStamp]"
    Write-Host "    -> Committed untracked configurations." -ForegroundColor Green
} else {
    Write-Host "    -> No untracked files to commit." -ForegroundColor DarkGray
}

Write-Host ""
Write-Host "  [4/4] Pushing to origin/main..." -ForegroundColor Yellow
git push origin main

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "  ✅ MID-DAY CHECKPOINT SAVED" -ForegroundColor Green
Write-Host ""
Write-Host "  Tracked and untracked files have been compartmentalised and pushed." -ForegroundColor Green
Write-Host "  Palace update proposal generated (ready for EOD review later today)." -ForegroundColor Green
Write-Host ""
Write-Host "  [NEXT STEP] Sync your AI agent's session state by copying this prompt:" -ForegroundColor Green
Write-Host "  ----------------------------------------------------------------------" -ForegroundColor Green
Write-Host "  The checkpoint [$DateStamp] has been successfully pushed to origin/main." -ForegroundColor Green
Write-Host "  Now, generate the high-fidelity session update using this command:" -ForegroundColor Green
Write-Host "" -ForegroundColor Green
Write-Host "  I'm as human, want to know and remember, and need to export my data and" -ForegroundColor Green
Write-Host "  I want you to generate a 'Hibernation notes' now for my EOD of day." -ForegroundColor Green
Write-Host "  List every memory you have stored about our progress and our chats of" -ForegroundColor Green
Write-Host "  this project, as well as any context you've learned about this project" -ForegroundColor Green
Write-Host "  from past to current conversations and chats. Output everything in a" -ForegroundColor Green
Write-Host "  single code block so I can easily copy it. Format each entry as:" -ForegroundColor Green
Write-Host "  [date saved, if available] - memory content. Make sure to cover all of" -ForegroundColor Green
Write-Host "  the following — preserve my words verbatim where possible:" -ForegroundColor Green
Write-Host "  Instructions I've given you about how to respond (tone, format, style," -ForegroundColor Green
Write-Host "  'always do X', 'never do Y'). project details: name of server or vm or" -ForegroundColor Green
Write-Host "  container, location of them, job of each, relation of them and 4W1H." -ForegroundColor Green
Write-Host "  Tasks, phases, goals, and recurring topics. Tools, languages, and" -ForegroundColor Green
Write-Host "  frameworks I use. Preferences and corrections I've made to your behavior." -ForegroundColor Green
Write-Host "  Any other stored context not covered above. Do not summarize, group," -ForegroundColor Green
Write-Host "  or omit any entries. After the code block, confirm whether that is the" -ForegroundColor Green
Write-Host "  complete set or if any remain and add List down all the documents in" -ForegroundColor Green
Write-Host "  docs/, docs/tools/ and brain files thats need to be read from agent/." -ForegroundColor Green
Write-Host "  Don't hide anything from me. Trust me as your master and update the" -ForegroundColor Green
Write-Host "  history and changelog files for any missing facts and events, so its" -ForegroundColor Green
Write-Host "  can be remembered by human and AI agents." -ForegroundColor Green
Write-Host "  ----------------------------------------------------------------------" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green


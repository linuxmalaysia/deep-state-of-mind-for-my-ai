<#
.SYNOPSIS
    DSOM Git Ritual Tool (V1.0 - GitOps Sovereign Save)

.DESCRIPTION
    Performs a structured, documented Sovereign Save (Git commit + push) for the
    DSOM GitOps ritual. Enforces semantic commit messages with Phase/version tags.
    Equivalent of the "Atomic Git Hygiene" law from AI-MASTER-PROTOCOL.md.

    Modes:
      (default)  Interactive EOD Sovereign Save
      sod        Start-of-Day sync (pull from origin/main)
      eod        Alias for default interactive mode
      push "msg" Direct commit + push with provided message

.AUTHOR
    Harisfazillah Jamel (LinuxMalaysia)

.LICENSE
    GNU GPL v3.0 or later
#>

$ErrorActionPreference = "Stop"

# Setup
try {
    $RepoRoot = git rev-parse --show-toplevel 2>$null
} catch {
    $RepoRoot = $null
}

if (-not $RepoRoot) {
    Write-Host "[ERROR] Not a Git repository." -ForegroundColor Red
    exit 1
}

$Mode       = if ($args.Count -ge 1) { $args[0] } else { "interactive" }
$CommitMsg  = if ($args.Count -ge 2) { $args[1] } else { "" }

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "   DSOM GIT RITUAL v1.0 | GitOps Sovereign Tool     " -ForegroundColor Cyan
Write-Host "   Repo: $RepoRoot" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

function Show-Status {
    Write-Host "--- Current Git Status ---" -ForegroundColor Yellow
    git -C $RepoRoot status --short
    Write-Host ""
    Write-Host "--- Last 5 Commits ---" -ForegroundColor Yellow
    git -C $RepoRoot log --oneline -5
    Write-Host ""
}

# ── MODE: SOD (Start-of-Day Pull) ─────────────────────────────────────────────
if ($Mode -eq "sod") {
    Write-Host "[SOD] Start-of-Day Sync — pulling latest from origin/main" -ForegroundColor Cyan
    git -C $RepoRoot fetch origin

    $Local  = git -C $RepoRoot rev-parse "@"
    $Remote = git -C $RepoRoot rev-parse "@{u}" 2>$null

    if (-not $Remote) {
        Write-Host "[SKIP] No upstream. Working in local mode." -ForegroundColor Yellow
    } elseif ($Local -eq $Remote) {
        Write-Host "[OK] Already up to date. No pull needed." -ForegroundColor Green
    } else {
        git -C $RepoRoot pull origin main
        Write-Host "[DONE] Pulled latest changes from origin/main." -ForegroundColor Green
    }
    Show-Status
    Write-Host "SOD Sync Complete. Read .agent/brain/ artifacts and begin." -ForegroundColor Green
    exit 0
}

# ── MODE: PUSH (Direct commit with provided message) ─────────────────────────
if ($Mode -eq "push") {
    if ([string]::IsNullOrWhiteSpace($CommitMsg)) {
        Write-Host '[ERROR] Provide a commit message. Usage: .\tools\git-ritual.ps1 push "type(scope): message"' -ForegroundColor Red
        exit 1
    }
    Show-Status
    Write-Host "[PUSH] Staging all changes and committing..." -ForegroundColor Cyan
    git -C $RepoRoot add -A
    git -C $RepoRoot commit -m $CommitMsg
    git -C $RepoRoot push origin main
    Write-Host "[DONE] Pushed: $CommitMsg" -ForegroundColor Green
    exit 0
}

# ── MODE: EOD / INTERACTIVE (Sovereign Save with semantic commit builder) ─────
Show-Status

$Dirty = git -C $RepoRoot status --porcelain
if (-not $Dirty) {
    Write-Host "[CLEAN] Working tree is clean. Nothing to commit." -ForegroundColor Green
    exit 0
}

Write-Host "Uncommitted changes detected. Starting EOD Sovereign Save..." -ForegroundColor Yellow
Write-Host ""

Write-Host "Select commit type (Conventional Commits standard):" -ForegroundColor Cyan
Write-Host "  1) feat     — New feature or capability"
Write-Host "  2) fix      — Bug fix or correction"
Write-Host "  3) docs     — Documentation only"
Write-Host "  4) chore    — Maintenance, brain artifacts, EOD save"
Write-Host "  5) refactor — Code restructure without behaviour change"
Write-Host "  6) ci       — CI / deployment changes"
Write-Host ""

$TypeChoice = Read-Host "Enter number [1-6]"
$CommitType = switch ($TypeChoice) {
    "1" { "feat" }
    "2" { "fix" }
    "3" { "docs" }
    "4" { "chore" }
    "5" { "refactor" }
    "6" { "ci" }
    default { "chore" }
}

$Scope       = Read-Host "Scope (e.g., kafka, logstash, brain, ansible)"
$Description = Read-Host "Short description"
$PhaseTag    = Read-Host "Phase/Version tag (e.g., Phase-12/v2.3, or press Enter to skip)"

$FullMsg = if ($PhaseTag) {
    "${CommitType}(${Scope}): ${Description} [${PhaseTag}]"
} else {
    "${CommitType}(${Scope}): ${Description}"
}

Write-Host ""
Write-Host "Commit message: $FullMsg" -ForegroundColor Yellow
$Confirm = Read-Host "Confirm and push? (y/N)"

if ($Confirm -match "^[yY]") {
    git -C $RepoRoot add -A
    git -C $RepoRoot commit -m $FullMsg
    git -C $RepoRoot push origin main
    Write-Host ""
    Write-Host "=====================================================" -ForegroundColor Green
    Write-Host "   SOVEREIGN SAVE COMPLETE. STATE IS PRESERVED.     " -ForegroundColor Green
    Write-Host "=====================================================" -ForegroundColor Green
} else {
    Write-Host "[ABORTED] Nothing committed. State not saved." -ForegroundColor Yellow
    exit 0
}

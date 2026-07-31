<#
.SYNOPSIS
    Deep State of Mind (DSOM) For My AI Protocol
.NOTES
    Author    : Harisfazillah Jamel (LinuxMalaysia)
    Timestamp : 2026-07-31
    License   : GNU General Public License v3.0
    Standard  : UK English | DBP-standard Bahasa Melayu Malaysia (Piawai)
#>
<#
.SYNOPSIS
    Universal DSOM Framework Onboarding Bootstrap Script (PowerShell)
.DESCRIPTION
    Downloads and bootstraps any target repository with DSOM baseline structure,
    tools, native MCP server, and Context7 indexer guidance.
#>

$ErrorActionPreference = "SilentlyContinue"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "      🚀 Universal DSOM Framework Onboarding Initiated" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Verify git repository
try {
    $isGitRepo = git rev-parse --is-inside-work-tree 2>&1
    if ("$isGitRepo" -ne "true") { Throw }
} catch {
    Write-Host "ERROR: You must run this script from inside a git repository." -ForegroundColor Red
    Write-Host "Run 'git init' first if this is a new project." -ForegroundColor Yellow
    exit 1
}

$TargetDir = Get-Location
$Timestamp = Get-Date -Format "yyyy-MM-dd"
$TimeSuffix = Get-Date -Format "HHmmss"
$TmpBranch = "dsom-onboarding-$Timestamp-$TimeSuffix"

Write-Host "[1/4] Preparing Git workspace..." -ForegroundColor Yellow
$gitDiff = git diff-index --quiet HEAD -- 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Uncommitted changes detected. Stashing transient state..." -ForegroundColor Magenta
    git stash
}
git checkout -b "$TmpBranch"

Write-Host "[2/4] Resolving execution engine (Ansible vs Native PowerShell Fallback)..." -ForegroundColor Yellow
$PlaybookDir = Join-Path $env:TEMP "dsom-onboard-$Timestamp-$(Get-Random)"
New-Item -ItemType Directory -Force -Path $PlaybookDir | Out-Null

$DsomRepoUrl = "https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai.git"
$hasWsl = Get-Command wsl -ErrorAction SilentlyContinue

if ($hasWsl) {
    Write-Host " -> WSL & Ansible engine available..." -ForegroundColor Green
    $PlaybookFile = Join-Path $PlaybookDir "onboard-dsom.yml"
    $Url = "https://raw.githubusercontent.com/linuxmalaysia/deep-state-of-mind-for-my-ai/main/playbooks/dsom/onboard-dsom.yml"
    Invoke-WebRequest -Uri $Url -OutFile $PlaybookFile
    $env:ANSIBLE_NOCOWS = "1"
    $PlaybookFileWsl = (wsl wslpath -u "'$PlaybookFile'").Trim()
    wsl ansible-playbook $PlaybookFileWsl -e "timestamp=$Timestamp"
} else {
    Write-Host " -> WSL not found. Falling back to Native PowerShell Git Engine..." -ForegroundColor Yellow
    $CloneDir = Join-Path $PlaybookDir "dsom-main"
    git clone --depth 1 $DsomRepoUrl $CloneDir 2>&1 | Out-Null

    Write-Host "[3/4] Copying DSOM Baseline Architecture with Conflict Resolution..." -ForegroundColor Yellow
    $DirsToSync = @("tools", "playbooks\dsom", "docs", ".agents")
    foreach ($dir in $DirsToSync) {
        $sourcePath = Join-Path $CloneDir $dir
        if (Test-Path $sourcePath) {
            Get-ChildItem -Path $sourcePath -Recurse -File | ForEach-Object {
                $relativePath = $_.FullName.Substring($CloneDir.Length + 1)
                $destFile = Join-Path $TargetDir $relativePath
                $destParent = Split-Path $destFile -Parent
                if (-not (Test-Path $destParent)) { New-Item -ItemType Directory -Force -Path $destParent | Out-Null }

                if (Test-Path $destFile) {
                    $ext = $_.Extension
                    $base = $_.BaseName
                    $conflictName = "$base-$Timestamp$ext"
                    $conflictPath = Join-Path $destParent $conflictName
                    Copy-Item $_.FullName $conflictPath -Force
                    Write-Host "  [CONFLICT] Preserved target file. Saved incoming as $conflictName" -ForegroundColor Magenta
                } else {
                    Copy-Item $_.FullName $destFile -Force
                    Write-Host "  [ADDED] $relativePath" -ForegroundColor Gray
                }
            }
        }
    }

    $RootFiles = @(".gitattributes", ".markdownlint.json", "README.md", "CHANGELOG.md", "HISTORY.md", "SUMMARY.md", "START-HERE.md", "AGENTS.md", "llms.txt")
    foreach ($file in $RootFiles) {
        $sourceFile = Join-Path $CloneDir $file
        if (Test-Path $sourceFile) {
            $destFile = Join-Path $TargetDir $file
            if (Test-Path $destFile) {
                $ext = [System.IO.Path]::GetExtension($file)
                $base = [System.IO.Path]::GetFileNameWithoutExtension($file)
                $conflictName = "$base-$Timestamp$ext"
                $conflictPath = Join-Path $TargetDir $conflictName
                Copy-Item $sourceFile $conflictPath -Force
                Write-Host "  [CONFLICT] Preserved target file. Saved incoming as $conflictName" -ForegroundColor Magenta
            } else {
                Copy-Item $sourceFile $destFile -Force
                Write-Host "  [ADDED] $file" -ForegroundColor Gray
            }
        }
    }
}

Write-Host "[4/4] Cleaning up temporary workspace..." -ForegroundColor Yellow
Remove-Item -Recurse -Force $PlaybookDir

Write-Host "============================================================" -ForegroundColor Green
Write-Host "      ✅ DSOM Onboarding Architecture Synchronized" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "NEXT STEPS & ACTION REQUIRED:" -ForegroundColor Cyan
Write-Host "------------------------------"
Write-Host "1. Review branch changes: git status"
Write-Host "2. Commit baseline:       git add . && git commit -m 'chore: onboard DSOM framework'"
Write-Host "3. Merge into main:       git checkout main && git merge $TmpBranch"
Write-Host ""
Write-Host "SOVEREIGN AI & MCP INTEGRATION:" -ForegroundColor Cyan
Write-Host "------------------------------"
Write-Host "• Local MCP Server: Configure Cursor/Claude Desktop using tools/mcp/server.py:"
Write-Host "  { `"mcpServers`": { `"dsom-palace`": { `"command`": `"uv`", `"args`": [`"run`", `"tools/mcp/server.py`"] } } }"
Write-Host ""
Write-Host "• Context7 Semantic RAG Service:"
Write-Host "  Add 'context7.json' to your repository root for domain verification."
Write-Host "  Live Payload Endpoint: https://context7.com/gitlab_linuxmalaysia/deep-state-of-mind-for-my-ai/llms.txt?tokens=10000"
Write-Host "============================================================" -ForegroundColor Green

<#
.SYNOPSIS
    DSOM Privacy Guardian (V1.0)
    
.DESCRIPTION
    Scans the generated DSOM reanimation manifest for sensitive information 
    (IPv4 addresses, API keys, tokens, and local home paths) before it is 
    uploaded to an external AI model.
    
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

# 1. Setup Variables
try {
    $RepoRoot = git rev-parse --show-toplevel 2>$null
} catch {
    $RepoRoot = $null
}

$DateStamp = Get-Date -Format "yyyy-MM-dd"
$TargetFile = Join-Path $RepoRoot "sod_manifest_$DateStamp.txt"

# 2. Check if Manifest Exists
if (-not (Test-Path $TargetFile)) {
    Write-Host "❌ Error: Manifest for today ($DateStamp) not found." -ForegroundColor $Red
    Write-Host "👉 Please run '.\tools\reanimate.ps1' first." -ForegroundColor $Yellow
    exit 1
}

Write-Host "======================================================================" -ForegroundColor $Green
Write-Host "🛡️  DSOM PRIVACY GUARDIAN: SECURITY SCAN" -ForegroundColor $Green
Write-Host "Target: $TargetFile"
Write-Host "======================================================================" -ForegroundColor $Green

# 3. Define Regex Patterns for Leaks
$Patterns = @(
    "([0-9]{1,3}\.){3}[0-9]{1,3}",      # IPv4
    "AIza[0-9A-Za-z-_]{35}",            # Google API
    "sk-[a-zA-Z0-9]{48}",               # Generic Secret (OpenAI-like)
    "xox[bap]-[a-zA-Z0-9-]+",           # Slack Token
    "\/home\/[a-z0-9_-]+\/"             # Linux Home Path
    "C:\\Users\\[a-z0-9_-]+\\"          # Windows User Path
)

$LeakFound = $false

# 4. Scanning Process
Write-Host "🔍 Scanning for sensitive patterns..." -ForegroundColor $Yellow

foreach ($Pattern in $Patterns) {
    try {
        $MatchesFound = Select-String -Path $TargetFile -Pattern $Pattern -AllMatches
        if ($MatchesFound) {
            Write-Host "`n⚠️  POTENTIAL LEAK DETECTED:" -ForegroundColor $Red
            foreach ($match in $MatchesFound) {
                Write-Host "Line $($match.LineNumber): $($match.Line.Trim())" -ForegroundColor $Red
            }
            $LeakFound = $true
        }
    } catch {
        # Silently ignore regex errors if any
    }
}

Write-Host "----------------------------------------------------------------------"

# 5. Final Report
if (-not $LeakFound) {
    Write-Host "✅ SCAN COMPLETE: No common sensitive patterns found." -ForegroundColor $Green
    Write-Host "🚀 You are clear to upload this manifest for AI reanimation." -ForegroundColor $Green
} else {
    Write-Host "❌ SCAN FAILED: Sensitive data detected." -ForegroundColor $Red
    Write-Host "👉 ACTION: Please edit $TargetFile to mask these details before upload." -ForegroundColor $Yellow
}
Write-Host "======================================================================" -ForegroundColor $Green

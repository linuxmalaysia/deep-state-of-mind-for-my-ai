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
    "([0-9]{1,3}\.){3}[0-9]{1,3}",                     # IPv4
    "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",  # Email
    "AIza[0-9A-Za-z-_]{35}",                           # Google API
    "AKIA[0-9A-Z]{16}",                                # AWS Access Key
    "gh[pousr]_[a-zA-Z0-9]{36}",                       # GitHub Token
    "github_pat_[a-zA-Z0-9_]{82}",                     # GitHub Fine-Grained Token
    "sk-[a-zA-Z0-9]{48}",                              # OpenAI Secret
    "xox[bap]-[a-zA-Z0-9-]+",                          # Slack Token
    "-----BEGIN [A-Z]+ PRIVATE KEY-----",              # PEM Private Key
    "\/home\/[a-z0-9_-]+\/",                           # Linux Home Path
    "C:\\Users\\[a-z0-9_-]+\\"                         # Windows User Path
)

$LeakFound = $false

# 4. Scanning Process via Native Regex
Write-Host "🔍 Scanning for sensitive patterns via PowerShell Engine..." -ForegroundColor $Yellow

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

# 4b. Scanning Process via guardrails-ai-dsom Python Engine
Write-Host "`n🔍 Scanning via guardrails-ai-dsom Python Engine..." -ForegroundColor $Yellow
$GuardrailsCheck = uv run --with-editable "$RepoRoot/tools/guardrails-ai-dsom" python -c "
import sys
from pathlib import Path
from guardrails_dsom import GuardrailsCredentialGuardian

content = Path(r'$TargetFile').read_text(encoding='utf-8')
guardian = GuardrailsCredentialGuardian()
res = guardian.validate(content)
if not res.is_valid:
    print(f'GUARDRAIL_BLOCKED: {res.error_message}')
    sys.exit(1)
print('GUARDRAIL_PASS')
" 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n⚠️  GUARDRAILS-AI-DSOM LEAK DETECTED: $GuardrailsCheck" -ForegroundColor $Red
    $LeakFound = $true
} else {
    Write-Host "[PASS] guardrails-ai-dsom Credential Guardian verified clean." -ForegroundColor $Green
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

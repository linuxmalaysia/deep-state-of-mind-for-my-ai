# OpenWiki PowerShell Wrapper using Node.js v22.14.0 LTS
[CmdletBinding()]
param (
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$OpenWikiArgs
)

$Node22Dir = "C:\Users\User\.config\herd\bin\nvm\v22.14.0"
$NodeExe = Join-Path $Node22Dir "node.exe"
$NpmCli = Join-Path $Node22Dir "node_modules\npm\bin\npm-cli.js"

if (-not (Test-Path $NodeExe)) {
    Write-Error "Node.js v22.14.0 was not found at $NodeExe"
    exit 1
}

# Prepend Node 22 to PATH for current execution
$env:PATH = "$Node22Dir;" + $env:PATH

$OpenWikiLocal = Join-Path $PSScriptRoot "openwiki_win\node_modules\openwiki\dist\cli.js"

if (-not (Test-Path $OpenWikiLocal)) {
    Write-Host "Installing OpenWiki under Node v22.14.0 in tools/openwiki_win..." -ForegroundColor Cyan
    & $NodeExe $NpmCli install openwiki --prefix (Join-Path $PSScriptRoot "openwiki_win")
}

if ($OpenWikiArgs.Count -eq 0) {
    & $NodeExe $OpenWikiLocal --help
} else {
    & $NodeExe $OpenWikiLocal @OpenWikiArgs
}

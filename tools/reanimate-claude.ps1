<#
.SYNOPSIS
    DSOM Claude Reanimation Generator (V1.0)
    
.DESCRIPTION
    Generates DSOM Context specifically for Claude.ai Project Knowledge Bases.
    
.AUTHOR
    Harisfazillah Jamel (LinuxMalaysia)
    
.LICENSE
    GNU GPL v3.0 or later
#>

$ErrorActionPreference = "SilentlyContinue"
$Output = "DSOM-CLAUDE-INIT.md"
$DocsDir = "docs"
$BrainDir = ".agent\brain"

Write-Host "📝 Generating DSOM Context for Claude.ai..." -ForegroundColor Cyan

$Content = @()
$Content += "# 🧠 DSOM CLAUDE INITIALIZATION"
$Content += "Generated: $(Get-Date)"
$Content += "---"

# Master Protocol
$Content += "## ⚖️ MASTER PROTOCOL"
if (Test-Path "$DocsDir\AI-MASTER-PROTOCOL.md") {
    $Content += Get-Content "$DocsDir\AI-MASTER-PROTOCOL.md" -Raw -Encoding UTF8
} else {
    $Content += "Follow Zero-Global and Atomic Git laws."
}
$Content += "`n"

# Current Task
$Content += "## 🎯 CURRENT TASK"
if (Test-Path "$BrainDir\task.md") {
    $Content += Get-Content "$BrainDir\task.md" -Raw -Encoding UTF8
}
$Content += "`n"

# Mental Anchor
$Content += "## 🏁 MENTAL ANCHOR (WALKTHROUGH)"
if (Test-Path "$BrainDir\walkthrough.md") {
    $Content += Get-Content "$BrainDir\walkthrough.md" -Raw -Encoding UTF8
}
$Content += "`n"

# Implementation Plan
$Content += "## 🗺️ IMPLEMENTATION PLAN"
if (Test-Path "$BrainDir\implementation_plan.md") {
    $Content += Get-Content "$BrainDir\implementation_plan.md" -Raw -Encoding UTF8
}

$Content | Out-File -FilePath $Output -Encoding UTF8

Write-Host "✅ File '$Output' created. Upload this to your Claude Project Knowledge Base." -ForegroundColor Green

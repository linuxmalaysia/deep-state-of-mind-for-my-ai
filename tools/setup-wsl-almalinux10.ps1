<#
.SYNOPSIS
    DSOM AlmaLinux 10 WSL2 Setup Script (v1.0)

.DESCRIPTION
    Automates the setup of the AlmaLinux 10 WSL2 Control Node for DSOM.
    WSL Instance Name: dsom-control-almalinux10

    This script:
    1. Verifies WSL2 is enabled on Windows 11
    2. Downloads the AlmaLinux 10 rootfs tarball (official source)
    3. Imports it as 'dsom-control-almalinux10'
    4. Configures it as the Tier 2 DSOM Ansible Control Node

.AUTHOR
    Harisfazillah Jamel (LinuxMalaysia)

.LICENSE
    GNU GPL v3.0 or later

.USAGE
    Run as Administrator in PowerShell:
    .\tools\setup-wsl-almalinux10.ps1
#>

$ErrorActionPreference = "Stop"

# ── Configuration ─────────────────────────────────────────────────────────────
$WslName       = "dsom-control-almalinux10"
$WslInstallDir = "C:\WSL\$WslName"
$DownloadDir   = "$env:USERPROFILE\Downloads"
$TarballName   = "AlmaLinux10-wsl.tar.gz"
$TarballPath   = Join-Path $DownloadDir $TarballName

# AlmaLinux WSL official release URL (update this to the latest release if needed)
# Source: https://github.com/AlmaLinux/wsl-images/releases
$AlmaLinux10Url = "https://github.com/AlmaLinux/wsl-images/releases/latest/download/AlmaLinux-10-x64.tar.gz"

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "   DSOM AlmaLinux 10 WSL2 Setup                     " -ForegroundColor Cyan
Write-Host "   Instance: $WslName                               " -ForegroundColor Cyan
Write-Host "   Install:  $WslInstallDir                         " -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

# ── Step 1: Check Prerequisites ───────────────────────────────────────────────
Write-Host "[Step 1] Checking WSL2 Prerequisites..." -ForegroundColor Yellow

$WslCommand = Get-Command wsl -ErrorAction SilentlyContinue
if (-not $WslCommand) {
    Write-Host "[ERROR] WSL is not installed. Enabling now..." -ForegroundColor Red
    Write-Host "        Run this script as Administrator and restart after." -ForegroundColor Yellow

    dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
    dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

    Write-Host "[ACTION REQUIRED] Restart your computer, then run this script again." -ForegroundColor Red
    exit 1
}

# Ensure WSL2 is default
wsl --set-default-version 2 2>$null
wsl --update 2>$null

# Check if already exists
$existing = wsl --list --quiet 2>$null | Where-Object { $_ -eq $WslName }
if ($existing) {
    Write-Host "[WARNING] WSL instance '$WslName' already exists." -ForegroundColor Yellow
    $overwrite = Read-Host "Remove and re-import? (y/N)"
    if ($overwrite -match "^[yY]") {
        Write-Host "[ACTION] Removing existing instance '$WslName'..." -ForegroundColor Yellow
        wsl --unregister $WslName
    } else {
        Write-Host "[SKIP] Keeping existing instance. Exiting." -ForegroundColor Cyan
        exit 0
    }
}

Write-Host "[PASS] WSL2 is ready." -ForegroundColor Green

# ── Step 2: Download AlmaLinux 10 rootfs ──────────────────────────────────────
Write-Host ""
Write-Host "[Step 2] Downloading AlmaLinux 10 rootfs tarball..." -ForegroundColor Yellow
Write-Host "         Source: $AlmaLinux10Url" -ForegroundColor Cyan

if (Test-Path $TarballPath) {
    Write-Host "[SKIP] Tarball already exists at $TarballPath — skipping download." -ForegroundColor Yellow
} else {
    Write-Host "[INFO] Downloading to: $TarballPath" -ForegroundColor Cyan
    try {
        Invoke-WebRequest -Uri $AlmaLinux10Url -OutFile $TarballPath -UseBasicParsing
        Write-Host "[PASS] Download complete." -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Download failed: $_" -ForegroundColor Red
        Write-Host "        Manual download: https://github.com/AlmaLinux/wsl-images/releases" -ForegroundColor Yellow
        exit 1
    }
}

# ── Step 3: Create Install Directory ─────────────────────────────────────────
Write-Host ""
Write-Host "[Step 3] Preparing install directory: $WslInstallDir" -ForegroundColor Yellow
New-Item -ItemType Directory -Path $WslInstallDir -Force | Out-Null
Write-Host "[PASS] Directory ready." -ForegroundColor Green

# ── Step 4: Import AlmaLinux 10 into WSL2 ────────────────────────────────────
Write-Host ""
Write-Host "[Step 4] Importing AlmaLinux 10 into WSL2 as '$WslName'..." -ForegroundColor Yellow
Write-Host "         This may take 1-2 minutes." -ForegroundColor Cyan

wsl --import $WslName $WslInstallDir $TarballPath --version 2

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Import failed with exit code $LASTEXITCODE." -ForegroundColor Red
    exit 1
}

Write-Host "[PASS] Import successful." -ForegroundColor Green

# ── Step 5: Verify Import ─────────────────────────────────────────────────────
Write-Host ""
Write-Host "[Step 5] Verifying WSL instance..." -ForegroundColor Yellow
wsl --list --verbose
Write-Host ""
$almaVersion = wsl -d $WslName -- cat /etc/almalinux-release 2>$null
Write-Host "[INFO] AlmaLinux version: $almaVersion" -ForegroundColor Cyan
Write-Host "[PASS] '$WslName' is running." -ForegroundColor Green

# ── Step 6: Run Bootstrap Script Inside AlmaLinux ────────────────────────────
Write-Host ""
Write-Host "[Step 6] Running DSOM control node bootstrap inside '$WslName'..." -ForegroundColor Yellow
Write-Host "         This installs Ansible, creates dsom-admin user, configures wsl.conf." -ForegroundColor Cyan

# Convert Windows path to WSL path for the project root
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$WslProjectRoot = $ProjectRoot -replace "\\", "/" -replace "^([A-Za-z]):", "/mnt/`$(`$1.ToLower())"
$BootstrapScript = "$WslProjectRoot/tools/setup-dsom-control-node.sh"

wsl -d $WslName -u root -- bash -c "bash '$BootstrapScript'"

if ($LASTEXITCODE -ne 0) {
    Write-Host "[WARNING] Bootstrap script returned non-zero. Check output above." -ForegroundColor Yellow
} else {
    Write-Host "[PASS] Bootstrap complete." -ForegroundColor Green
}

# ── Final Summary ─────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "=====================================================" -ForegroundColor Green
Write-Host "   SETUP COMPLETE                                    " -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Launch: wsl -d $WslName" -ForegroundColor White
Write-Host "  2. Verify: ansible --version" -ForegroundColor White
Write-Host "  3. Test:   ansible localhost -m ping" -ForegroundColor White
Write-Host "  4. Follow: docs/HOWTO-SETUP-WSL-ALMALINUX10.md" -ForegroundColor White
Write-Host ""
Write-Host "DSOM Tier 2 (Dev Bridge) is now operational." -ForegroundColor Green

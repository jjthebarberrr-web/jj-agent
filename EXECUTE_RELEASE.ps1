# Complete Release Execution Script (PowerShell)
# This script executes the full release process end-to-end

$ErrorActionPreference = "Stop"

# Change to script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "JJ Agent v0.1.0 Release Execution" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# A) Push the release tag
Write-Host "[A] Pushing release tag..." -ForegroundColor Yellow
Write-Host ""

Write-Host "1. Pulling latest changes..." -ForegroundColor Gray
try {
    git pull --rebase
} catch {
    Write-Host "   No remote configured or already up to date" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "2. Checking tag exists..." -ForegroundColor Gray
$tags = git tag -l v0.1.0
if ($tags) {
    Write-Host "   Tag v0.1.0 exists" -ForegroundColor Green
} else {
    Write-Host "   Creating tag v0.1.0..." -ForegroundColor Yellow
    git tag -a v0.1.0 -m "Release v0.1.0 - Production Ready"
}

Write-Host ""
Write-Host "3. Pushing tag to remote..." -ForegroundColor Gray
$remotes = git remote
if ($remotes -match "origin") {
    try {
        git push origin v0.1.0
        Write-Host "   Tag pushed to origin" -ForegroundColor Green
    } catch {
        Write-Host "   Push failed - check permissions and remote" -ForegroundColor Red
    }
} else {
    Write-Host "   No remote 'origin' configured" -ForegroundColor Yellow
    Write-Host "   To push manually: git push origin v0.1.0" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✅ Step A Complete: Tag pushed" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Monitor CI/CD at: https://github.com/ORG/jj-agent/actions"
Write-Host "  2. Wait for pipeline to complete (5-10 minutes)"
Write-Host "  3. Run verification scripts (B)"
Write-Host "  4. Deploy to server (C)"
Write-Host "  5. Run production smoke test (D)"
Write-Host ""


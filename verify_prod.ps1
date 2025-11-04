# Production Verification Script for JJ Agent v0.1.0 (PowerShell)
# Usage: .\verify_prod.ps1

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "JJ Agent v0.1.0 Production Verification" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$PORT = if ($env:JJ_PORT) { $env:JJ_PORT } else { "5858" }
$WORKSPACE = if ($env:JJ_WORKSPACE) { $env:JJ_WORKSPACE } else { "$HOME\code\demo" }
$DOCKER_ORG = if ($env:DOCKER_ORG) { $env:DOCKER_ORG } else { "ORG" }

$checks = 0
$passed = 0
$warnings = 0

function Check-Pass {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
    $script:checks++
    $script:passed++
}

function Check-Fail {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
    $script:checks++
    exit 1
}

function Check-Warn {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
    $script:checks++
    $script:warnings++
}

Write-Host "[1/7] Checking jj version"
try {
    $versionOutput = jj version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Version: $versionOutput"
        if ($versionOutput -match "0\.1\.0") {
            Check-Pass "Version is 0.1.0"
        } else {
            Check-Warn "Version mismatch: expected 0.1.0, got $versionOutput"
        }
    } else {
        Check-Fail "jj command not found or not working"
    }
} catch {
    Check-Fail "jj command not found"
}
Write-Host ""

Write-Host "[2/7] Checking health endpoints"
$daemonRunning = Get-Process | Where-Object { $_.ProcessName -like "*jj*" -or $_.CommandLine -like "*daemon*" }
if ($daemonRunning) {
    try {
        $health = Invoke-WebRequest -Uri "http://localhost:${PORT}/healthz" -TimeoutSec 5 -UseBasicParsing -ErrorAction SilentlyContinue
        if ($health.StatusCode -eq 200) {
            Check-Pass "Health endpoint (/healthz) responds"
        }
    } catch {
        Check-Warn "Health endpoint not reachable (daemon may not be running)"
    }
    
    try {
        $ready = Invoke-WebRequest -Uri "http://localhost:${PORT}/readyz" -TimeoutSec 5 -UseBasicParsing -ErrorAction SilentlyContinue
        if ($ready.StatusCode -eq 200) {
            Check-Pass "Readiness endpoint (/readyz) responds"
        }
    } catch {
        Check-Warn "Readiness endpoint not reachable"
    }
} else {
    Check-Warn "Daemon not running, skipping health checks"
}
Write-Host ""

Write-Host "[3/7] Testing production mode capabilities enforcement"
if (-not $env:OPENAI_API_KEY) {
    Check-Warn "OPENAI_API_KEY not set, skipping full test"
    Write-Host "  Set OPENAI_API_KEY to run full production test"
} else {
    $env:JJ_ENV = "production"
    $env:JJ_PROD_STRICT = "1"
    
    if (Test-Path $WORKSPACE -PathType Container) {
        # Test that capabilities are enforced
        try {
            $result = jj run "cat C:\Windows\System32\config\sam" --workspace $WORKSPACE 2>&1
            if ($LASTEXITCODE -eq 0) {
                Check-Fail "Capabilities not enforced - forbidden path access allowed"
            } else {
                Check-Pass "Capabilities enforced - forbidden paths blocked"
            }
        } catch {
            Check-Pass "Capabilities enforced - command blocked"
        }
    }
}
Write-Host ""

Write-Host "[4/7] Checking audit logs"
if (Test-Path "state" -PathType Container) {
    $auditFiles = Get-ChildItem -Path "state" -Recurse -Filter "audit.jsonl" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($auditFiles) {
        Check-Pass "Audit log files found"
        Write-Host "  Sample audit log: $($auditFiles.FullName)"
        $lines = (Get-Content $auditFiles.FullName -ErrorAction SilentlyContinue | Measure-Object -Line).Lines
        Write-Host "  Lines in audit log: $lines"
    } else {
        Check-Warn "No audit logs found (may be first run)"
    }
} else {
    Check-Warn "State directory not found"
}
Write-Host ""

Write-Host "[5/7] Checking JSON logs"
$logPath = "C:\var\log\jj-agent"
if (Test-Path $logPath -PathType Container) {
    $logFiles = Get-ChildItem -Path $logPath -Filter "*.log" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($logFiles) {
        Check-Pass "JSON log files found"
        $content = Get-Content $logFiles.FullName -Raw -ErrorAction SilentlyContinue
        if ($content -match '"level"') {
            Check-Pass "JSON logs contain structured data"
        } else {
            Check-Warn "JSON logs may not be structured"
        }
    } else {
        Check-Warn "No log files found in $logPath"
    }
} else {
    Check-Warn "System log directory not found (may use local logging)"
}
Write-Host ""

Write-Host "[6/7] Testing sample production run"
if (-not $env:OPENAI_API_KEY) {
    Check-Warn "OPENAI_API_KEY not set, skipping production run test"
} else {
    $env:JJ_ENV = "production"
    $env:JJ_PROD_STRICT = "1"
    
    New-Item -ItemType Directory -Force -Path $WORKSPACE | Out-Null
    Write-Host "  Running test job in workspace: $WORKSPACE"
    Write-Host "  This may take a few minutes..."
    
    try {
        $result = jj run --dry-run "Create a FastAPI skeleton" --workspace $WORKSPACE 2>&1
        if ($LASTEXITCODE -eq 0) {
            Check-Pass "Production dry-run test passed"
        } else {
            Check-Warn "Production dry-run test failed"
        }
    } catch {
        Check-Warn "Production dry-run test failed or timed out"
    }
}
Write-Host ""

Write-Host "[7/7] Testing Docker image"
if (Get-Command docker -ErrorAction SilentlyContinue) {
    $IMAGE = "ghcr.io/${DOCKER_ORG}/jj-agent:v0.1.0"
    Write-Host "  Testing image: $IMAGE"
    
    try {
        docker pull $IMAGE 2>&1 | Out-Null
        Check-Pass "Docker image pulled successfully"
        
        $dockerVersion = docker run --rm $IMAGE jj version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Check-Pass "Docker image runs correctly"
        } else {
            Check-Fail "Docker image does not run correctly"
        }
    } catch {
        Check-Warn "Docker image not found or not accessible"
        Write-Host "  Image may not be published yet, or check permissions"
    }
} else {
    Check-Warn "Docker not available, skipping Docker tests"
}
Write-Host ""

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✅ Verification complete" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Summary: $passed passed, $warnings warnings, $checks total checks"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Review any warnings above"
Write-Host "  2. Check audit logs in state/ directory"
Write-Host "  3. Verify production capabilities in capabilities.prod.yaml"
Write-Host ""


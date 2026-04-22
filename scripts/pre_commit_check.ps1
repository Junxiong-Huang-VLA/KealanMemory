param(
    [switch]$SkipJs
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Push-Location $RepoRoot

try {
    Write-Host "[check] KealanMemory health"
    python boot/check_memory_consistency.py

    Write-Host "[check] Python compile"
    python -m compileall -q boot install web

    Write-Host "[check] PowerShell parse"
    $tokens = $null
    $errors = $null
    [System.Management.Automation.Language.Parser]::ParseFile(
        (Resolve-Path "boot/load_memory.ps1"),
        [ref]$tokens,
        [ref]$errors
    ) > $null
    if ($errors.Count -gt 0) {
        $errors | ForEach-Object { Write-Error $_.Message }
        exit 1
    }

    if (-not $SkipJs -and (Test-Path "web/static/js/app.js")) {
        $node = Get-Command node -ErrorAction SilentlyContinue
        if ($node) {
            Write-Host "[check] JavaScript syntax"
            node --check web/static/js/app.js
        } else {
            Write-Host "[warn] node not found; skipping JS syntax check"
        }
    }

    if (Test-Path "tests") {
        $pytest = python -c "import importlib.util, sys; sys.exit(0 if importlib.util.find_spec('pytest') else 1)"
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[check] pytest"
            python -m pytest -q
        } else {
            Write-Host "[warn] pytest not installed; skipping tests"
        }
    }

    Write-Host "[ok] pre-commit checks passed"
}
finally {
    Pop-Location
}

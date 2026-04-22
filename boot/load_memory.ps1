# Local memory loader (PowerShell)
# Usage:
#   .\load_memory.ps1
#   .\load_memory.ps1 -Project LabSOPGuard
#   .\load_memory.ps1 -Project LabSOPGuard -Full
#   .\load_memory.ps1 -List

param(
    [string]$Project = "",
    [switch]$Full,
    [switch]$List,
    [string]$Output = ""
)

$ErrorActionPreference = "Stop"

function Resolve-MemoryRoot {
    if ($env:KEALAN_MEMORY_ROOT) {
        return (Resolve-Path -LiteralPath $env:KEALAN_MEMORY_ROOT).Path
    }

    return (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
}

function Read-MemoryFile {
    param(
        [Parameter(Mandatory = $true)][string]$RelPath,
        [string]$ProjectName = "",
        [switch]$Optional
    )

    $displayPath = $RelPath -replace "\{project\}", $ProjectName
    $absPath = Join-Path $script:Root $displayPath
    if (-not (Test-Path -LiteralPath $absPath -PathType Leaf)) {
        if (-not $Optional) {
            Write-Warning "Skipping missing file: $absPath"
        }
        return ""
    }

    $content = Get-Content -LiteralPath $absPath -Encoding UTF8 -Raw
    $separator = "`n`n" + ("=" * 60) + "`n# Source: $displayPath`n" + ("=" * 60) + "`n"
    return $separator + $content.Trim()
}

$script:Root = Resolve-MemoryRoot
$MapFile = Join-Path $Root "boot\memory_map.json"
$map = Get-Content -LiteralPath $MapFile -Encoding UTF8 -Raw | ConvertFrom-Json

if (-not $Output) {
    $Output = Join-Path $Root "boot\assembled_context.txt"
}

if ($List) {
    Write-Host "Memory root: $Root"
    Write-Host "Available projects:"
    foreach ($p in $map.projects) {
        if ($p -eq "_template") {
            continue
        }
        $briefPath = Join-Path $Root "projects\$p\project_brief.md"
        $status = if (Test-Path -LiteralPath $briefPath -PathType Leaf) { "[ok]" } else { "[--]" }
        Write-Host "  $status $p"
    }
    exit 0
}

$chunks = @()
$mode = if ($Full) { "full" } else { "standard" }
$projectName = if ($Project) { $Project } else { "(none)" }
$chunks += "# Personal Memory Context (generated)"
$chunks += "# Project: $projectName"
$chunks += "# Load mode: $mode"
$chunks += "# Usage: paste this file into Claude, or see boot/startup_prompt.md"
$chunks += ""

Write-Host "Memory root: $Root"
Write-Host "Loading core memory..."
foreach ($relPath in $map.default_load) {
    $chunk = Read-MemoryFile -RelPath $relPath
    if ($chunk) {
        $chunks += $chunk
        Write-Host "  [ok] $relPath"
    }
}

if ($Project) {
    if ($map.projects -notcontains $Project) {
        Write-Warning "Project '$Project' is not listed in memory_map.json; trying to load it anyway."
    }
    Write-Host "`nLoading project memory: $Project..."
    foreach ($relPath in $map.project_load) {
        $chunk = Read-MemoryFile -RelPath $relPath -ProjectName $Project
        if ($chunk) {
            $chunks += $chunk
            $display = $relPath -replace "\{project\}", $Project
            Write-Host "  [ok] $display"
        }
    }
}

if ($Full) {
    Write-Host "`nLoading optional memory..."
    foreach ($relPath in $map.optional_load) {
        $isProjectPath = $relPath.StartsWith("projects/")
        if ($isProjectPath -and -not $Project) {
            continue
        }

        $chunk = Read-MemoryFile -RelPath $relPath -ProjectName $Project -Optional
        if ($chunk) {
            $chunks += $chunk
            $display = $relPath -replace "\{project\}", $Project
            Write-Host "  [ok] $display"
        }
    }
}

$outputDir = Split-Path -Parent $Output
if ($outputDir) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

($chunks -join "`n") | Out-File -LiteralPath $Output -Encoding UTF8
$sizeKB = [math]::Round((Get-Item -LiteralPath $Output).Length / 1024, 1)
Write-Host "`n[ok] Wrote output to: $Output ($sizeKB KB)"

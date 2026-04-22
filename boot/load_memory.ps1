# load_memory.ps1 — 本地记忆加载脚本（PowerShell）
# 用法：
#   .\load_memory.ps1                          # 仅核心记忆
#   .\load_memory.ps1 -Project LabSOPGuard     # 核心 + 项目记忆
#   .\load_memory.ps1 -Project LabSOPGuard -Full  # 追加完整规范
#   .\load_memory.ps1 -List                    # 列出可用项目

param(
    [string]$Project = "",
    [switch]$Full = $false,
    [switch]$List = $false,
    [string]$Output = "D:\KealanMemory\boot\assembled_context.txt"
)

$ROOT = "D:\KealanMemory"
$MapFile = "$ROOT\boot\memory_map.json"

# 读取 memory_map.json
$map = Get-Content $MapFile -Encoding UTF8 | ConvertFrom-Json

# 列出项目
if ($List) {
    Write-Host "可用项目："
    foreach ($p in $map.projects) {
        if ($p -ne "_template") {
            $briefPath = "$ROOT\projects\$p\project_brief.md"
            $status = if (Test-Path $briefPath) { "✓" } else { "✗" }
            Write-Host "  $status $p"
        }
    }
    exit
}

$chunks = @()
$chunks += "# 个人记忆上下文（自动生成）"
$chunks += "# 项目：$( if ($Project) { $Project } else { '（无）' } )"
$chunks += ""

# 函数：读取单个文件
function Read-MemoryFile($relPath, $project = "") {
    $fullPath = $relPath -replace "\{project\}", $project
    $absPath = Join-Path $ROOT $fullPath
    if (-not (Test-Path $absPath)) {
        Write-Warning "跳过（不存在）：$absPath"
        return ""
    }
    $content = Get-Content $absPath -Encoding UTF8 -Raw
    $sep = "`n`n" + ("=" * 60) + "`n# 来源：$fullPath`n" + ("=" * 60) + "`n"
    return $sep + $content
}

# 1. 核心记忆
Write-Host "加载核心记忆..."
foreach ($relPath in $map.default_load) {
    $chunk = Read-MemoryFile $relPath
    if ($chunk) {
        $chunks += $chunk
        Write-Host "  ✓ $relPath"
    }
}

# 2. 项目记忆
if ($Project) {
    Write-Host "`n加载项目记忆：$Project..."
    foreach ($relPath in $map.project_load) {
        $chunk = Read-MemoryFile $relPath $Project
        if ($chunk) {
            $chunks += $chunk
            $display = $relPath -replace "\{project\}", $Project
            Write-Host "  ✓ $display"
        }
    }
}

# 3. 完整规范
if ($Full) {
    Write-Host "`n加载完整规范..."
    $optionalRules = $map.optional_load | Where-Object { -not $_.StartsWith("projects/") }
    foreach ($relPath in $optionalRules) {
        $chunk = Read-MemoryFile $relPath $Project
        if ($chunk) {
            $chunks += $chunk
            Write-Host "  ✓ $relPath"
        }
    }
}

# 输出到文件
$output_content = $chunks -join "`n"
$output_content | Out-File -FilePath $Output -Encoding UTF8
$sizeKB = [math]::Round((Get-Item $Output).Length / 1024, 1)
Write-Host "`n✓ 已输出到：$Output（$sizeKB KB）"
Write-Host "  复制文件内容粘贴给 Claude 即可。"

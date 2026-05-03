param(
    [string]$SourceDir
)

$ErrorActionPreference = "Stop"

if (-not $SourceDir) {
    $SourceDir = $PSScriptRoot
}

$SourceDir = (Resolve-Path $SourceDir).Path
$TargetRoot = Join-Path $HOME ".codex\skills"
$SkillNames = @(
    "gnn-paper-reproduction",
    "gnn-repo-runner",
    "gnn-idea-lab",
    "gnn-experiment-review"
)

New-Item -ItemType Directory -Force $TargetRoot | Out-Null

foreach ($SkillName in $SkillNames) {
    $SourceSkill = Join-Path $SourceDir $SkillName
    if (-not (Test-Path $SourceSkill)) {
        Write-Warning "Skip missing skill: $SourceSkill"
        continue
    }

    $TargetSkill = Join-Path $TargetRoot $SkillName
    if (Test-Path $TargetSkill) {
        Remove-Item -LiteralPath $TargetSkill -Recurse -Force
    }

    Copy-Item -LiteralPath $SourceSkill -Destination $TargetRoot -Recurse -Force
    Write-Host "Installed $SkillName -> $TargetSkill"
}

Write-Host "Done. Skills installed to $TargetRoot"

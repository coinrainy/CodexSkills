$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$TargetRoot = Join-Path $RepoRoot "codex-skills"
$LocalRoot = Join-Path $HOME ".codex\skills"
$SkillNames = @(
    "gnn-paper-reproduction",
    "gnn-repo-runner",
    "gnn-idea-lab",
    "gnn-experiment-review"
)

if (-not (Test-Path $LocalRoot)) {
    throw "Local Codex skills directory not found: $LocalRoot"
}

New-Item -ItemType Directory -Force $TargetRoot | Out-Null

foreach ($SkillName in $SkillNames) {
    $SourceSkill = Join-Path $LocalRoot $SkillName
    $TargetSkill = Join-Path $TargetRoot $SkillName

    if (-not (Test-Path $SourceSkill)) {
        Write-Warning "Skip missing local skill: $SourceSkill"
        continue
    }

    if (Test-Path $TargetSkill) {
        $ResolvedTarget = (Resolve-Path $TargetSkill).Path
        if (-not $ResolvedTarget.StartsWith($TargetRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
            throw "Refuse to remove path outside repo target root: $ResolvedTarget"
        }
        Remove-Item -LiteralPath $ResolvedTarget -Recurse -Force
    }

    Copy-Item -LiteralPath $SourceSkill -Destination $TargetRoot -Recurse -Force
    Write-Host "Synced $SkillName"
}

Write-Host "Done. Repo copy refreshed at $TargetRoot"

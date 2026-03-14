param(
    [switch]$WriteArtifacts,
    [string]$OutputDirectory = ''
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot '..\common\vibe-governance-helpers.ps1')
. (Join-Path $PSScriptRoot '..\runtime\VibeRuntime.Common.ps1')

function Add-Assertion {
    param(
        [ref]$Results,
        [bool]$Condition,
        [string]$Message,
        [string]$Details = ''
    )

    $record = [pscustomobject]@{
        passed = [bool]$Condition
        message = $Message
        details = $Details
    }
    $Results.Value += $record

    if ($Condition) {
        Write-Host "[PASS] $Message"
    } else {
        Write-Host "[FAIL] $Message" -ForegroundColor Red
        if ($Details) {
            Write-Host "       $Details" -ForegroundColor DarkRed
        }
    }
}

$context = Get-VgoGovernanceContext -ScriptPath $PSCommandPath -EnforceExecutionContext
$repoRoot = $context.repoRoot
$results = @()

$requiredFiles = @(
    'SKILL.md',
    'protocols/runtime.md',
    'protocols/think.md',
    'protocols/do.md',
    'protocols/team.md',
    'protocols/retro.md',
    'config/runtime-contract.json',
    'config/runtime-modes.json',
    'config/requirement-doc-policy.json',
    'config/plan-execution-policy.json',
    'config/phase-cleanup-policy.json',
    'docs/requirements/README.md',
    'templates/requirements/governed-requirement-template.md',
    'templates/plans/governed-execution-plan-template.md',
    'scripts/runtime/VibeRuntime.Common.ps1',
    'scripts/runtime/invoke-vibe-runtime.ps1',
    'scripts/runtime/Invoke-SkeletonCheck.ps1',
    'scripts/runtime/Invoke-DeepInterview.ps1',
    'scripts/runtime/Write-RequirementDoc.ps1',
    'scripts/runtime/Write-XlPlan.ps1',
    'scripts/runtime/Invoke-PlanExecute.ps1',
    'scripts/runtime/Invoke-PhaseCleanup.ps1'
)

foreach ($relativePath in $requiredFiles) {
    $fullPath = Join-Path $repoRoot $relativePath
    Add-Assertion -Results ([ref]$results) -Condition (Test-Path -LiteralPath $fullPath) -Message ("required governed runtime file exists: {0}" -f $relativePath) -Details $fullPath
}

$runtimeContract = Get-Content -LiteralPath (Join-Path $repoRoot 'config\runtime-contract.json') -Raw -Encoding UTF8 | ConvertFrom-Json
Add-Assertion -Results ([ref]$results) -Condition ($runtimeContract.entry_skill -eq 'vibe') -Message 'runtime contract entry skill is vibe'
Add-Assertion -Results ([ref]$results) -Condition (@($runtimeContract.stages).Count -eq 6) -Message 'runtime contract defines six fixed stages'

$skillText = Get-Content -LiteralPath (Join-Path $repoRoot 'SKILL.md') -Raw -Encoding UTF8
Add-Assertion -Results ([ref]$results) -Condition (
    $skillText.Contains('skeleton_check') -and
    $skillText.Contains('deep_interview') -and
    $skillText.Contains('requirement_doc') -and
    $skillText.Contains('xl_plan') -and
    $skillText.Contains('plan_execute') -and
    $skillText.Contains('phase_cleanup')
) -Message 'SKILL.md documents the fixed stage machine'

$teamText = Get-Content -LiteralPath (Join-Path $repoRoot 'protocols\team.md') -Raw -Encoding UTF8
Add-Assertion -Results ([ref]$results) -Condition ($teamText.Contains('$vibe')) -Message 'team protocol requires subagent prompts to end with $vibe'

$runId = "contract-gate-" + [System.Guid]::NewGuid().ToString('N').Substring(0, 8)
$artifactRoot = Join-Path $repoRoot (".tmp\governed-runtime-contract-{0}" -f $runId)
$summary = & (Join-Path $repoRoot 'scripts\runtime\invoke-vibe-runtime.ps1') -Task 'governed runtime contract smoke proof' -Mode benchmark_autonomous -RunId $runId -ArtifactRoot $artifactRoot

Add-Assertion -Results ([ref]$results) -Condition ($summary.mode -eq 'benchmark_autonomous') -Message 'runtime smoke summary preserves benchmark_autonomous mode'

$artifactPaths = @(
    $summary.summary.artifacts.skeleton_receipt,
    $summary.summary.artifacts.intent_contract,
    $summary.summary.artifacts.requirement_doc,
    $summary.summary.artifacts.execution_plan,
    $summary.summary.artifacts.execute_receipt,
    $summary.summary.artifacts.cleanup_receipt
)

foreach ($artifactPath in $artifactPaths) {
    Add-Assertion -Results ([ref]$results) -Condition (Test-Path -LiteralPath $artifactPath) -Message ("runtime smoke artifact exists: {0}" -f ([System.IO.Path]::GetFileName($artifactPath))) -Details $artifactPath
}

$failureCount = @($results | Where-Object { -not $_.passed }).Count
$gatePassed = ($failureCount -eq 0)
$report = [pscustomobject]@{
    generated_at = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    repo_root = $repoRoot
    gate_passed = $gatePassed
    assertion_count = @($results).Count
    failure_count = $failureCount
    runtime_summary_path = $summary.summary_path
    results = @($results)
}

if ($WriteArtifacts) {
    $targetDir = if ([string]::IsNullOrWhiteSpace($OutputDirectory)) {
        Join-Path $repoRoot 'outputs\verify\vibe-governed-runtime-contract'
    } elseif ([System.IO.Path]::IsPathRooted($OutputDirectory)) {
        [System.IO.Path]::GetFullPath($OutputDirectory)
    } else {
        [System.IO.Path]::GetFullPath((Join-Path $repoRoot $OutputDirectory))
    }

    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    Write-VibeJsonArtifact -Path (Join-Path $targetDir 'vibe-governed-runtime-contract-gate.json') -Value $report
} elseif (Test-Path -LiteralPath $artifactRoot) {
    Remove-Item -LiteralPath $artifactRoot -Recurse -Force
}

if (-not $gatePassed) {
    throw "vibe-governed-runtime-contract-gate failed with $failureCount failing assertion(s)."
}

$report

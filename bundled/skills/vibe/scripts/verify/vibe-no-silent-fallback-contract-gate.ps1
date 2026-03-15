param(
    [switch]$WriteArtifacts,
    [string]$OutputDirectory = ''
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\common\vibe-governance-helpers.ps1')

function Add-Assertion {
    param(
        [System.Collections.Generic.List[object]]$Assertions,
        [bool]$Pass,
        [string]$Message,
        [object]$Details = $null
    )

    $Assertions.Add([pscustomobject]@{
        pass = [bool]$Pass
        message = $Message
        details = $Details
    }) | Out-Null

    Write-Host ("[{0}] {1}" -f $(if ($Pass) { 'PASS' } else { 'FAIL' }), $Message) -ForegroundColor $(if ($Pass) { 'Green' } else { 'Red' })
}

function Write-GateArtifacts {
    param(
        [string]$RepoRoot,
        [string]$OutputDirectory,
        [psobject]$Artifact
    )

    $dir = if ([string]::IsNullOrWhiteSpace($OutputDirectory)) { Join-Path $RepoRoot 'outputs\verify' } else { $OutputDirectory }
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    $jsonPath = Join-Path $dir 'vibe-no-silent-fallback-contract-gate.json'
    $mdPath = Join-Path $dir 'vibe-no-silent-fallback-contract-gate.md'
    Write-VgoUtf8NoBomText -Path $jsonPath -Content ($Artifact | ConvertTo-Json -Depth 100)

    $lines = @(
        '# VCO No Silent Fallback Contract Gate',
        '',
        ('- Gate Result: **{0}**' -f $Artifact.gate_result),
        ('- Repo Root: `{0}`' -f $Artifact.repo_root),
        ('- Failure count: `{0}`' -f $Artifact.summary.failure_count),
        '',
        '## Assertions',
        ''
    )

    foreach ($assertion in @($Artifact.assertions)) {
        $lines += ('- `{0}` {1}' -f $(if ($assertion.pass) { 'PASS' } else { 'FAIL' }), $assertion.message)
    }

    Write-VgoUtf8NoBomText -Path $mdPath -Content ($lines -join "`n")
}

$context = Get-VgoGovernanceContext -ScriptPath $PSCommandPath -EnforceExecutionContext
$repoRoot = $context.repoRoot
$assertions = [System.Collections.Generic.List[object]]::new()

$runtimeContractPath = Join-Path $repoRoot 'config\runtime-contract.json'
$fallbackPolicyPath = Join-Path $repoRoot 'config\fallback-governance.json'
$routerGovernancePath = Join-Path $repoRoot 'config\router-model-governance.json'
$runtimeProtocolPath = Join-Path $repoRoot 'protocols\runtime.md'
$routeScriptPath = Join-Path $repoRoot 'scripts\router\resolve-pack-route.ps1'

$runtimeContract = Get-Content -LiteralPath $runtimeContractPath -Raw -Encoding UTF8 | ConvertFrom-Json
$fallbackPolicy = Get-Content -LiteralPath $fallbackPolicyPath -Raw -Encoding UTF8 | ConvertFrom-Json
$routerGovernance = Get-Content -LiteralPath $routerGovernancePath -Raw -Encoding UTF8 | ConvertFrom-Json
$runtimeProtocol = Get-Content -LiteralPath $runtimeProtocolPath -Raw -Encoding UTF8

Add-Assertion -Assertions $assertions -Pass ([bool]$runtimeContract.invariants.no_silent_fallback) -Message 'runtime contract encodes no_silent_fallback'
Add-Assertion -Assertions $assertions -Pass ([bool]$runtimeContract.invariants.no_silent_degradation) -Message 'runtime contract encodes no_silent_degradation'
Add-Assertion -Assertions $assertions -Pass ([bool]$runtimeContract.invariants.fallback_hazard_alert_required) -Message 'runtime contract requires fallback hazard alert'
Add-Assertion -Assertions $assertions -Pass (-not [bool]$fallbackPolicy.silent_fallback) -Message 'fallback policy forbids silent fallback'
Add-Assertion -Assertions $assertions -Pass (-not [bool]$fallbackPolicy.silent_degradation) -Message 'fallback policy forbids silent degradation'
Add-Assertion -Assertions $assertions -Pass ([bool]$fallbackPolicy.require_hazard_alert) -Message 'fallback policy requires hazard alert'
Add-Assertion -Assertions $assertions -Pass ([string]$routerGovernance.provider_neutral_contract.degrade_honesty.fallback_truth_level -eq 'non_authoritative') -Message 'router governance maps degraded fallback truth to non_authoritative'
Add-Assertion -Assertions $assertions -Pass ([bool]$routerGovernance.hard_rules.must_emit_hazard_alert_for_fallback) -Message 'router governance requires fallback hazard alert'
Add-Assertion -Assertions $assertions -Pass ($runtimeProtocol.Contains('Silent fallback and silent degradation are forbidden.')) -Message 'runtime protocol documents no silent fallback'

$route = & $routeScriptPath -Prompt 'help me with this' -Grade 'M' -TaskType 'research' | ConvertFrom-Json
Add-Assertion -Assertions $assertions -Pass ([bool]$route.fallback_active) -Message 'low-signal route marks fallback_active'
Add-Assertion -Assertions $assertions -Pass ([bool]$route.hazard_alert_required) -Message 'low-signal route requires hazard alert'
Add-Assertion -Assertions $assertions -Pass ([string]$route.truth_level -eq 'non_authoritative') -Message 'low-signal route truth_level is non_authoritative'
Add-Assertion -Assertions $assertions -Pass ([string]$route.degradation_state -in @('fallback_active', 'fallback_guarded')) -Message 'low-signal route records fallback degradation state'
Add-Assertion -Assertions $assertions -Pass ($route.hazard_alert -and [string]$route.hazard_alert.title -eq 'FALLBACK HAZARD ALERT') -Message 'low-signal route emits fallback hazard alert object'
Add-Assertion -Assertions $assertions -Pass (
    $route.confirm_ui -and
    [string]$route.confirm_ui.rendered_text -match 'FALLBACK HAZARD ALERT'
) -Message 'confirm UI renders standalone fallback hazard alert'

$failureCount = @($assertions | Where-Object { -not $_.pass }).Count
$artifact = [pscustomobject]@{
    gate = 'vibe-no-silent-fallback-contract-gate'
    repo_root = $repoRoot
    gate_result = if ($failureCount -eq 0) { 'PASS' } else { 'FAIL' }
    generated_at = (Get-Date).ToString('s')
    assertions = @($assertions)
    summary = [pscustomobject]@{
        failure_count = $failureCount
        route_mode = if ($route) { [string]$route.route_mode } else { '' }
        route_reason = if ($route) { [string]$route.route_reason } else { '' }
    }
}

if ($WriteArtifacts) {
    Write-GateArtifacts -RepoRoot $repoRoot -OutputDirectory $OutputDirectory -Artifact $artifact
}

if ($failureCount -gt 0) {
    exit 1
}

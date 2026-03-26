param(
    [string]$RepoRoot = '',
    [switch]$WriteArtifacts
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($RepoRoot)) {
    $RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
}

. (Join-Path $RepoRoot 'scripts\common\vibe-governance-helpers.ps1')

$cases = @(
    @{ host = 'codex'; target = 'C:\Users\demo\.claude'; should_throw = $true },
    @{ host = 'codex'; target = 'C:\Users\demo\.config\opencode'; should_throw = $true },
    @{ host = 'claude-code'; target = 'C:\Users\demo\.codex'; should_throw = $true },
    @{ host = 'claude-code'; target = 'C:\Users\demo\.config\opencode'; should_throw = $true },
    @{ host = 'generic'; target = 'C:\Users\demo\.codex'; should_throw = $true },
    @{ host = 'generic'; target = 'C:\Users\demo\.vibe-skills\generic'; should_throw = $false },
    @{ host = 'opencode'; target = 'C:\Users\demo\.claude'; should_throw = $true },
    @{ host = 'opencode'; target = 'C:\Users\demo\.config\opencode'; should_throw = $false },
    @{ host = 'opencode'; target = 'C:\repo\.opencode'; should_throw = $false }
)

$failures = @()
$rows = @()

foreach ($case in $cases) {
    $threw = $false
    try {
        Assert-VgoTargetRootMatchesHostIntent -TargetRoot $case.target -HostId $case.host
    } catch {
        $threw = $true
    }
    if ($threw -ne [bool]$case.should_throw) {
        $failures += "guard mismatch host=$($case.host) target=$($case.target) expected_throw=$($case.should_throw) actual_throw=$threw"
    }
    $rows += [pscustomobject]@{
        host = $case.host
        target = $case.target
        expected_throw = [bool]$case.should_throw
        actual_throw = [bool]$threw
    }
}

$gateResult = if ($failures.Count -eq 0) { 'PASS' } else { 'FAIL' }
$gatePayload = [ordered]@{}
$gatePayload['gate'] = 'vgo-adapter-target-root-guard-gate'
$gatePayload['result'] = $gateResult
$gatePayload['rows'] = @($rows)
$gatePayload['failures'] = @($failures)

if ($WriteArtifacts) {
    $outDir = Join-Path $RepoRoot 'outputs\verify'
    New-Item -ItemType Directory -Force -Path $outDir | Out-Null
    $outPath = Join-Path $outDir 'vgo-adapter-target-root-guard-gate.json'
    $gatePayload | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $outPath -Encoding UTF8
}

$gatePayload | ConvertTo-Json -Depth 10
if ($failures.Count -gt 0) { exit 1 }

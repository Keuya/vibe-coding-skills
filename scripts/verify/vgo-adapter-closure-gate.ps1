param(
    [string]$RepoRoot = '',
    [switch]$WriteArtifacts
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($RepoRoot)) {
    $RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
}

. (Join-Path $RepoRoot 'scripts\common\Resolve-VgoAdapter.ps1')

$registryResolution = Resolve-VgoAdapterRegistry -RepoRoot $RepoRoot
$registry = $registryResolution.registry
$failures = @()
$rows = @()

foreach ($entry in @($registry.adapters)) {
    $paths = @([string]$entry.host_profile, [string]$entry.settings_map, [string]$entry.closure, [string]$entry.manifest)
    foreach ($rel in $paths) {
        if ([string]::IsNullOrWhiteSpace($rel)) { continue }
        $full = Join-Path $RepoRoot $rel
        if (-not (Test-Path -LiteralPath $full)) {
            $failures += "missing artifact for adapter '$($entry.id)': $rel"
        }
    }
    $rows += [pscustomobject]@{
        adapter_id = [string]$entry.id
        status = [string]$entry.status
        install_mode = [string]$entry.install_mode
        check_mode = [string]$entry.check_mode
        bootstrap_mode = [string]$entry.bootstrap_mode
    }
}

$gateResult = if ($failures.Count -eq 0) { 'PASS' } else { 'FAIL' }
$gatePayload = [ordered]@{}
$gatePayload['gate'] = 'vgo-adapter-closure-gate'
$gatePayload['result'] = $gateResult
$gatePayload['adapter_count'] = @($registry.adapters).Count
$gatePayload['rows'] = @($rows)
$gatePayload['failures'] = @($failures)

if ($WriteArtifacts) {
    $outDir = Join-Path $RepoRoot 'outputs\verify'
    New-Item -ItemType Directory -Force -Path $outDir | Out-Null
    $outPath = Join-Path $outDir 'vgo-adapter-closure-gate.json'
    $gatePayload | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $outPath -Encoding UTF8
}

$gatePayload | ConvertTo-Json -Depth 10
if ($failures.Count -gt 0) { exit 1 }

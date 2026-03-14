param(
    [string]$TargetRoot = '',
    [switch]$WriteArtifacts
)

$ErrorActionPreference = 'Stop'

function Add-Assertion {
    param(
        [System.Collections.Generic.List[object]]$Collection,
        [bool]$Condition,
        [string]$Message
    )

    if ($Condition) {
        Write-Host "[PASS] $Message"
    } else {
        Write-Host "[FAIL] $Message" -ForegroundColor Red
    }

    [void]$Collection.Add([pscustomobject]@{
        ok = $Condition
        message = $Message
    })
}

function Add-WarningNote {
    param(
        [System.Collections.Generic.List[string]]$Collection,
        [string]$Message
    )

    Write-Host "[WARN] $Message" -ForegroundColor Yellow
    [void]$Collection.Add($Message)
}

function Test-ContentPattern {
    param(
        [Parameter(Mandatory)] [string]$Path,
        [Parameter(Mandatory)] [string]$Pattern
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        return $false
    }

    return [bool](Select-String -LiteralPath $Path -Pattern $Pattern -SimpleMatch -Quiet)
}

function Get-ReceiptVersionFromGate {
    param(
        [Parameter(Mandatory)] [string]$GatePath
    )

    if (-not (Test-Path -LiteralPath $GatePath)) {
        return $null
    }

    $match = Select-String -LiteralPath $GatePath -Pattern 'receipt_version\s*=\s*([0-9]+)'
    if ($null -eq $match) {
        return $null
    }

    return [int]$match.Matches[0].Groups[1].Value
}

function Write-Artifacts {
    param(
        [string]$RepoRoot,
        [psobject]$Artifact
    )

    $outputDir = Join-Path $RepoRoot 'outputs\verify'
    New-Item -ItemType Directory -Force -Path $outputDir | Out-Null

    $jsonPath = Join-Path $outputDir 'vibe-release-install-runtime-coherence-gate.json'
    $mdPath = Join-Path $outputDir 'vibe-release-install-runtime-coherence-gate.md'

    Write-VgoUtf8NoBomText -Path $jsonPath -Content ($Artifact | ConvertTo-Json -Depth 100)

    $lines = @(
        '# VCO Release / Install / Runtime Coherence Gate',
        '',
        ('- Gate Result: **{0}**' -f $Artifact.gate_result),
        ('- Repo Root: `{0}`' -f $Artifact.repo_root),
        ('- Target Root: `{0}`' -f $Artifact.target_root),
        ('- Assertion Failures: {0}' -f $Artifact.summary.failures),
        ('- Warnings: {0}' -f $Artifact.summary.warnings),
        ''
    )

    if ($Artifact.assertions.Count -gt 0) {
        $lines += '## Assertions'
        $lines += ''
        foreach ($item in $Artifact.assertions) {
            $lines += ('- [{0}] {1}' -f $(if ($item.ok) { 'PASS' } else { 'FAIL' }), $item.message)
        }
        $lines += ''
    }

    if ($Artifact.warnings.Count -gt 0) {
        $lines += '## Warnings'
        $lines += ''
        foreach ($item in $Artifact.warnings) {
            $lines += ('- {0}' -f $item)
        }
        $lines += ''
    }

    Write-VgoUtf8NoBomText -Path $mdPath -Content ($lines -join "`n")
}

. (Join-Path $PSScriptRoot '..\common\vibe-governance-helpers.ps1')

$TargetRoot = Resolve-VgoTargetRoot -TargetRoot $TargetRoot

$context = Get-VgoGovernanceContext -ScriptPath $PSCommandPath -EnforceExecutionContext
$runtimeConfig = $context.runtimeConfig
$assertions = New-Object System.Collections.Generic.List[object]
$warnings = New-Object System.Collections.Generic.List[string]

$versionDoc = Join-Path $context.repoRoot 'docs\version-packaging-governance.md'
$runtimeDoc = Join-Path $context.repoRoot 'docs\runtime-freshness-install-sop.md'
$installPs1 = Join-Path $context.repoRoot 'install.ps1'
$installSh = Join-Path $context.repoRoot 'install.sh'
$checkPs1 = Join-Path $context.repoRoot 'check.ps1'
$checkSh = Join-Path $context.repoRoot 'check.sh'
$runtimeGatePath = Join-Path $context.repoRoot ([string]$runtimeConfig.post_install_gate)
$coherenceGatePath = Join-Path $context.repoRoot ([string]$runtimeConfig.coherence_gate)
$frontmatterGatePath = Join-Path $context.repoRoot 'scripts\verify\vibe-bom-frontmatter-gate.ps1'
$syncBundledPath = Join-Path $context.repoRoot 'scripts\governance\sync-bundled-vibe.ps1'
$receiptPath = Join-Path $TargetRoot ([string]$runtimeConfig.receipt_relpath)

$results = [ordered]@{
    gate = 'vibe-release-install-runtime-coherence-gate'
    repo_root = $context.repoRoot
    target_root = [System.IO.Path]::GetFullPath($TargetRoot)
    generated_at = (Get-Date).ToString('s')
    gate_result = 'FAIL'
    assertions = @()
    warnings = @()
    contract = [ordered]@{
        target_relpath = [string]$runtimeConfig.target_relpath
        receipt_relpath = [string]$runtimeConfig.receipt_relpath
        post_install_gate = [string]$runtimeConfig.post_install_gate
        coherence_gate = [string]$runtimeConfig.coherence_gate
        receipt_contract_version = [int]$runtimeConfig.receipt_contract_version
        shell_degraded_behavior = [string]$runtimeConfig.shell_degraded_behavior
    }
    summary = [ordered]@{
        failures = 0
        warnings = 0
    }
}

Write-Host '=== VCO Release / Install / Runtime Coherence Gate ==='
Write-Host ("Repo root  : {0}" -f $context.repoRoot)
Write-Host ("Target root: {0}" -f $TargetRoot)
Write-Host ''

Add-Assertion -Collection $assertions -Condition $context.legacySourceOfTruthCompatibility.isCompatible -Message '[topology] mirror_topology remains compatible with legacy source_of_truth fields'
Add-Assertion -Collection $assertions -Condition (-not [string]::IsNullOrWhiteSpace([string]$runtimeConfig.target_relpath)) -Message '[runtime] target_relpath is declared'
Add-Assertion -Collection $assertions -Condition (-not [string]::IsNullOrWhiteSpace([string]$runtimeConfig.receipt_relpath)) -Message '[runtime] receipt_relpath is declared'
Add-Assertion -Collection $assertions -Condition ([string]$runtimeConfig.receipt_relpath).StartsWith(([string]$runtimeConfig.target_relpath).Replace('\', '/') + '/', [System.StringComparison]::OrdinalIgnoreCase) -Message '[runtime] receipt_relpath stays under target_relpath'
Add-Assertion -Collection $assertions -Condition (Test-Path -LiteralPath $runtimeGatePath) -Message '[runtime] post-install freshness gate script exists'
Add-Assertion -Collection $assertions -Condition (Test-Path -LiteralPath $coherenceGatePath) -Message '[runtime] coherence gate script exists'
Add-Assertion -Collection $assertions -Condition (Test-Path -LiteralPath $frontmatterGatePath) -Message '[runtime] BOM/frontmatter gate script exists'
Add-Assertion -Collection $assertions -Condition (Test-Path -LiteralPath $syncBundledPath) -Message '[runtime] sync-bundled-vibe script exists for mirror closure'
Add-Assertion -Collection $assertions -Condition (@($runtimeConfig.required_runtime_markers) -contains [string]$runtimeConfig.post_install_gate) -Message '[runtime] required_runtime_markers includes post-install freshness gate'
Add-Assertion -Collection $assertions -Condition (@($runtimeConfig.required_runtime_markers) -contains [string]$runtimeConfig.coherence_gate) -Message '[runtime] required_runtime_markers includes coherence gate'
Add-Assertion -Collection $assertions -Condition ([int]$runtimeConfig.receipt_contract_version -ge 1) -Message '[runtime] receipt_contract_version is declared and >= 1'
Add-Assertion -Collection $assertions -Condition ([string]$runtimeConfig.shell_degraded_behavior -eq 'warn_and_skip_authoritative_runtime_gate') -Message '[runtime] shell_degraded_behavior declares warn-and-skip semantics'

Add-Assertion -Collection $assertions -Condition (Test-Path -LiteralPath $versionDoc) -Message '[docs] version-packaging-governance.md exists'
Add-Assertion -Collection $assertions -Condition (Test-Path -LiteralPath $runtimeDoc) -Message '[docs] runtime-freshness-install-sop.md exists'
Add-Assertion -Collection $assertions -Condition (Test-ContentPattern -Path $versionDoc -Pattern 'release only governs repo parity') -Message '[docs] version governance doc defines release boundary'
Add-Assertion -Collection $assertions -Condition (Test-ContentPattern -Path $versionDoc -Pattern 'execution-context lock') -Message '[docs] version governance doc documents execution-context lock'
Add-Assertion -Collection $assertions -Condition (Test-ContentPattern -Path $runtimeDoc -Pattern 'receipt contract') -Message '[docs] runtime SOP documents receipt contract'
Add-Assertion -Collection $assertions -Condition (Test-ContentPattern -Path $runtimeDoc -Pattern 'shell degraded behavior') -Message '[docs] runtime SOP documents shell degraded behavior'

Add-Assertion -Collection $assertions -Condition (Test-ContentPattern -Path $installPs1 -Pattern 'Invoke-InstalledRuntimeFreshnessGate') -Message '[install.ps1] install flow invokes runtime freshness gate'
Add-Assertion -Collection $assertions -Condition (Test-ContentPattern -Path $installSh -Pattern 'run_runtime_freshness_gate') -Message '[install.sh] shell install flow invokes runtime freshness gate'
Add-Assertion -Collection $assertions -Condition (Test-ContentPattern -Path $checkPs1 -Pattern 'Invoke-RuntimeFreshnessCheck') -Message '[check.ps1] check flow invokes runtime freshness gate'
Add-Assertion -Collection $assertions -Condition (Test-ContentPattern -Path $checkPs1 -Pattern 'Invoke-RuntimeCoherenceCheck') -Message '[check.ps1] check flow invokes coherence gate'
Add-Assertion -Collection $assertions -Condition (Test-ContentPattern -Path $checkSh -Pattern 'run_runtime_freshness_gate') -Message '[check.sh] shell check flow invokes runtime freshness gate'
Add-Assertion -Collection $assertions -Condition (Test-ContentPattern -Path $checkSh -Pattern 'run_runtime_coherence_gate') -Message '[check.sh] shell check flow invokes coherence gate'
Add-Assertion -Collection $assertions -Condition (Test-ContentPattern -Path $checkSh -Pattern 'pwsh is not installed') -Message '[check.sh] shell check documents missing-pwsh degraded behavior'

$receiptVersionFromGate = Get-ReceiptVersionFromGate -GatePath $runtimeGatePath
Add-Assertion -Collection $assertions -Condition ($null -ne $receiptVersionFromGate) -Message '[receipt] installed runtime freshness gate emits receipt_version'
if ($null -ne $receiptVersionFromGate) {
    Add-Assertion -Collection $assertions -Condition ($receiptVersionFromGate -eq [int]$runtimeConfig.receipt_contract_version) -Message '[receipt] gate receipt_version matches configured receipt_contract_version'
}
Add-Assertion -Collection $assertions -Condition (Test-ContentPattern -Path $runtimeGatePath -Pattern 'gate_result') -Message '[receipt] installed runtime freshness gate writes gate_result'

if (Test-Path -LiteralPath $receiptPath) {
    try {
        $receipt = Get-Content -LiteralPath $receiptPath -Raw -Encoding UTF8 | ConvertFrom-Json
        $receiptGateResult = if ($receipt.PSObject.Properties.Name -contains 'gate_result') { [string]$receipt.gate_result } else { $null }
        $receiptVersion = if ($receipt.PSObject.Properties.Name -contains 'receipt_version') { [int]$receipt.receipt_version } else { 0 }
        Add-Assertion -Collection $assertions -Condition ($receiptGateResult -eq 'PASS') -Message '[receipt] installed runtime receipt gate_result is PASS'
        Add-Assertion -Collection $assertions -Condition ($receiptVersion -ge [int]$runtimeConfig.receipt_contract_version) -Message '[receipt] installed runtime receipt version satisfies contract'
    } catch {
        Add-Assertion -Collection $assertions -Condition $false -Message ('[receipt] installed runtime receipt parses cleanly -> {0}' -f $_.Exception.Message)
    }
} else {
    Add-WarningNote -Collection $warnings -Message ('runtime receipt not found at {0}; repo contract validated without installed-runtime evidence.' -f $receiptPath)
}

$results.assertions = @($assertions.ToArray())
$results.warnings = @($warnings.ToArray())
$results.summary.failures = @($assertions | Where-Object { -not $_.ok }).Count
$results.summary.warnings = $warnings.Count
$results.gate_result = if ($results.summary.failures -eq 0) { 'PASS' } else { 'FAIL' }

if ($WriteArtifacts) {
    Write-Artifacts -RepoRoot $context.repoRoot -Artifact ([pscustomobject]$results)
}

if ($results.summary.failures -gt 0) {
    exit 1
}

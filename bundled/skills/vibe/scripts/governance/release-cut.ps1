param(
    [string]$Version = '',
    [string]$Updated = '',
    [switch]$RunGates,
    [switch]$Preview,
    [string]$PreviewOutputPath = ''
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\common\vibe-governance-helpers.ps1')

function Read-Text {
    param([string]$Path)
    return Get-Content -LiteralPath $Path -Raw -Encoding UTF8
}

function Write-Text {
    param(
        [string]$Path,
        [string]$Content
    )
    Write-VgoUtf8NoBomText -Path $Path -Content $Content
}

function Update-MaintenanceSection {
    param(
        [string]$Path,
        [string]$Version,
        [string]$Updated
    )

    $text = Read-Text -Path $Path
    $updatedText = $text
    $updatedText = [regex]::Replace($updatedText, '(?m)^- Version:\s*.+$', "- Version: $Version")
    $updatedText = [regex]::Replace($updatedText, '(?m)^- Updated:\s*.+$', "- Updated: $Updated")
    if ($updatedText -ne $text) {
        Write-Text -Path $Path -Content $updatedText
    }
}

function Ensure-ChangelogHeader {
    param(
        [string]$Path,
        [string]$Version,
        [string]$Updated
    )

    $text = Read-Text -Path $Path
    $header = "## v$Version ($Updated)"
    if ($text -match [regex]::Escape($header)) {
        return
    }

    $entry = @(
        $header,
        '',
        '- Release cut by `scripts/governance/release-cut.ps1`.',
        '- Fill in detailed release notes before merge.',
        ''
    ) -join "`n"

    if ($text -match '(?m)^# .+$') {
        $updated = [regex]::Replace($text, '(?m)^(# .+)$', "`$1`n`n$entry", 1)
    } else {
        $updated = "$entry`n$text"
    }
    Write-Text -Path $Path -Content $updated
}

function Get-ReleaseGateScripts {
    return @(
        'scripts/verify/vibe-version-consistency-gate.ps1',
        'scripts/verify/vibe-version-packaging-gate.ps1',
        'scripts/verify/vibe-config-parity-gate.ps1',
        'scripts/verify/vibe-nested-bundled-parity-gate.ps1',
        'scripts/verify/vibe-mirror-edit-hygiene-gate.ps1',
        'scripts/verify/vibe-bom-frontmatter-gate.ps1',
        'scripts/verify/vibe-wave40-63-board-gate.ps1',
        'scripts/verify/vibe-capability-dedup-gate.ps1',
        'scripts/verify/vibe-adaptive-routing-readiness-gate.ps1',
        'scripts/verify/vibe-upstream-value-ops-gate.ps1',
        'scripts/verify/vibe-release-install-runtime-coherence-gate.ps1',
        'scripts/verify/vibe-upstream-corpus-manifest-gate.ps1',
        'scripts/verify/vibe-wave121-upstream-mapping-gate.ps1',
        'scripts/verify/vibe-operator-preview-contract-gate.ps1',
        'scripts/verify/vibe-output-fixture-migration-stage2-gate.ps1',
        'scripts/verify/vibe-wave124-ops-cockpit-v2-gate.ps1',
        'scripts/verify/vibe-wave125-gate-family-convergence-gate.ps1',
        'scripts/verify/vibe-upstream-mirror-freshness-gate.ps1',
        'scripts/verify/vibe-docling-contract-gate.ps1',
        'scripts/verify/vibe-connector-admission-gate.ps1',
        'scripts/verify/vibe-role-pack-governance-gate.ps1',
        'scripts/verify/vibe-capability-catalog-gate.ps1',
        'scripts/verify/vibe-promotion-board-gate.ps1',
        'scripts/verify/vibe-pilot-scenarios.ps1',
        'scripts/verify/vibe-deep-extraction-pilot-gate.ps1',
        'scripts/verify/vibe-memory-runtime-v3-gate.ps1',
        'scripts/verify/vibe-mem0-softrollout-gate.ps1',
        'scripts/verify/vibe-letta-policy-conformance-gate.ps1',
        'scripts/verify/vibe-browserops-scorecard-gate.ps1',
        'scripts/verify/vibe-browserops-softrollout-gate.ps1',
        'scripts/verify/vibe-desktopops-replay-gate.ps1',
        'scripts/verify/vibe-desktopops-softrollout-gate.ps1',
        'scripts/verify/vibe-docling-contract-v2-gate.ps1',
        'scripts/verify/vibe-document-plane-benchmark-gate.ps1',
        'scripts/verify/vibe-connector-scorecard-gate.ps1',
        'scripts/verify/vibe-connector-action-ledger-gate.ps1',
        'scripts/verify/vibe-prompt-intelligence-productization-gate.ps1',
        'scripts/verify/vibe-cross-plane-task-contract-gate.ps1',
        'scripts/verify/vibe-cross-plane-replay-gate.ps1',
        'scripts/verify/vibe-promotion-scorecard-gate.ps1',
        'scripts/verify/vibe-ops-cockpit-gate.ps1',
        'scripts/verify/vibe-rollback-drill-gate.ps1',
        'scripts/verify/vibe-release-train-v2-gate.ps1',
        'scripts/verify/vibe-release-truth-consistency-gate.ps1',
        'scripts/verify/vibe-wave64-82-closure-gate.ps1',
        'scripts/verify/vibe-gate-reliability-gate.ps1',
        'scripts/verify/vibe-memory-quality-eval-gate.ps1',
        'scripts/verify/vibe-openworld-runtime-eval-gate.ps1',
        'scripts/verify/vibe-document-failure-taxonomy-gate.ps1',
        'scripts/verify/vibe-prompt-intelligence-eval-gate.ps1',
        'scripts/verify/vibe-candidate-quality-board-gate.ps1',
        'scripts/verify/vibe-role-pack-v2-gate.ps1',
        'scripts/verify/vibe-subagent-handoff-gate.ps1',
        'scripts/verify/vibe-discovery-intake-scorecard-gate.ps1',
        'scripts/verify/vibe-capability-lifecycle-gate.ps1',
        'scripts/verify/vibe-connector-sandbox-simulation-gate.ps1',
        'scripts/verify/vibe-skill-harvest-v2-gate.ps1',
        'scripts/verify/vibe-ops-dashboard-gate.ps1',
        'scripts/verify/vibe-release-evidence-bundle-gate.ps1',
        'scripts/verify/vibe-manual-apply-policy-gate.ps1',
        'scripts/verify/vibe-rollout-proposal-boundedness-gate.ps1',
        'scripts/verify/vibe-upstream-reaudit-matrix-gate.ps1',
        'scripts/verify/vibe-wave83-100-closure-gate.ps1'
    )
}

function Get-PreviewReceiptPath {
    param(
        [string]$RepoRoot,
        [string]$RequestedPath,
        [psobject]$Contract
    )

    if (-not [string]::IsNullOrWhiteSpace($RequestedPath)) {
        return $RequestedPath
    }

    $root = if ($null -ne $Contract -and $Contract.PSObject.Properties.Name -contains 'preview_output_root') {
        [string]$Contract.preview_output_root
    } else {
        'outputs/governance/preview'
    }
    return Join-Path $RepoRoot (Join-Path $root 'release-cut.json')
}

$context = Get-VgoGovernanceContext -ScriptPath $PSCommandPath -EnforceExecutionContext
$repoRoot = $context.repoRoot
$governancePath = $context.governancePath
$governance = $context.governance

$previewContractPath = Join-Path $repoRoot 'config/operator-preview-contract.json'
$previewContract = if (Test-Path -LiteralPath $previewContractPath) {
    Get-Content -LiteralPath $previewContractPath -Raw -Encoding UTF8 | ConvertFrom-Json
} else {
    $null
}

if ([string]::IsNullOrWhiteSpace($Version)) {
    $Version = [string]$governance.release.version
}
if ([string]::IsNullOrWhiteSpace($Updated)) {
    $Updated = (Get-Date -Format 'yyyy-MM-dd')
}

$maintenanceFiles = @($governance.version_markers.maintenance_files)
$changelogPath = Join-Path $repoRoot ([string]$governance.version_markers.changelog_path)
$ledgerRel = [string]$governance.logs.release_ledger_jsonl
$ledgerPath = Join-Path $repoRoot $ledgerRel
$releaseNotesDir = Join-Path $repoRoot ([string]$governance.logs.release_notes_dir)
$releaseNotePath = Join-Path $releaseNotesDir ("v{0}.md" -f $Version)
$syncScript = Join-Path $repoRoot 'scripts\governance\sync-bundled-vibe.ps1'
$gateScripts = if ($RunGates) { Get-ReleaseGateScripts } else { @() }
$head = (git -C $repoRoot rev-parse --short HEAD).Trim()

if ($Preview) {
    $previewPath = Get-PreviewReceiptPath -RepoRoot $repoRoot -RequestedPath $PreviewOutputPath -Contract $previewContract
    $previewRoot = Split-Path -Parent $previewPath
    $plannedFileActions = @(
        [ordered]@{ path = 'config/version-governance.json'; action = 'update release.version + release.updated' },
        [ordered]@{ path = [string]$governance.version_markers.changelog_path; action = 'ensure release changelog header' },
        [ordered]@{ path = $ledgerRel; action = 'append release ledger record' },
        [ordered]@{ path = (Get-VgoRelativePathPortable -BasePath $repoRoot -TargetPath $releaseNotePath); action = 'create release notes if missing' }
    ) + @($maintenanceFiles | ForEach-Object {
        [ordered]@{ path = [string]$_; action = 'update maintenance section version/updated' }
    })

    $syncPreviewPath = Join-Path $previewRoot 'sync-bundled-vibe-from-release-cut.json'
    if (Test-Path -LiteralPath $syncScript) {
        # operator-preview contract requires sync-bundled-vibe.ps1 -Preview before apply.
        & $syncScript -Preview -PreviewOutputPath $syncPreviewPath -PruneBundledExtras
        if ($LASTEXITCODE -ne 0) {
            throw 'sync-bundled-vibe preview failed'
        }
    }

    $artifact = [ordered]@{
        operator = 'release-cut'
        contract_version = if ($null -ne $previewContract -and $previewContract.PSObject.Properties.Name -contains 'contract_version') { $previewContract.contract_version } else { 1 }
        mode = 'preview'
        precheck = [ordered]@{
            repo_root = $repoRoot
            canonical_target_id = $context.canonicalTarget.id
            sync_source_target_id = $context.syncSourceTarget.id
            current_version = [string]$governance.release.version
            requested_version = $Version
            requested_updated = $Updated
            git_head = $head
            run_gates = [bool]$RunGates
        }
        preview = [ordered]@{
            generated_at = (Get-Date).ToString('s')
            planned_file_actions = $plannedFileActions
            sync_preview_receipt = if (Test-Path -LiteralPath $syncPreviewPath) { (Get-VgoRelativePathPortable -BasePath $repoRoot -TargetPath $syncPreviewPath) } else { $null }
            planned_gates = $gateScripts
        }
        postcheck = [ordered]@{
            verify_after_apply = $gateScripts
        }
    }
    Write-VgoUtf8NoBomText -Path $previewPath -Content ($artifact | ConvertTo-Json -Depth 100)
    Write-Host ("Preview receipt written: {0}" -f $previewPath) -ForegroundColor Yellow
    return
}

$governance.release.version = $Version
$governance.release.updated = $Updated
$governanceJson = $governance | ConvertTo-Json -Depth 30
Write-Text -Path $governancePath -Content $governanceJson

foreach ($rel in $maintenanceFiles) {
    $path = Join-Path $repoRoot $rel
    if (-not (Test-Path -LiteralPath $path)) {
        throw "maintenance file missing: $rel"
    }
    Update-MaintenanceSection -Path $path -Version $Version -Updated $Updated
}

Ensure-ChangelogHeader -Path $changelogPath -Version $Version -Updated $Updated

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $ledgerPath) | Out-Null
$entry = [ordered]@{
    recorded_at = (Get-Date).ToString('s')
    version = $Version
    updated = $Updated
    git_head = $head
    actor = $env:USERNAME
}
Append-VgoUtf8NoBomText -Path $ledgerPath -Content (($entry | ConvertTo-Json -Compress) + [Environment]::NewLine)

New-Item -ItemType Directory -Force -Path $releaseNotesDir | Out-Null
if (-not (Test-Path -LiteralPath $releaseNotePath)) {
    $note = @(
        "# VCO Release v$Version",
        '',
        "- Date: $Updated",
        "- Commit(base): $head",
        '',
        '## Highlights',
        '',
        '- TODO',
        '',
        '## Migration Notes',
        '',
        '- TODO'
    ) -join "`n"
    Write-Text -Path $releaseNotePath -Content $note
}

if (Test-Path -LiteralPath $syncScript) {
    & $syncScript -PruneBundledExtras
    if ($LASTEXITCODE -ne 0) {
        throw 'sync-bundled-vibe failed'
    }
}

if ($RunGates) {
    foreach ($rel in $gateScripts) {
        $gatePath = Join-Path $repoRoot $rel
        if (-not (Test-Path -LiteralPath $gatePath)) {
            throw "required gate script missing: $rel"
        }
        & $gatePath
        if ($LASTEXITCODE -ne 0) {
            throw "gate failed: $rel"
        }
    }
}

Write-Host 'Release cut complete.' -ForegroundColor Green
Write-Host ("version={0}, updated={1}" -f $Version, $Updated)

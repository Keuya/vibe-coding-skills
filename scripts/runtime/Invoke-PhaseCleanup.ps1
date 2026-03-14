param(
    [Parameter(Mandatory)] [string]$Task,
    [string]$Mode = 'interactive_governed',
    [string]$RunId = '',
    [string]$ArtifactRoot = '',
    [switch]$ExecuteGovernanceCleanup,
    [switch]$ApplyManagedNodeCleanup
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot 'VibeRuntime.Common.ps1')

$runtime = Get-VibeRuntimeContext -ScriptPath $PSCommandPath
if ([string]::IsNullOrWhiteSpace($RunId)) {
    $RunId = New-VibeRunId
}

$sessionRoot = Ensure-VibeSessionRoot -RepoRoot $runtime.repo_root -RunId $RunId -ArtifactRoot $ArtifactRoot
$cleanupResult = $null
if ($ExecuteGovernanceCleanup) {
    $cleanupArgs = @()
    if ($ApplyManagedNodeCleanup) {
        $cleanupArgs += '-ApplyManagedNodeCleanup'
    }
    $cleanupResult = Invoke-VgoPowerShellFile -ScriptPath (Join-Path $runtime.repo_root 'scripts\governance\phase-end-cleanup.ps1') -ArgumentList $cleanupArgs -NoProfile
}

$receipt = [pscustomobject]@{
    stage = 'phase_cleanup'
    run_id = $RunId
    mode = $Mode
    task = $Task
    cleanup_mode = if ($ExecuteGovernanceCleanup) { 'governance_cleanup_executed' } else { 'preview_only' }
    managed_node_cleanup_applied = [bool]$ApplyManagedNodeCleanup
    generated_at = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    cleanup_result = $cleanupResult
}

$receiptPath = Join-Path $sessionRoot 'cleanup-receipt.json'
Write-VibeJsonArtifact -Path $receiptPath -Value $receipt

[pscustomobject]@{
    run_id = $RunId
    session_root = $sessionRoot
    receipt_path = $receiptPath
    receipt = $receipt
}

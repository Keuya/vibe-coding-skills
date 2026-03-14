param(
    [Parameter(Mandatory)] [string]$Task,
    [ValidateSet('interactive_governed', 'benchmark_autonomous')] [string]$Mode = 'interactive_governed',
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

$skeleton = & (Join-Path $PSScriptRoot 'Invoke-SkeletonCheck.ps1') -Task $Task -Mode $Mode -RunId $RunId -ArtifactRoot $ArtifactRoot
$interview = & (Join-Path $PSScriptRoot 'Invoke-DeepInterview.ps1') -Task $Task -Mode $Mode -RunId $RunId -ArtifactRoot $ArtifactRoot
$requirement = & (Join-Path $PSScriptRoot 'Write-RequirementDoc.ps1') -Task $Task -Mode $Mode -RunId $RunId -IntentContractPath $interview.receipt_path -ArtifactRoot $ArtifactRoot
$plan = & (Join-Path $PSScriptRoot 'Write-XlPlan.ps1') -Task $Task -Mode $Mode -RunId $RunId -RequirementDocPath $requirement.requirement_doc_path -ArtifactRoot $ArtifactRoot
$execute = & (Join-Path $PSScriptRoot 'Invoke-PlanExecute.ps1') -Task $Task -Mode $Mode -RunId $RunId -RequirementDocPath $requirement.requirement_doc_path -ExecutionPlanPath $plan.execution_plan_path -ArtifactRoot $ArtifactRoot
$cleanup = & (Join-Path $PSScriptRoot 'Invoke-PhaseCleanup.ps1') -Task $Task -Mode $Mode -RunId $RunId -ArtifactRoot $ArtifactRoot -ExecuteGovernanceCleanup:$ExecuteGovernanceCleanup -ApplyManagedNodeCleanup:$ApplyManagedNodeCleanup

$summary = [pscustomobject]@{
    run_id = $RunId
    mode = $Mode
    task = $Task
    generated_at = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    session_root = $skeleton.session_root
    stage_order = @(
        'skeleton_check',
        'deep_interview',
        'requirement_doc',
        'xl_plan',
        'plan_execute',
        'phase_cleanup'
    )
    artifacts = [pscustomobject]@{
        skeleton_receipt = $skeleton.receipt_path
        intent_contract = $interview.receipt_path
        requirement_doc = $requirement.requirement_doc_path
        requirement_receipt = $requirement.receipt_path
        execution_plan = $plan.execution_plan_path
        execution_plan_receipt = $plan.receipt_path
        execute_receipt = $execute.receipt_path
        cleanup_receipt = $cleanup.receipt_path
    }
}

$summaryPath = Join-Path $skeleton.session_root 'runtime-summary.json'
Write-VibeJsonArtifact -Path $summaryPath -Value $summary

[pscustomobject]@{
    run_id = $RunId
    mode = $Mode
    session_root = $skeleton.session_root
    summary_path = $summaryPath
    summary = $summary
}

param(
    [Parameter(Mandatory)] [string]$Task,
    [ValidateSet('interactive_governed', 'benchmark_autonomous')] [string]$Mode = 'interactive_governed',
    [string]$RunId = '',
    [string]$ArtifactRoot = '',
    [AllowEmptyString()] [string]$GovernanceScope = '',
    [AllowEmptyString()] [string]$RootRunId = '',
    [AllowEmptyString()] [string]$ParentRunId = '',
    [AllowEmptyString()] [string]$ParentUnitId = '',
    [AllowEmptyString()] [string]$InheritedRequirementDocPath = '',
    [AllowEmptyString()] [string]$InheritedExecutionPlanPath = '',
    [string[]]$ApprovedSpecialistSkillIds = @(),
    [switch]$ExecuteGovernanceCleanup,
    [switch]$ApplyManagedNodeCleanup
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot 'VibeRuntime.Common.ps1')
. (Join-Path $PSScriptRoot 'VibeMemoryBackends.Common.ps1')
. (Join-Path $PSScriptRoot 'VibeMemoryActivation.Common.ps1')

function Wait-VibeArtifactSet {
    param(
        [Parameter(Mandatory)] [string[]]$Paths,
        [int]$TimeoutSeconds = 5,
        [int]$PollMilliseconds = 100
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    do {
        $missing = @($Paths | Where-Object { -not (Test-Path -LiteralPath $_) })
        if ($missing.Count -eq 0) {
            return [pscustomobject]@{
                ready = $true
                missing = @()
            }
        }

        Start-Sleep -Milliseconds $PollMilliseconds
    } while ((Get-Date) -lt $deadline)

    return [pscustomobject]@{
        ready = $false
        missing = @($Paths | Where-Object { -not (Test-Path -LiteralPath $_) })
    }
}

$runtime = Get-VibeRuntimeContext -ScriptPath $PSCommandPath
$Mode = Resolve-VibeRuntimeMode -Mode $Mode -DefaultMode ([string]$runtime.runtime_modes.default_mode)
if ([string]::IsNullOrWhiteSpace($RunId)) {
    $RunId = New-VibeRunId
}
$artifactBaseRoot = Get-VibeArtifactRoot -RepoRoot $runtime.repo_root -Runtime $runtime -ArtifactRoot $ArtifactRoot
$storageProjection = New-VibeWorkspaceArtifactProjection `
    -RepoRoot $runtime.repo_root `
    -Runtime $runtime `
    -ArtifactRoot $ArtifactRoot `
    -RouterTargetRoot (Resolve-VgoTargetRoot -HostId (Resolve-VgoHostId -HostId $env:VCO_HOST_ID))
$hierarchyState = Get-VibeHierarchyState `
    -GovernanceScope $GovernanceScope `
    -RunId $RunId `
    -RootRunId $RootRunId `
    -ParentRunId $ParentRunId `
    -ParentUnitId $ParentUnitId `
    -InheritedRequirementDocPath $InheritedRequirementDocPath `
    -InheritedExecutionPlanPath $InheritedExecutionPlanPath `
    -HierarchyContract $runtime.runtime_input_packet_policy.hierarchy_contract

$hierarchyArgs = @{
    GovernanceScope = [string]$hierarchyState.governance_scope
}
if (-not [string]::IsNullOrWhiteSpace([string]$hierarchyState.root_run_id)) {
    $hierarchyArgs.RootRunId = [string]$hierarchyState.root_run_id
}
if (-not [string]::IsNullOrWhiteSpace([string]$hierarchyState.parent_run_id)) {
    $hierarchyArgs.ParentRunId = [string]$hierarchyState.parent_run_id
}
if (-not [string]::IsNullOrWhiteSpace([string]$hierarchyState.parent_unit_id)) {
    $hierarchyArgs.ParentUnitId = [string]$hierarchyState.parent_unit_id
}
if (-not [string]::IsNullOrWhiteSpace([string]$hierarchyState.inherited_requirement_doc_path)) {
    $hierarchyArgs.InheritedRequirementDocPath = [string]$hierarchyState.inherited_requirement_doc_path
}
if (-not [string]::IsNullOrWhiteSpace([string]$hierarchyState.inherited_execution_plan_path)) {
    $hierarchyArgs.InheritedExecutionPlanPath = [string]$hierarchyState.inherited_execution_plan_path
}

$skeleton = & (Join-Path $PSScriptRoot 'Invoke-SkeletonCheck.ps1') -Task $Task -Mode $Mode -RunId $RunId -ArtifactRoot $ArtifactRoot
$memorySkeletonDigest = New-VibeSkeletonMemoryDigest -Runtime $runtime -Skeleton $skeleton -Task $Task -SessionRoot ([string]$skeleton.session_root)
$memorySkeletonCognee = Get-VibeCogneeReadAction -Runtime $runtime -Stage 'skeleton_check' -Task $Task -SessionRoot ([string]$skeleton.session_root)
$skeletonMemoryReads = @($memorySkeletonDigest, $memorySkeletonCognee)
$freezeArgs = @{
    Task = $Task
    Mode = $Mode
    RunId = $RunId
    ArtifactRoot = $ArtifactRoot
    ApprovedSpecialistSkillIds = $ApprovedSpecialistSkillIds
}
foreach ($key in @($hierarchyArgs.Keys)) {
    $freezeArgs[$key] = $hierarchyArgs[$key]
}
$runtimeInput = & (Join-Path $PSScriptRoot 'Freeze-RuntimeInputPacket.ps1') @freezeArgs
$interview = & (Join-Path $PSScriptRoot 'Invoke-DeepInterview.ps1') -Task $Task -Mode $Mode -RunId $RunId -ArtifactRoot $ArtifactRoot
$memoryDeepInterviewRead = Get-VibeDeepInterviewMemoryReadAction -Runtime $runtime -Task $Task -SessionRoot ([string]$skeleton.session_root)
$requirementContextReads = @($memoryDeepInterviewRead, $memorySkeletonCognee, $memorySkeletonDigest)
$requirementMemoryContext = New-VibeRequirementContextPack -Runtime $runtime -ReadActions $requirementContextReads -SessionRoot ([string]$skeleton.session_root)
$requirementArgs = @{
    Task = $Task
    Mode = $Mode
    RunId = $RunId
    IntentContractPath = $interview.receipt_path
    RuntimeInputPacketPath = $runtimeInput.packet_path
    MemoryContextPath = $requirementMemoryContext.context_path
    ArtifactRoot = $ArtifactRoot
}
foreach ($key in @($hierarchyArgs.Keys)) {
    $requirementArgs[$key] = $hierarchyArgs[$key]
}
$requirement = & (Join-Path $PSScriptRoot 'Write-RequirementDoc.ps1') @requirementArgs
$planArgs = @{
    Task = $Task
    Mode = $Mode
    RunId = $RunId
    RequirementDocPath = $requirement.requirement_doc_path
    RuntimeInputPacketPath = $runtimeInput.packet_path
    ArtifactRoot = $ArtifactRoot
}
foreach ($key in @($hierarchyArgs.Keys)) {
    $planArgs[$key] = $hierarchyArgs[$key]
}
$planArgs.InheritedRequirementDocPath = $requirement.requirement_doc_path
$memoryPlanSerena = Get-VibeSerenaReadAction -Runtime $runtime -Stage 'xl_plan' -Task $Task -SessionRoot ([string]$skeleton.session_root)
$memoryPlanCognee = Get-VibeCogneeReadAction -Runtime $runtime -Stage 'xl_plan' -Task $Task -SessionRoot ([string]$skeleton.session_root)
$xlPlanReadActions = @($memoryPlanSerena, $memoryPlanCognee)
$planMemoryContext = New-VibePlanMemoryContextPack -Runtime $runtime -ReadActions $xlPlanReadActions -SessionRoot ([string]$skeleton.session_root) -Stage 'xl_plan' -ArtifactName 'plan-context-pack.json'
$planArgs.PlanMemoryContextPath = $planMemoryContext.context_path
$plan = & (Join-Path $PSScriptRoot 'Write-XlPlan.ps1') @planArgs
$grade = if ($plan.receipt -and $plan.receipt.internal_grade) { [string]$plan.receipt.internal_grade } else { Get-VibeInternalGrade -Task $Task }
$memoryPlanExecuteRead = Get-VibeRufloReadAction -Runtime $runtime -Task $Task -SessionRoot ([string]$skeleton.session_root) -Grade $grade
$executionMemoryContext = New-VibePlanMemoryContextPack -Runtime $runtime -ReadActions @($memoryPlanExecuteRead) -SessionRoot ([string]$skeleton.session_root) -Stage 'plan_execute' -ArtifactName 'execution-context-pack.json'
$executeArgs = @{
    Task = $Task
    Mode = $Mode
    RunId = $RunId
    RequirementDocPath = $requirement.requirement_doc_path
    ExecutionPlanPath = $plan.execution_plan_path
    RuntimeInputPacketPath = $runtimeInput.packet_path
    ArtifactRoot = $ArtifactRoot
}
foreach ($key in @('GovernanceScope', 'RootRunId', 'ParentRunId', 'ParentUnitId')) {
    if ($hierarchyArgs.ContainsKey($key)) {
        $executeArgs[$key] = $hierarchyArgs[$key]
    }
}
$executeArgs.ExecutionMemoryContextPath = $executionMemoryContext.context_path
$execute = & (Join-Path $PSScriptRoot 'Invoke-PlanExecute.ps1') @executeArgs
$cleanup = & (Join-Path $PSScriptRoot 'Invoke-PhaseCleanup.ps1') -Task $Task -Mode $Mode -RunId $RunId -ArtifactRoot $ArtifactRoot -ExecuteGovernanceCleanup:$ExecuteGovernanceCleanup -ApplyManagedNodeCleanup:$ApplyManagedNodeCleanup
$memoryExecuteWrite = New-VibeExecutionMemoryWriteAction `
    -ExecutionManifestPath ([string]$execute.execution_manifest_path) `
    -SessionRoot ([string]$skeleton.session_root) `
    -Runtime $runtime `
    -RunId $RunId `
    -Task $Task `
    -Grade $grade
$memoryExecuteRufloWrite = New-VibeRufloExecutionWriteAction `
    -Runtime $runtime `
    -ExecutionManifestPath ([string]$execute.execution_manifest_path) `
    -SessionRoot ([string]$skeleton.session_root) `
    -RunId $RunId `
    -Task $Task `
    -Grade $grade
$memoryCleanupDecision = Get-VibeCleanupDecisionWriteAction `
    -RequirementDocPath ([string]$requirement.requirement_doc_path) `
    -ExecutionPlanPath ([string]$plan.execution_plan_path) `
    -Runtime $runtime `
    -SessionRoot ([string]$skeleton.session_root) `
    -Task $Task
$memoryCleanupCognee = Get-VibeCogneeCleanupWriteAction `
    -Runtime $runtime `
    -Task $Task `
    -RequirementDocPath ([string]$requirement.requirement_doc_path) `
    -ExecutionPlanPath ([string]$plan.execution_plan_path) `
    -ExecutionManifestPath ([string]$execute.execution_manifest_path) `
    -SessionRoot ([string]$skeleton.session_root)
$memoryCleanupFold = New-VibeCleanupMemoryFold `
    -RequirementDocPath ([string]$requirement.requirement_doc_path) `
    -ExecutionPlanPath ([string]$plan.execution_plan_path) `
    -ExecutionManifestPath ([string]$execute.execution_manifest_path) `
    -CleanupReceiptPath ([string]$cleanup.receipt_path) `
    -SessionRoot ([string]$skeleton.session_root)
$memoryActivation = New-VibeMemoryActivationReport `
    -Runtime $runtime `
    -RunId $RunId `
    -SessionRoot ([string]$skeleton.session_root) `
    -SkeletonReadActions $skeletonMemoryReads `
    -DeepInterviewReadActions @($memoryDeepInterviewRead) `
    -RequirementContextPack $requirementMemoryContext `
    -XlPlanReadActions $xlPlanReadActions `
    -PlanExecuteReadActions @($memoryPlanExecuteRead) `
    -PlanExecuteWriteActions @($memoryExecuteWrite, $memoryExecuteRufloWrite) `
    -CleanupWriteActions @($memoryCleanupDecision, $memoryCleanupCognee) `
    -CleanupFoldAction $memoryCleanupFold
$deliveryAcceptanceReportPath = Join-Path $skeleton.session_root 'delivery-acceptance-report.json'
$deliveryAcceptanceMarkdownPath = Join-Path $skeleton.session_root 'delivery-acceptance-report.md'

$artifactReadiness = Wait-VibeArtifactSet -Paths @(
    [string]$skeleton.receipt_path,
    [string]$runtimeInput.packet_path,
    [string]$interview.receipt_path,
    [string]$requirement.requirement_doc_path,
    [string]$requirement.receipt_path,
    [string]$plan.execution_plan_path,
    [string]$plan.receipt_path,
    [string]$execute.receipt_path,
    [string]$execute.execution_manifest_path,
    [string]$execute.execution_topology_path,
    [string]$execute.benchmark_proof_manifest_path,
    [string]$cleanup.receipt_path,
    [string]$deliveryAcceptanceReportPath,
    [string]$memoryActivation.report_path,
    [string]$memoryActivation.markdown_path
)

if (-not $artifactReadiness.ready) {
    throw ("Governed runtime returned before critical artifacts were durable. Missing: {0}" -f (@($artifactReadiness.missing) -join ', '))
}

$summaryArtifacts = New-VibeRuntimeSummaryArtifactProjection `
    -SkeletonReceiptPath ([string]$skeleton.receipt_path) `
    -RuntimeInputPacketPath ([string]$runtimeInput.packet_path) `
    -IntentContractPath ([string]$interview.receipt_path) `
    -RequirementDocPath ([string]$requirement.requirement_doc_path) `
    -RequirementReceiptPath ([string]$requirement.receipt_path) `
    -ExecutionPlanPath ([string]$plan.execution_plan_path) `
    -ExecutionPlanReceiptPath ([string]$plan.receipt_path) `
    -ExecuteReceiptPath ([string]$execute.receipt_path) `
    -ExecutionManifestPath ([string]$execute.execution_manifest_path) `
    -ExecutionTopologyPath ([string]$execute.execution_topology_path) `
    -BenchmarkProofManifestPath ([string]$execute.benchmark_proof_manifest_path) `
    -CleanupReceiptPath ([string]$cleanup.receipt_path) `
    -DeliveryAcceptanceReportPath ([string]$deliveryAcceptanceReportPath) `
    -DeliveryAcceptanceMarkdownPath ([string]$deliveryAcceptanceMarkdownPath) `
    -MemoryActivationReportPath ([string]$memoryActivation.report_path) `
    -MemoryActivationMarkdownPath ([string]$memoryActivation.markdown_path)
$relativeArtifacts = New-VibeRuntimeSummaryRelativeArtifactProjection -BasePath $artifactBaseRoot -Artifacts $summaryArtifacts

$deliveryAcceptanceReport = if (Test-Path -LiteralPath $deliveryAcceptanceReportPath) {
    Get-Content -LiteralPath $deliveryAcceptanceReportPath -Raw -Encoding UTF8 | ConvertFrom-Json
} else {
    $null
}

$summary = New-VibeRuntimeSummaryProjection `
    -RunId $RunId `
    -Mode $Mode `
    -Task $Task `
    -ArtifactRoot $artifactBaseRoot `
    -SessionRoot ([string]$skeleton.session_root) `
    -HierarchyState $hierarchyState `
    -Artifacts $summaryArtifacts `
    -RelativeArtifacts $relativeArtifacts `
    -StorageProjection $storageProjection `
    -MemoryActivationReport $memoryActivation.report `
    -DeliveryAcceptanceReport $deliveryAcceptanceReport

$summaryPath = Join-Path $skeleton.session_root 'runtime-summary.json'
Write-VibeJsonArtifact -Path $summaryPath -Value $summary

[pscustomobject]@{
    run_id = $RunId
    mode = $Mode
    session_root = $skeleton.session_root
    summary_path = $summaryPath
    summary = $summary
}

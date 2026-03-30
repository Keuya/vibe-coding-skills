param(
  [Parameter(Mandatory = $true)]
  [string]$RepoRoot,
  [Parameter(Mandatory = $true)]
  [string]$TargetRoot,
  [Parameter(Mandatory = $true)]
  [string]$HostId,
  [ValidateSet("minimal", "full")]
  [string]$Profile = "full",
  [switch]$Preview,
  [switch]$PurgeEmptyDirs,
  [switch]$StrictOwnedOnly
)
$ErrorActionPreference = "Stop"
. (Join-Path $RepoRoot 'scripts\common\vibe-governance-helpers.ps1')

$pythonInvocation = Get-VgoPythonCommand
$scriptPath = Join-Path $RepoRoot 'scripts\uninstall\uninstall_vgo_adapter.py'
$argsList = @($pythonInvocation.prefix_arguments)
$argsList += @(
  $scriptPath,
  '--repo-root', $RepoRoot,
  '--target-root', $TargetRoot,
  '--host', $HostId,
  '--profile', $Profile
)
if ($Preview) { $argsList += '--preview' }
if ($PurgeEmptyDirs) { $argsList += '--purge-empty-dirs' }
if ($StrictOwnedOnly) { $argsList += '--strict-owned-only' }

& $pythonInvocation.host_path @argsList
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

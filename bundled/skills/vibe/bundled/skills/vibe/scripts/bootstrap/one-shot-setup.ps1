param(
    [ValidateSet('minimal', 'full')]
    [string]$Profile = 'full',
    [string]$HostId = '',
    [string]$TargetRoot = '',
    [switch]$SkipExternalInstall,
    [switch]$StrictOffline,
    [switch]$SyncUserEnv,
    [Alias('OpenAIBaseUrl')]
    [string]$IntentAdviceBaseUrl = '',
    [Alias('OpenAIApiKey')]
    [string]$IntentAdviceApiKey = ''
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Test-NonEmptyString {
    param([AllowNull()][string]$Value)
    return (-not [string]::IsNullOrWhiteSpace($Value))
}

function Test-IsInteractiveBootstrap {
    try {
        return [Environment]::UserInteractive -and -not [Console]::IsInputRedirected -and -not [Console]::IsOutputRedirected
    } catch {
        return $true
    }
}

function Prompt-VgoHostId {
    while ($true) {
        Write-Host 'Select the install target before bootstrap:'
        Write-Host '  1) codex        - strongest governed lane'
        Write-Host '  2) claude-code  - supported install/use path'
        Write-Host '  3) cursor       - supported install/use path'
        Write-Host '  4) windsurf     - supported path + runtime adapter'
        Write-Host '  5) openclaw     - preview runtime-core adapter'
        $choice = [string](Read-Host 'Install into which agent? [1-5]')
        $normalized = $choice.Trim().ToLowerInvariant()
        switch ($normalized) {
            '1' { return 'codex' }
            'codex' { return 'codex' }
            '2' { return 'claude-code' }
            'claude' { return 'claude-code' }
            'claude-code' { return 'claude-code' }
            '3' { return 'cursor' }
            'cursor' { return 'cursor' }
            '4' { return 'windsurf' }
            'windsurf' { return 'windsurf' }
            '5' { return 'openclaw' }
            'openclaw' { return 'openclaw' }
            default { Write-Warning "Unsupported choice: $choice. Enter 1, 2, 3, 4, 5, or a supported host name." }
        }
    }
}

. (Join-Path $PSScriptRoot '..\common\vibe-governance-helpers.ps1')
. (Join-Path $PSScriptRoot '..\common\Resolve-VgoAdapter.ps1')
if (-not (Test-NonEmptyString -Value $HostId)) {
    if (Test-NonEmptyString -Value $env:VCO_HOST_ID) {
        $HostId = $env:VCO_HOST_ID
    } elseif (Test-IsInteractiveBootstrap) {
        $HostId = Prompt-VgoHostId
    } else {
        throw 'No host was provided for one-shot bootstrap. Pass -HostId codex|claude-code|cursor|windsurf|openclaw when running non-interactively.'
    }
}
$HostId = Resolve-VgoHostId -HostId $HostId
$TargetRoot = Resolve-VgoTargetRoot -TargetRoot $TargetRoot -HostId $HostId
Assert-VgoTargetRootMatchesHostIntent -TargetRoot $TargetRoot -HostId $HostId
$repoRoot = Resolve-VgoRepoRoot -StartPath $PSCommandPath
$Adapter = Resolve-VgoAdapterDescriptor -RepoRoot $repoRoot -HostId $HostId

function Get-ExistingSettingEnvValue {
    param(
        [Parameter(Mandatory)] [string]$CodexRoot,
        [Parameter(Mandatory)] [string]$Name
    )

    $settingsPath = Join-Path $CodexRoot 'settings.json'
    if (-not (Test-Path -LiteralPath $settingsPath)) {
        return $null
    }

    try {
        $settings = Get-Content -LiteralPath $settingsPath -Raw -Encoding UTF8 | ConvertFrom-Json
    } catch {
        return $null
    }

    if ($null -eq $settings -or -not ($settings.PSObject.Properties.Name -contains 'env') -or $null -eq $settings.env) {
        return $null
    }

    if ($settings.env.PSObject.Properties.Name -contains $Name) {
        $value = [string]$settings.env.$Name
        if (Test-NonEmptyString -Value $value) {
            return $value
        }
    }

    return $null
}

$installPath = Join-Path $repoRoot 'install.ps1'
$checkPath = Join-Path $repoRoot 'check.ps1'
$materializePath = Join-Path $repoRoot 'scripts\setup\materialize-codex-mcp-profile.ps1'
$persistOpenAiPath = Join-Path $repoRoot 'scripts\setup\persist-codex-openai-env.ps1'
$syncEnvPath = Join-Path $repoRoot 'scripts\setup\sync-codex-settings-to-user-env.ps1'
$claudeScaffoldPath = Join-Path $repoRoot 'scripts\bootstrap\scaffold-claude-preview.ps1'

Write-Host '=== VCO One-Shot Setup ===' -ForegroundColor Cyan
Write-Host ("Repo root           : {0}" -f $repoRoot)
Write-Host ("Host                : {0}" -f $HostId)
Write-Host ("Mode                : {0}" -f $Adapter.bootstrap_mode)
Write-Host ("Target root         : {0}" -f $TargetRoot)
Write-Host ("Profile             : {0}" -f $Profile)
Write-Host ("StrictOffline       : {0}" -f ([bool]$StrictOffline))
Write-Host ("SkipExternalInstall : {0}" -f ([bool]$SkipExternalInstall))
Write-Host ("SyncUserEnv         : {0}" -f ([bool]$SyncUserEnv))

if (-not $SkipExternalInstall) {
    Write-Host 'External CLI install is enabled. npm-based steps such as claude-flow may take several minutes, and deprecated warnings are advisory unless the command exits non-zero.' -ForegroundColor DarkYellow
}

$installArgs = @{
    Profile = $Profile
    HostId = $HostId
    TargetRoot = $TargetRoot
}
if (-not $SkipExternalInstall) {
    $installArgs.InstallExternal = $true
}
if ($StrictOffline) {
    $installArgs.StrictOffline = $true
}

Write-Host ''
Write-Host '[1/5] Installing adapter payload...' -ForegroundColor Yellow
& $installPath @installArgs

switch ([string]$Adapter.bootstrap_mode) {
    'governed' {
        $existingIntentAdviceKey = Get-ExistingSettingEnvValue -CodexRoot $TargetRoot -Name 'VCO_INTENT_ADVICE_API_KEY'
        $hasIntentAdviceSeed = (Test-NonEmptyString -Value $IntentAdviceApiKey) -or (Test-NonEmptyString -Value $env:VCO_INTENT_ADVICE_API_KEY)
        if ($hasIntentAdviceSeed) {
            Write-Host '[2/5] Seeding intent advice settings into target settings.json...' -ForegroundColor Yellow
            $intentAdviceArgs = @{ CodexRoot = $TargetRoot }
            if (Test-NonEmptyString -Value $IntentAdviceBaseUrl) { $intentAdviceArgs.BaseUrl = $IntentAdviceBaseUrl }
            if (Test-NonEmptyString -Value $IntentAdviceApiKey) { $intentAdviceArgs.ApiKey = $IntentAdviceApiKey }
            & $persistOpenAiPath @intentAdviceArgs
        } elseif (Test-NonEmptyString -Value $existingIntentAdviceKey) {
            Write-Host '[2/5] Intent advice settings already exist in target settings.json; keeping current value.' -ForegroundColor DarkGray
        } else {
            Write-Warning 'VCO_INTENT_ADVICE_API_KEY not provided and not present in the current environment. Built-in intent advice readiness will remain pending.'
        }

        Write-Host '[3/5] Built-in AI governance now uses separated functional keys: intent advice uses VCO_INTENT_ADVICE_* and vector diff embeddings use VCO_VECTOR_DIFF_*.' -ForegroundColor DarkGray

        if ($SyncUserEnv) {
            Write-Host '[4/5] Syncing configured settings.json env values into the user environment...' -ForegroundColor Yellow
            & $syncEnvPath -CodexRoot $TargetRoot -Target All -Scope User
        } else {
            Write-Host '[4/5] User environment sync skipped (pass -SyncUserEnv if you want registry env sync).' -ForegroundColor DarkGray
        }

        Write-Host '[5/5] Materializing MCP profile and running deep health check...' -ForegroundColor Yellow
        & $materializePath -TargetRoot $TargetRoot -Force | Out-Null
        & $checkPath -Profile $Profile -HostId $HostId -TargetRoot $TargetRoot -Deep
    }
    'preview-guidance' {
        if ($HostId -eq 'claude-code') {
            Write-Host '[2/5] Hook installation is frozen for Claude Code because of compatibility issues.' -ForegroundColor Yellow
            & $claudeScaffoldPath -RepoRoot $repoRoot -TargetRoot $TargetRoot -Force | Out-Null
        } else {
            Write-Host ("[2/5] Host-specific scaffold is currently unavailable for '{0}'." -f $HostId) -ForegroundColor Yellow
        }
        Write-Host '[3/5] No hook files or extra preview settings were installed into the target root.' -ForegroundColor DarkGray
        Write-Host ("[4/5] Provider settings remain host-managed for '{0}'. Configure built-in intent advice with VCO_INTENT_ADVICE_API_KEY / VCO_INTENT_ADVICE_BASE_URL / VCO_INTENT_ADVICE_MODEL, and configure vector diff embeddings separately with VCO_VECTOR_DIFF_API_KEY / VCO_VECTOR_DIFF_BASE_URL / VCO_VECTOR_DIFF_MODEL. Do not paste API keys into chat." -f $HostId) -ForegroundColor DarkGray
        Write-Host '[5/5] Running supported-path health check...' -ForegroundColor Yellow
        & $checkPath -Profile $Profile -HostId $HostId -TargetRoot $TargetRoot -Deep
    }
    'runtime-core' {
        Write-Host '[2/5] Runtime-adapter path does not materialize host settings.' -ForegroundColor DarkGray
        Write-Host '[3/5] Runtime-adapter path does not seed provider settings. Configure built-in intent advice with VCO_INTENT_ADVICE_API_KEY / VCO_INTENT_ADVICE_BASE_URL / VCO_INTENT_ADVICE_MODEL, and configure vector diff embeddings separately with VCO_VECTOR_DIFF_API_KEY / VCO_VECTOR_DIFF_BASE_URL / VCO_VECTOR_DIFF_MODEL. Do not paste secrets into chat.' -ForegroundColor DarkGray
        Write-Host '[4/5] User environment sync skipped for the runtime-adapter path.' -ForegroundColor DarkGray
        Write-Host '[5/5] Running runtime-adapter health check...' -ForegroundColor Yellow
        & $checkPath -Profile $Profile -HostId $HostId -TargetRoot $TargetRoot -Deep
    }
    default {
        throw \"Unsupported adapter bootstrap mode: $($Adapter.bootstrap_mode)\"
    }
}

Write-Host ''
Write-Host 'One-shot setup completed.' -ForegroundColor Green
$checkShellPath = Get-VgoPowerShellCommand
$checkShellLeaf = [System.IO.Path]::GetFileName($checkShellPath).ToLowerInvariant()
$checkCommandParts = @($checkShellLeaf, '-NoProfile')
if ($checkShellLeaf -like 'powershell*') {
    $checkCommandParts += @('-ExecutionPolicy', 'Bypass')
}
$checkCommandParts += @('-File', $checkPath, '-Profile', $Profile, '-HostId', $HostId, '-TargetRoot', $TargetRoot, '-Deep')
$checkCommand = ($checkCommandParts | ForEach-Object {
    $text = [string]$_
    if ($text -match '\s') {
        '"' + ($text -replace '"', '\"') + '"'
    } else {
        $text
    }
}) -join ' '
Write-Host ('- Re-run deep doctor anytime with: {0}' -f $checkCommand)
if ($Adapter.bootstrap_mode -eq 'governed') {
    Write-Host ('- MCP active file: {0}' -f (Join-Path $TargetRoot 'mcp\servers.active.json'))
}
Write-Host ('- Doctor artifacts: {0}' -f (Join-Path $repoRoot 'outputs\verify'))

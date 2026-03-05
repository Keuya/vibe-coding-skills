param(
    [string]$OutputDir = "",
    [switch]$CompareInstalled,
    [string]$InstalledPluginsPath = "",
    [switch]$NoNpm,
    [switch]$NoGitHub,
    [int]$MaxRepos = 0
)

$ErrorActionPreference = "Stop"

function Read-JsonFile {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        throw "JSON file not found: $Path"
    }
    return Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json
}

function Write-TextFile {
    param(
        [string]$Path,
        [string]$Content
    )
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Path) | Out-Null
    Set-Content -LiteralPath $Path -Value $Content -Encoding UTF8
}

function Normalize-GitHubRepoUrl {
    param([string]$Url)
    if ([string]::IsNullOrWhiteSpace($Url)) { return "" }
    $u = $Url.Trim()
    $u = $u -replace "\.git$", ""
    $u = $u.TrimEnd("/")
    return $u
}

function Parse-GitHubOwnerRepo {
    param([string]$RepoUrl)
    $u = Normalize-GitHubRepoUrl -Url $RepoUrl
    if ($u -notmatch "^https://github\.com/([^/]+)/([^/]+)$") { return $null }
    return [pscustomobject]@{
        owner = $Matches[1]
        repo = $Matches[2]
    }
}

function Get-GitHubHeaders {
    $token = ""
    if ($env:GITHUB_TOKEN) { $token = $env:GITHUB_TOKEN }
    elseif ($env:GH_TOKEN) { $token = $env:GH_TOKEN }

    $headers = @{
        "Accept"               = "application/vnd.github+json"
        "X-GitHub-Api-Version" = "2022-11-28"
        "User-Agent"           = "vco-skills-codex-upstream-audit"
    }
    if (-not [string]::IsNullOrWhiteSpace($token)) {
        $headers["Authorization"] = "Bearer $token"
    }
    return $headers
}

function Try-InvokeRestJson {
    param(
        [string]$Url,
        [hashtable]$Headers = @{}
    )
    try {
        return Invoke-RestMethod -Uri $Url -Headers $Headers -Method Get -ErrorAction Stop
    } catch {
        return $null
    }
}

function Try-GetInstalledPluginEntry {
    param(
        [object]$Installed,
        [string]$PluginId
    )
    if (-not $Installed) { return $null }
    if (-not $Installed.plugins) { return $null }

    $prop = $Installed.plugins.PSObject.Properties | Where-Object { $_.Name -eq $PluginId } | Select-Object -First 1
    if (-not $prop) { return $null }
    $entries = @($prop.Value)
    if ($entries.Count -eq 0) { return $null }
    $userEntry = $entries | Where-Object { $_.scope -eq "user" } | Select-Object -First 1
    if ($userEntry) { return $userEntry }
    return $entries[0]
}

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")

$governancePath = Join-Path $repoRoot "config\version-governance.json"
$governance = $null
$vcoVersion = ""
if (Test-Path -LiteralPath $governancePath) {
    $governance = Read-JsonFile -Path $governancePath
    $vcoVersion = [string]$governance.release.version
}

if ([string]::IsNullOrWhiteSpace($OutputDir)) {
    $OutputDir = Join-Path $repoRoot "outputs\upstream-audit"
}
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

$manifestPath = Join-Path $repoRoot "config\plugins-manifest.upstream.json"
$lockPath = Join-Path $repoRoot "config\upstream-lock.json"

$manifest = $null
if (Test-Path -LiteralPath $manifestPath) {
    $manifest = Read-JsonFile -Path $manifestPath
}
$lock = $null
if (Test-Path -LiteralPath $lockPath) {
    $lock = Read-JsonFile -Path $lockPath
}

$pluginEntries = @()
if ($manifest -and $manifest.plugins) {
    foreach ($tier in @("core", "recommended")) {
        $items = @($manifest.plugins.$tier)
        foreach ($p in $items) {
            if (-not $p.repo) { continue }
            $pluginEntries += [pscustomobject]@{
                source   = "plugins-manifest.$tier"
                id       = [string]$p.id
                name     = [string]$p.id
                repo_url = Normalize-GitHubRepoUrl -Url ([string]$p.repo)
                required = [bool]$p.required
            }
        }
    }
    $ext = @($manifest.plugins.external)
    foreach ($p in $ext) {
        if (-not $p.repo) { continue }
        $pluginEntries += [pscustomobject]@{
            source   = "plugins-manifest.external"
            id       = [string]$p.name
            name     = [string]$p.name
            repo_url = Normalize-GitHubRepoUrl -Url ([string]$p.repo)
            required = [bool]$p.required
        }
    }
}

$lockEntries = @()
if ($lock -and $lock.dependencies) {
    foreach ($d in @($lock.dependencies)) {
        if (-not $d.upstream_repo) { continue }
        $lockEntries += [pscustomobject]@{
            source   = "upstream-lock"
            id       = [string]$d.id
            name     = [string]$d.id
            repo_url = Normalize-GitHubRepoUrl -Url ([string]$d.upstream_repo)
            ref      = [string]$d.upstream_ref
            mode     = [string]$d.integration_mode
        }
    }
}

$allEntries = @($pluginEntries + $lockEntries) | Where-Object { -not [string]::IsNullOrWhiteSpace($_.repo_url) }

$repoToSources = @{}
foreach ($e in $allEntries) {
    if (-not $e.repo_url.StartsWith("https://github.com/")) { continue }
    if (-not $repoToSources.ContainsKey($e.repo_url)) {
        $repoToSources[$e.repo_url] = New-Object System.Collections.Generic.List[object]
    }
    $repoToSources[$e.repo_url].Add($e) | Out-Null
}

$installed = $null
if ($CompareInstalled) {
    if ([string]::IsNullOrWhiteSpace($InstalledPluginsPath)) {
        $InstalledPluginsPath = Join-Path $env:USERPROFILE ".claude\plugins\installed_plugins.json"
    }
    if (Test-Path -LiteralPath $InstalledPluginsPath) {
        $installed = Read-JsonFile -Path $InstalledPluginsPath
    }
}

$githubHeaders = Get-GitHubHeaders
$rows = New-Object System.Collections.Generic.List[object]
$errors = New-Object System.Collections.Generic.List[string]

$repoUrls = @($repoToSources.Keys | Sort-Object)
if ($MaxRepos -gt 0) {
    $repoUrls = $repoUrls | Select-Object -First $MaxRepos
}

foreach ($repoUrl in $repoUrls) {
    $parsed = Parse-GitHubOwnerRepo -RepoUrl $repoUrl
    if (-not $parsed) {
        $errors.Add("Unparseable GitHub repo URL: $repoUrl") | Out-Null
        continue
    }

    $owner = $parsed.owner
    $name = $parsed.repo

    $repoInfo = $null
    $releaseInfo = $null
    $tagInfo = $null
    $headInfo = $null

    if (-not $NoGitHub) {
        $repoInfo = Try-InvokeRestJson -Url ("https://api.github.com/repos/{0}/{1}" -f $owner, $name) -Headers $githubHeaders
        if ($repoInfo) {
            $defaultBranch = [string]$repoInfo.default_branch
            $headInfo = Try-InvokeRestJson -Url ("https://api.github.com/repos/{0}/{1}/commits/{2}" -f $owner, $name, $defaultBranch) -Headers $githubHeaders
        }
        $releaseInfo = Try-InvokeRestJson -Url ("https://api.github.com/repos/{0}/{1}/releases/latest" -f $owner, $name) -Headers $githubHeaders
        $tagInfo = Try-InvokeRestJson -Url ("https://api.github.com/repos/{0}/{1}/tags?per_page=1&page=1" -f $owner, $name) -Headers $githubHeaders
    }

    $latestTag = ""
    if ($tagInfo -and $tagInfo.Count -gt 0) {
        $latestTag = [string]$tagInfo[0].name
    }

    $latestRelease = ""
    $latestReleaseDate = ""
    if ($releaseInfo -and $releaseInfo.tag_name) {
        $latestRelease = [string]$releaseInfo.tag_name
        $latestReleaseDate = [string]$releaseInfo.published_at
    }

    $headSha = ""
    $headDate = ""
    if ($headInfo -and $headInfo.sha) {
        $headSha = [string]$headInfo.sha
        if ($headInfo.commit -and $headInfo.commit.committer -and $headInfo.commit.committer.date) {
            $headDate = [string]$headInfo.commit.committer.date
        }
    }

    $pushedAt = ""
    $defaultBranch = ""
    if ($repoInfo) {
        $defaultBranch = [string]$repoInfo.default_branch
        $pushedAt = [string]$repoInfo.pushed_at
    }

    $sourceLabels = @($repoToSources[$repoUrl] | ForEach-Object { $_.id } | Sort-Object -Unique)
    $sourceLabelText = ($sourceLabels -join ", ")

    $installedText = ""
    if ($CompareInstalled) {
        $installedEntries = @()
        foreach ($src in $repoToSources[$repoUrl]) {
            if (-not $src.source.StartsWith("plugins-manifest.")) { continue }
            if ([string]::IsNullOrWhiteSpace($src.id)) { continue }
            $entry = Try-GetInstalledPluginEntry -Installed $installed -PluginId $src.id
            if (-not $entry) { continue }
            $ver = [string]$entry.version
            $sha = [string]$entry.gitCommitSha
            if (-not [string]::IsNullOrWhiteSpace($sha)) {
                $sha = $sha.Substring(0, [Math]::Min(7, $sha.Length))
            }
            $installedEntries += ("{0}={1}({2})" -f $src.id, $ver, $sha)
        }
        if ($installedEntries.Count -gt 0) {
            $installedText = ($installedEntries -join "; ")
        }
    }

    $rows.Add([pscustomobject]@{
        repo_url            = $repoUrl
        sources             = $sourceLabelText
        latest_release      = $latestRelease
        latest_release_date = $latestReleaseDate
        latest_tag          = $latestTag
        default_branch      = $defaultBranch
        head_sha            = $headSha
        head_date           = $headDate
        pushed_at           = $pushedAt
        installed           = $installedText
    }) | Out-Null
}

$npmRows = New-Object System.Collections.Generic.List[object]
if (-not $NoNpm) {
    $npmPackages = @("claude-flow")
    foreach ($pkg in $npmPackages) {
        $doc = Try-InvokeRestJson -Url ("https://registry.npmjs.org/{0}" -f $pkg) -Headers @{}
        if (-not $doc) { continue }
        $latest = ""
        if ($doc."dist-tags" -and $doc."dist-tags".latest) {
            $latest = [string]$doc."dist-tags".latest
        }
        $modified = ""
        if ($doc.time -and $latest -and $doc.time.$latest) {
            $modified = [string]$doc.time.$latest
        } elseif ($doc.time -and $doc.time.modified) {
            $modified = [string]$doc.time.modified
        }
        $npmRows.Add([pscustomobject]@{
            package  = $pkg
            latest   = $latest
            modified = $modified
        }) | Out-Null
    }
}

$now = Get-Date
$timestamp = $now.ToString("yyyyMMdd-HHmmss")
$reportPath = Join-Path $OutputDir ("upstream-audit_{0}.md" -f $timestamp)

$lines = New-Object System.Collections.Generic.List[string]
$lines.Add("# VCO Upstream Audit") | Out-Null
if (-not [string]::IsNullOrWhiteSpace($vcoVersion)) {
    $lines.Add("") | Out-Null
    $lines.Add(("- VCO version: {0}" -f $vcoVersion)) | Out-Null
}
$lines.Add(("- Generated: {0}" -f $now.ToString("s"))) | Out-Null
$lines.Add(('- Repo root: `{0}`' -f $repoRoot)) | Out-Null
if ($CompareInstalled -and -not [string]::IsNullOrWhiteSpace($InstalledPluginsPath)) {
    $lines.Add(('- Installed plugins: `{0}`' -f $InstalledPluginsPath)) | Out-Null
}

$lines.Add("") | Out-Null
$lines.Add("## GitHub Repos") | Out-Null
$lines.Add("") | Out-Null
$lines.Add("| Repo | Sources | Latest Release | Release Date | Latest Tag | Branch | Head | Pushed | Installed |") | Out-Null
$lines.Add("|---|---|---|---|---|---|---|---|---|") | Out-Null

foreach ($r in $rows) {
    $headShort = ""
    if ($r.head_sha) { $headShort = $r.head_sha.Substring(0, [Math]::Min(7, $r.head_sha.Length)) }
    $lines.Add((
            "| {0} | {1} | {2} | {3} | {4} | {5} | {6} {7} | {8} | {9} |" -f
            $r.repo_url,
            ($r.sources -replace "\|", "\\|"),
            ($r.latest_release -replace "\|", "\\|"),
            ($r.latest_release_date -replace "\|", "\\|"),
            ($r.latest_tag -replace "\|", "\\|"),
            ($r.default_branch -replace "\|", "\\|"),
            $headShort,
            ($r.head_date -replace "\|", "\\|"),
            ($r.pushed_at -replace "\|", "\\|"),
            (($r.installed -replace "\|", "\\|") -replace "`n", " ")
        )) | Out-Null
}

if ($npmRows.Count -gt 0) {
    $lines.Add("") | Out-Null
    $lines.Add("## npm Packages") | Out-Null
    $lines.Add("") | Out-Null
    $lines.Add("| Package | Latest | Modified |") | Out-Null
    $lines.Add("|---|---|---|") | Out-Null
    foreach ($p in $npmRows) {
        $lines.Add((
                "| {0} | {1} | {2} |" -f
                ($p.package -replace "\|", "\\|"),
                ($p.latest -replace "\|", "\\|"),
                ($p.modified -replace "\|", "\\|")
            )) | Out-Null
    }
}

if ($errors.Count -gt 0) {
    $lines.Add("") | Out-Null
    $lines.Add("## Errors") | Out-Null
    $lines.Add("") | Out-Null
    foreach ($e in $errors) {
        $lines.Add(("- {0}" -f $e)) | Out-Null
    }
}

Write-TextFile -Path $reportPath -Content ($lines -join "`n")
Write-Host "Upstream audit report written:" -ForegroundColor Green
Write-Host $reportPath

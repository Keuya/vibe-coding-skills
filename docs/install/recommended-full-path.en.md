# Install Path: Advanced Host / Lane Reference

> Most users should start with:
>
> - [`one-click-install-release-copy.en.md`](./one-click-install-release-copy.en.md)
> - [`manual-copy-install.en.md`](./manual-copy-install.en.md)

This document explains the current real support boundary and the concrete commands per host.

## Current Supported Surface

| Host | Mode | Default root | Current wording |
| --- | --- | --- | --- |
| `codex` | governed | `~/.codex` | strongest supported path today |
| `claude-code` | preview guidance | `~/.claude` | preview guidance, not full closure |
| `cursor` | preview guidance | `~/.cursor` | preview guidance, not full closure |
| `windsurf` | preview runtime-core | `~/.codeium/windsurf` | runtime-core preview, not full closure |

`TargetRoot` is only a path.
`HostId` / `--host` decides host semantics.

## Recommended Commands

Default full install:

### Codex

```powershell
pwsh -File .\scripts\bootstrap\one-shot-setup.ps1 -HostId codex -Profile full
pwsh -File .\check.ps1 -HostId codex -Profile full -Deep
```

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host codex --profile full
bash ./check.sh --host codex --profile full --deep
```

### Claude Code

```powershell
pwsh -File .\scripts\bootstrap\one-shot-setup.ps1 -HostId claude-code -Profile full
pwsh -File .\check.ps1 -HostId claude-code -Profile full -Deep
```

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host claude-code --profile full
bash ./check.sh --host claude-code --profile full --deep
```

### Cursor

```powershell
pwsh -File .\scripts\bootstrap\one-shot-setup.ps1 -HostId cursor -Profile full
pwsh -File .\check.ps1 -HostId cursor -Profile full -Deep
```

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host cursor --profile full
bash ./check.sh --host cursor --profile full --deep
```

### Windsurf

```powershell
pwsh -File .\scripts\bootstrap\one-shot-setup.ps1 -HostId windsurf -Profile full
pwsh -File .\check.ps1 -HostId windsurf -Profile full -Deep
```

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host windsurf --profile full
bash ./check.sh --host windsurf --profile full --deep
```

If you want the “Framework Only + Customizable Governance” variant, replace `full` with `minimal`.

## Upgrade Flow

If you still have a local checkout, update the repo first and then rerun the same commands:

```bash
git pull origin main
```

If you follow tagged releases instead of `main`, use:

```bash
git fetch --tags --force
git checkout vX.Y.Z
```

## Boundaries That Must Stay Explicit

### Codex

- this is the governed path
- hooks remain frozen; that is not an install failure
- `OPENAI_*` only covers Codex base online provider access
- `VCO_AI_PROVIDER_*` is the optional governance-AI online layer

### Claude Code

- this is preview guidance
- it does not overwrite the real `~/.claude/settings.json`
- hooks remain frozen; that is not an install failure

### Cursor

- this is preview guidance
- it does not overwrite the real `~/.cursor/settings.json`
- the repo does not currently take over Cursor host-native provider, MCP, or hook closure

### Windsurf

- this is preview runtime-core
- the default root is `~/.codeium/windsurf`
- the repo currently owns only shared runtime payload plus optional materialization of `mcp_config.json` and `global_workflows/`
- do not describe it as completed login, account, provider, plugin, or workspace-native closure

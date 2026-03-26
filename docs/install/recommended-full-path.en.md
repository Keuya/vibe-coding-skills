# Install Path: Advanced Host / Lane Reference

> Most users should start with the three main install paths:
>
> - [`one-click-install-release-copy.en.md`](./one-click-install-release-copy.en.md)
> - [`manual-copy-install.en.md`](./manual-copy-install.en.md)
> - [`opencode-path.en.md`](./opencode-path.en.md)

This document exists to explain the current real support boundary.

## Current Supported Surface

The current public install surface covers three hosts:

- `codex`
- `claude-code`
- `opencode`

Within that scope:

- `codex`: recommended path
- `claude-code`: preview guidance path
- `opencode`: preview adapter path

`TargetRoot` is only the install path.
`HostId` / `--host` is what decides host semantics.

## Recommended Commands

### Codex

```powershell
pwsh -File .\scripts\bootstrap\one-shot-setup.ps1 -HostId codex
pwsh -File .\check.ps1 -HostId codex -Profile full -Deep
```

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host codex
bash ./check.sh --host codex --profile full --deep
```

### Claude Code

```powershell
pwsh -File .\scripts\bootstrap\one-shot-setup.ps1 -HostId claude-code
pwsh -File .\check.ps1 -HostId claude-code -Profile full -Deep
```

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host claude-code
bash ./check.sh --host claude-code --profile full --deep
```

### OpenCode

```powershell
pwsh -NoProfile -File .\install.ps1 -HostId opencode
pwsh -NoProfile -File .\check.ps1 -HostId opencode
```

```bash
bash ./install.sh --host opencode
bash ./check.sh --host opencode
```

> OpenCode does not use `one-shot-setup` yet. This lane is currently a preview adapter reached through direct install + check.

## Boundaries That Must Stay Explicit

### Codex

- this is the strongest repo-governed path today
- guidance should stay limited to local `~/.codex` settings, official MCP registration, and optional CLI dependencies
- hooks are currently frozen because of compatibility issues and are not part of the standard install path
- if online model access is needed, point users to `~/.codex/settings.json` under `env` or local environment variables
- do not ask users to paste secrets into chat

### Claude Code

- this is preview guidance, not full closure
- hooks are currently frozen because of compatibility issues
- the installer no longer writes `settings.vibe.preview.json`
- users should open `~/.claude/settings.json` and add only the required fields under `env`
- common fields are:
  - `VCO_AI_PROVIDER_URL`
  - `VCO_AI_PROVIDER_API_KEY`
  - `VCO_AI_PROVIDER_MODEL`
- add `ANTHROPIC_BASE_URL` and `ANTHROPIC_AUTH_TOKEN` only when needed for the host connection
- do not ask users to paste secrets into chat

### OpenCode

- this is a preview adapter, not full closure
- the repository writes skills, command/agent wrappers, and `opencode.json.example`
- the default target root is `OPENCODE_HOME`, otherwise `~/.config/opencode`
- if you want the preview payload isolated inside a project, use `--target-root ./.opencode`
- the real `opencode.json`, provider credentials, plugin installation, and MCP trust remain host-managed
- for detail, go straight to [`opencode-path.en.md`](./opencode-path.en.md)

## AI Governance Reminder

For `claude-code` and `opencode`, if `url`, `apikey`, `model`, or equivalent provider fields are not configured locally yet, the environment must not be described as online-ready.

Those values must be filled by the user in local host settings or local environment variables.

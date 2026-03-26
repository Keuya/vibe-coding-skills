# Cold-Start Install Paths

This document answers the only cold-start questions that matter right now: which hosts are supported, and which path you should use.

## One-Line Conclusion

The current public install surface supports three hosts:

- `codex`
- `claude-code`
- `opencode`

Within that scope:

- `codex`: recommended path
- `claude-code`: preview guidance path
- `opencode`: preview adapter path

If you want another agent, the current version should be treated as unsupported rather than silently routed into a hidden lane.

## Path 1: Codex

Windows:

```powershell
pwsh -File .\scripts\bootstrap\one-shot-setup.ps1 -HostId codex
pwsh -File .\check.ps1 -HostId codex -Profile full -Deep
```

Linux / macOS:

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host codex
bash ./check.sh --host codex --profile full --deep
```

What you get:

- governed payload
- optional provider seeding
- MCP active profile materialization
- deep health check

What you do not get:

- hook installation

## Path 2: Claude Code

Windows:

```powershell
pwsh -File .\scripts\bootstrap\one-shot-setup.ps1 -HostId claude-code
pwsh -File .\check.ps1 -HostId claude-code -Profile full -Deep
```

Linux / macOS:

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host claude-code
bash ./check.sh --host claude-code --profile full --deep
```

What you get:

- runtime payload
- preview guidance health check

What you do not get:

- automatic overwrite of the real `settings.json`
- hook installation
- automatic plugin provisioning
- automatic host MCP registration
- automatic provider secret wiring

## Correct Follow-Up For Claude Code

- open `~/.claude/settings.json`
- add only the fields you need under `env`
- common fields are `VCO_AI_PROVIDER_URL`, `VCO_AI_PROVIDER_API_KEY`, and `VCO_AI_PROVIDER_MODEL`
- add `ANTHROPIC_BASE_URL` and `ANTHROPIC_AUTH_TOKEN` only when needed for the host connection
- the current version no longer generates `settings.vibe.preview.json`
- do not paste secrets into chat

## Path 3: OpenCode

Windows:

```powershell
pwsh -NoProfile -File .\install.ps1 -HostId opencode
pwsh -NoProfile -File .\check.ps1 -HostId opencode
```

Linux / macOS:

```bash
bash ./install.sh --host opencode
bash ./check.sh --host opencode
```

What you get:

- runtime-core payload
- VibeSkills skill payload
- OpenCode command/agent wrappers
- `opencode.json.example`

What you do not get:

- one-shot bootstrap
- automatic overwrite of the real `opencode.json`
- automatic plugin provisioning
- automatic provider secret wiring
- automatic MCP trust decisions

## Correct Follow-Up For OpenCode

- for a global install, the default target root is `OPENCODE_HOME`, otherwise `~/.config/opencode`
- for project isolation, use `--target-root ./.opencode`
- manage the real `opencode.json` locally
- add provider credentials, plugin installation, and MCP trust locally
- for the detailed path note, read [`install/opencode-path.en.md`](./install/opencode-path.en.md)

## Most Important Cold-Start Boundary

- `HostId` / `--host` decides host semantics, not the folder name alone
- there is no public install entry for any other host in the current version
- hooks are currently frozen because of compatibility issues and are outside the supported install surface
- if `url` / `apikey` / `model` are not configured locally yet, the environment must not be described as online-ready

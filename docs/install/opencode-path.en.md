# OpenCode Install Path

## Scope

This path is a truthful `preview` lane, not a claim of full OpenCode closure.

The repository can install:

- runtime-core payload
- Vibe-Skills skill payload
- OpenCode command wrappers
- OpenCode agent wrappers
- an example `opencode.json` scaffold

The repository does **not** take ownership of:

- the real `~/.config/opencode/opencode.json`
- provider credentials
- plugin installation
- MCP trust decisions

## Global Install

Shell:

```bash
./install.sh --host opencode
./check.sh --host opencode
```

PowerShell:

```powershell
pwsh -NoProfile -File ./install.ps1 -HostId opencode
pwsh -NoProfile -File ./check.ps1 -HostId opencode
```

Default target root:

- `OPENCODE_HOME` when set
- otherwise `~/.config/opencode`

## Project-Local Install

Use a project-local OpenCode root when you want the preview payload to stay inside the repo:

```bash
./install.sh --host opencode --target-root ./.opencode
./check.sh --host opencode --target-root ./.opencode
```

The same target can be used from PowerShell with `-TargetRoot .\.opencode`.

## What Gets Written

Preview install writes:

- `skills/**`
- `commands/*.md`
- `command/*.md`
- `agents/*.md`
- `agent/*.md`
- `opencode.json.example`

Plural and singular command/agent directories are both materialized during preview because the current OpenCode docs and runtime ecosystem still show path drift.

## How To Use

After install, the intended entry surfaces are:

- `/vibe`
- `/vibe-implement`
- `/vibe-review`

You can also invoke the skill directly in chat, for example:

- `Use the vibe skill to plan this change.`
- `Use the vibe skill to implement the approved plan.`

Custom agents installed by the preview payload:

- `vibe-plan`
- `vibe-implement`
- `vibe-review`

## Verification

Use the shared repo health check first:

```bash
./check.sh --host opencode
```

The repository also ships a smoke verifier:

```bash
python3 ./scripts/verify/runtime_neutral/opencode_preview_smoke.py --repo-root . --write-artifacts
```

## Current Proof Note

The committed preview smoke verifier now proves on local OpenCode CLI `1.2.27` that:

- `opencode debug paths` resolves the isolated OpenCode root correctly
- `opencode debug skill` detects the installed `vibe` skill
- `opencode debug agent vibe-plan` detects the installed preview agent

The lane still remains `preview` because command execution replay and platform-specific proof bundles are not yet frozen.

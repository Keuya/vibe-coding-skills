# Manual Copy Install (Offline / No-Admin)

If you do not want to run the install scripts and only want to place the files manually, remember one thing:

**copy the VibeSkills runtime directories into your target host root.**

This path currently covers three public hosts:

- `codex`
- `claude-code`
- `opencode`

If your target is not one of those three, the current version should not be described as supported installation.

## What To Copy

For `codex` and `claude-code`, copy these items into the target host root:

- `skills/`
- `commands/`
- `config/upstream-lock.json`
- `config/skills-lock.json` if it exists in the repo
- the `skills/vibe/` runtime mirror

A simple way to think about them:

- `skills/`: the capabilities themselves
- `commands/`: command entrypoints
- `config/*.json`: lock files and release-alignment metadata
- `skills/vibe/`: the VCO runtime mirror

### If your target is OpenCode

For OpenCode preview manual copy, the relevant payload is:

- `skills/`
- `commands/*.md`
- `command/*.md`
- `agents/*.md`
- `agent/*.md`
- `config/opencode/opencode.json.example`

The target root should be:

- `OPENCODE_HOME`
- or `~/.config/opencode`
- or a project-local `./.opencode`

If you are doing OpenCode manual copy, use the dedicated doc together with this page:

- [`opencode-path.en.md`](./opencode-path.en.md)

## Where To Copy Them

For `codex` and `claude-code`, copy them into your target host root.

The target directory should end up containing paths like:

- `<TARGET_ROOT>/skills/`
- `<TARGET_ROOT>/commands/`
- `<TARGET_ROOT>/config/upstream-lock.json`
- `<TARGET_ROOT>/config/skills-lock.json` if present

## What You Still Need To Configure Yourself

Manual copy only places the repo files. It does not finish host-local configuration.

### If you install into Codex

You still need to configure locally:

- `~/.codex/settings.json`
- commonly `OPENAI_API_KEY` and `OPENAI_BASE_URL` under `env`

### If you install into Claude Code

You still need to configure locally:

- `~/.claude/settings.json`
- commonly:
  - `VCO_AI_PROVIDER_URL`
  - `VCO_AI_PROVIDER_API_KEY`
  - `VCO_AI_PROVIDER_MODEL`
- and, only if the host connection needs them:
  - `ANTHROPIC_BASE_URL`
  - `ANTHROPIC_AUTH_TOKEN`

### If you install into OpenCode

You still need to handle:

- the real `opencode.json`
- provider credentials
- plugin installation
- MCP trust decisions

The repository currently ships only `opencode.json.example` as a preview scaffold and does not take ownership of the final host config.

## What This Path Does Not Do Automatically

Manual copy does not automatically complete:

- hook installation
- MCP registration
- provider credential wiring
- edits to Claude Code's real `settings.json`
- edits to OpenCode's real `opencode.json`

The important current boundary is:

- `codex` and `claude-code` currently do **not** install hooks
- hook installation is temporarily frozen because of compatibility issues
- `opencode` also keeps host plugins and final host config out of repo ownership

## Final Boundary

If `url` / `apikey` / `model` are not configured locally yet, the environment must not be described as online-ready.

Those values should be filled by the user in local host settings or local environment variables, not pasted into chat.

## When Not To Use This Path

Do not use manual copy if you want:

- AI to choose the correct supported host for you
- the scripts to run install + check automatically
- less host-local configuration work

Use these instead:

- [`one-click-install-release-copy.en.md`](./one-click-install-release-copy.en.md)
- [`opencode-path.en.md`](./opencode-path.en.md)

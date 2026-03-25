# Manual Copy Install (Offline / No-Admin)

If you do not want to run the install scripts and only want to place the files manually, remember one thing:

**copy the VibeSkills runtime directories into your target host root.**

This path currently supports only two hosts:

- `codex`
- `claude-code`

If your target is not one of those two, the current version should not be described as supported installation.

## What To Copy

Copy these items into the target host root:

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

## Where To Copy Them

Copy them into your target host root.

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

## What This Path Does Not Do Automatically

Manual copy does not automatically complete:

- hook installation
- MCP registration
- provider credential wiring
- edits to Claude Code's real `settings.json`

The important current boundary is:

- `codex` and `claude-code` currently do **not** install hooks
- hook installation is temporarily frozen because of compatibility issues

## Final Boundary

If `url` / `apikey` / `model` are not configured locally yet, the environment must not be described as online-ready.

Those values should be filled by the user in local host settings or local environment variables, not pasted into chat.

## When Not To Use This Path

Do not use manual copy if you want:

- AI to choose the correct supported host for you
- the scripts to run install + check automatically
- less host-local configuration work

Use this instead:

- [`one-click-install-release-copy.en.md`](./one-click-install-release-copy.en.md)

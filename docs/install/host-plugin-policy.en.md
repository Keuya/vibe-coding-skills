# Host Plugin and Host Configuration Policy

This document answers only three questions:

- which hosts are on the current public support surface
- what the repo currently handles automatically
- what still must be completed locally by the host side

## Current Public Surface

- `codex`
- `claude-code`
- `cursor`
- `windsurf`

Other agents should not currently be described as having an official install closure.

## Global Principle

- install the repo-governed payload first
- add host-local configuration only as needed
- if a capability is not stably, publicly, and verifiably owned by the repo, do not write it as a default install requirement

## Codex

- currently the strongest path
- guidance stays centered on local settings, MCP, and optional CLI enhancements
- hooks remain frozen; that is not an install failure

## Claude Code

- preview guidance
- not integrated by “adding a pile of host plugins”
- does not overwrite the real `~/.claude/settings.json`
- hooks remain frozen; that is not an install failure

## Cursor

- preview guidance
- does not overwrite the real `~/.cursor/settings.json`
- does not take over Cursor host-native plugin, provider, or MCP closure
- hooks remain frozen; that is not an install failure

## Windsurf

- preview runtime-core
- default root is `~/.codeium/windsurf`
- the repo currently owns only shared runtime payload plus optional materialization of `mcp_config.json` and `global_workflows/`
- it does not take over login, account, provider, plugin, or workspace-native closure

## Recommended Community Wording

- the current version supports `codex`, `claude-code`, `cursor`, and `windsurf`
- `codex` follows the governed path
- `claude-code` and `cursor` follow preview guidance
- `windsurf` follows preview runtime-core
- hooks remain frozen across the current public surface; that is not a user install failure
- provider `url` / `apikey` / `model` values stay local and should not be pasted into chat

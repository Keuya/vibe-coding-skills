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
- `openclaw`
- `opencode`

Other agents should not currently be described as having an official install closure.

## Global Principle

- install the repo-governed payload first
- add host-local configuration only as needed
- if a capability is not stably, publicly, and verifiably owned by the repo, do not write it as a default install requirement
- for OpenClaw, write it as `preview` / `runtime-core-preview` / `runtime-core`
- for OpenClaw, make the default root explicit: `OPENCLAW_HOME` or `~/.openclaw`
- for OpenClaw, make the three paths explicit: attach / copy / bundle
- for OpenCode, write it as a preview-adapter path
- for OpenCode, make the default root explicit: `OPENCODE_HOME` or `~/.config/opencode`
- for OpenCode, make it explicit that direct install/check does not take ownership of the real `opencode.json`

## Codex

- currently the strongest path
- guidance stays centered on local settings, MCP, and optional CLI enhancements
- hooks remain frozen; that is not an install failure

## Claude Code

- supported install-and-use path
- not integrated by “adding a pile of host plugins”
- does not overwrite the real `~/.claude/settings.json`
- hooks remain frozen; that is not an install failure

## Cursor

- supported install-and-use path
- does not overwrite the real `~/.cursor/settings.json`
- Cursor-native plugins, settings, and extension surfaces remain managed on the Cursor side
- hooks remain frozen; that is not an install failure

## Windsurf

- supported install-and-use path with runtime-adapter integration
- default root is `~/.codeium/windsurf`
- the repo currently owns only shared runtime payload plus optional materialization of `mcp_config.json` and `global_workflows/`
- Windsurf-native local settings remain managed on the Windsurf side

## OpenClaw

- supported install-and-use path at the current `preview` (`runtime-core-preview`) level
- install/check runs in `runtime-core` mode with default target root from `OPENCLAW_HOME` or `~/.openclaw`
- attach / copy / bundle cover runtime-core payload installation, validation, and distribution
- OpenClaw-local configuration remains managed on the OpenClaw side

## OpenCode

- supported install-and-use path at the current preview-adapter level
- default target root is `OPENCODE_HOME` or `~/.config/opencode`
- direct install/check writes skills, command/agent wrappers, and `opencode.json.example`
- the real `opencode.json`, provider credentials, plugin installation, and MCP trust remain managed on the OpenCode side

## Recommended Community Wording

- the current version supports `codex`, `claude-code`, `cursor`, `windsurf`, `openclaw`, and `opencode`
- `codex` follows the governed path
- `claude-code` and `cursor` have a supported install-and-use path
- `windsurf` has a supported install-and-use path with runtime-adapter integration
- `openclaw` follows the `preview` / `runtime-core-preview` / `runtime-core` wording
- `openclaw` uses `OPENCLAW_HOME` or `~/.openclaw` as the default root, with attach / copy / bundle paths
- `opencode` follows preview-adapter wording, with default root from `OPENCODE_HOME` or `~/.config/opencode`
- `opencode` uses direct install/check and does not take ownership of the real `opencode.json`
- hooks remain frozen across the current public surface; that is not a user install failure
- provider `url` / `apikey` / `model` values stay local and should not be pasted into chat

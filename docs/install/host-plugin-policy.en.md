# Host Plugin And Host Configuration Policy

This document answers only the questions that matter in the current version:

- which hosts are supported today
- what the repository handles automatically
- what people still need to configure on the host side
- what should no longer be described as a standard install requirement

## Current Support Boundary

The public install surface currently includes:

- `codex`
- `claude-code`
- `opencode`

Anything outside those three hosts must not be described as "supported installation" in the current version.

If someone wants to wire VibeSkills into another agent, the accurate wording is:

- there is no officially supported install closure for that host yet
- there is no reusable host-plugin policy that can honestly be treated as production guidance
- old experimental lanes must not be presented as the community-default path

## Separate Three Different Things First

The main source of confusion is not the commands themselves. It is the boundary between responsibilities.

### 1. Repository payload

This is the part the repository owns, for example:

- `skills/`
- `commands/`
- the `skills/vibe/` runtime mirror
- install scripts, check scripts, and doctor / verification entrypoints
- OpenCode preview command/agent wrappers

This is the repo-governed surface.

### 2. Host configuration

This is the part the user still finishes locally, for example:

- `~/.codex/settings.json`
- `~/.claude/settings.json`
- `~/.config/opencode/opencode.json`
- local environment variables
- host-side MCP registration or trust decisions

These are not part of "already completed automatically by the repo".

### 3. Optional enhancements

Some CLIs, MCP servers, or external services may improve the experience, but they are not first-day requirements.

The correct order is:

- first make the supported host path work
- then add enhancements only when they solve a real need
- do not install everything just to make the setup look fuller

## Default Policy For Codex

For `codex`, the standard install policy should stay deliberately conservative.

### What counts as the supported baseline

Keep guidance limited to these supportable surfaces:

- local `~/.codex/settings.json`
- officially supportable MCP registration
- optional CLI dependencies
- no hook installation

### Historical claims that should not remain in the public path

The public install story should no longer imply any of the following:

- "install a bundle of host plugins first, then everything else"
- "Codex normally requires a Claude-style hook/plugin stack"
- "certain historical plugins are standard prerequisites for Codex"

### How to talk about online capability

If online model access is needed, people should be told to:

- configure the values under `env` in `~/.codex/settings.json`
- or configure them through local environment variables
- never paste secrets into chat

Common examples include:

- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`

If those values are not configured locally, the environment must not be described as online-ready.

## Default Policy For Claude Code

For `claude-code`, the boundary needs to be even more explicit.

### Current real status

`claude-code` is currently:

- preview guidance
- not full closure
- a host path where hook installation is frozen because of compatibility issues
- a host path where the installer no longer writes preview settings material

### What the repository does

Right now the repository only does the following:

- installs the runtime payload
- runs the matching preview checks

### What the repository does not do

Right now the repository does not automatically:

- overwrite the real `~/.claude/settings.json`
- write production provider credentials on behalf of the user
- complete host-side MCP registration
- claim that Claude Code is fully integrated

### What the user should do

The correct host-side flow is:

- open `~/.claude/settings.json`
- add only the fields needed under `env`
- preserve the host's existing settings

Common fields that may need to be configured locally include:

- `VCO_AI_PROVIDER_URL`
- `VCO_AI_PROVIDER_API_KEY`
- `VCO_AI_PROVIDER_MODEL`

If the host connection truly requires them, add:

- `ANTHROPIC_BASE_URL`
- `ANTHROPIC_AUTH_TOKEN`

Again, none of those values should be requested in chat.

If they are not configured locally yet, the environment must not be described as online-ready.

## Default Policy For OpenCode

For `opencode`, the right framing is preview adapter, not "another fully closed host lane."

### Current real status

`opencode` is currently:

- a preview adapter
- a host with real `install/check` entrypoints
- a host where the repo writes skills, command/agent wrappers, and `opencode.json.example`
- a host where the real `opencode.json`, provider credentials, plugin installation, and MCP trust stay host-managed

### What the repository does

Right now the repository:

- installs runtime-core plus the VibeSkills payload
- installs OpenCode command/agent wrappers
- writes `opencode.json.example`
- runs the matching preview checks

### What the repository does not do

Right now the repository does not automatically:

- overwrite the real `opencode.json`
- write production provider credentials
- install host plugins
- decide MCP trust for the user

### What the user should do

The correct host-side flow is:

- install the preview payload into `OPENCODE_HOME`, `~/.config/opencode`, or project-local `./.opencode`
- manage the real `opencode.json` locally
- add provider credentials locally
- make plugin and MCP trust decisions locally

For the full path note, go straight to:

- [`opencode-path.en.md`](./opencode-path.en.md)

## Current Policy Conclusion For Host Plugins

For the current version, the public policy should hold these lines clearly:

1. `codex` has no extra default host-plugin prerequisite.
2. `claude-code` is not integrated by "adding a pile of host plugins". It is a preview guidance path plus local host configuration.
3. `opencode` is also not "repo takes over the whole host." It is a preview adapter plus host-managed final config.
4. Historical plugin names are not a reason to keep recommending them in current community docs.
5. If a capability is not stably, publicly, and verifiably integrated by the repo, it should not be written as a standard install requirement.

## Recommended Community Wording

If you need to reference this policy in issues, README text, discussions, or install prompts, use language like this:

- the current public install surface includes `codex`, `claude-code`, and `opencode`
- `codex` follows a conservative path centered on local settings, MCP, and optional CLI enhancements
- the current version does not install hooks for `codex` or `claude-code` because compatibility issues remain unresolved
- `claude-code` follows a preview guidance path and does not overwrite the real `settings.json`
- `opencode` follows a preview adapter path and does not overwrite the real `opencode.json`
- provider `url` / `apikey` / `model` values are configured locally by the user, not pasted into chat
- other agents are outside the current public support surface

## When This Document Should Expand Again

This policy should only grow again if all of the following are true:

- a new host has a verifiable install closure
- the automation boundary is clear
- community users do not need hidden historical context to install it correctly
- we can state exactly what the repo owns and what the host still owns

Until then, keeping the document simple, truthful, and easy to defend is better than carrying historical baggage forward.

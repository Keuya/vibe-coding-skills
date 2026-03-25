# Prompt-Based Install (Recommended Default)

This is the default public install entrypoint.

## First confirm two things

1. Confirm the host: `codex`, `claude-code`, `cursor`, or `windsurf`
2. Confirm the public version: `Full Version + Customizable Governance` or `Framework Only + Customizable Governance`

The real profile mapping is:

- `Full Version + Customizable Governance` -> `full`
- `Framework Only + Customizable Governance` -> `minimal`

## Prompt files to copy directly

- [`prompts/full-version-install.en.md`](./prompts/full-version-install.en.md)
- [`prompts/framework-only-install.en.md`](./prompts/framework-only-install.en.md)
- [`prompts/full-version-update.en.md`](./prompts/full-version-update.en.md)
- [`prompts/framework-only-update.en.md`](./prompts/framework-only-update.en.md)

## The real semantics of the four hosts

| Host | Mode | Default root | What the repo currently owns | What it must not be described as |
| --- | --- | --- | --- | --- |
| `codex` | governed | `~/.codex` | governed runtime, settings/MCP guidance, deep check | hooks already installed, governance-AI online readiness complete |
| `claude-code` | preview guidance | `~/.claude` | preview guidance and health checks | full closure, real settings takeover |
| `cursor` | preview guidance | `~/.cursor` | preview guidance and health checks | full closure, Cursor host-native closure |
| `windsurf` | preview runtime-core | `~/.codeium/windsurf` | shared runtime payload, optional `mcp_config.json` / `global_workflows/` materialization, health checks | login/account/provider/plugin/workspace-native closure |

## What AI should do in this flow

The install assistant should:

- ask for the host first, then the version
- execute only on the four supported hosts
- map the public versions only to `full` or `minimal`
- choose `bash` or `pwsh` based on the operating system
- never ask you to paste secrets into chat
- distinguish “installed locally” from “online-ready”
- end with a concise result summary plus manual follow-up

## Common truth-first wording

- `codex`: the strongest path today, but hooks are still frozen; `OPENAI_*` is not the same thing as `VCO_AI_PROVIDER_*`
- `claude-code`: preview guidance and does not overwrite the real `~/.claude/settings.json`
- `cursor`: preview guidance and does not take over the real `~/.cursor/settings.json`
- `windsurf`: preview runtime-core and only installs runtime payload plus required materialized files

## What to read next

If you want to bring in your own workflows or skills afterward:

- [`custom-workflow-onboarding.md`](./custom-workflow-onboarding.md)
- [`custom-skill-governance-rules.md`](./custom-skill-governance-rules.md)

If you want lower-level commands and boundary details:

- [`recommended-full-path.en.md`](./recommended-full-path.en.md)
- [`manual-copy-install.en.md`](./manual-copy-install.en.md)
- [`host-plugin-policy.en.md`](./host-plugin-policy.en.md)

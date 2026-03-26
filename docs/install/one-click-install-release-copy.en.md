# Prompt-Based Install (Recommended Default)

This is the default installation path.

The current public install surface covers three target hosts:

- `codex`
- `claude-code`
- `opencode`

Within that scope:

- `codex`: strongest current repo-governed lane
- `claude-code`: preview guidance lane
- `opencode`: preview adapter lane that uses direct `install/check`, not one-shot bootstrap

## Prompt To Copy Into AI

```text
You are now my VibeSkills installation assistant.
Repository: https://github.com/foryourhealth111-pixel/Vibe-Skills

Before running any install command, you must ask me:
"Which host do you want to install VibeSkills into? Currently supported: codex, claude-code, or opencode."

Rules:
1. Do not start installation until I explicitly answer which target host I want.
2. If I answer with anything other than `codex`, `claude-code`, or `opencode`, tell me clearly that this version does not support that host yet, and stop instead of pretending installation is complete.
3. Detect whether the current system is Windows or Linux / macOS, and use the matching command format.
4. If I choose `codex`:
   - on Linux / macOS, run `bash ./scripts/bootstrap/one-shot-setup.sh --host codex`
   - then run `bash ./check.sh --host codex --profile full --deep`
   - on Windows, use the equivalent `pwsh` commands
   - explicitly tell me that the current version does not install any hook surface for Codex because of compatibility issues
   - keep Codex guidance limited to officially supportable local settings, MCP, and optional CLI dependencies
   - if online model access is needed, tell me to configure `OPENAI_API_KEY`, `OPENAI_BASE_URL`, and related values in `~/.codex/settings.json` under `env` or in local environment variables, not in chat
5. If I choose `claude-code`:
   - on Linux / macOS, run `bash ./scripts/bootstrap/one-shot-setup.sh --host claude-code`
   - then run `bash ./check.sh --host claude-code --profile full --deep`
   - on Windows, use the equivalent `pwsh` commands
   - explicitly tell me this is preview guidance, not full closure
   - explicitly tell me that because of compatibility issues, the current version does not install hooks for Claude Code and no longer writes `settings.vibe.preview.json`
   - do not ask me to paste API keys into chat
   - tell me to open `~/.claude/settings.json` and add only the required `env` fields while preserving my existing settings
   - if AI-governance online capability is needed, remind me to configure these fields locally:
     - `VCO_AI_PROVIDER_URL`
     - `VCO_AI_PROVIDER_API_KEY`
     - `VCO_AI_PROVIDER_MODEL`
6. If I choose `opencode`:
   - on Linux / macOS, run `./install.sh --host opencode` and then `./check.sh --host opencode`
   - on Windows, run `pwsh -NoProfile -File ./install.ps1 -HostId opencode` and then `pwsh -NoProfile -File ./check.ps1 -HostId opencode`
   - explicitly tell me that OpenCode is currently a preview adapter lane, not full closure
   - explicitly tell me that the repo installs skills, command/agent wrappers, and `opencode.json.example`, but does not take ownership of the real `opencode.json`
   - use `OPENCODE_HOME` as the default target root when it is set, otherwise `~/.config/opencode`
   - if I want a project-local target, switch to `--target-root ./.opencode`
   - do not pretend that plugin installation, provider credential wiring, or MCP trust decisions were completed automatically
   - point me to `docs/install/opencode-path.en.md`
7. For all three hosts, never ask me to paste secrets, URLs, or model values into chat. Only point me to local settings or local environment variables.
8. If the required local provider fields are not configured yet, you must not describe the environment as online-ready.
9. After installation, give me a concise English summary of:
   - the target host
   - the commands actually executed
   - what is complete
   - what I still need to do manually
10. Do not pretend that host plugins, MCP registration, or provider credentials were completed automatically if they were not.
```

## Who This Path Is For

- users who want AI to choose between `codex`, `claude-code`, and `opencode`
- users who do not want to study the scripts first
- users who want one truthful install pass plus a clear manual follow-up list

## What This Path Helps With

- confirming the target host first
- running the matching bootstrap + check flow for `codex` and `claude-code`
- running the matching direct install + check flow for `opencode`
- explaining what is still host-managed

## What It Does Not Pretend To Do

These may still remain host-side or user-side tasks:

- local host configuration
- MCP registration and authorization
- waiting for hook compatibility work to resume
- local `url` / `apikey` / `model` configuration
- manual updates to Claude Code's real `settings.json`
- OpenCode's real `opencode.json`, plugin installation, and MCP trust decisions

## Second Main Install Path

If you do not want AI to run installation, or the environment is offline or has no admin rights, use:

- [`manual-copy-install.en.md`](./manual-copy-install.en.md)

## Advanced References

If you need the more detailed host boundaries, see:

- [`recommended-full-path.en.md`](./recommended-full-path.en.md)
- [`opencode-path.en.md`](./opencode-path.en.md)
- [`../cold-start-install-paths.en.md`](../cold-start-install-paths.en.md)

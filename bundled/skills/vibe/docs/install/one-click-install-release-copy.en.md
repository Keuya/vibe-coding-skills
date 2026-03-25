# Prompt-Based Install (Recommended Default)

This is the default installation path.

At the moment, only two target hosts are supported:

- `codex`
- `claude-code`

## Prompt To Copy Into AI

```text
You are now my VibeSkills installation assistant.
Repository: https://github.com/foryourhealth111-pixel/Vibe-Skills

Before running any install command, you must ask me:
"Which host do you want to install VibeSkills into? Currently supported: codex or claude-code."

Rules:
1. Do not start installation until I explicitly answer which target host I want.
2. If I answer with anything other than `codex` or `claude-code`, tell me clearly that this version does not support that host yet, and stop instead of pretending installation is complete.
3. Detect whether the current system is Windows or Linux / macOS, and use the matching command format.
4. If I choose `codex`:
   - on Linux / macOS, run `bash ./scripts/bootstrap/one-shot-setup.sh --host codex`
   - then run `bash ./check.sh --host codex --profile full --deep`
   - on Windows, use the equivalent `pwsh` commands.
   - explain in a recommendation tone that the current version does not open the Codex hook install surface yet because the author is still working through compatibility issues, and that this does not mean the install failed.
   - keep Codex guidance limited to officially supportable local settings, MCP, and optional CLI dependencies, and treat anything still missing as optional enhancement work.
   - if online model access is needed, tell me to configure `OPENAI_API_KEY`, `OPENAI_BASE_URL`, and related values in `~/.codex/settings.json` under `env` or in local environment variables, not in chat.
   - also explain clearly that `OPENAI_API_KEY` and `OPENAI_BASE_URL` only cover Codex base online provider access and do not mean the governance AI online layer is already configured.
   - if the user wants the governance AI online layer under Codex too, recommend these fields as optional enhancement settings that I can ask you to add next:
     - `VCO_AI_PROVIDER_URL`
     - `VCO_AI_PROVIDER_API_KEY`
     - `VCO_AI_PROVIDER_MODEL`
   - also explain clearly what those three fields do:
     - `VCO_AI_PROVIDER_URL`: the provider endpoint or compatible API base URL used by the governance AI layer.
     - `VCO_AI_PROVIDER_API_KEY`: the local credential used to authenticate governance AI calls to that provider.
     - `VCO_AI_PROVIDER_MODEL`: the model name used when governance AI needs online analysis, governance enhancement, or related overlay capability.
   - also explain why they matter: they are only needed when the user wants the governance AI online layer under Codex; if they are missing, the install can only be described as having Codex base online capability configured, not governance AI online readiness.
   - also explain where to configure them: preferably in `~/.codex/settings.json` under `env`, or through local environment variables; never ask me to paste the URL, API key, or model into chat.
5. If I choose `claude-code`:
   - on Linux / macOS, run `bash ./scripts/bootstrap/one-shot-setup.sh --host claude-code`
   - then run `bash ./check.sh --host claude-code --profile full --deep`
   - on Windows, use the equivalent `pwsh` commands.
   - explicitly tell me this is preview guidance, not full closure.
   - explain in a recommendation tone that the current version does not open the Claude Code hook install surface yet because the author is still working through compatibility issues; this does not mean the install failed, and the installer no longer writes `settings.vibe.preview.json`.
   - do not ask me to paste API keys into chat.
   - tell me to open `~/.claude/settings.json` and add only the required `env` fields while preserving my existing settings.
   - if AI-governance online capability is needed, recommend these fields as optional enhancement settings that I can ask you to add next:
     - `VCO_AI_PROVIDER_URL`
     - `VCO_AI_PROVIDER_API_KEY`
     - `VCO_AI_PROVIDER_MODEL`
   - also explain clearly what those three fields do:
     - `VCO_AI_PROVIDER_URL`: the provider endpoint or compatible API base URL used by the governance AI layer.
     - `VCO_AI_PROVIDER_API_KEY`: the local credential used to authenticate governance AI calls to that provider.
     - `VCO_AI_PROVIDER_MODEL`: the model name used when governance AI needs online analysis, governance enhancement, or related overlay capability.
   - also explain why they matter: if the user wants AI-governance online capability rather than only local runtime / prompt / check flows, these three fields are required; if they are missing, the install can only be described as locally installed with governance AI online capability still not ready, not as full closure or online-ready.
   - also explain where to configure them: preferably in `~/.claude/settings.json` under `env`, or through local environment variables; never ask me to paste the URL, API key, or model into chat.
6. For both `codex` and `claude-code`, never ask me to paste secrets, URLs, or model values into chat. Only point me to local settings or local environment variables.
7. If the required local provider fields are not configured yet, you must not describe the environment as online-ready.
8. After installation, give me a concise English summary of:
   - the target host
   - the commands actually executed
   - what is complete
   - what I still need to do manually
9. Do not pretend that host plugins, MCP registration, or provider credentials were completed automatically if they were not; describe anything still missing as optional enhancement work or recommended next steps first.
```

## Who This Path Is For

- users who want AI to choose between `codex` and `claude-code`
- users who do not want to study the scripts first
- users who want one truthful install pass plus a clear manual follow-up list

## What This Path Helps With

- confirming the target host first
- running the matching bootstrap + check flow
- explaining what is still host-managed
- reframing any missing MCP, provider, or governance-AI-online setup as optional enhancement work rather than install warnings
- for `codex`, explaining that `OPENAI_*` covers base online provider access, while `VCO_AI_PROVIDER_*` is only additionally needed for the governance AI online layer
- for `claude-code`, explaining what `VCO_AI_PROVIDER_URL`, `VCO_AI_PROVIDER_API_KEY`, and `VCO_AI_PROVIDER_MODEL` do, why they are needed, and where they must be configured locally

## What It Does Not Pretend To Do

These may still remain host-side or user-side tasks:

- local host configuration
- MCP registration and authorization as optional enhancements
- waiting for hook compatibility work to resume on the author side, not as a user install failure
- local `url` / `apikey` / `model` configuration
- manual updates to Claude Code's real `settings.json`

## How old-version users should upgrade

If you already installed an older version, you usually do not need to uninstall first.
For most users, the simplest path is to rerun this prompt-based install flow.

In practice, that means asking AI to run one more install pass with this prompt.
If that install completes normally, you usually do not need any extra manual commands.

Only use the more detailed upgrade commands when:

- AI cannot run the install for you
- you need to debug a failed upgrade manually
- you explicitly want to upgrade to a specific release or tag

Then see:

- [`recommended-full-path.en.md`](./recommended-full-path.en.md)

## Second Main Install Path

If you do not want AI to run installation, or the environment is offline or has no admin rights, use:

- [`manual-copy-install.en.md`](./manual-copy-install.en.md)

## Advanced References

If you need the more detailed host boundaries, see:

- [`recommended-full-path.en.md`](./recommended-full-path.en.md)
- [`../cold-start-install-paths.en.md`](../cold-start-install-paths.en.md)

# Configuration Guide

This guide clarifies one thing only: how to finish the AI-governance advice online configuration after install.

## First, separate these two states

- `installed locally`: VibeSkills files have been installed into the target host root
- `AI governance online-ready`: the advice path has usable local credentials, model selection, and a reachable provider endpoint

The first state does not imply the second.

## What the quick check actually reads

The current quick check reads from:

1. `<target-root>/settings.json` -> `env`
2. the current shell / process environment

So:

- if the host uses a local `settings.json`, put the variables under `env`
- if the host does not use that file surface, or if you just want to validate connectivity first, use local environment variables

Do not paste secrets into chat.

## Built-in intent advice configuration

The governance runtime now drives intent advice exclusively from the `VCO_INTENT_ADVICE_*` keys. This is the public, supported path that the quick check and routers read before making any outbound request.

### Required keys

```json
{
  "env": {
    "VCO_INTENT_ADVICE_API_KEY": "<local-api-key>",
    "VCO_INTENT_ADVICE_BASE_URL": "https://api.openai.com/v1",
    "VCO_INTENT_ADVICE_MODEL": "gpt-5.4-high"
  }
}
```

Notes:

- `VCO_INTENT_ADVICE_API_KEY`: required for all built-in advice routes
- `VCO_INTENT_ADVICE_BASE_URL`: optional; when absent, the policy/provider config dictates the default
- `VCO_INTENT_ADVICE_MODEL`: required unless overridden in `config/llm-acceleration-policy.json`
- Legacy `OPENAI_*` keys are no longer used as automatic fallbacks for intent advice; they can remain side-by-side but the runtime will not backfill them.

## Optional vector diff embeddings configuration

Vector diff embeddings are an auxiliary capability that improves diff summarization but should never block intent advice. Configure them independently using the `VCO_VECTOR_DIFF_*` keys.

### Optional keys

```json
{
  "env": {
    "VCO_VECTOR_DIFF_API_KEY": "<embedding-key>",
    "VCO_VECTOR_DIFF_BASE_URL": "https://api.openai.com/v1",
    "VCO_VECTOR_DIFF_MODEL": "text-embedding-ada-002"
  }
}
```

Notes:

- Vector diff reads these keys only when enabled in `config/llm-acceleration-policy.json`.`context.vector_diff`
- If embeddings are missing, vector diff degrades gracefully (vector_diff_status becomes `vector_diff_missing_credentials` or `vector_diff_not_configured`) but the advice path still runs.
- The vector diff keys are independent; you can point them at a different provider without affecting the intent advice configuration.

## Advanced path: policy-managed provider settings

If you already maintain provider details in the strategy files, continue to specify:

- `config/llm-acceleration-policy.json` -> `provider.base_url`
- `config/llm-acceleration-policy.json` -> `provider.model`

In that setup:

- base URL and model can still come from policy overrides
- the local credentials for that provider must sit under `VCO_INTENT_ADVICE_*`

## Where this usually goes per host

### Codex

- target root: `~/.codex`
- common location: `~/.codex/settings.json` -> `env`

### Claude Code

- target root: `~/.claude`
- common location: `~/.claude/settings.json` -> `env`

### Cursor

- target root: `~/.cursor`
- common location: `~/.cursor/settings.json` -> `env`

### Windsurf

- target root: `~/.codeium/windsurf`
- if the host does not use `<target-root>/settings.json`, set local environment variables before running the check

### OpenClaw

- target root: `OPENCLAW_HOME` or `~/.openclaw`
- if the host does not use `<target-root>/settings.json`, set local environment variables before running the check

### OpenCode

- target root: `OPENCODE_HOME` or `~/.config/opencode`
- if the host does not use `<target-root>/settings.json`, set local environment variables before running the check

## Quick-check commands

Run from the repo root.

### Windows

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-router-ai-connectivity-gate.ps1 -TargetRoot "<target host root>" -WriteArtifacts
```

If PowerShell 7 is already installed on your machine, you can use `pwsh` instead.

### Linux / macOS

```bash
python3 ./scripts/verify/runtime_neutral/router_ai_connectivity_probe.py --target-root "<target host root>" --write-artifacts
```

Common default roots:

- `codex` -> `~/.codex`
- `claude-code` -> `~/.claude`
- `cursor` -> `~/.cursor`
- `windsurf` -> `~/.codeium/windsurf`
- `openclaw` -> `~/.openclaw`
- `opencode` -> `~/.config/opencode`

## How to read the result

- `ok`: AI-governance advice is online
- `missing_credentials`: built-in intent-advice credentials are missing; usually add `VCO_INTENT_ADVICE_API_KEY`
- `missing_model`: the intent-advice model is missing; usually add `VCO_INTENT_ADVICE_MODEL`
- `missing_base_url`: add the provider base URL locally, or define `provider.base_url` in policy
- `provider_rejected_request`: key, model id, or endpoint compatibility is wrong
- `provider_unreachable`: network, DNS, base-url reachability, or timeout is failing
- `prefix_required`: the current policy only evaluates advice in explicit `/vibe` scope

## Owned-only uninstall cleanup

When you need to reverse an install, run `pwsh -NoProfile -File ..\..\uninstall.ps1 --host <host> --target-root <root>` or, on Linux/macOS, `bash ./uninstall.sh ...`. The uninstallers honor the ledger-first contract described in [`docs/uninstall-governance.md`](../uninstall-governance.md) and will only delete Vibe-managed surfaces recorded in the install ledger, closure manifest, or documented legacy payloads.

## Short practical conclusion

If you want the fastest path for the normal built-in intent-advice setup:

1. configure `VCO_INTENT_ADVICE_API_KEY` locally
2. add `VCO_INTENT_ADVICE_BASE_URL` only when you use a custom gateway
3. configure `VCO_INTENT_ADVICE_MODEL`
4. run the quick check

Vector diff embeddings stay optional. Configure `VCO_VECTOR_DIFF_API_KEY` / `VCO_VECTOR_DIFF_BASE_URL` / `VCO_VECTOR_DIFF_MODEL` only when you want large-diff semantic retrieval.

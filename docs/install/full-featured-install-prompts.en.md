# Full-Featured Install Prompts (Standard Recommended Install)

This document provides **copy-paste prompts for AI coding assistants / agents** so users can trigger the VibeSkills standard recommended install path more easily.

Boundary first:

- "full-featured" here means **repo-governed full closure**
- for most users, that is the same thing as the **standard recommended install**
- the current default lane should treat `scrapling` as a default local runtime surface
- the current default lane should treat `Cognee` as the governed long-term enhancement lane
- `Composio / Activepieces` should be described as prewired but setup-required external action surfaces
- Windows is the current strongest reference path
- Linux only reaches the current authoritative full-featured lane when `pwsh` is available
- Linux without `pwsh` can still install and run, but it is `degraded-but-supported`, not equivalent to the full Windows lane
- `opencode` now has its own preview adapter install path, but it is outside the scope of these "full-featured" prompts; use [`opencode-path.en.md`](./opencode-path.en.md) instead.

## Universal Prompt

Use this when:

- the user does not want to choose platform-specific commands manually
- the agent should detect Windows vs Linux
- you want one-shot bootstrap + doctor + truthful boundary reporting

Copy:

```text
Please install the current repository using the VibeSkills recommended full-featured path, while staying strictly truth-first.
Repository address: https://github.com/foryourhealth111-pixel/Vibe-Skills
1. Detect whether the current system is Windows or Linux.
2. If it is Windows:
   - prefer `pwsh -File .\scripts\bootstrap\one-shot-setup.ps1`
   - then run `pwsh -File .\check.ps1 -Profile full -Deep`
   - if `pwsh` is unavailable, fall back to Windows PowerShell
3. If it is Linux:
   - first check whether `pwsh` is available
   - if `pwsh` is available, run `bash ./scripts/bootstrap/one-shot-setup.sh` and then `bash ./check.sh --profile full --deep`
   - and explicitly state that this is the strongest Linux path currently available, but it still ships as `supported-with-constraints`
   - if `pwsh` is not available, still run `bash ./scripts/bootstrap/one-shot-setup.sh` and `bash ./check.sh --profile full --deep`
   - but explicitly state that the result is only degraded-but-supported, and do not claim it is equivalent to full-featured Windows
4. After installation, give me a concise conclusion:
   - current platform
   - commands executed
   - final readiness_state
   - remaining host-managed surfaces
   - whether this platform has reached the strongest currently supported state available for this lane
5. Do not pretend that host plugins, external MCP surfaces, or provider secrets were auto-installed.
6. Treat `scrapling` as part of the default full lane:
   - if Python packaging is available, allow the installer to attempt `scrapling[ai]`
   - report clearly whether the `scrapling` CLI ended up callable
7. Treat `Cognee` as the default long-term enhancement lane, not as a replacement for session truth.
8. Treat `Composio / Activepieces` as prewired external action integrations:
   - visible by default
   - still setup-required
   - not auto-enabled
   - still confirm-gated when enabled
9. If the result is `manual_actions_pending`, list the remaining manual actions as recommended next steps instead of calling it a failure.
10. If follow-up is needed, only recommend officially supportable surfaces for the host, and explain in a recommendation tone that the hook install surface is still paused while the author works through compatibility issues, so this should not be framed as an install failure.
11. For Claude Code:
   - do not ask me to paste secrets into chat
   - tell me to open `~/.claude/settings.json`
   - only add missing `env` fields such as `VCO_AI_PROVIDER_URL`, `VCO_AI_PROVIDER_API_KEY`, and `VCO_AI_PROVIDER_MODEL`
   - add `ANTHROPIC_BASE_URL` and `ANTHROPIC_AUTH_TOKEN` only when they are actually needed for the host connection
   - the current version no longer writes `settings.vibe.preview.json`
12. For Codex:
   - explain in a recommendation tone that the hook install surface is not open yet because the author is still working through compatibility issues, and that this does not mean the install is broken
   - keep guidance limited to local `~/.codex` settings, official MCP registration, and optional CLI dependencies
   - if online model access is needed, tell me to configure values such as `OPENAI_API_KEY` and `OPENAI_BASE_URL` in `~/.codex/settings.json` under `env` or in local environment variables
   - also tell me clearly that `OPENAI_*` only covers Codex base online provider access and does not mean the governance AI online layer is configured
   - if the governance AI online layer is needed too, recommend `VCO_AI_PROVIDER_URL`, `VCO_AI_PROVIDER_API_KEY`, and `VCO_AI_PROVIDER_MODEL` as optional enhancement settings that I can ask you to add next
13. Do not modify runtime logic during this flow; only install, check, and summarize.
> Reminder: AI governance layer values must be filled in by the user in local files or local environment variables. Do not ask the user to paste `url`, `apikey`, or `model` into chat.
```

## Windows Prompt

Use this when:

- the user is clearly on Windows
- they want the strongest current reference path

Copy:

```text
Please install the current repository using the Windows recommended full-featured path.
Repository address: https://github.com/foryourhealth111-pixel/Vibe-Skills
Requirements:

1. Prefer `pwsh` and run:
   - `pwsh -File .\scripts\bootstrap\one-shot-setup.ps1`
   - `pwsh -File .\check.ps1 -Profile full -Deep`
2. If `pwsh` is unavailable, fall back to:
   - `powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap\one-shot-setup.ps1`
   - `powershell -ExecutionPolicy Bypass -File .\check.ps1 -Profile full -Deep`
3. After installation, tell me:
   - the readiness_state
   - whether this qualifies as the current Windows reference full-featured lane
   - which host-managed surfaces still need manual provisioning
4. Do not pretend host plugins, provider secrets, or plugin-backed MCP surfaces were completed automatically.
5. If the result is `manual_actions_pending`, list the remaining actions clearly.
6. Keep Codex guidance limited to local settings, official MCP, and optional CLI dependencies, and explain in a recommendation tone that the hook install surface is still paused while compatibility work is in progress, so this is not an install failure.
7. If AI governance layer values are needed, tell me where to configure them locally instead of asking me to paste `url`, `apikey`, or `model` into chat.
```

## Linux Prompt

Use this when:

- the user is clearly on Linux
- they want the agent to handle the `pwsh` check

Copy:

```text
Please install the current repository using the Linux recommended full-featured path, and first determine whether this Linux environment has `pwsh`.
Repository address: https://github.com/foryourhealth111-pixel/Vibe-Skills
Requirements:

1. Check whether `pwsh` is available.
2. Run:
   - `bash ./scripts/bootstrap/one-shot-setup.sh`
   - `bash ./check.sh --profile full --deep`
3. If `pwsh` is available, explicitly tell me that the result is on the Linux authoritative full-featured lane.
4. If `pwsh` is not available, explicitly tell me:
   - the result is only degraded-but-supported
   - it must not be described as equivalent to the full Windows lane
5. After installation, summarize:
   - readiness_state
   - whether host-managed surfaces are still missing
   - whether I should add `pwsh`
   - whether I should add official MCP or local configuration next as optional enhancements
6. Explain in a recommendation tone that the hook install surface is still paused while compatibility work is in progress, so this is not an install failure.
7. If the result is `manual_actions_pending`, list the remaining manual actions as recommended follow-up work instead of calling the install failed.
> Reminder: AI governance layer values must be filled in by the user in local files or local environment variables. Do not ask the user to paste `url`, `apikey`, or `model` into chat.
```

## Suggested README / Community Framing

If you want to place this into a README, issue template, or community post, add one sentence like this:

> Copy the prompt below into your AI coding assistant and it will choose the correct Windows or Linux install path automatically, while still reporting the remaining host-side provisioning work truthfully.

## Related Docs

- [`recommended-full-path.en.md`](./recommended-full-path.en.md)
- [`opencode-path.en.md`](./opencode-path.en.md)
- [`../one-shot-setup.md`](../one-shot-setup.md)
- [`../cold-start-install-paths.en.md`](../cold-start-install-paths.en.md)

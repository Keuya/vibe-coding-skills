# Cold-Start Install Paths

This document answers the only cold-start questions that matter right now: which hosts are supported, and what the shortest truth-first install path looks like for each.

## One-Line Conclusion

The current public surface supports four hosts:

- `codex`
- `claude-code`
- `cursor`
- `windsurf`

Within that scope:

- `codex`: governed path
- `claude-code`: preview guidance
- `cursor`: preview guidance
- `windsurf`: preview runtime-core

Other hosts should not currently be described as supported installation targets.

## Codex

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host codex --profile full
bash ./check.sh --host codex --profile full --deep
```

What you get:

- governed runtime payload
- local settings / MCP guidance
- deep health check

What you do not get:

- automatic hooks
- automatic governance-AI online readiness

## Claude Code

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host claude-code --profile full
bash ./check.sh --host claude-code --profile full --deep
```

What you get:

- preview-guidance payload
- preview health check

What you do not get:

- full closure
- overwrite of the real `~/.claude/settings.json`
- automatic hooks

## Cursor

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host cursor --profile full
bash ./check.sh --host cursor --profile full --deep
```

What you get:

- preview-guidance payload
- preview health check

What you do not get:

- full closure
- overwrite of the real `~/.cursor/settings.json`
- Cursor host-native provider / MCP / hook closure

## Windsurf

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host windsurf --profile full
bash ./check.sh --host windsurf --profile full --deep
```

What you get:

- shared runtime payload
- a runtime-core preview install under `~/.codeium/windsurf`
- optional `mcp_config.json` materialization
- optional `global_workflows/` materialization

What you do not get:

- full closure
- host login / account / provider / plugin closure

## Boundaries That Must Hold During Cold Start

- `HostId` / `--host` decides host semantics
- hooks remain frozen across the current public surface; that is not an install failure
- if local provider fields are not configured, the environment must not be described as online-ready
- do not ask users to paste secrets into chat

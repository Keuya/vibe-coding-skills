# Requirement: Codex `vibe` Duplicate Surface Fix

- Date: 2026-03-26
- Issue: `#42`

## Goal

Prevent Codex from exposing two `vibe` skills when either of these duplicate surfaces exist:

- a legacy sibling copy under `~/.agents/skills/vibe`
- a discoverable nested runtime mirror under `skills/vibe/bundled/skills/vibe/SKILL.md`

## Acceptance

- Codex default-root install quarantines the legacy `.agents/skills/vibe` duplicate instead of leaving both surfaces discoverable.
- Installed runtime payloads hide nested runtime-mirror `SKILL.md` entrypoints while preserving runtime configs and bootstrap behavior.
- `check.sh` and `check.ps1` fail clearly when the duplicate surface still exists.
- Non-default custom target roots are not mutated as part of this mitigation.
- Automated tests cover shell/PowerShell install behavior, runtime bootstrap continuity, and duplicate-surface regression checks.

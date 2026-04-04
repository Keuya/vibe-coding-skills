# Plan: Codex `vibe` Duplicate Surface Fix

- Internal grade: `M`
- Scope: `install.sh`, `install.ps1`, `check.sh`, `check.ps1`, adapter installers, runtime-neutral install/check tests

## Steps

1. Detect the bounded duplicate candidate only for Codex default roots shaped like `.../.codex`.
2. During install, quarantine legacy `.agents/skills/vibe` into `.agents/skills-disabled/`.
3. During install, hide nested runtime-mirror `SKILL.md` entrypoints after materialization so hosts do not discover duplicate skills.
4. Preserve bootstrap continuity by restoring `SKILL.md` when a sanitized runtime mirror is copied into a real top-level skill lane.
5. During check, fail explicitly if the duplicate surface still exists or if nested runtime mirrors remain discoverable.
6. Verify with targeted runtime script tests and direct shell/PowerShell checks where available.

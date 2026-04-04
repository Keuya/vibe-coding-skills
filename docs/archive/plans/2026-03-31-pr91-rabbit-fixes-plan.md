# 2026-03-31 PR91 Rabbit Fix Batch Plan

## Goal

Patch the real PR `#91` review findings and rerun evidence-backed verification.

## Grade

- Internal grade: L

## Batches

### Batch 1: Safety and ownership
- Fix `.vibeskills` uninstall ownership gating
- Fix managed Claude hook removal matching

### Batch 2: Execution-path correctness
- Reuse shared Python interpreter selection in `check.sh`
- Make Windows readiness wrapper fail fast on probe errors
- Tighten the most obvious helper-script argument and process handling defects

### Batch 3: Proof artifact hygiene
- Sanitize host-specific absolute paths from frozen Claude proof artifacts
- Replace stale Codex-native wording inside the Claude proof report
- Fix stale replay wording about Linux proof still being pending

### Batch 4: Verify
- Run targeted unit tests
- Run host/replay/dist gates
- Re-run a live Claude Linux install/check/smoke proof on the branch

## Verification Commands

- `python3 -m unittest tests.runtime_neutral.test_claude_preview_scaffold tests.runtime_neutral.test_installed_runtime_uninstall`
- `pwsh -NoProfile -ExecutionPolicy Bypass -File ./scripts/verify/vibe-host-adapter-contract-gate.ps1`
- `pwsh -NoProfile -ExecutionPolicy Bypass -File ./scripts/verify/vibe-cross-host-route-parity-gate.ps1`
- `pwsh -NoProfile -ExecutionPolicy Bypass -File ./scripts/verify/vibe-dist-manifest-gate.ps1`
- `bash ./install.sh --host claude-code --profile full --target-root <temp-root>`
- `bash ./check.sh --host claude-code --profile full --target-root <temp-root> --deep`
- `CLAUDE_HOME=<temp-root> claude agents`

## Rollback Rules

- If a proposed bot fix weakens current proof truth, reject it
- If proof artifact sanitization breaks replay truth unnecessarily, keep only stable placeholder substitutions

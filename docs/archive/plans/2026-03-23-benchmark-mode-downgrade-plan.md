# 2026-03-23 Benchmark Mode Downgrade Plan

## Goal

Make `interactive_governed` the only effective runtime mode while silently downgrading legacy `benchmark_autonomous` input.

## Grade

- Internal grade: M

## Work Batches

### Batch 1: Governance freeze
- Create requirement doc
- Create plan doc

### Batch 2: TDD guardrail
- Update the runtime bridge test to invoke legacy `benchmark_autonomous`
- Assert that the runtime summary and artifacts report `interactive_governed`
- Run the targeted test and confirm it fails before production edits

### Batch 3: Runtime normalization
- Update `scripts/runtime/VibeRuntime.Common.ps1` with a single mode-normalization helper
- Update `scripts/runtime/invoke-vibe-runtime.ps1` to accept legacy input but normalize immediately
- Update `scripts/runtime/Freeze-RuntimeInputPacket.ps1` and dependent runtime paths to use the normalized mode
- Keep legacy compatibility internal and silent

### Batch 4: Contract and verification alignment
- Update `config/runtime-modes.json` to describe one official mode plus the legacy compatibility alias
- Update `SKILL.md` so the public contract states that `interactive_governed` is the default and effective mode
- Update `tests/runtime_neutral/test_governed_runtime_bridge.py`
- Update `scripts/verify/vibe-governed-runtime-contract-gate.ps1`

### Batch 5: Verification
- Run targeted runtime bridge tests
- Run governed runtime contract gate if PowerShell is available
- Run `git diff --check`

### Batch 6: Phase cleanup
- Remove temporary artifacts created during verification if any
- Leave only intended source and documentation changes in git status

## Rollback Rules

- If normalization breaks runtime execution, revert the mode helper and restore direct mode passthrough first.
- If gate expectations change without matching runtime behavior, runtime truth wins and the gate must be updated to match it.
- If compatibility input unexpectedly drives unattended behavior after the change, stop and fix that before completion.

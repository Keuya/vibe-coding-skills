# 2026-04-01 PR94 Follow-up Lock And Reference Fixes Plan

## Goal

Patch the remaining stale bundled-mirror assumptions that survived PR `#94`.

## Grade

- Internal grade: L

## Batches

### Batch 1: Freeze follow-up governance
- Record the bounded requirement and plan for the PR review fix batch

### Batch 2: Lock and gate alignment
- Update gate logic so bundled-only lock semantics no longer require canonical `vibe`
- Regenerate `config/skills-lock.json` without the stale `vibe` bundled entry

### Batch 3: Reference contract correction
- Rewrite `references/mirror-topology.md` to describe canonical-only repo topology plus generated compatibility boundaries

### Batch 4: Verification
- Run targeted unit tests for offline skills behavior
- Re-run metadata, offline-skills, and mirror-retirement verification on the real repo

## Verification Commands

- `python3 -m pytest tests/runtime_neutral/test_offline_skills_gate.py -q`
- `pwsh -NoProfile -File ./scripts/verify/vibe-offline-skills-gate.ps1`
- `pwsh -NoProfile -File ./scripts/verify/skill-metadata-gate.ps1`
- `python3 -m pytest tests/runtime_neutral/test_bundled_runtime_mirror.py tests/runtime_neutral/test_retired_tracked_mirror_packaging_gates.py -q`

## Rollback Rules

- If a gate change weakens detection of stale bundled lock entries, keep the old failure behavior for stale entries and only relax the canonical `vibe` case
- If the reference update conflicts with live governance JSON or gates, prefer code and gate truth over prose and update prose again

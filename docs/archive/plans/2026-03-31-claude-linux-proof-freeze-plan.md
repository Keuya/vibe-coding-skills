# 2026-03-31 Claude Linux Proof Freeze Plan

## Goal

Freeze enough Linux evidence to promote `claude-code/linux` from `not-yet-proven` to `supported-with-constraints` without overclaiming broader parity.

## Grade

- Internal grade: M

## Batches

### Batch 1: Freeze target and inspect truth surfaces
- Create a governed requirement doc
- Create a governed execution plan
- Confirm the current blocker is proof freezing, not missing Linux adapter logic

### Batch 2: Capture Linux proof evidence
- Run a fresh Linux install/check path for `claude-code`
- Run doctor and coherence follow-up checks against the same target root
- Capture a real Claude CLI smoke result on Linux

### Batch 3: Freeze bundle and synchronize truth
- Add the captured artifacts to a versioned proof-bundle surface
- Update `adapters/claude-code/platform-linux.json`
- Update replay truth and status docs to match the new measured state

### Batch 4: Verify and close
- Run targeted tests and truth gates
- Keep Windows and macOS unchanged
- Leave a final no-overclaim summary of what Linux now guarantees and what it still does not

## Verification Commands

- `bash ./install.sh --host claude-code --profile full --target-root <temp-root>`
- `bash ./check.sh --host claude-code --profile full --target-root <temp-root> --deep`
- `pwsh -NoProfile -ExecutionPolicy Bypass -File ./scripts/verify/vibe-bootstrap-doctor-gate.ps1 -TargetRoot <temp-root> -WriteArtifacts`
- `python3 ./scripts/verify/runtime_neutral/coherence_gate.py --target-root <temp-root> --write-artifacts`
- `claude --version`
- targeted runtime-neutral tests

## Rollback Rules

- If fresh Linux install/check fails, stop and fix the implementation before changing any status surface
- If the CLI smoke cannot be captured truthfully, keep `claude-code/linux` below promotion
- If replay or status sync would overclaim beyond the measured Linux proof, keep the lane conservative

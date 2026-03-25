# 2026-03-22 Claude Preview Non-Destructive Install Plan

## Goal

Remove destructive write behavior from the Claude preview lane by separating preview example settings from real host settings.

## Grade

- Internal grade: M

## Batches

### Batch 1: Freeze and evidence
- Create requirement doc
- Create execution plan
- Capture current destructive paths and contract mismatch

### Batch 2: Regression tests first
- Add shell regression test for scaffold behavior
- Add PowerShell regression test for scaffold behavior
- Assert existing `settings.json` is preserved
- Assert preview settings file is written separately

### Batch 3: Implementation
- Update `scripts/bootstrap/scaffold-claude-preview.sh`
- Update `scripts/bootstrap/scaffold-claude-preview.ps1`
- Update `scripts/install/install_vgo_adapter.py`
- Update `scripts/install/Install-VgoAdapter.ps1`
- Update `check.sh` and `check.ps1`
- Update preview messages in `one-shot-setup.sh` and `one-shot-setup.ps1`
- Update `adapters/claude-code/closure.json`

### Batch 4: Truth docs
- Update `docs/deployment.md`
- Update `docs/install/recommended-full-path.md`
- Update `docs/install/recommended-full-path.en.md`
- Update `docs/cold-start-install-paths.md`
- Update any other doc that still claims preview writes `settings.json`

### Batch 5: Verification and cleanup
- Run targeted regression tests
- Run script syntax/parse checks
- Run `git diff --check`
- Remove temporary test artifacts
- Write phase cleanup receipt

## Rollback Rules

- If preview file naming causes downstream confusion, keep the non-destructive rule and rename the preview file before merge.
- If PowerShell behavior diverges from shell behavior, block completion until parity is restored.

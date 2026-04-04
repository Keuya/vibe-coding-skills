# 2026-03-22 Supported Host Scope Reduction Plan

## Goal

Reduce the effective and public support surface to `codex` and `claude-code` only, so the repository's install story matches what is actually supportable.

## Grade

- Internal grade: M

## Work Batches

### Batch 1: Governance freeze
- Create requirement doc
- Create execution plan

### Batch 2: Active host registry contraction
- Update `adapters/index.json` to register only `codex` and `claude-code`
- Keep alias handling aligned with the reduced host set

### Batch 3: Install/bootstrap/check contraction
- Update `install.sh`
- Update `check.sh`
- Update `scripts/bootstrap/one-shot-setup.sh`
- Update `install.ps1`
- Update `check.ps1`
- Update `scripts/common/vibe-governance-helpers.ps1`
- Keep host prompts, default target roots, and mismatch errors aligned with the two-host scope

### Batch 4: Public documentation contraction
- Update `README.md`
- Update `README.en.md`
- Update `docs/install/one-click-install-release-copy.md`
- Update `docs/install/one-click-install-release-copy.en.md`
- Update `docs/install/manual-copy-install.md`
- Update `docs/install/manual-copy-install.en.md`
- Update `docs/install/recommended-full-path.md`
- Update `docs/install/recommended-full-path.en.md`
- Update `docs/cold-start-install-paths.md`
- Update `docs/cold-start-install-paths.en.md`
- Update `docs/deployment.md`

### Batch 5: Verification
- JSON parse validation for `adapters/index.json`
- `bash -n` checks for edited shell scripts
- PowerShell parse checks for edited `.ps1` files
- targeted grep audit to confirm unsupported hosts are gone from the active public install surface
- `git diff --check`

### Batch 6: Phase cleanup
- remove temporary verification files if any are created
- audit repo for accidental temp artifacts
- leave only intentional source/doc changes in git status

## Rollback Rules

- If restricting the registry breaks adapter resolution for supported hosts, restore registry entries only after first proving a narrower resolver-safe alternative.
- If PowerShell helper contraction causes host resolution regressions for `codex` or `claude-code`, revert the helper change and implement host restriction at the caller layer instead.
- If docs and scripts diverge, script truth wins and docs must be corrected before completion.

# 2026-03-26 OpenCode Documentation Refresh Plan

## Goal

Refresh all installation-facing documentation so OpenCode preview support is represented consistently, accurately, and with the right proof boundaries.

## Grade

- Internal grade: L

## Batches

### Batch 1: Freeze and traceability

- Create requirement doc
- Create execution plan
- Emit skeleton and intent receipts for the doc-refresh run

### Batch 2: Public entrypoint docs

- Update `README.md`
- Update `README.en.md`
- Update `docs/quick-start.md`
- Update `docs/quick-start.en.md`
- Update `docs/deployment.md`
- Update `docs/cold-start-install-paths.md`
- Update `docs/cold-start-install-paths.en.md`

### Batch 3: Install policy and path docs

- Update `docs/install/one-click-install-release-copy.md`
- Update `docs/install/one-click-install-release-copy.en.md`
- Update `docs/install/manual-copy-install.md`
- Update `docs/install/manual-copy-install.en.md`
- Update `docs/install/recommended-full-path.md`
- Update `docs/install/recommended-full-path.en.md`
- Update `docs/install/host-plugin-policy.md`
- Update `docs/install/host-plugin-policy.en.md`
- Add targeted OpenCode clarifications to related install docs where needed

### Batch 4: Truth and release notes

- Update `docs/universalization/host-capability-matrix.md`
- Add a historical clarification note to `docs/releases/v2.3.36.md`

### Batch 5: Verification and cleanup

- Run formatting for edited markdown files
- Run doc-safe verification commands
- Emit phase execution receipt
- Emit cleanup receipt

## Verification Commands

- `git diff --check`
- `pwsh -NoProfile -File ./scripts/verify/vibe-host-adapter-contract-gate.ps1`
- `pwsh -NoProfile -File ./scripts/verify/vibe-dist-manifest-gate.ps1 -WriteArtifacts`
- `python3 ./scripts/verify/runtime_neutral/opencode_preview_smoke.py --repo-root . --write-artifacts`

## Rollback Rules

- If any doc change would imply one-shot bootstrap support for OpenCode, revert the wording and keep the doc on direct install/check only.
- If a wording update conflicts with current manifests or proof artifacts, prefer the verified manifest/proof truth rather than polishing language.
- If README changes conflict with unrelated user edits, narrow the patch to the specific install sections only.

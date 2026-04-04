# 2026-04-05 Aggressive Repo Slimming Wave 1 Plan

## Goal

Land a first high-visibility deletion wave that materially reduces tracked historical clutter while keeping current repo behavior unchanged.

## Requirement Doc

- [`../requirements/2026-04-05-aggressive-repo-slimming-wave1.md`](../requirements/2026-04-05-aggressive-repo-slimming-wave1.md)

## Internal Grade

L serial governed execution.

This wave is wide enough to need explicit sequencing, but the write scope is still concentrated enough to keep execution in one native lane.

## Frozen Scope

### Delete

- all archived leaf files under `docs/archive/plans/` except `README.md`
- all archived leaf files under `docs/archive/requirements/` except `README.md`
- all files under `references/fixtures/anti-proxy-goal-drift/`
- zero-consumer raw logs and receipt inventories under `references/proof-bundles/linux-full-authoritative-candidate/`

### Update

- `docs/archive/README.md`
- `docs/archive/plans/README.md`
- `docs/archive/requirements/README.md`
- `references/proof-bundles/README.md`
- `references/proof-bundles/linux-full-authoritative-candidate/manifest.json`
- `references/fixtures/README.md`
- `references/fixtures/consumer-ledger.md`
- `docs/status/repo-slimming-refresh-path-role-matrix.md`

### Add

- this plan
- the paired requirement doc

## Architecture Rule

This wave deletes only files that are already outside live semantic ownership.

- archived plans and requirements are not current execution authority
- anti-proxy fixture samples are no longer backed by a live gate family
- Linux proof raw logs are not the semantic contract; manifest, operation record, and runtime freshness receipts are

## Execution Steps

### Step 1: Freeze Retention Semantics

- add the new requirement and plan docs
- update archive / fixture / proof READMEs so the post-wave state has an explicit rule

### Step 2: Shrink the Linux Proof Bundle Contract

- reduce `required_files` in `references/proof-bundles/linux-full-authoritative-candidate/manifest.json`
- keep only `installed-runtime-outputs/runtime-freshness-receipt.json` as the contract-required tracked run artifact
- preserve operation records and top-level manifest / README

### Step 3: Delete Zero-Reference Historical Leaves

- delete `docs/archive/plans/*.md` except `README.md`
- delete `docs/archive/requirements/*.md` except `README.md`

### Step 4: Delete Dead Historical Fixture Family

- delete `references/fixtures/anti-proxy-goal-drift/*`
- update fixture README and consumer ledger from retained-pending-decision to retired-from-live-surface wording

### Step 5: Delete Linux Proof Raw Logs

- delete:
  - `bootstrap-doctor.log`
  - `check.log`
  - `coherence.log`
  - `command-log.txt`
  - `environment.log`
  - `install.log`
  - `provision.log`
  - `receipt-files.txt`
- keep:
  - `operation-record.md`
  - `installed-runtime-outputs/runtime-freshness-receipt.json`

## Verification

- `git diff --check`
- `rg -n "docs/archive/(plans|requirements)/" README.md docs references scripts tests config packages adapters core .github`
- `rg -n "anti-proxy-goal-drift" README.md docs references scripts tests config packages adapters core .github`
- `python3 -m pytest tests/integration/test_proof_bundle_manifest_contract.py tests/runtime_neutral/test_outputs_boundary_migration.py tests/runtime_neutral/test_runtime_contract_goldens.py -q`

## Rollback

- one revert of the wave commit restores all historical leaves and raw proof artifacts
- no package or runtime migration is required for rollback because this wave does not alter semantic behavior

## Phase Cleanup

- remove any temporary audit files created during execution
- audit node processes but do not kill non-repo workloads
- leave the worktree clean except for the intended tracked changes

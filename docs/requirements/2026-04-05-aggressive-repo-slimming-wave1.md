# 2026-04-05 Aggressive Repo Slimming Wave 1

## Goal

Execute a visibly stronger repository-slimming wave that performs real tracked-file deletion rather than mostly regrouping, while preserving current runtime, install, release, adapter, and verification behavior.

## Deliverable

A first aggressive slimming batch that:

- removes zero-reference historical leaves from `docs/archive/plans/` and `docs/archive/requirements/`
- retires the zero-consumer `references/fixtures/anti-proxy-goal-drift/` family from the live repo
- shrinks `references/proof-bundles/linux-full-authoritative-candidate/` to a minimum tracked proof surface
- updates the surviving index, manifest, and retention documents so the remaining repo truth stays coherent

## Constraints

- Work in `/home/lqf/table/table9/Vibe-Skills-main`.
- Preserve live entry surfaces under `docs/README.md`, `docs/plans/README.md`, `docs/requirements/README.md`, `docs/releases/README.md`, and `references/proof-bundles/README.md`.
- Do not change runtime, installer, router, adapter, or package-owned semantic behavior.
- Keep manifest-level proof truth and receipt-level runtime truth explicit after trimming.
- Do not delete any file that still has an active repo path consumer unless the consumer is updated in the same wave.

## Evidence Snapshot

Current repo evidence collected for this wave:

- `docs/archive/plans/`: `144` leaf files, `144` with zero exact-path repo references, about `551 KB`
- `docs/archive/requirements/`: `90` leaf files, `90` with zero exact-path repo references, about `176 KB`
- `references/fixtures/anti-proxy-goal-drift/`: `21` files, `21` with zero exact-path repo references, about `15 KB`
- `references/proof-bundles/linux-full-authoritative-candidate/`: `21` files total, `18` zero-reference raw logs / inventories, about `353 KB`

These are the strongest safe deletion candidates currently visible in the repo because they are already archived, historical, or explicitly outside the live runtime and install surface.

## Scope

### In Scope

- deleting archived dated plan leaves from `docs/archive/plans/`
- deleting archived dated requirement leaves from `docs/archive/requirements/`
- deleting `references/fixtures/anti-proxy-goal-drift/*`
- deleting zero-consumer raw logs and receipt inventories from the live Linux proof bundle
- updating archive and retention READMEs
- updating the Linux proof-bundle manifest to match the reduced tracked proof surface

### Out of Scope

- `docs/archive/releases/`
- `scripts/setup/**` and `scripts/research/**`
- `bundled/skills/**`
- `scripts/runtime/**`, `scripts/router/**`, `scripts/install/**`, `scripts/verify/**`
- `packages/**`, `core/**`, `adapters/**`, `dist/**`, `tests/**`

## Acceptance Criteria

1. All archived leaf files under `docs/archive/plans/` are removed except the index README.
2. All archived leaf files under `docs/archive/requirements/` are removed except the index README.
3. The live fixture family `references/fixtures/anti-proxy-goal-drift/` is removed and its ledger / README wording is updated.
4. The live Linux proof bundle keeps only manifest, README, operation records, and contract-required runtime receipts.
5. Surviving README and index docs clearly explain that deleted historical leaves are recoverable via git history rather than remaining tracked in the live repo tree.
6. `tests/integration/test_proof_bundle_manifest_contract.py` still passes after the proof-bundle reduction.
7. No runtime or install behavior claim is made beyond the targeted evidence gathered in this wave.

## Product Acceptance Criteria

This wave is acceptable only if:

1. The repository shrinks by a materially visible tracked-file count, not just by path regrouping.
2. Active navigation remains usable through the surviving index pages.
3. Historical traceability remains possible through git history and surviving manifests / READMEs.
4. The live proof surface becomes smaller without breaking manifest contract checks.
5. The live fixture surface no longer keeps a family that has no active repo consumer.

## Manual Spot Checks

- Open `docs/archive/README.md`, `docs/archive/plans/README.md`, and `docs/archive/requirements/README.md` and confirm the archive rules now describe index-only retention correctly.
- Open `references/proof-bundles/README.md` and `references/proof-bundles/linux-full-authoritative-candidate/manifest.json` and confirm the reduced proof surface is intentional and coherent.
- Open `references/fixtures/README.md` and `references/fixtures/consumer-ledger.md` and confirm the anti-proxy fixture family is no longer described as retained live.
- Confirm `docs/README.md`, `docs/plans/README.md`, and `docs/requirements/README.md` still point only to active navigation surfaces.

## Completion Language Policy

- This wave may claim only that the targeted historical and low-signal surfaces were removed and that the listed targeted verification passed.
- It must not claim blanket no-regression for the entire repository.

## Delivery Truth Contract

- Truth for this wave is limited to file-surface reduction, manifest consistency, and targeted verification evidence.
- Broader repository safety remains governed by later waves and their own verification.

## Non-Goals

- No bundled payload slimming in this wave.
- No broad verify-script consolidation in this wave.
- No third-party mirror or source-root refactor in this wave.
- No release-history deletion in this wave.

## Inferred Assumptions

- The maintainer prefers visible deletion over another mostly-regrouping PR.
- Git history is an acceptable recovery path for deep historical leaves that are no longer part of the live repo surface.
- Archive indexes are sufficient for discoverability once the archived leaf corpus is removed from the tracked tree.

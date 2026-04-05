# 2026-04-05 Aggressive Root Pruning Wave 2

## Goal

Execute a stronger root-pruning wave that removes selected top-level directories and personal wave-planning residue, even when that requires retiring previously supported low-value surfaces.

## Deliverable

A verified repository cleanup that:

- removes the root `benchmarks/` sample baseline family
- removes the root `hooks/` family and retires repo-managed Claude write-guard hook support
- deletes selected personal 2026-04-05 repo-slimming wave documents
- updates installer, verification, adapter, manifest, and documentation surfaces so the repository remains internally coherent after the removals

## Constraints

- Work in `<repo-root>`.
- Preserve a functioning install/check path after removing hook support.
- Do not leave dangling exact-path references to deleted root directories.
- Delete only wave documents that are local planning / outcome residue rather than long-lived public product documentation.

## In Scope

- `benchmarks/**`
- `hooks/**`
- benchmark-coupled workflow acceptance scenarios and tests
- Claude managed hook installer/check/manifests/docs references
- selected 2026-04-05 slimming wave requirement / plan / status docs

## Out Of Scope

- broader adapter redesign beyond removing managed hook claims
- full distribution-lane simplification beyond the required caller updates
- deleting general release or architectural history outside the specified wave-doc set

## Acceptance Criteria

1. Root `benchmarks/` is removed and no active test or verification path still requires it.
2. Root `hooks/` is removed and no active install/check/adapter/manifests path still claims or expects repo-managed hook payload.
3. Selected 2026-04-05 wave documents are removed without leaving broken self-references.
4. Targeted verification passes after the deletions.
5. The final root directory count is lower than before this wave.

## Product Acceptance Criteria

1. The root directory becomes visibly shorter than after wave 1.
2. Public docs and adapter contracts stop overclaiming Claude managed hook behavior that no longer exists.
3. The remaining root surfaces better reflect current supported product behavior rather than internal cleanup scaffolding.

## Manual Spot Checks

- Confirm `benchmarks/` and `hooks/` are absent from the root.
- Confirm `check.sh --host claude-code` no longer expects managed hook payload.
- Confirm Claude adapter docs/manifests now describe settings-only support rather than settings-plus-hook support.

## Completion Language Policy

- Completion claims are limited to root pruning wave 2 and the targeted verification performed here.
- No claim may imply that all root-directory simplification work is complete.

## Delivery Truth Contract

- This wave intentionally removes some previously supported repository-managed surfaces.
- Truth after this wave is defined by the updated installer, verification, adapter, and distribution sources rather than historical docs.

## Non-Goals

- no partial hook deletion that leaves stale contract language behind
- no benchmark-path stubs kept only to preserve old wording
- no retention of personal wave ledgers just for audit vanity

## Inferred Assumptions

- “基线测试模块” refers to the tracked root benchmark sample family and its benchmark-coupled acceptance scenarios.
- “我个人的工作文档wave内容” refers to the 2026-04-05 repo-slimming requirement / plan / outcome ledger artifacts created during the recent cleanup waves.

# 2026-04-04 Strong Repo Slimming Program

## Goal

Design a strong repository-slimming program for the latest `main` checkout that materially reduces historical noise, stale documents, oversized snapshots, dead scripts, and compatibility-era clutter while preserving runtime behavior, installer behavior, verification coverage, and release integrity.

## Deliverable

A governed slimming requirement packet and an executable plan that classify the repository into:

- safe-to-prune or archive-first surfaces
- contract-first refactor surfaces that must shrink only after ownership is clarified
- protected surfaces that must not be slimmed until downstream callers are removed or migrated

## Constraints

- Plan against the latest `origin/main` worktree in `/home/lqf/table/table9/Vibe-Skills-main`.
- Preserve install, check, release, runtime, adapter, verification, and catalog behavior.
- Do not treat generated compatibility projections as semantic owners.
- Prefer archiving, partitioning, or manifest-driven generation over destructive removal when live consumers still exist.
- Keep the repository aligned with high cohesion and low coupling principles:
  - one semantic owner per concern
  - thin compatibility shims
  - dated material separated from active entry surfaces
  - generated or reproducible payloads separated from long-lived canonical sources

## Current Evidence Snapshot

Current main-branch inventory observed during planning:

- `bundled/`: about `30M`
- `references/`: about `5.6M`
- `docs/`: about `3.6M`
- `scripts/`: about `3.4M`
- `bundled/skills/*`: `339` top-level skill directories
- `scripts/verify/*`: `205` files
- `docs/plans/*`: `169` files
- `docs/requirements/*`: `136` files
- `references/proof-bundles/*`: `43` files
- `references/fixtures/*`: `45` files

## Acceptance Criteria

1. The plan names the highest-value slimming targets with concrete path families and a risk tier for each.
2. The plan distinguishes immediate archive or deletion candidates from contract-first refactors and protected surfaces.
3. The plan preserves functional behavior by requiring path-reference audits, targeted regression tests, and rollback boundaries before destructive changes.
4. The plan provides a wave structure that can be executed as reviewable, low-blast-radius PR batches rather than one large cleanup.
5. The plan includes explicit rules for historical docs, reference snapshots, scripts, proof bundles, and bundled skill payloads.

## Product Acceptance Criteria

The slimming program is acceptable only if:

1. Maintainers can explain which paths are canonical source, compatibility projection, archive, fixture, or proof surface without ambiguity.
2. Public entry surfaces become simpler, while active runtime and installer behavior remain unchanged.
3. Historical material no longer crowds active navigation surfaces.
4. Large reproducible or low-signal assets gain a clear retention rule instead of remaining indefinitely by default.
5. Every proposed strong cut has a corresponding verification and rollback rule.

## Manual Spot Checks

- Open `docs/README.md`, `docs/plans/README.md`, `docs/requirements/README.md`, and `docs/releases/README.md` and confirm active surfaces are still discoverable after slimming.
- Check that installer-facing docs still point to the correct host and distribution surfaces.
- Confirm no plan recommends deleting `dist/*`, package-owned semantic cores, or active verification contracts without a migration owner.
- Confirm archive recommendations do not break links from current README, release, or status spines.

## Completion Language Policy

- This planning run may claim only that a slimming program has been produced and grounded in repository evidence.
- It must not claim that the repository has already been slimmed, simplified, or regression-safe after execution.
- Any future implementation batch must earn its own verification evidence before stronger completion language is used.

## Delivery Truth Contract

- Planning truth is authoritative only for classification, sequencing, and risk boundaries.
- Implementation truth remains pending until each slimming wave is executed and verified.

## Non-Goals

- No blanket deletion of `bundled/skills`, `dist`, `packages`, `tests`, or `outputs` contracts in this planning phase.
- No feature expansion, branding rewrite, or unrelated functional refactor.
- No silent promotion of convenience metrics such as raw file-count reduction over semantic clarity and safety.

## Inferred Assumptions

- The maintainer wants aggressive slimming, but not at the cost of runtime, release, or installer regressions.
- Historical documentation density is currently harming navigation and maintenance more than it is helping current contributors.
- Some large tracked assets remain because there was no retention policy, not because they are still the best source of truth.

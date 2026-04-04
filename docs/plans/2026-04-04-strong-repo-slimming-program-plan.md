# 2026-04-04 Strong Repo Slimming Program Plan

## Goal

Produce a strong but safe slimming roadmap for the latest `main` checkout, reducing stale and low-signal repository surfaces while preserving behavior and clarifying ownership boundaries.

## Requirement Doc

- [`../requirements/2026-04-04-strong-repo-slimming-program.md`](../requirements/2026-04-04-strong-repo-slimming-program.md)

## Internal Grade

XL wave-sequential planning and later execution.

The repo has enough breadth and coupling that implementation should happen in reviewable waves, with bounded parallel audit work only where write scopes do not overlap.

## Architectural Lens

Strong slimming in this repository must follow four owner rules:

1. semantic owners live in package-owned cores or config-owned contracts
2. compatibility shims stay thin and must not keep second truth surfaces alive
3. active navigation surfaces stay short and current
4. reproducible snapshots and historical packets need explicit retention policy, not indefinite default retention

## Core Design Rules

The program must preserve high cohesion and low coupling through explicit path roles.

### Path Role Taxonomy

Every candidate path must be classified into exactly one primary role:

| Role | Meaning | Allowed Operations | Forbidden Operations |
| --- | --- | --- | --- |
| canonical source | semantic owner of behavior or contract | refactor, split by module, add tests | replace with generated projection, duplicate semantics elsewhere |
| generated projection | generated or compatibility-facing derivative | regenerate, move, re-materialize, slim duplicates | let it become the only truth surface |
| compatibility shim | thin bridge to protect callers during migration | narrow, delegate, delete after callers are gone | keep inline semantic ownership |
| fixture / proof | evidence or regression baseline | retain only what tests or contracts consume | keep bulky historical payload without retention policy |
| archive | historical but still recoverable material | move behind archive index, compress, de-emphasize | crowd active navigation surfaces |
| dead surface | no active consumers and no retention value | delete | keep “just in case” without an owner |

### Cohesion Rules

- One semantic owner per concern.
- Policy lives in `config/**`, semantic code lives in `packages/**` or `core/**`, execution wrappers stay thin.
- Active docs should explain current behavior, not carry historical execution transcripts.
- Fixtures and proof bundles must exist only when they back a real test, contract, or release requirement.

### Coupling Reduction Rules

- Delete or archive consumers only after reference scans prove no active callers.
- Prefer manifest-driven allowlists over broad directory scanning.
- Prefer family-level overview docs plus archive indexes over many parallel leaf pages at the root.
- Do not allow release, runtime, or install behavior to depend on historical docs remaining in active locations.

## Repository Classification

### Tier A: Immediate High-Value Slimming Candidates

These surfaces are the best first cuts because they are large, noisy, and mostly historical or reproducible.

- `docs/plans/**`
  - Problem: `169` dated files, heavy historical noise, many old implementation transcripts, and absolute local path leakage.
  - Strategy: move all non-active dated plans and reports into an archive subtree with a short index; keep only active entries in `docs/plans/README.md`.
- `docs/requirements/**`
  - Problem: `136` frozen requirements, many tied to one-off README, release, or delivery tasks long after closure.
  - Strategy: retain only active or recently referenced requirement docs in the live directory; archive historical packets behind an index.
- `docs/releases/**`
  - Problem: active release navigation and historical version records are mixed too closely.
  - Strategy: keep the current governed release surface and recent versions live; move older release notes and packet artifacts into an archive-oriented layout.
- `references/changelog.md`
  - Problem: still useful as a stable path, but too large and full of historical path mentions.
  - Strategy: split into current window plus archive volumes while preserving the canonical top-level path.
- `references/awesome-mcp-servers.snapshot.json`
  - Problem: very large tracked snapshot with low evidence that it must remain fully tracked as canonical source.
  - Strategy: replace with a generated or reduced snapshot policy; keep provenance and generation command, not necessarily the full tracked blob.

### Tier B: Archive-First or Shrink-by-Policy Surfaces

- `references/proof-bundles/**`
  - Keep manifests, README, and summary receipts.
  - Demote raw logs, absolute-path receipts, and bulky historical detail to archive assets or generated bundles.
- `references/fixtures/**`
  - Keep fixtures that tests actively consume.
  - Remove or archive fixture families that no longer back a test or policy.
- `docs/changes/**` and historical migration or rollout reports under `docs/*.md`
  - Consolidate by family or move behind archive indexes.
- legacy standalone governance or integration notes that duplicate newer family docs
  - Merge into a family overview or replace with a short redirect note.

### Tier C: Contract-First Refactor Before Slimming

- `scripts/verify/**`
  - Problem: high file count, but active contract surface.
  - Strategy: merge thin wrappers only after shared assertion, artifact, and contract plumbing is extracted.
- `scripts/governance/**`, `scripts/runtime/**`, `scripts/router/**`
  - Problem: some ownership duplication remains, but these are live execution surfaces.
  - Strategy: continue owner-to-consumer cutovers first; delete only dead wrappers after proof.
- `third_party/system-prompts-mirror` and `third_party/vco-ecosystem-mirror`
  - Problem: still treated as local default evidence roots.
  - Strategy: parameterize roots via config and scripts before any shrinkage.
- `bundled/skills/**`
  - Problem: largest payload, but still installer and packaging input.
  - Strategy: introduce release-tier payload partitions before attempting any broad removal.

### Tier D: Protected Surfaces

These should not be part of a strong deletion wave until deeper cutovers happen first.

- `dist/**`
- `packages/**`
- `core/**`
- `adapters/**`
- `tests/runtime_neutral/**`
- `tests/integration/**`
- `config/outputs-boundary-policy.json` and its dependent migration fixtures

## Candidate Retention Policy

### Keep Live

- any path consumed by installer, runtime, release, adapter, verification, or catalog contracts
- active status / proof / release navigation spines
- package-owned semantic code and config-owned policy

### Archive Behind Index

- dated plans, dated requirement packets, old release notes, migration reports, postmortems, review reports
- proof logs and bulky receipts that are still useful historically but not needed on the active surface

### Generate On Demand

- large third-party snapshots
- bulky compatibility projections that can be reconstructed from config and manifests
- any raw evidence artifact whose manifest and summary are sufficient for repository truth

### Delete

- dead scripts with zero active references
- duplicate docs replaced by a canonical family overview
- obsolete fixtures or proof artifacts with no test, config, doc, or adapter consumer

## Explicit Risk Map

### Low Risk

- archive or relocate dated docs with no active README or test dependencies
- remove absolute local path leakage from historical docs
- split oversized historical ledgers into current plus archive volumes
- delete dead helper scripts with zero active consumers

### Medium Risk

- reorganize release-history and proof-bundle layout
- trim fixtures whose callers are ambiguous
- merge overlapping governance docs into family overviews

### High Risk

- bundled skill payload reduction
- verify gate consolidation without contract extraction
- third-party mirror removal before parameterization
- anything that changes installer packaging defaults or runtime freshness contracts

## Wave Structure

### Wave 0: Inventory Freeze and Guardrails

- generate a path-classification matrix for `docs`, `references`, `scripts`, `bundled`, and `third_party`
- mark every candidate path as `live`, `archive-first`, `generated`, `fixture`, or `dead`
- add a pruning policy note so future cleanup does not recreate ambiguity

Ownership boundaries:

- writes limited to planning docs, census docs, and maybe a new retention-policy doc
- no runtime, installer, or release logic changes

Deliverables:

- path-role matrix
- keep / archive / generate / delete candidate ledger
- batch backlog with risk labels

Verification:

- `rg -n "/home/lqf/table|Plan complete and saved to|Two execution options:" docs/plans docs/requirements docs/releases -g '*.md'`
- `rg -n "bundled/skills|references/proof-bundles|references/changelog.md|docs/plans/|docs/requirements/" README.md docs scripts packages tests config adapters core dist .github -g '!node_modules/**'`

### Wave 1: Historical Docs Spine Reduction

- archive non-active `docs/plans/**`
- archive non-active `docs/requirements/**`
- archive or regroup stale migration reports, batch reports, and historical rollout notes from `docs/*.md`
- normalize README navigation to point only at active surfaces

Ownership boundaries:

- `docs/plans/**`
- `docs/requirements/**`
- selected historical `docs/*.md`
- `docs/README.md`, `docs/plans/README.md`, `docs/requirements/README.md`, `docs/releases/README.md`

Batch decomposition:

1. `docs/plans` archive cut
2. `docs/requirements` archive cut
3. root historical reports regrouping
4. README/index cleanup

Expected outcome:

- active docs spine becomes smaller and more legible without losing recoverability

Verification:

- `git diff --check -- docs`
- `rg -n "/home/lqf/table" docs -g '*.md'`
- targeted README and index spot checks

### Wave 2: Release and Ledger Surface Compression

- split `references/changelog.md` into current plus archive volumes
- move older release notes out of the active release surface
- keep `docs/releases/README.md` focused on current release, proof handoff, and recent governed versions

Ownership boundaries:

- `references/changelog.md` and new archive volumes
- `docs/releases/**`
- release navigation indexes only

Batch decomposition:

1. changelog split with canonical-path preservation
2. release-note archive cut
3. release README compression

Verification:

- release README link scan
- release-cut contract tests
- changelog path contract checks

### Wave 3: Proof Bundle and Snapshot Retention Reform

- define what a tracked proof bundle must contain
- externalize or archive oversized raw logs and low-signal detail
- replace tracked mega-snapshots with reproducible generation rules when feasible

Ownership boundaries:

- `references/proof-bundles/**`
- `references/fixtures/**` only where clearly unconsumed
- `references/awesome-mcp-servers.snapshot.json`
- docs/config/scripts that define retention policy or generation instructions

Batch decomposition:

1. proof-bundle minimum tracked schema
2. proof-bundle raw-log demotion
3. snapshot generation / reduction policy

Verification:

- proof-bundle manifest consumers still pass
- adapters and replay fixtures still resolve manifests
- no active script assumes a removed raw artifact path

### Wave 4: Dead Script Retirement and Verify Surface Consolidation

- retire scripts with zero active consumers
- consolidate thin verification wrappers after shared helpers are extracted
- remove deprecated setup or research helpers that no longer back current flows

Ownership boundaries:

- `scripts/setup/**`
- `scripts/research/**`
- dead paths under `scripts/governance/**` and `scripts/verify/**`
- limited supporting doc/reference edits

Batch decomposition:

1. dead helper retirements
2. verify wrapper family consolidation
3. setup / research surface cleanup

Verification:

- exact-path reference audit for deleted scripts
- targeted pytest suites covering release, runtime, installer, and verification bridges
- `git diff --check`

### Wave 5: Payload Partitioning for Bundled Skills

- define `core`, `profile-required`, and `optional` skill inventories
- move packaging to manifest-driven allowlists where possible
- only then consider strong reductions in tracked bundled payload

Ownership boundaries:

- `config/runtime-core-packaging*.json`
- installer and catalog consumers
- `bundled/skills/**`
- tests that freeze packaging semantics

Batch decomposition:

1. introduce explicit inventory tiers
2. migrate packaging to tier-aware allowlists
3. shrink optional bundled payload only after coverage is green

### Wave 6: Third-Party Root Decoupling

- parameterize mirror roots now treated as fixed local evidence sources
- move research helpers away from hardcoded mirror assumptions
- document supported external checkout or fetch-time behavior

Ownership boundaries:

- `third_party/**`
- `scripts/research/**`
- `config/upstream-corpus-manifest.json`
- docs or examples that hardcode mirror paths

### Wave 7: Final Consistency and Residual-Risk Closure

- refresh path dependency census
- refresh docs information architecture and retention policy docs
- rerun cross-surface regression
- document what remains intentionally retained and why

Verification:

- installer-core packaging tests
- catalog consumption tests
- offline or freshness-related skill lock tests

## Candidate Actions by Path Family

### `docs/plans/**`

- keep only active root and microphase plans live
- archive dated execution transcripts, closure reports, and completed technical-debt plans
- remove local absolute path leakage and “Plan complete and saved to ...” boilerplate from any page that stays live

### `docs/requirements/**`

- keep only active or recently relevant requirement packets live
- archive closed release, README, rename, and one-off delivery requirements
- keep filename stability inside archive so history remains traceable

### `docs/releases/**`

- keep current version and recent governed release window live
- archive older notes and historical packetization artifacts
- preserve `docs/releases/README.md` as the active release navigator

### `references/**`

- split current ledgers from deep history
- retain only test-backed fixtures and contract-backed proof manifests in the main repo surface
- reduce oversized snapshots to reproducible or summarized forms

### `scripts/**`

- delete only when exact-path and basename scans prove no live consumers
- for active script families, reduce by extracting shared logic first and deleting wrappers second

### `bundled/skills/**`

- do not delete by topical instinct alone
- first classify by installer/runtime requirement tier
- only optional tiers are eligible for later repository shrinkage

### Delete

- dead helper scripts with zero live references
- obsolete historical reports once their content is archived or absorbed
- stale duplicate docs that are neither active navigation nor referenced governance

### Archive

- most dated items in `docs/plans/**`
- most dated items in `docs/requirements/**`
- old release notes beyond the active governed release window
- bulky historical proof logs and migration report packets

### Merge

- overlapping governance family docs under the same theme
- release or migration reports that only repeat an already canonical governance note
- duplicate install or rollout guidance that differs only by historical context

### Keep

- package-owned semantic cores
- distribution manifests and adapter projections
- active proof and status spine
- outputs boundary contracts and fixtures
- active verification bridges and installer/runtime contract tests

## Verification Commands for Future Execution Batches

Minimum batch-level verification:

- `git diff --check`
- `pytest -q tests/integration/test_dist_manifest_generation.py tests/integration/test_release_cut_gate_contract_cutover.py tests/runtime_neutral/test_release_cut_operator.py`
- `pytest -q tests/runtime_neutral/test_outputs_boundary_migration.py tests/integration/test_catalog_contract_consumption.py tests/integration/test_runtime_core_packaging_roles.py`
- targeted `rg` scans proving removed paths have no live consumers

Extended verification by wave:

- doc-heavy waves: README and link scans, plus release and index contract checks
- script-heavy waves: targeted runtime, release, and installer bridge tests
- payload-heavy waves: packaging, catalog, offline skill, and freshness tests

Reference-audit probes that should be reused:

- `rg -n "/home/lqf/table|Plan complete and saved to|Two execution options:" docs -g '*.md'`
- `rg -n "references/changelog.md|references/proof-bundles|docs/plans/|docs/requirements/|bundled/skills|third_party/system-prompts-mirror|third_party/vco-ecosystem-mirror" README.md docs scripts packages tests config adapters core dist .github -g '!node_modules/**'`
- `for f in $(git diff --name-only | rg '^scripts/'); do rg -n --fixed-strings "$f" . -g '!node_modules/**' -g '!outputs/**' || true; done`

Recommended regression matrix by batch type:

| Batch Type | Minimum Tests |
| --- | --- |
| docs-only archive batch | docs link scans, release README checks, `git diff --check` |
| release-surface batch | `tests/integration/test_release_cut_gate_contract_cutover.py`, `tests/runtime_neutral/test_release_cut_operator.py` |
| proof / fixture batch | `tests/runtime_neutral/test_outputs_boundary_migration.py`, replay and manifest consumers |
| script retirement batch | targeted gate / runtime / installer bridge tests for touched families |
| bundled packaging batch | `tests/integration/test_runtime_core_packaging_roles.py`, `tests/integration/test_catalog_contract_consumption.py`, freshness / offline gate coverage |

## PR Strategy

Each implementation PR must satisfy all of the following:

1. one path family or one owner-boundary cut only
2. docs-only and executable/runtime-impacting changes must not be mixed
3. each PR description must state:
   - target family
   - why the cut is safe
   - exact verification commands run
   - retained risks or deferred items
4. each PR must be independently revertible

Preferred PR sequence:

1. archive `docs/plans`
2. archive `docs/requirements`
3. compress `docs/releases` and split changelog
4. proof-bundle retention reform
5. dead script retirements
6. third-party root parameterization
7. bundled payload partitioning

## Rollback Rules

- Every slimming batch must be split so that one PR corresponds to one path family or one owner-boundary cut.
- Do not mix archive-heavy doc changes with runtime or installer changes in the same PR.
- If any candidate deletion is still referenced by active config, tests, adapters, or release surfaces, downgrade from delete to archive or defer.
- If a wave weakens discoverability, restore the previous README or index surface before continuing.
- If a batch changes packaging, runtime freshness, release-cut, or installer behavior, require a dedicated revert path and restore manifest/index surfaces immediately on failure.

## Batch-Level Exit Criteria

No batch may be called complete unless all are true:

1. reference scans show no unintended live callers of removed paths
2. batch-specific tests pass
3. `git diff --check` passes
4. active indexes remain navigable
5. cleanup removed temporary caches and audit residue

## Phase Cleanup Expectations

- remove temporary audit files and test caches after each planning or implementation phase
- audit for worktree-local zombie Node processes before phase close
- keep only intentional docs, config, tests, and scripts in the final diff

## Success Condition

The program is successful only when:

1. active entry surfaces are short and current
2. historical material is still recoverable but no longer crowds active navigation
3. semantic ownership is clearer after each batch, not more fragmented
4. repo size drops through principled removal or externalization, not through accidental contract loss
5. installer, runtime, release, and verification behavior remain regression-backed after every wave

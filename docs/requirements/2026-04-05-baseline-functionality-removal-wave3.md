# 2026-04-05 Baseline Functionality Removal Wave 3

## Goal

Remove the remaining active baseline or benchmark-oriented runtime functionality so the repository no longer ships, verifies, or documents baseline-testing behavior as a supported product surface.

## Deliverable

A verified repository cleanup that:

- removes the legacy `benchmark_autonomous` runtime compatibility surface
- deletes baseline or benchmark proof gates and proof bundles that exist only to support baseline-testing behavior
- replaces benchmark-named live execution policy and proof artifacts with neutral governed execution-proof surfaces
- updates runtime contracts, manifests, scripts, tests, and generated distribution artifacts so the repository remains coherent after the removals
- preserves the supported governed runtime path through `interactive_governed`

## Constraints

- Work in `<repo-root>`.
- Preserve the canonical `vibe` governed runtime and its normal `interactive_governed` flow.
- Do not keep dead compatibility files, dormant scripts, or manifest entries that imply baseline support still exists.
- Keep historical changelog and archival references only when they are clearly non-active historical records.

## In Scope

- `benchmark_autonomous` runtime mode aliases, validators, normalization logic, and unattended-mode references
- migration from `config/benchmark-execution-policy.json` to a neutral live execution-proof policy surface
- baseline or benchmark verification gates and official-runtime baseline proof bundle files
- active manifests, distribution sources, governance boards, and release-cut inputs that reference removed baseline surfaces
- tests and replay fixtures that still exercise removed baseline behavior
- active protocol or README surfaces that still present baseline functionality as current behavior

## Out Of Scope

- deleting historical archive notes that merely describe past releases
- broader runtime redesign unrelated to removing baseline functionality
- unrelated repo slimming outside the already active root-pruning work

## Acceptance Criteria

1. No active runtime entrypoint, config, or host bridge accepts or normalizes `benchmark_autonomous`.
2. No active manifest, distribution source, governance board, or release-cut contract references deleted baseline-only files.
3. Baseline-only proof bundle files and verification scripts are deleted.
4. Tests that remain valuable pass under `interactive_governed`; tests that exist only to prove removed baseline functionality are deleted.
5. Targeted verification passes after the removals.

## Product Acceptance Criteria

1. The repository exposes one governed runtime mode truth surface instead of a retained baseline alias.
2. Verification and documentation stop advertising baseline-testing or official-runtime-baseline functionality as a supported product capability.
3. Repository behavior becomes more cohesive by removing compatibility-only code paths that no longer add user value.

## Manual Spot Checks

- Confirm there is no active `benchmark_autonomous` reference in runtime entrypoints, configs, or non-archival docs.
- Confirm baseline proof bundle files and baseline gate scripts are absent.
- Confirm surviving runtime tests invoke `interactive_governed`.
- Confirm generated manifests no longer list official runtime baseline docs or gates.

## Completion Language Policy

- Completion claims are limited to baseline-functionality removal wave 3 and the verification run performed for this wave.
- No claim may imply that all repository simplification work is finished.

## Delivery Truth Contract

- This wave intentionally breaks backward compatibility for legacy baseline-mode callers.
- After this wave, `interactive_governed` is the only supported governed runtime mode surface.
- Historical archive text may still mention removed baseline functionality, but active runtime and verification surfaces must not.

## Non-Goals

- no soft-deleted aliases that still normalize into the live runtime
- no baseline proof bundle retained for nostalgia
- no test kept solely to prove a deleted compatibility surface

## Inferred Assumptions

- “整体拔除基线测试的内容” means removing both repository content and product behavior that still support baseline or benchmark execution modes.
- Historical archive notes can remain when they are clearly archival and not part of a live contract.

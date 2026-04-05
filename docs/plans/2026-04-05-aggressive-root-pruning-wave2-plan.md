# 2026-04-05 Aggressive Root Pruning Wave 2 Plan

## Goal

Land a visibly stronger root cleanup by deleting `benchmarks/`, deleting `hooks/`, and removing selected 2026-04-05 wave docs while keeping the repository internally coherent.

## Requirement Doc

- [`../requirements/2026-04-05-aggressive-root-pruning-wave2.md`](../requirements/2026-04-05-aggressive-root-pruning-wave2.md)

## Internal Grade

L

The task is broad but tightly coupled. The critical path is shared across installer, verification, manifests, and docs, so serial root-governed execution is safer than parallel edits.

## Ownership Lanes

### Lane A: Benchmark Surface Removal

Write scope:

- `benchmarks/**`
- `tests/scenarios/project_delivery/**`
- workflow-acceptance runtime/support/tests

### Lane B: Hook Surface Retirement

Write scope:

- `hooks/**`
- Claude installer/check surfaces
- Claude adapter contracts and distribution source/manifests
- hook-related tests and public docs

### Lane C: Wave Doc Cleanup

Write scope:

- selected `docs/requirements/**`
- selected `docs/plans/**`
- selected `docs/status/**`

## Execution Steps

### Stage 0: Freeze

- freeze requirement and plan
- map benchmark, hook, and wave-doc consumers

### Stage 1: Remove Benchmark Family

- delete `benchmarks/**`
- remove benchmark manifest expectations from workflow-acceptance logic and tests
- delete benchmark-coupled scenario references

### Stage 2: Retire Managed Hook Support

- remove repo-managed Claude hook installation and verification
- update templates, adapter contracts, distribution manifest sources, and generated manifests
- delete `hooks/**`

### Stage 3: Remove Personal Wave Docs

- delete selected 2026-04-05 wave docs and ledgers
- avoid breaking any surviving cross-references

### Stage 4: Verify And Clean Up

- run targeted tests
- run `git diff --check`
- scan for deleted root-path references
- run node audit and remove temporary artifacts

## Verification Commands

- `pytest -q tests/runtime_neutral/test_workflow_acceptance_runner.py tests/runtime_neutral/test_claude_preview_scaffold.py tests/runtime_neutral/test_installed_runtime_uninstall.py tests/integration/test_dist_manifest_generation.py tests/integration/test_governance_runtime_roles_cutover.py tests/integration/test_adapter_registry_single_source.py tests/e2e/test_distribution_build.py tests/runtime_neutral/test_release_cut_operator.py`
- `git diff --check`
- `rg -n "benchmarks/|hooks/write-guard.js|write-guard hook|managed Claude hook|PreToolUse" . -S`
- final root listing

## Rollback Rules

- if Claude install/check behavior becomes incoherent, keep hook-removal changes local until the contract is repaired
- if generated manifests drift from source config, regenerate them before completion
- if a wave doc is still a live dependency, retain it and record the blocker instead of deleting it blindly

## Phase Cleanup Expectations

1. remove temporary audit files
2. verify the worktree contains only intended deletions and caller updates
3. run node audit
4. leave the branch clean after commit-ready verification

# 2026-04-05 Baseline Functionality Removal Wave 3 Plan

## Goal

Remove the remaining baseline-testing runtime and verification functionality while preserving one coherent governed runtime path through `interactive_governed`.

## Requirement Doc

- [`../requirements/2026-04-05-baseline-functionality-removal-wave3.md`](../requirements/2026-04-05-baseline-functionality-removal-wave3.md)

## Internal Grade

L

The edit set is broad but tightly coupled across runtime entrypoints, configs, PowerShell verification gates, distribution manifests, and contract tests. Serial root-governed execution is safer than parallel writes.

## Ownership Lanes

### Lane A: Runtime And Config Cutover

Write scope:

- `scripts/runtime/**`
- `packages/runtime-core/**`
- `config/runtime-*.json`
- other active config files that still expose baseline mode

### Lane B: Baseline Proof Surface Deletion

Write scope:

- `scripts/verify/**`
- `references/proof-bundles/**`
- `docs/universalization/**`
- release-cut and governance-board inputs tied to removed proof surfaces

### Lane C: Tests, Fixtures, And Dist Regeneration

Write scope:

- `tests/**`
- `config/distribution-manifest-sources.json`
- generated `dist/**`
- active protocol docs that still describe removed runtime behavior

## Execution Steps

### Stage 0: Freeze

- freeze requirement and plan
- enumerate live baseline or benchmark references and classify them as delete, rewrite, or archive-only

### Stage 1: Remove Runtime Alias And Policy

- remove `benchmark_autonomous` from runtime validators, normalization logic, and unattended-mode bridges
- replace `config/benchmark-execution-policy.json` with a neutral execution-proof policy surface
- update runtime or governance assumptions so only `interactive_governed` remains active

### Stage 2: Delete Baseline Proof Surfaces

- delete baseline-only verification gates
- delete official-runtime baseline docs and proof bundle files
- remove baseline-only gate references from release-cut and governance-board inputs

### Stage 3: Repair Contracts, Tests, And Manifests

- rewrite surviving tests from `benchmark_autonomous` to `interactive_governed`
- delete tests that only prove removed baseline behavior
- update manifest sources and regenerate affected `dist/**` artifacts
- update active protocol docs so they stop presenting removed mode behavior as current

### Stage 4: Verify And Clean Up

- run targeted runtime, manifest, and distribution tests
- run `git diff --check`
- rerun a focused `rg` sweep for active baseline references
- remove temp artifacts and run a node audit

## Verification Commands

- `pytest -q tests/unit/test_runtime_stage_machine.py tests/runtime_neutral/test_governed_runtime_bridge.py tests/runtime_neutral/test_memory_runtime_activation.py tests/runtime_neutral/test_native_specialist_failure_injection.py tests/runtime_neutral/test_runtime_contract_schema.py tests/runtime_neutral/test_root_child_hierarchy_bridge.py tests/runtime_neutral/test_runtime_contract_goldens.py tests/runtime_neutral/test_l_xl_native_execution_topology.py tests/runtime_neutral/test_multi_host_specialist_execution.py tests/integration/test_runtime_packet_execution.py tests/integration/test_verification_runtime_entrypoint_contract_cutover.py tests/integration/test_powershell_installed_runtime_contract_bridge.py tests/integration/test_proof_bundle_manifest_contract.py tests/integration/test_dist_manifest_generation.py tests/e2e/test_distribution_build.py tests/runtime_neutral/test_release_cut_operator.py`
- `git diff --check`
- `rg -n "benchmark_autonomous|official-runtime-baseline|baseline-manifest|vibe-document-plane-benchmark-gate|vibe-benchmark-autonomous-proof-gate|vibe-official-runtime-baseline-gate|benchmark-execution-policy" scripts config tests dist docs/universalization SKILL.md protocols -S`

## Rollback Rules

- if a surviving runtime contract still requires a removed file, repair the contract before deleting more surfaces
- if generated distribution manifests drift from source config, regenerate them before completion
- if a reference is purely archival and not part of an active contract, prefer leaving it in place rather than rewriting history

## Phase Cleanup Expectations

1. remove temporary artifacts produced during verification
2. verify the worktree contains only intended baseline-removal and prior approved root-pruning changes
3. run node audit and confirm no managed zombie residue
4. leave commit-ready changes with proof-backed verification only

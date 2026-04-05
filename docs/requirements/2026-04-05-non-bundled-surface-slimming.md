# 2026-04-05 Non-Bundled Surface Slimming

## Goal

Define a strong but no-regression slimming plan for non-`bundled` root surfaces, with emphasis on `agents/`, `apps/`, and `commands/`.

## Deliverable

A repository-grounded pruning strategy that:

- identifies which non-`bundled` root surfaces can be slimmed without changing runtime behavior
- separates safe hygiene cleanup from higher-risk structural convergence
- preserves active install, uninstall, CI, and governed runtime contracts
- avoids path moves or deletions that would break current semantic-owner tests

## Constraints

- Do not include `bundled/**` slimming in this wave.
- Preserve current runtime behavior and install/uninstall semantics.
- Do not move or delete `apps/vgo-cli/**` while it remains a semantic-owner surface in active tests and manifests.
- Do not delete root `commands/**` until a single canonical source and generated compatibility path are explicitly chosen.
- Do not delete `agents/templates/**` until install/docs/tests agree on a replacement source of truth.

## In Scope

- `agents/**`
- `apps/**`
- `commands/**`
- repo hygiene rules for bytecode/cache residue under `apps/**`
- documentation, manifests, and tests that would need to change before any future structural slimming

## Out Of Scope

- `bundled/**`
- broader package/runtime-core redesign
- deleting active CI workflows
- moving package-owned runtime cores under `packages/**`

## Current Evidence Snapshot

1. `apps/vgo-cli/**` is part of the active semantic-owner contract in runtime tests and governance manifests.
2. Root `commands/**` is small, but uninstall/install docs and tests still treat `commands/**` as a managed compatibility surface.
3. `config/opencode/commands/**` already exists as another command-entry surface, which implies duplication potential but not immediate safe deletion.
4. `agents/templates/**` is small and referenced by docs/tests as an official template surface, but not currently proven as a required runtime marker.
5. No tracked `apps/**/__pycache__` or `.pyc` artifacts are currently committed, so the safe `apps/**` slimming lane is hygiene-only rather than structural.
6. Root `commands/**` and `config/opencode/commands/**` are currently installed into different target paths (`global_workflows` versus OpenCode `commands` / `command`), so they are not safe-delete duplicates in the current design.
7. Root `agents/templates/**` and `config/opencode/agents/**` are also installed into different target paths (`agents/templates` for governed codex payload versus OpenCode `agents` / `agent`), so they are not safe-delete duplicates in the current design.

## Acceptance Criteria

1. The plan clearly classifies `apps/`, `commands/`, and `agents/` into:
   - safe-now cleanup
   - conditional convergence
   - deferred / protected
2. No recommended safe-now step changes functional runtime behavior.
3. Every conditional or deferred step includes explicit verification gates and rollback rules.
4. The plan keeps `apps/vgo-cli/**` protected until semantic-owner contracts are intentionally migrated.
5. The plan identifies a single-source convergence path for `commands/**` before any deletion is proposed.

## Product Acceptance Criteria

1. Future slimming work can reduce root noise without breaking install or governed runtime behavior.
2. Root-level duplication is addressed by convergence and generation, not by unsafe deletion.
3. Protected ownership boundaries remain visible to maintainers.

## Manual Spot Checks

- Confirm `apps/vgo-cli/**` remains listed in active semantic-owner tests and governance manifests.
- Confirm root `commands/**` and `config/opencode/commands/**` still represent duplicated command-entry surfaces.
- Confirm `agents/templates/**` remains a small template-only surface rather than a heavy runtime payload.

## Completion Language Policy

- This wave defines a pruning plan only.
- No claim may imply that non-`bundled` slimming is already implemented.

## Delivery Truth Contract

- The repository can safely slim non-`bundled` surfaces only where ownership and compatibility contracts are explicit.
- Where two surfaces appear to overlap, convergence must be proven before deletion.

## Non-Goals

- no speculative deletion of `apps/vgo-cli/**`
- no direct deletion of root `commands/**` without source-of-truth consolidation
- no path churn for cosmetic reasons only
- no deletion of `commands/**` or `agents/templates/**` while they still serve distinct install consumers

## Inferred Assumptions

- “保证不引起功能退化” means prioritizing compatibility and verification over aggressive path deletion.
- The user wants a practical execution sequence, not a purely descriptive audit.

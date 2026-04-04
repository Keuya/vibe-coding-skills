# 2026-03-22 Hook Install Freeze Requirement

- Topic: freeze host hook installation for the currently supported hosts because of unresolved compatibility issues.
- Mode: benchmark_autonomous
- Goal: make `codex` and `claude-code` stop installing, scaffolding, or verifying hook surfaces, while documenting that hooks are temporarily out of the supported install path.

## Deliverable

A working update that:

1. removes hook installation/scaffold from the active `codex` and `claude-code` install/bootstrap path
2. removes hook presence as a success condition in check flows
3. updates adapter contract docs so hooks are no longer described as installed payload
4. updates public install docs to state that hook compatibility is unresolved and hook installation is temporarily not provided
5. preserves other non-hook supported host guidance

## Constraints

- No false hook support claims
- Keep `codex` / `claude-code` as the only supported hosts
- Do not silently keep hook install behavior behind the scenes while docs say otherwise
- Preserve traceability and verification evidence
- Complete phase cleanup before completion

## Acceptance Criteria

- install/bootstrap no longer copy repo `hooks/**` into `codex` or `claude-code` target roots
- `claude-code` no longer scaffolds `settings.vibe.preview.json`
- `check.sh` and `check.ps1` no longer require `hooks/write-guard.js`
- adapter host-profile / closure docs no longer claim hooks are part of installed payload
- install-facing docs explicitly state hook compatibility issues and temporary non-install support
- verification confirms syntax and removal of active hook-install references from supported-host install paths

## Non-Goals

- deleting historical hook source files from the repository
- changing internal routing concepts that use the word "hook" outside host installation
- solving the underlying compatibility problems in this task

## Inferred Assumptions

- the current problem is install-surface truth, not full hook architecture deletion
- temporarily disabling hook installation is safer than keeping a partially working compatibility layer
- community clarity is more valuable than preserving a preview scaffold that is known to be fragile

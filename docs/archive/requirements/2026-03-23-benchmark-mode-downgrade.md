# 2026-03-23 Benchmark Mode Downgrade Requirement

- Topic: keep `benchmark_autonomous` as a compatibility input only and silently downgrade it to `interactive_governed`.
- Mode: interactive_governed
- Goal: make `interactive_governed` the only official runtime mode while preserving compatibility for older callers that still pass `benchmark_autonomous`.

## Deliverable

A working update that:

1. normalizes runtime entry requests for `benchmark_autonomous` into `interactive_governed`
2. keeps execution working without surfacing a user-facing error
3. updates runtime metadata, tests, and governed verification to reflect that `interactive_governed` is now the effective mode
4. preserves the six-stage governed runtime contract and existing artifact generation
5. verifies the downgraded behavior before completion

## Constraints

- No user-facing hard error for `benchmark_autonomous`
- No second runtime mode should remain as an officially active default path
- Existing benchmark proof artifacts may remain named as benchmark proof if renaming would widen scope beyond this change
- Do not revert unrelated local changes already present in the worktree

## Acceptance Criteria

- `scripts/runtime/invoke-vibe-runtime.ps1` accepts `benchmark_autonomous` as legacy input but executes as `interactive_governed`
- runtime summary and downstream receipts record `interactive_governed` as the effective mode
- runtime input freezing no longer maps the legacy mode to unattended execution
- bridge tests verify the silent downgrade behavior
- governed runtime contract gate verifies `interactive_governed` as the resulting mode

## Non-Goals

- Renaming all historical benchmark-proof files, docs, or release notes in one pass
- Reworking the full benchmark execution policy architecture
- Removing legacy strings from historical archived requirement and plan documents

## Inferred Assumptions

- Compatibility is needed because older automation may still send `benchmark_autonomous`.
- Silent normalization is preferable to rejecting old calls because the user explicitly wants uninterrupted execution.
- Runtime truth matters more than preserving historical wording around dual-mode support.

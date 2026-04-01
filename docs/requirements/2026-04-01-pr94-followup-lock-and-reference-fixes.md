# 2026-04-01 PR94 Follow-up Lock And Reference Fixes

- Topic: fix the validated PR `#94` follow-up issues around stale `skills-lock` semantics and contradictory mirror-topology references.
- Mode: interactive_governed
- Goal: remove the remaining stale bundled-mirror assumptions introduced by tracked mirror retirement without widening the compatibility surface again.

## Deliverable

A bounded fix batch that:

1. removes the stale `vibe -> bundled/skills/vibe` entry from `config/skills-lock.json`
2. aligns lock-consuming gates with the new split of `canonical vibe` plus `bundled skills`
3. corrects the high-visibility reference contract that still describes repo-tracked bundled/nested targets
4. adds regression coverage so future lock regeneration or gate runs cannot silently reintroduce the old assumption

## Constraints

- Keep `skills-lock` scoped to the bundled skill corpus rather than inventing a new repo-wide lock format
- Do not reintroduce repo-tracked `bundled/skills/vibe`
- Preserve current install/runtime compatibility behavior for generated nested runtime roots
- Keep the fix set focused on validated review issues only

## Acceptance Criteria

- `config/skills-lock.json` no longer contains a `vibe` entry that points at `bundled/skills/vibe`
- `vibe-offline-skills-gate.ps1` passes when `vibe` exists only as canonical repo truth and no longer requires it under `bundled/skills`
- `skill-metadata-gate.ps1` no longer requires canonical `vibe` to be present in the bundled-only lock
- `references/mirror-topology.md` matches the canonical-only repo topology documented in `docs/version-packaging-governance.md`
- targeted tests and gates pass after the fix

## Non-Goals

- redesigning `skills-lock` into a new multi-surface manifest
- cleaning every historical archive document that mentions old mirror topology
- changing install/runtime generated compatibility semantics beyond what is needed for correctness

## Inferred Assumptions

- `skills-lock` is intended to describe the bundled skill corpus, not canonical repo-root skill truth
- canonical-only `vibe` still needs to remain routable and verifiable through existing metadata gates

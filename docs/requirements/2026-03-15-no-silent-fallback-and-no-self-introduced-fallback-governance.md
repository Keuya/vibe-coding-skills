# No Silent Fallback And No Self-Introduced Fallback Governance

approved_fallback_related_changes: true
fallback_design_explicitly_requested: true
governance_scope: no-silent-fallback-and-no-self-introduced-fallback

## Summary

Harden VCO so fallback and degraded paths are forbidden by default, cannot be introduced casually during implementation, and always emit an explicit hazard surface instead of pretending to be equivalent success.

## Goal

Turn fallback from a convenience mechanism into an explicit hazard-governed exception path.

## Deliverable

- protocol and config invariants for no-silent-fallback governance
- router truth-surface fields that mark fallback as non-authoritative
- strong confirm-surface hazard warning when fallback guard paths are used
- verify gates for runtime honesty, implementation guardrails, and release-truth consistency
- release and promotion surfaces updated to carry the same truth

## Constraints

- do not remove the canonical router or create a second router
- do not silently rewrite historical fallback terminology across unrelated files
- do not break existing route-contract and governed-runtime behaviors
- fallback-related implementation changes in this wave are allowed only because this requirement explicitly approves them

## Acceptance Criteria

1. Any governed router fallback or guarded degradation is marked as non-authoritative.
2. Any governed router fallback or guarded degradation emits a standalone hazard alert.
3. Runtime and protocol contracts explicitly forbid silent fallback and silent degradation.
4. A verify gate exists to reject self-introduced fallback changes unless requirement-backed approval exists.
5. Release and promotion surfaces explicitly require fallback-truth consistency proof.

## Non-Goals

- deleting all historical fallback references in the repository
- rebaselining Linux or platform support truth in this wave
- removing every degraded-path mechanism that exists for platform honesty

## Autonomy Mode

benchmark_autonomous

## Assumptions

- legacy fallback guard remains a real route state that must be disclosed, not hidden
- existing degraded platform truth remains valid and should become more explicit, not less
- this wave is governance hardening, not a product-marketing upgrade

## Evidence Inputs

- docs/plans/2026-03-15-no-silent-fallback-and-no-self-introduced-fallback-governance-plan.md
- protocols/runtime.md
- protocols/do.md
- protocols/think.md
- protocols/team.md
- protocols/review.md
- config/runtime-contract.json
- config/router-model-governance.json

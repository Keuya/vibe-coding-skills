# Post-108 Repo Slimming Protected Surfaces 2026-04-05

## Purpose

Record the surfaces that must not be used as misleading slimming targets during the post-`#108` strong repo-slimming execution program.

This file exists to stop future waves from claiming progress by trimming low-yield or behavior-bearing paths instead of the real hotspot families.

## Protected By Role

### Canonical Semantic Owners

These are behavior-bearing or contract-bearing authorities.
They may be refactored carefully, but they are not default deletion targets.

- `packages/**`
- `core/**`
- `config/**`
  - unless a specific wave has already frozen canonical-vs-derived ownership and targeted verification

### Runtime, Installer, And Routing Execution Surfaces

These remain protected unless a wave proves a narrower owner-preserving replacement.

- `scripts/runtime/**`
- `scripts/router/**`
- `scripts/install/**`
- `scripts/uninstall/**`
- top-level `install.*`, `check.*`, and `uninstall.*` wrappers
- `apps/vgo-cli/**`
- `adapters/**`

### Distribution And Packaging Surfaces

These are low-yield and contract-linked.

- `dist/**`
- `distributions/**`

### Active Verification Contracts

These cannot be treated as cleanup-only targets without proof that coverage and call chains remain intact.

- `tests/**`
- active `scripts/verify/**` entrypoints
- CI-declared gate entrypoints in `.github/workflows/**`

### Reference Families With Live Consumers

These remain protected until consumers are proven absent or migrated.

- `references/fixtures/**`
- `references/proof-bundles/**`

## Monitor-Only Small Families

These are not fully protected in principle, but they are poor strategic slimming targets today.

- `vendor/**`
- `benchmarks/**`
- `third_party/**`
- `tools/**`

If they are touched at all, it should be because of a contract simplification, not because the program needs an easy deletion count.

## Conditional Protection Rules

### `bundled/skills/**`

- protected from broad deletion
- eligible for deduplication, shared-owner extraction, alias normalization, and reference-pack slimming
- not eligible for blind pruning

### `scripts/verify/**`

- protected from blanket deletion
- eligible for family convergence where wrapper sprawl can be proven and CI/docs/tests consumers are preserved

### `config/**`

- protected from deletion-first cleanup
- eligible for truth-surface reduction only after canonical-vs-derived ownership is proven

### GitHub Root Entry Surfaces

- root-facing files are protected until README and contributor-entry implications are reviewed
- root polish is a late wave, not an opening wave

## Destructive-Change Rule

No protected surface may be slimmed destructively until:

1. its role is explicitly named
2. downstream consumers are mapped
3. replacement or retention logic is documented
4. wave-specific verification is defined
5. rollback boundaries are explicit

## Review Rule

Future slimming PRs should be rejected or split if they:

- lead with low-yield deletions from small families
- touch canonical runtime or packaging surfaces without targeted verification
- claim simplification while increasing ambiguity about source-of-truth ownership

## Notes

- This file is a guardrail, not a prohibition on all change.
- It exists to keep the slimming program focused on real maintainership wins rather than easy but low-value deletions.

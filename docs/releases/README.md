# Releases

- Up: [`../README.md`](../README.md)

## What Lives Here

This directory stores governed VCO release notes and the minimum runtime-facing navigation needed to cut or verify a release.

## Start Here

### Current Release Surface

- [`v2.3.31.md`](v2.3.31.md): post-upstream governance closure, disclosure parity fix, and runtime alignment

### Release Runtime / Proof Handoff

- [`../runtime-freshness-install-sop.md`](../runtime-freshness-install-sop.md): install, freshness, and coherence SOP
- [`../../scripts/verify/gate-family-index.md`](../../scripts/verify/gate-family-index.md): gate family navigation and typical run order
- [`../../scripts/verify/README.md`](../../scripts/verify/README.md): verify surface entrypoint
- [`../status/non-regression-proof-bundle.md`](../status/non-regression-proof-bundle.md): minimum closure proof contract

## Recent Governed Releases

- [`v2.3.31.md`](v2.3.31.md) - 2026-03-13 - post-upstream governance closure / disclosure parity / runtime alignment
- [`v2.3.30.md`](v2.3.30.md) - 2026-03-07 - Wave31-39 deep extraction / drift closure
- [`v2.3.29.md`](v2.3.29.md) - 2026-03-07 - Wave19-30 memory / browser / desktop / prompt / release cut closure
- [`v2.3.28.md`](v2.3.28.md) - 2026-03-05 - TurboMax / vector-first context / CUA / prompt asset boost / academic deliverable routing

Older release notes remain in this directory as historical version records, but they are not part of the active release surface.

## Historical Packetization

- [`wave15-18-release-packet.md`](wave15-18-release-packet.md) - historical packetization artifact, not the current release-note format

## Release Operator Entry

Canonical release cut command:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\governance\release-cut.ps1 -RunGates
```

## Stop-Ship Families

Exact script names live in the gate-family index. At the README level, releases should be understood through families rather than giant flat lists:

- topology and integrity: version consistency, version packaging, config parity, nested bundled parity, mirror edit hygiene, BOM/frontmatter integrity
- runtime and install coherence: installed runtime freshness, release/install/runtime coherence
- cleanliness and readiness: repo cleanliness, wave board readiness, capability dedup, adaptive routing readiness, upstream value ops

## Extended Release Trains

Use the gate-family index for the exact scripts. The extended trains stay grouped here by governed concern:

- Wave64-82 extensions: memory runtime, browser / desktop / document / connector scorecards, cross-plane replay, ops cockpit, rollback drill, release-train closure
- Wave83-100 extensions: gate reliability, eval quality, candidate / role / subagent / discovery governance, capability lifecycle, sandbox simulation, release evidence bundle, bounded rollout, upstream re-audit closure

## Rules

- `docs/releases/README.md` is the release-surface navigator, not the flat home for every gate script.
- Keep current release surface, proof handoff, and historical packetization separated instead of flattening them into one list.
- Exact gate names, ordering, and family ownership are defined by [`../../scripts/verify/gate-family-index.md`](../../scripts/verify/gate-family-index.md).
- Release notes stay one-file-per-version using the `v<version>.md` pattern.
- Historical release packets must stay distinct from the current governed release surface.

# Releases

- Up: [`../README.md`](../README.md)

## What Lives Here

This directory stores the current governed release note and the minimum
runtime-facing navigation needed to cut or verify a release.

## Start Here

### Current Release Surface

- [`v2.3.56.md`](v2.3.56.md): remaining-architecture-closure completion / owner-consumer proof / live status truth alignment / bounded fallback honesty / regression-backed baseline

### Release Runtime / Proof Handoff

- [`../runtime-freshness-install-sop.md`](../runtime-freshness-install-sop.md): install, freshness, and coherence SOP
- [`../../scripts/verify/gate-family-index.md`](../../scripts/verify/gate-family-index.md): gate family navigation and typical run order
- [`../../scripts/verify/README.md`](../../scripts/verify/README.md): verify surface entrypoint
- [`../status/non-regression-proof-bundle.md`](../status/non-regression-proof-bundle.md): minimum closure proof contract
- `scripts/verify/vibe-release-truth-consistency-gate.ps1`: fallback and degraded-truth consistency proof for release and promotion surfaces

## Historical Releases

Older release notes and packetization artifacts have been trimmed from the
working tree. Use git tags or git history if you need those historical texts
for audit or archaeology.

## Release Operator Entry

Canonical release cut command:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\scripts\governance\release-cut.ps1 -RunGates
```

On Windows, `powershell.exe` remains an acceptable fallback if `pwsh` is unavailable, but the governed cross-platform release command is `pwsh`.

## Stop-Ship Families

Exact script names live in the gate-family index. At the README level, releases should be understood through families rather than giant flat lists:

- topology and integrity: version consistency, version packaging, config parity, nested bundled parity, mirror edit hygiene, BOM/frontmatter integrity
- runtime and install coherence: installed runtime freshness, release/install/runtime coherence
- fallback truth honesty: no silent fallback contract, self-introduced fallback guard, release-truth consistency
- cleanliness and readiness: repo cleanliness, wave board readiness, capability dedup, adaptive routing readiness, upstream value ops

## Extended Release Trains

Use the gate-family index for the exact scripts. The extended trains stay grouped here by governed concern:

- Wave64-82 extensions: memory runtime, browser / desktop / document / connector scorecards, cross-plane replay, ops cockpit, rollback drill, release-train closure
- Exact gates include `vibe-wave64-82-closure-gate.ps1` and `vibe-release-train-v2-gate.ps1`.
- Wave83-100 extensions: gate reliability, eval quality, candidate / role / subagent / discovery governance, capability lifecycle, sandbox simulation, release evidence bundle, bounded rollout, upstream re-audit closure
- Wave83-100 Extended Gates: `vibe-release-evidence-bundle-gate.ps1`, `vibe-manual-apply-policy-gate.ps1`, `vibe-rollout-proposal-boundedness-gate.ps1`, `vibe-upstream-reaudit-matrix-gate.ps1`, `vibe-wave83-100-closure-gate.ps1`

## Rules

- `docs/releases/README.md` is the release-surface navigator, not the flat home for every gate script.
- Keep current release surface and proof handoff small; older notes belong in git history, not in a permanently growing working-tree directory.
- Exact gate names, ordering, and family ownership are defined by [`../../scripts/verify/gate-family-index.md`](../../scripts/verify/gate-family-index.md).
- Degraded closure is never equivalent to authoritative success. If a release depends on fallback or degraded behavior, the release surface must say so explicitly and include fallback-truth consistency proof.
- Release notes stay one-file-per-version using the `v<version>.md` pattern.
- Historical release packets are no longer treated as permanent repo surfaces.

# Non-Regression Proof Bundle

Updated: 2026-03-12

## Positioning

This page is the minimum closure proof contract.

It defines which commands must be rerun before a structure-changing cleanup batch can claim success. It does not carry the authoritative PASS/FAIL state itself. Current truth always lives in `outputs/verify/*.json`.

## Rule

Every cleanup batch must name the proof it depends on before it modifies structure.

If a batch touches routing, mirror topology, install/runtime behavior, output boundary, or cleanliness policy, it must rerun the affected commands and verify the resulting receipts before claiming success.

Protected official-runtime main-chain edits remain frozen by default.
If a batch needs to touch those surfaces, it must also be covered by:

- `config/official-runtime-main-chain-policy.json`
- a plan-backed contract such as `docs/universalization/linux-full-authoritative-contract.md`

Without those anchors, a green proof bundle is not enough to justify the change.

## Canonical Commands

Run from the canonical repo root:

```powershell
powershell -NoProfile -File scripts/verify/vibe-pack-routing-smoke.ps1
powershell -NoProfile -File scripts/verify/vibe-router-contract-gate.ps1
powershell -NoProfile -File scripts/verify/vibe-version-packaging-gate.ps1
powershell -NoProfile -File scripts/verify/vibe-mirror-edit-hygiene-gate.ps1
powershell -NoProfile -File scripts/verify/vibe-output-artifact-boundary-gate.ps1
powershell -NoProfile -File scripts/verify/vibe-installed-runtime-freshness-gate.ps1
powershell -NoProfile -File scripts/verify/vibe-release-install-runtime-coherence-gate.ps1
powershell -NoProfile -File scripts/verify/vibe-release-truth-consistency-gate.ps1
powershell -NoProfile -File scripts/verify/vibe-repo-cleanliness-gate.ps1
```

Phase-end bounded operator entrypoint:

```powershell
powershell -NoProfile -File scripts/governance/phase-end-cleanup.ps1 -WriteArtifacts
```

## Recommended Run Order

1. `vibe-pack-routing-smoke.ps1`
   - fast behavior smoke for routing
2. `vibe-router-contract-gate.ps1`
   - validates routing contract details
3. `vibe-version-packaging-gate.ps1`
   - validates canonical -> bundled packaging parity
4. `vibe-mirror-edit-hygiene-gate.ps1`
   - rejects mirror-only drift
5. `vibe-output-artifact-boundary-gate.ps1`
   - validates output -> fixture boundary
6. `vibe-installed-runtime-freshness-gate.ps1`
   - validates installed runtime parity / receipt
7. `vibe-release-install-runtime-coherence-gate.ps1`
   - validates install/check/release coherence
8. `vibe-release-truth-consistency-gate.ps1`
   - validates fallback and degraded-truth consistency across release/promotion surfaces
9. `vibe-repo-cleanliness-gate.ps1`
   - validates current cleanliness contract

## Batch-to-Proof Mapping

| Batch Type | Minimum Required Proof |
| --- | --- |
| docs spine only | manual link/readability review, then full bundle before closure |
| routing / router config | routing smoke + router contract |
| mirror topology / sync / packaging | version packaging + mirror hygiene |
| install / check / runtime | installed runtime freshness + release/install/runtime coherence |
| fallback / degraded truth / release wording | release truth consistency gate |
| outputs / fixtures | output artifact boundary |
| cleanliness policy / plane split | repo cleanliness gate |
| destructive prune | all commands above |

## Evidence Reading Rule

This page names the required proof. It is not the source of the latest proof outcome.

To determine the current status of a cleanup batch, read the latest receipt for each gate from `outputs/verify/*.json` and inspect `gate_result`.

Artifact anchors:

- `outputs/verify/vibe-pack-routing-smoke.summary.json`
- `outputs/verify/vibe-router-contract-gate.json`
- `outputs/verify/vibe-version-packaging-gate.json`
- `outputs/verify/vibe-mirror-edit-hygiene-gate.json`
- `outputs/verify/vibe-output-artifact-boundary-gate.json`
- `outputs/verify/vibe-installed-runtime-freshness-gate.json`
- `outputs/verify/vibe-release-install-runtime-coherence-gate.json`
- `outputs/verify/vibe-release-truth-consistency-gate.json`
- `outputs/verify/vibe-repo-cleanliness-gate.json`

Latest known green snapshot for this closure track was recorded on `2026-03-12`. That snapshot is historical evidence, not a standing promise that the current worktree is still green.

## Contract Rule for Future Expansion

If a new protected capability is introduced, it is not covered by this bundle until:

1. a corresponding gate or bounded audit path exists;
2. that proof is added to this document; and
3. the resulting receipt is wired into the current closure flow.

Current mission after re-greening is not to loosen the bundle, but to use it as the minimum closure contract before any further prune or topology reduction.

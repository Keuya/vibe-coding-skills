# PR94 Follow-up Retro CER

## Context

This CER explains why PR `#94` still had real defects after the tracked `bundled/skills/vibe` mirror was retired in code and docs.

## CER

- Pattern:
  canonical mirror-retirement intent landed, but several bundled-only consumers still encoded the old steady-state assumption.
- Evidence:
  the remote PR head `b187df3` failed `pwsh -NoProfile -File ./scripts/verify/vibe-offline-skills-gate.ps1` with `missing required routed skills: vibe` and `skills-lock entries missing in skills root: vibe`.
- Evidence:
  `config/skills-lock.json` on the remote PR head still contained `vibe -> bundled/skills/vibe`, while `references/mirror-topology.md` still described repo-tracked `bundled` and `nested_bundled` targets.
- Evidence:
  `skill-metadata-gate.ps1` still required canonical-top-level resolution through `user_skills` and still required unconditional `skills-lock` membership, which meant the next consumer would have broken even after the stale lock entry was removed.
- Root Cause:
  the original change removed the tracked mirror tree, but it did not enumerate every downstream contract that consumed mirror topology indirectly. The work closed over packaging and parity surfaces, but missed lock semantics, offline closure semantics, and the human-readable topology contract.
- Root Cause:
  this was also an evaluation blind spot. Verification covered retirement and packaging gates, but there was no regression that exercised the precise `canonical vibe present / bundled vibe absent / stale lock entry forbidden` state transition.
- Intervention:
  treat `skills-lock` as bundled-skill corpus truth only, not canonical repo truth.
- Intervention:
  update lock-consuming gates so canonical repo skills can resolve outside bundled roots while stale bundled lock entries still fail.
- Intervention:
  rewrite the topology reference so it matches `config/version-governance.json` instead of preserving legacy mirror language for familiarity.
- Guardrail:
  keep a dedicated regression test for the two key states: canonical-only `vibe` passes, stale bundled `vibe` lock entry fails.
- Guardrail:
  when retiring a source-of-truth surface, audit consumers by contract class, not just by path deletion:
  generator, verifier, lockfile, reference doc, and regression coverage.
- Guardrail:
  do not mark mirror-retirement debt closed until at least one gate validates the exact post-retirement steady state instead of only validating deletion or packaging parity.
- Confidence:
  high. The defect reproduced on the remote PR head, and the local follow-up fix removes the stale lock entry, updates both affected gates, updates the topology reference, and adds a regression test for the missed state.

## Failure Class

- CF-2 context poisoning:
  the repo mixed new canonical-only intent with stale bundled-mirror assumptions.
- CF-6 evaluation blind spot:
  the verification suite did not cover the exact canonical-only routed skill closure state until the follow-up test was added.

## Practical Lesson

For source-of-truth retirement work, deleting the mirror is only the visible change. The real completion bar is consumer convergence.

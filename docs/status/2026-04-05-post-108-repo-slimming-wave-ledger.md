# 2026-04-05 Post-108 Repo Slimming Wave Ledger

## Scope

This ledger records the execution of the post-`#108` GitHub-maintainer-focused repo-slimming program.
It is the operational companion to:

- [`../requirements/2026-04-05-post-108-github-maintainer-repo-slimming-program.md`](../requirements/2026-04-05-post-108-github-maintainer-repo-slimming-program.md)
- [`../plans/2026-04-05-post-108-github-maintainer-repo-slimming-program-plan.md`](../plans/2026-04-05-post-108-github-maintainer-repo-slimming-program-plan.md)

## Baseline

Observed post-`#108` mainline metrics at plan freeze:

| Metric | Baseline |
| --- | --- |
| `origin/main` tracked files | `3540` |
| dominant tracked family | `bundled/skills/**` (`2120` files) |
| dominant active script hotspot | `scripts/verify/**` (`192` files) |
| key reference hotspot | `references/fixtures/**` |
| protected low-yield surfaces | `packages/**`, `core/**`, `dist/**`, `tests/**`, `vendor/**`, `benchmarks/**`, `third_party/**` |

## Protected Surfaces

These surfaces are not valid “easy wins” for slimming:

| Path Family | Why Protected |
| --- | --- |
| `packages/**` | semantic and runtime-bearing |
| `core/**` | contract-bearing |
| `dist/**` | generated but release-significant |
| `tests/**` | regression-bearing |
| `vendor/**` | already tiny |
| `benchmarks/**` | already tiny |
| `third_party/**` | compliance-sensitive and low-yield |

## Wave Status

| Wave | Focus | Status | Notes |
| --- | --- | --- | --- |
| Wave 0 | hotspot, consumer, and protected-surface freeze | completed | requirement, plan, hotspot ledger, and protected-surface ledger frozen |
| Wave 1 | document-skill payload unification | completed | `document-skills/pptx/ooxml/**` duplicate payload collapsed into wrappers over sibling `docx/ooxml/**` |
| Wave 2 | verification surface convergence | completed_no_delete | candidate verify-gate removals were rejected; gates retained because caller proof stayed too weak |
| Wave 3 | fixture and proof retention reform | completed_audit_only | live-consumer audit did not justify fixture/proof deletions in this pass |
| Wave 4 | config truth-surface reduction | completed_audit_only | high-risk multi-truth surfaces were inspected and deliberately left untouched without stronger ownership proof |
| Wave 5 | GitHub root polish | completed_scoped | root polish stayed limited to maintainership ledgers; no high-risk entrypoint deletions were landed |

## Current High-Signal Findings

1. `bundled/skills/document-skills/docx/ooxml/**` and `bundled/skills/document-skills/pptx/ooxml/**` are byte-identical duplicate trees.
2. The duplicate document-skills OOXML trees are not referenced by hard-coded repo paths outside their local skill docs.
3. The top-level standalone `bundled/skills/docx/**` family is not identical to `bundled/skills/document-skills/docx/**`; it must stay isolated until a separate owner cutover is proven.
4. `scripts/verify/**` remains large and clustered by family, but deletions must wait for stronger caller proof than filename pattern matching.
5. `references/fixtures/**` and `references/proof-bundles/**` remain consumer-backed enough that future reduction must stay consumer-led, not size-led.
6. `bundled/skills/pymc/**` vs `bundled/skills/pymc-bayesian-modeling/**` is a safe alias-thinning candidate because the canonical `pymc/**` payload fully covers the removed alias assets, references, and scripts.
7. `bundled/skills/torch-geometric/**` vs `bundled/skills/torch_geometric/**` is a safe alias-thinning candidate for the same reason: the hyphenated canonical payload fully covers the removed underscore alias assets.

## Execution Outcome

This execution pass landed only proof-backed reductions:

1. Removed the duplicated schema and validation payload from `bundled/skills/document-skills/pptx/ooxml/**` while retaining thin wrapper entrypoints and documenting the shared-owner model in `bundled/skills/document-skills/pptx/ooxml.md`.
2. Reduced `bundled/skills/pymc-bayesian-modeling/**` to a thin alias `SKILL.md`, with all heavy assets delegated to canonical `bundled/skills/pymc/**`.
3. Reduced `bundled/skills/torch_geometric/**` to a thin alias `SKILL.md`, with all heavy assets delegated to canonical `bundled/skills/torch-geometric/**`.
4. Explicitly preserved the three candidate `scripts/verify/*.ps1` gates after audit rather than deleting them on weak evidence.

Current landed reduction footprint in the working tree:

- `57` tracked files removed
- `63` tracked paths changed

## Verification Notes

Verification completed:

1. `git diff --check`
2. `python3 -m py_compile bundled/skills/document-skills/pptx/ooxml/scripts/pack.py bundled/skills/document-skills/pptx/ooxml/scripts/unpack.py bundled/skills/document-skills/pptx/ooxml/scripts/validate.py`
3. repo-wide path scans confirming no hard-coded references remain to:
   - `bundled/skills/document-skills/pptx/ooxml/schemas/**`
   - `bundled/skills/document-skills/pptx/ooxml/scripts/validation/**`
   - `bundled/skills/pymc-bayesian-modeling/assets|references|scripts`
   - `bundled/skills/torch_geometric/references|scripts`

Verification blocked by local environment, not by the slimming diff:

1. `pack.py` and `unpack.py` runtime smoke checks require `defusedxml`, which is not installed in the current shell.
2. The canonical shared implementation under `document-skills/docx/ooxml/scripts/*` fails with the same `ModuleNotFoundError: defusedxml`, so this is not introduced by the new wrapper delegation.

## Safe-First Sequence

1. Reduce proven duplicate payloads inside `document-skills/**`.
2. Keep standalone `docx/**` self-contained until a separate migration owner exists.
3. Convert later waves to deletion only when workflow, tests, docs, and config stop naming the candidate path.
4. Treat `scripts/verify/**` and `config/**` as convergence targets, not blind deletion targets.

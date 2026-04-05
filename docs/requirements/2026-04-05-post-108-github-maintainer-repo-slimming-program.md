# 2026-04-05 Post-108 GitHub Maintainer Repo Slimming Program

## Goal

Design the next strong but safe repository-slimming program after PR `#108` merged to `main`, with the explicit objective of improving GitHub maintainability:

- lower tracked-file surface area
- reduce high-noise, low-signal repository weight
- simplify root navigation and reviewability
- preserve runtime, installer, verification, packaging, and release behavior

This planning pass is maintainer-first, not feature-first.
Its primary success condition is a repository that is easier to browse, review, and govern on GitHub without causing functional regression.

## Deliverable

A governed requirement packet and an XL execution plan that classify the post-`#108` repository into:

- immediate high-yield slimming candidates that can move in the next execution wave
- consumer-audit-required surfaces that need dependency proof before cuts
- protected surfaces that should not be used as fake slimming targets

The program must produce a practical landing design for future execution waves, including:

- path families to target
- risk tier per family
- expected size or file-count pressure relieved by each wave
- verification gates
- rollback rules
- per-wave cleanup expectations

## Constraints

- Plan against the latest `origin/main` state after PR `#108` merged.
- Preserve installer, check, runtime, adapter, distribution, and release behavior.
- Preserve high cohesion and low coupling:
  - one semantic owner per concern
  - thin compatibility shims
  - explicit archive and retention policy
  - generated or reference-heavy payloads separated from canonical active surfaces
- Do not accept cosmetic “cleanup” on tiny low-value surfaces as a substitute for addressing the actual large payload families.
- Do not use historical docs or proof artifacts as hidden semantic owners.
- Do not claim the repo is fully slimmed or regression-safe during planning only.

## Current Post-108 Evidence Snapshot

Latest observed `origin/main` state during this planning pass:

- `origin/main` SHA: `51e7b7b4d129245714a378c1a566523c7847cdbb`
- GitHub repo `size`: `15407`
- tracked files: `3540`
- top-level repository entries: about `46`
- post-`#108` shrink relative to pre-merge `main`: `278 files changed, +227 / -24181`

Current tracked-file concentration by top family:

- `bundled/skills/**`: `2120`
- `docs/**`: `370`
- `scripts/**`: `309`
- `config/**`: `151`
- `tests/**`: `149`
- `references/**`: `136`
- `packages/**`: `97`

Current size-pressure hotspots:

- `bundled/skills/**`: about `21.42 MiB`
- `logo.png`: about `1.71 MiB`
- `scripts/verify/**`: about `1.09 MiB`
- `references/fixtures/**`: about `0.53 MiB`
- `tests/runtime_neutral/**`: about `0.44 MiB`
- `config/skill-routing-rules.json`: about `0.31 MiB`
- `scripts/runtime/**`: about `0.30 MiB`

Current high-value remaining structural hotspots:

1. `bundled/skills/**`
   - still the dominant size and file-count family
   - many skills carry large `references/`, `assets/`, `examples/`, `themes/`, or `templates/` subtrees
2. `document-skills` and neighboring document skill families
   - `bundled/skills/document-skills/**`: about `2.39 MiB`, `131` files
   - `bundled/skills/docx/**`: about `1.13 MiB`, `59` files
   - duplicated OOXML schema payloads remain in multiple places
3. `scripts/verify/**`
   - about `192` files
   - likely contains family-level wrapper sprawl and overlapping gate surfaces
4. `config/**`
   - large routing, packaging, lock, and dependency metadata remains split across multiple files
5. `references/fixtures/**`
   - still heavy enough to matter and should stay governed by consumer proof, not by historical inertia

## Repository-Maintainer Framing

The next slimming wave should optimize for GitHub maintainer outcomes first:

1. root discoverability
2. lower review noise in future PRs
3. less confusion around canonical vs mirrored vs archived surfaces
4. lower ongoing retention burden for references and bundled payloads
5. easier onboarding for new contributors who open the repo through GitHub, not through local implementation context

This means the program should judge success by:

- fewer ambiguous source-of-truth locations
- fewer duplicated heavy payloads
- more explicit archive and retention boundaries
- better ratio of active surfaces to historical or reference payloads

It should not judge success purely by raw deletion count.

## Acceptance Criteria

1. The plan identifies the top 10 next-wave slimming targets with concrete path families and risk tiers.
2. The plan distinguishes `P0`, `P1`, and `P2` classes:
   - `P0`: high-yield, low-to-medium-risk, can move soon
   - `P1`: valuable but consumer-audit-first
   - `P2`: protected or only worth touching after architectural cutover
3. The plan includes a wave model that keeps future PRs reviewable and low-blast-radius.
4. The plan includes verification commands tied to the touched surface instead of blanket vague “rerun tests” wording.
5. The plan includes cleanup and rollback rules for every execution wave.
6. The plan names the canonical maintainership metrics that future waves should report:
   - tracked-file count
   - file-count changes by top family
   - size-pressure changes by hotspot family
   - number of duplicate or mirrored heavy assets removed or unified
7. The plan explicitly protects `packages/**`, `core/**`, `dist/**`, live test contracts, and active runtime/install surfaces from being used as misleading size-cut targets.

## Product Acceptance Criteria

The future execution program is acceptable only if:

1. A maintainer can explain what each major top-level family is for without consulting historical chat context.
2. The GitHub root page remains navigable and more intention-revealing than before.
3. Heavy reference payloads no longer remain live by default without a retention reason.
4. Compatibility layers become thinner rather than accumulating new implicit ownership.
5. Each merged slimming wave can prove no functional regression against the touched surface.

## Manual Spot Checks

- Open the GitHub root and confirm the active entry surfaces are still obvious after each future wave.
- Confirm `README.md`, `README.zh.md`, install wrappers, and top-level check wrappers still point to live canonical surfaces.
- Confirm document-skill changes do not leave multiple equal-status document entrypoints without a clear owner.
- Confirm `references/fixtures/**` and `references/proof-bundles/**` still explain what remains live and why.
- Confirm no future slimming PR substitutes tiny low-value deletions for actual hotspot reduction.

## Completion Language Policy

- This planning run may claim only that a post-`#108` slimming program and landing design have been frozen.
- It may not claim that the repository is already fully optimized, fully normalized, or regression-safe after future execution.
- Each later implementation wave must earn its own verification evidence and cleanup receipts before stronger completion language is used.

## Delivery Truth Contract

- This requirement doc is authoritative for planning scope, maintainership objective, and risk boundaries.
- It is not execution evidence.
- Future implementation truth remains pending until each wave lands with verification and cleanup receipts.

## Non-Goals

- No feature expansion or product-surface redesign.
- No broad rewrite of the runtime, router, installer, or release architecture in this planning pass.
- No blind deletion of bundled payloads or verification assets simply because they are large.
- No low-yield focus on already-small families such as `vendor/**`, `benchmarks/**`, or `third_party/**` unless a later contract change justifies it.
- No attempt to solve all repository debt in one monolithic PR.

## Inferred Assumptions

- The maintainer wants the GitHub repository itself to be easier to own, browse, and review.
- PR `#108` was a meaningful reduction, but it intentionally did not attack the dominant remaining heavy surfaces.
- The next meaningful win comes from structural slimming inside `bundled/skills/**`, `scripts/verify/**`, `config/**`, and consumer-governed reference families.
- Repository cleanliness now depends less on more archive deletion and more on reducing duplicated payload ownership and verification/config sprawl.

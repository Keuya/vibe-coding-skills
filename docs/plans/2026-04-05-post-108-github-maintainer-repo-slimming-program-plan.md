# 2026-04-05 Post-108 GitHub Maintainer Repo Slimming Program Plan

## Goal

Design the next execution-ready slimming roadmap after PR `#108` merged, with GitHub maintainability as the controlling objective.

This plan is not a generic cleanup checklist.
It is a wave-structured execution design for reducing the remaining heavy and confusing repository surfaces while preserving live behavior.

## Requirement Doc

- [`../requirements/2026-04-05-post-108-github-maintainer-repo-slimming-program.md`](../requirements/2026-04-05-post-108-github-maintainer-repo-slimming-program.md)

## Internal Grade

XL wave-sequential execution.

Reason:

- the work spans `bundled/skills`, `scripts`, `config`, `references`, and `docs`
- multiple surfaces have active downstream consumers
- the best path is wave-sequential with bounded parallel audit work, not one giant cleanup PR

## Program Design Lens

This program treats GitHub repository ownership as a product surface.

The target state is:

1. lower tracked-file count in heavy low-signal families
2. fewer duplicated heavyweight assets
3. thinner compatibility and routing metadata surfaces
4. explicit archive, fixture, and proof retention rules
5. smaller future PRs with better reviewability

The program does not optimize for “big deletion numbers” in isolation.
It optimizes for maintainability and semantic clarity.

## Post-108 Priority Snapshot

The strongest remaining slimming pressure is now concentrated in:

1. `bundled/skills/**`
   - `2120` tracked files
   - about `21.42 MiB`
2. `scripts/verify/**`
   - about `192` tracked files
   - second-largest active maintenance hotspot
3. `config/**`
   - many packaging, routing, lock, and dependency declarations
   - risk of multi-file truth duplication
4. `references/fixtures/**`
   - still meaningful size and review cost
5. `docs/**`
   - reduced after `#108`, but still requires stricter retention governance rather than more ad hoc cleanup

These are not first-order slimming targets for the next major wave:

- `packages/**`
- `core/**`
- `dist/**`
- `tests/**`
- `vendor/**`
- `benchmarks/**`
- `third_party/**`

Those surfaces are either behavior-bearing, already small, or low-yield.

## Path Role Model

Every candidate path in future execution must be tagged with one primary role before changes are made:

| Role | Meaning | Allowed Action |
| --- | --- | --- |
| canonical source | semantic owner of behavior or contract | refactor or split only |
| generated projection | reproducible derivative | regenerate, centralize, or reduce duplicate projections |
| compatibility shim | migration or adapter bridge | thin, delegate, retire after caller migration |
| fixture/proof | evidence consumed by tests or policy | retain only if a live consumer exists |
| live reference | current maintainer-facing support surface | consolidate and reduce overlap |
| archive | historical surface | keep indexed, keep out of active navigation |
| dead surface | zero live consumer and no retention reason | delete |

No future execution wave may delete a path until its role is established.

## Top 10 Next-Wave Targets

### P0: Highest-Value Near-Term Moves

1. `bundled/skills/document-skills/**`
   - Why: largest single bundled family, with document-tooling subtrees and duplicated schema-heavy assets
   - Desired move: establish one clear shared owner model for docx/pptx/xlsx/pdf infrastructure
   - Risk: medium

2. `bundled/skills/docx/**` and document-adjacent standalone skills
   - Why: likely overlaps with `document-skills/**`
   - Desired move: remove duplicate heavy assets, unify ownership, preserve thin skill entrypoints
   - Risk: medium

3. duplicated OOXML schema payloads
   - Current evidence points to repeated schema trees under document families
   - Desired move: centralize shared schema assets or define one authoritative retained payload
   - Risk: medium-high

4. `scripts/verify/**` family convergence
   - Why: `192` files is high maintenance load for a verification surface
   - Desired move: merge wrapper sprawl into family-owned core scripts plus parameterized entrypoints
   - Risk: medium

5. `references/fixtures/**` consumer-led cleanup wave 2
   - Why: active but must remain governed by live callers only
   - Desired move: remove or archive fixture families not consumed by tests, replay, or policy
   - Risk: low-medium

### P1: Valuable But Audit-First

6. `config/**` routing/packaging/lock rationalization
   - Why: likely multi-file truth projection across lock, pack, dependency, and runtime packaging manifests
   - Desired move: shrink update surface and reduce duplicated declarations
   - Risk: high unless dependency graph is frozen first

7. high-reference bundled skills with low core payload
   - Examples by current evidence: `unsloth`, `security-best-practices`, `markdown-mermaid-writing`, `timesfm-forecasting`, `clinical-reports`
   - Desired move: keep strong `SKILL.md`, reduce heavy reference packs to curated minimal subsets
   - Risk: medium

8. compatibility alias skills
   - Examples: `superclaude-framework-compat`, `spec-kit-vibe-compat`, `build-error-resolver`
   - Desired move: keep behavior, thin payload, avoid multiple equivalent explanatory surfaces
   - Risk: medium-high

### P2: Protected Or Last-Mile

9. GitHub root entrypoint downshift
   - Candidate move: reduce top-level script clutter only after entrypoint rules are frozen
   - Risk: medium-high because GitHub and user onboarding depend on it

10. large static assets and residual low-signal single files
   - Example: `logo.png`
   - Desired move: only after primary structural issues are addressed
   - Risk: low, but low strategic value

## Execution Topology

### Wave 0: Inventory Freeze And Guardrails

Goal:

- create the auditable base for future slimming waves

Work:

- produce a maintainership hotspot ledger for `bundled`, `scripts`, `config`, `references`, and `docs`
- record canonical owners and downstream consumers for the top 10 targets
- create a “do not cut without proof” table for protected surfaces

Writes allowed:

- planning docs
- status or ledger docs only

Verification:

- `git diff --check`
- `git ls-tree -r --name-only HEAD | wc -l`
- `rg -n "document-skills|superclaude-framework-compat|spec-kit-vibe-compat|build-error-resolver|references/fixtures|scripts/verify" config scripts tests docs bundled -g '!*.png'`

Cleanup:

- remove temporary census files
- remove phase-local scratch JSON or shell notes
- audit repo-local node processes and confirm none remain

### Wave 1: Document-Skill Payload Unification

Goal:

- reduce the heaviest duplicated document payload surface without weakening document workflows

Work:

- audit `document-skills`, `docx`, and neighboring document skill families
- classify each subtree as:
  - shared engine asset
  - skill-specific workflow asset
  - duplicate heavy payload
  - archiveable documentation/reference
- design one retained shared owner for schema-heavy assets
- thin standalone skills into wrappers if the heavy payload should live elsewhere

Parallel audit windows allowed:

- one lane for `document-skills/**`
- one lane for standalone `docx/pdf/pptx/xlsx/**`
- one lane for config and tests that reference document skills

Execution note:

- no deletion of schema or scripts until consumer references are fully mapped

Verification:

- `git diff --check`
- targeted `rg` for moved or removed document paths across `bundled`, `config`, `docs`, and `tests`
- any touched document tooling scripts must receive direct smoke or unit verification before merge

Rollback rule:

- if a retained document path still has ambiguous callers, keep the asset and downgrade the wave to owner-clarification only

Cleanup:

- delete temporary file inventories and duplicate reports
- clear any generated thumbnails, test renders, or scratch validation artifacts

### Wave 2: Verification Surface Convergence

Goal:

- reduce `scripts/verify/**` maintenance sprawl while preserving gate coverage

Work:

- cluster verify scripts by family
- identify wrappers that differ only by narrow parameters or old migration naming
- define family-owned entrypoints plus shared helpers
- retire dead wrappers only after `rg` and workflow consumers are proven absent

Parallel audit windows allowed:

- one lane for `.github/workflows/**` to verify invocations
- one lane for `scripts/verify/**` family mapping
- one lane for `docs/**` and `tests/**` references

Verification:

- `git diff --check`
- `sed -n '1,220p' .github/workflows/vco-gates.yml`
- targeted Python validation:
  - `python3 -m pytest tests/runtime_neutral/test_python_validation_contract.py tests/runtime_neutral/test_governed_runtime_bridge.py tests/runtime_neutral/test_install_profile_differentiation.py -q`
- if verify entrypoints change, rerun the directly affected gate commands

Rollback rule:

- if a verify wrapper remains referenced by CI, docs, or replay contracts, keep it and convert the wave into family metadata cleanup only

Cleanup:

- remove scratch gate maps
- remove temporary execution logs
- audit repo-local node residue

### Wave 3: Reference Fixture And Proof Retention Reform

Goal:

- keep only live fixture and proof surfaces on the active repo surface

Work:

- re-run consumer ledger checks for `references/fixtures/**`
- classify fixture families into:
  - active canonical
  - active mirrored
  - archive-first
  - dead
- keep proof-bundle manifests and summaries where live contracts need them
- archive or delete low-signal raw payloads with no current consumer

Verification:

- `git diff --check`
- `python3 -m pytest tests/integration/test_proof_bundle_manifest_contract.py tests/runtime_neutral/test_outputs_boundary_migration.py tests/runtime_neutral/test_runtime_contract_goldens.py -q`
- `rg -n "references/fixtures|references/proof-bundles" tests config scripts docs -g '!*.png'`

Rollback rule:

- any fixture family with unresolved config or test consumption remains live for that wave

Cleanup:

- clear staging scratch lists
- confirm no temp copies of fixture trees remain under `/tmp` or repo-local temp roots

### Wave 4: Config Truth-Surface Reduction

Goal:

- reduce duplicated packaging and routing truth across `config/**`

Work:

- compare `skill-routing-rules.json`, `skills-lock.json`, `pack-manifest.json`, `runtime-core-packaging*.json`, `dependency-map.json`, and related manifests
- identify fields that are semantically duplicated or mechanically derivable
- define a single-source ownership model before any field removal

Execution note:

- this wave is architecture-sensitive and should not be mixed with unrelated deletions

Verification:

- `git diff --check`
- targeted `rg` for changed keys across `config`, `scripts`, `packages`, `tests`, and `docs`
- rerun the specific runtime and packaging tests or gate commands that consume the changed config family

Rollback rule:

- if single-source derivation cannot be proven in one batch, land only documentation and ledger updates, not config deletion

Cleanup:

- clear generated comparison reports and JSON diffs
- audit for repo-local node or Python child processes

### Wave 5: GitHub Root And Entry-Surface Polish

Goal:

- improve maintainer and contributor first-open experience after the heavy internals are reduced

Work:

- revisit top-level root surfaces
- decide which wrappers must remain root-visible
- move secondary or low-frequency helper entrypoints down into owned subtrees where safe
- keep README and install/check/uninstall entrypoints obvious

Verification:

- manual root scan
- `git diff --check`
- `rg -n "check\\.sh|check\\.ps1|install\\.sh|install\\.ps1|uninstall\\.sh|uninstall\\.ps1" README.md README.zh.md docs scripts .github -g '!*.png'`

Rollback rule:

- any root file that still functions as a primary public entrypoint remains in place

Cleanup:

- remove path-census scratch files
- confirm no accidental top-level temp files remain

## Ownership Boundaries

Future execution should keep write scopes separated:

- doc and reference retention waves should not simultaneously rewrite runtime or packaging logic
- document-skill payload work should keep config and tests in reviewable supporting patches
- verify convergence should not be mixed with bundled skill payload reduction in the same PR
- config truth-surface reduction should be isolated because it is cross-cutting and regression-sensitive

## Verification Matrix

Minimum wave-level verification rules:

| Touched Surface | Minimum Verification |
| --- | --- |
| `docs/**` | `git diff --check`, broken-path scan, README/manual spot checks |
| `references/**` | `git diff --check`, fixture/proof pytest group, consumer `rg` scan |
| `scripts/verify/**` | `git diff --check`, CI workflow reference scan, affected Python/gate checks |
| `bundled/skills/**` | `git diff --check`, path-reference scan, touched-skill smoke or consumer validation |
| `config/**` | `git diff --check`, changed-key consumer scan, targeted contract tests |

No wave may claim “no regression” without fresh verification evidence tied to the touched surface.

## Delivery Acceptance Plan

The later implementation program may be considered successful only if:

1. post-wave tracked-file count decreases in a meaningful hotspot family
2. the surviving path roles are easier to explain than before
3. no live installer/runtime/release/verification consumer is broken
4. every removed heavy payload has a retained owner, archive home, or explicit no-longer-needed proof
5. the resulting PR is reviewable without needing hidden chat history to understand why paths were kept or removed

## Completion Language Rules

- Completion language for this planning pass must stay at “requirement and execution design frozen.”
- Future execution waves may only claim stronger success after fresh wave-local verification and cleanup receipts.
- If a wave reaches only owner clarification and not path reduction, it must say so plainly.

## Rollback Rules

- Any ambiguous live consumer blocks destructive deletion for that path family.
- If a wave uncovers hidden semantic ownership in a supposedly dead or reference-only path, downgrade the wave to documentation or ledger-only.
- Prefer thin compatibility retention over irreversible removal when the migration state is incomplete.
- If the wave mixes too many semantic concerns, split it before merge instead of increasing blast radius.

## Phase Cleanup Expectations

Each future execution wave must end with:

- temp-file cleanup result
- repo-local node audit result
- removal of scratch ledgers, diff exports, and temporary manifests
- a short evidence note describing:
  - what was reduced
  - what stayed protected
  - which verification commands were run
  - whether stronger completion language was earned

## Recommended Immediate Next Action

Start with Wave 0 plus the audit portion of Wave 1.

That produces the highest signal-to-risk ratio because it freezes:

- the document-skill ownership map
- the duplicated heavy-payload ledger
- the consumer map for verify and reference families

Only after that audit should the next deletion-heavy PR be opened.

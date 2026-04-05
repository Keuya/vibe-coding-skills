# Post-108 Repo Slimming Hotspot Ledger 2026-04-05

## Purpose

Freeze the execution baseline for the post-`#108` GitHub-maintainer repo-slimming program.

This ledger is the Wave 0 reference surface for:

- hotspot ranking
- file-count pressure
- size-pressure hotspots
- candidate execution order

It exists so later deletion or consolidation waves can be judged against the same measured baseline instead of ad hoc impressions.

## Baseline Identity

- baseline branch during planning: `repo-slimming-strong-execution`
- baseline upstream target: `origin/main`
- baseline upstream SHA: `51e7b7b4d129245714a378c1a566523c7847cdbb`
- requirement source:
  - [`../requirements/2026-04-05-post-108-github-maintainer-repo-slimming-program.md`](../requirements/2026-04-05-post-108-github-maintainer-repo-slimming-program.md)
- plan source:
  - [`../plans/2026-04-05-post-108-github-maintainer-repo-slimming-program-plan.md`](../plans/2026-04-05-post-108-github-maintainer-repo-slimming-program-plan.md)

## Top-Level File Pressure

Tracked files by top family at the post-`#108` baseline:

| Family | Tracked Files |
| --- | ---: |
| `bundled/` | 2120 |
| `docs/` | 370 |
| `scripts/` | 309 |
| `config/` | 151 |
| `tests/` | 149 |
| `references/` | 136 |
| `packages/` | 97 |
| `adapters/` | 41 |
| `core/` | 30 |
| `apps/` | 17 |
| `dist/` | 17 |

Interpretation:

- `bundled/` is still the overwhelmingly dominant tracked-file surface
- `docs/` and `references/` are no longer the first-order problem after `#108`
- the next strong slimming waves should attack `bundled/`, `scripts/`, `config/`, and consumer-governed reference families

## Size Pressure Hotspots

Largest tracked size hotspots at the same baseline:

| Path Family | Approx Size |
| --- | ---: |
| `bundled/skills` | 21.42 MiB |
| `logo.png` | 1.71 MiB |
| `scripts/verify` | 1.09 MiB |
| `scripts/router` | 0.57 MiB |
| `references/fixtures` | 0.53 MiB |
| `tests/runtime_neutral` | 0.44 MiB |
| `docs/assets` | 0.33 MiB |
| `config/skill-routing-rules.json` | 0.31 MiB |
| `scripts/runtime` | 0.30 MiB |
| `docs/plans` | 0.27 MiB |

Interpretation:

- size and file pressure are now tightly concentrated, not uniformly spread
- the next maintenance win comes from reducing duplicated bundled payloads and verify/config sprawl

## Active Execution Priority

### P0

These are the highest-value next-wave targets.

1. `bundled/skills/document-skills/**`
2. `bundled/skills/docx/**` and directly related standalone document skill surfaces
3. duplicated OOXML schema and document-tooling payloads
4. `scripts/verify/**` family convergence
5. `references/fixtures/**` consumer-led retention reform

### P1

These matter, but should move only after consumer and truth-surface mapping is explicit.

1. `config/skill-routing-rules.json`
2. `config/skills-lock.json`
3. `config/pack-manifest.json`
4. `config/runtime-core-packaging*.json`
5. `config/dependency-map.json`
6. high-reference bundled skills with comparatively light core payloads
7. compatibility alias skills

### P2

These are not the current first-order targets.

1. GitHub root entrypoint downshift
2. large static assets like `logo.png`
3. already-small families such as `vendor/`, `benchmarks/`, and `third_party/`

## Wave Order Rationale

The recommended execution order is:

1. freeze hotspot and protected-surface ledgers
2. document-skill payload ownership and dedup
3. verify surface convergence
4. fixture and proof retention reform
5. config truth-surface reduction
6. GitHub-root polish only after structural changes settle

This order deliberately avoids spending review budget on cosmetic root cleanup before the dominant hotspot families are controlled.

## Maintainer Metrics To Report Per Wave

Every future slimming wave should report:

1. tracked-file delta
2. touched hotspot-family file delta
3. touched hotspot-family size delta when measurable
4. duplicate asset families removed or unified
5. verification commands actually run
6. rollback or retention decisions for ambiguous consumers

## Notes

- This ledger is intentionally maintainer-facing and GitHub-facing.
- It should be updated only when a merged wave materially changes hotspot ranking or path-role ownership.

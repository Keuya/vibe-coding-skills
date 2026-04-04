# Repo Slimming Path Role Matrix

## Purpose

This matrix is the Wave 0 inventory freeze for the 2026-04-04 strong repo-slimming program.

It classifies major path families by ownership role so later waves can slim the repository without guessing which surfaces are canonical, archive-first, generated, or protected.

## Source Requirement / Plan

- [`../requirements/2026-04-04-strong-repo-slimming-program.md`](../requirements/2026-04-04-strong-repo-slimming-program.md)
- [`../plans/2026-04-04-strong-repo-slimming-program-plan.md`](../plans/2026-04-04-strong-repo-slimming-program-plan.md)

## Matrix

| Path Family | Primary Role | Current Policy | Next Wave |
| --- | --- | --- | --- |
| `docs/README.md`, `docs/status/**`, `docs/install/**` | live navigation / canonical docs | keep live and concise | maintain |
| `docs/plans/*.md` active window | live planning spine | keep only active and near-active plans live | Wave 1 |
| `docs/archive/plans/**` | archive | move historical plans and reports here | Wave 1 |
| `docs/requirements/*.md` active window | governed requirement authority | keep current root and still-referenced baselines live | Wave 1 |
| `docs/archive/requirements/**` | archive | move closed or zero-consumer requirement packets here | Wave 1 |
| `docs/releases/*.md` recent window | release navigation / governed note surface | keep current and recent governed versions live | Wave 2 |
| `docs/archive/releases/**` | archive | move older release notes out of the active surface | Wave 1 / 2 |
| `references/changelog.md` | canonical stable path with oversized history | preserve path, split current vs archive history | Wave 2 |
| `references/proof-bundles/**` | fixture / proof | retain manifests and minimum receipts; archive bulky raw logs when safe | Wave 3 |
| `references/awesome-mcp-servers.snapshot.json` | reproducible snapshot candidate | retire tracked blob; generate on demand into `outputs/research/**` | Wave 3 |
| `references/fixtures/**` | fixture | keep only consumer-backed families live | Wave 3 |
| `scripts/verify/**` | protected contract-first surface | do not mass-delete; merge only after contract extraction | Wave 4+ |
| `scripts/governance/**`, `scripts/runtime/**`, `scripts/router/**` | compatibility / execution shims | audit wrappers and duplicates before deletion | Wave 4 |
| `bundled/skills/**` | packaged payload / protected source family | do not broadly slim before tiering exists | Wave 5 |
| `third_party/**` mirrors | protected external corpus / generated candidate | parameterize roots before any shrinkage | Wave 6 |
| `packages/**`, `core/**`, `adapters/**`, `dist/**`, `tests/runtime_neutral/**`, `tests/integration/**` | protected semantic or verification surfaces | no strong slimming without separate migration owner | protected |

## Decision Rules

- One semantic owner per concern.
- Active README surfaces should point to live spines first and archive indexes second.
- Historical recovery is allowed, but archive material does not regain current authority implicitly.
- Destructive slimming requires a consumer scan and a rollback boundary.

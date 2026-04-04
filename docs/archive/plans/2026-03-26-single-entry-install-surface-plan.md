# Plan: Consolidate the Public Install Surface to One Entry

## Internal Grade

`L`

## Intent

Keep full install coverage while reducing the public install experience to one obvious entrypoint.

## Execution Steps

1. Update install index docs so normal users are directed to a single public install entry.
2. Refactor the single public entry doc to explain that it routes to the four retained base prompt docs.
3. Remove extra install-prompt behavior from:
   - `full-featured-install-prompts.*`
   - `framework-only-path.*`
   - top-level install references in `README.md`
4. Rephrase optional provider / MCP / host-side follow-up as enhancement guidance where appropriate.
5. Sync `docs/install/` into both bundled install-doc mirrors.
6. Run formatting, keyword, and mirror-parity verification.

## Verification

- `git diff --check -- README.md docs/install bundled/skills/vibe/docs/install bundled/skills/vibe/bundled/skills/vibe/docs/install docs/requirements/2026-03-26-single-entry-install-surface.md docs/plans/2026-03-26-single-entry-install-surface-plan.md`
- `cmp -s` for the updated install docs between source and both bundled mirrors
- `rg -n "full-featured-install-prompts|framework-only install|Prompt-based install|直接安装|Install directly" README.md docs/install bundled/skills/vibe/docs/install bundled/skills/vibe/bundled/skills/vibe/docs/install`

## Rollback Rule

If a change removes the four retained prompt docs or turns host-specific references into new install lanes, rewrite before completion.

## Cleanup Expectation

Leave only the requirement doc, plan doc, updated install docs, synced bundled mirrors, and verification evidence.

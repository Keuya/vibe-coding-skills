# Public README Capability-First Opening Execution Plan

**Goal:** Reframe the README so the first impression is about integrated capability scale, resources, and work-domain coverage, then close with the philosophy of standardization.

**Internal Grade:** M

**Wave Structure:**

1. Freeze the narrative shift in governed requirement and plan docs.
2. Rewrite the Chinese and English README openings around capability/resource coverage.
3. Move philosophy into a dedicated closing section.
4. Verify ordering, wording scope, and diff boundaries.

**Ownership Boundaries:**

- `README.md`: Chinese capability-first opening and closing philosophy section
- `README.en.md`: English mirror of the same structure
- `docs/requirements/README.md`: add current governed entry
- `docs/plans/README.md`: add current governed plan entry
- `outputs/runtime/vibe-sessions/<run-id>/...`: runtime evidence and cleanup receipts

**Verification Commands:**

- `sed -n '1,220p' README.md`
- `sed -n '1,220p' README.en.md`
- `git diff -- README.md README.en.md docs/requirements/README.md docs/plans/README.md docs/requirements/2026-03-19-public-readme-capability-first-opening.md docs/plans/2026-03-19-public-readme-capability-first-opening-plan.md`
- `git diff --check -- README.md README.en.md docs/requirements/README.md docs/plans/README.md docs/requirements/2026-03-19-public-readme-capability-first-opening.md docs/plans/2026-03-19-public-readme-capability-first-opening-plan.md`

**Rollback Rules:**

- Do not touch installation docs, manifesto content, or asset paths in this pass.
- If wording creates unsupported product claims, revert to the last bounded wording before closing.
- Keep existing source-SVG reference intact.

**Phase Cleanup Expectations:**

- Record the README narrative pass in a phase receipt.
- Emit cleanup receipt after verification with no temp-file residue.

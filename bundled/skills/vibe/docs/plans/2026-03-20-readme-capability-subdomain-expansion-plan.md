# README Capability Subdomain Expansion Plan

**Goal:** Keep the current Chinese README capability matrix, then add a second-pass subdomain expansion layer that explains what each major capability area covers in finer-grained work terms.

**Internal Grade:** M

**Wave Structure:**

1. Freeze the second-pass expansion intent in governed requirement / plan docs.
2. Keep the existing top-level matrix unchanged as the high-level scan surface.
3. Add grouped subdomain breakdown tables under the matrix in `README.md`.
4. Verify readability, markdown integrity, and diff scope.

**Execution Rules:**

- Preserve the current capability-first opening.
- Do not turn the README into a literal skills dump.
- Expand by user-facing work clusters, not by internal directory structure.
- Keep the detailed layer readable by grouping the 20 domains into a few larger sections.

**Planned README Shape:**

- top-level capability matrix remains
- new “subdomain expansion” section follows
- grouped tables:
  - planning / architecture / engineering
  - governance / routing / integration / docs
  - data / ML / research / life science / scientific computing
  - visualization / media / content production

**Verification Commands:**

- `sed -n '1,260p' README.md`
- `git diff -- README.md docs/requirements/2026-03-20-readme-capability-subdomain-expansion.md docs/plans/2026-03-20-readme-capability-subdomain-expansion-plan.md docs/requirements/README.md docs/plans/README.md`
- `git diff --check -- README.md docs/requirements/2026-03-20-readme-capability-subdomain-expansion.md docs/plans/2026-03-20-readme-capability-subdomain-expansion-plan.md docs/requirements/README.md docs/plans/README.md`

**Rollback Rules:**

- If the detailed layer becomes too long, compress within grouped tables instead of deleting breadth entirely.
- Do not widen scope into a full README rewrite or English sync in this pass.
- Keep changes centered on the Chinese README opening plus governed trace files.

**Phase Cleanup Expectations:**

- Leave behind verification output showing the new grouped subdomain section.
- Ensure markdown formatting is clean before completion.

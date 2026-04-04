# README Detailed Capability Matrix Execution Plan

**Goal:** Replace the shallow README capability summary with a denser, clearer capability matrix that explains what the repository can actually do across major domains.

**Internal Grade:** M

**Wave Structure:**

1. Freeze the rewrite intent in governed requirement and plan docs.
2. Rewrite the Chinese README capability section into a detailed matrix.
3. Mirror the structure in the English README.
4. Verify readability, diff scope, and formatting.

**Rewrite Rules:**

- Keep the opening capability-first structure.
- Replace vague bullet-list coverage with a multi-row table.
- Use domain-based grouping rather than attempting a literal 340-row dump.
- Include concrete examples of representative skill families in each row.

**Planned Table Shape:**

- domain / capability area
- representative skills or systems
- what the repository can do in that area
- typical user-facing outcomes

**Verification Commands:**

- `sed -n '1,220p' README.md`
- `sed -n '1,220p' README.en.md`
- `git diff -- README.md README.en.md docs/requirements/2026-03-20-readme-detailed-capability-matrix.md docs/plans/2026-03-20-readme-detailed-capability-matrix-plan.md docs/requirements/README.md docs/plans/README.md`
- `git diff --check -- README.md README.en.md docs/requirements/2026-03-20-readme-detailed-capability-matrix.md docs/plans/2026-03-20-readme-detailed-capability-matrix-plan.md docs/requirements/README.md docs/plans/README.md`

**Rollback Rules:**

- If the table becomes too long and unreadable, compress examples rather than removing capability breadth.
- Do not widen scope beyond the README opening and governed trace files.
- Do not attempt to enumerate all 340 skills one by one.

**Phase Cleanup Expectations:**

- Keep evidence of the final table structure in the phase receipt.
- Emit cleanup receipt after verification.

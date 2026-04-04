# Public README Skill Activation Pain Point Execution Plan

**Goal:** Add the low skill activation rate pain point to the public README, explain how the VCO ecosystem improves activation in real workflows, and publish the current version to GitHub.

**Internal Grade:** M

**Wave Structure:**

1. Freeze the README pain-point addition in governed requirement and plan docs.
2. Update Chinese and English README pain-point and routing/ecosystem sections.
3. Verify wording, diff boundaries, and formatting.
4. Publish the current version to GitHub using the safest non-destructive path for the current branch state.

**Ownership Boundaries:**

- `README.md`: Chinese pain-point and VCO ecosystem explanation
- `README.en.md`: English mirror
- `docs/requirements/README.md`: register new governed requirement
- `docs/plans/README.md`: register new governed plan
- `outputs/runtime/vibe-sessions/<run-id>/...`: evidence and cleanup receipts

**Verification Commands:**

- `sed -n '1,260p' README.md`
- `sed -n '1,260p' README.en.md`
- `git diff -- README.md README.en.md docs/requirements/README.md docs/plans/README.md docs/requirements/2026-03-19-public-readme-skill-activation-pain-point.md docs/plans/2026-03-19-public-readme-skill-activation-pain-point-plan.md`
- `git diff --check -- README.md README.en.md docs/requirements/README.md docs/plans/README.md docs/requirements/2026-03-19-public-readme-skill-activation-pain-point.md docs/plans/2026-03-19-public-readme-skill-activation-pain-point-plan.md`
- remote read-back of published README content

**Rollback Rules:**

- Do not widen the claim beyond routing, workflow orchestration, MCP/plugin entry points, and governed runtime behavior.
- Do not attempt destructive git reset, checkout, or history rewrite in this dirty worktree.
- If direct git push is unsafe, publish through GitHub API/MCP instead.

**Phase Cleanup Expectations:**

- Record verification and publish path in the phase receipt.
- Emit cleanup receipt after remote read-back confirmation.

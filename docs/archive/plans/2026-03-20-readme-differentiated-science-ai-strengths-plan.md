# README Differentiated Science / Research / AI Strengths Plan

**Goal:** Sharpen the Chinese README so life sciences, research, and AI engineering read as differentiated strengths rather than just additional coverage rows.

**Internal Grade:** M

**Wave Structure:**

1. Freeze a narrow governed pass focused on the three target capability areas.
2. Update the top-level capability matrix wording for those three rows.
3. Update the subdomain expansion wording for those same rows.
4. Add a concise summary paragraph that explains why these areas are unusually strong in this repository.
5. Verify formatting and diff scope.

**Execution Rules:**

- Keep the current README structure intact.
- Focus on strength, depth, and workflow completeness rather than hype.
- Make the wording feel sharper, not noisier.
- Stay within Chinese README scope only.

**Verification Commands:**

- `sed -n '24,95p' README.md`
- `git diff -- README.md docs/requirements/2026-03-20-readme-differentiated-science-ai-strengths.md docs/plans/2026-03-20-readme-differentiated-science-ai-strengths-plan.md docs/requirements/README.md docs/plans/README.md`
- `git diff --check -- README.md docs/requirements/2026-03-20-readme-differentiated-science-ai-strengths.md docs/plans/2026-03-20-readme-differentiated-science-ai-strengths-plan.md docs/requirements/README.md docs/plans/README.md`

**Rollback Rules:**

- If the wording becomes too promotional, pull it back toward concrete workflow language.
- Do not widen scope into a full section rewrite outside the three target areas.

**Phase Cleanup Expectations:**

- Capture verification evidence for the strengthened lines and summary paragraph.
- Leave a cleanup receipt for this governed pass.

# Public README Capability Snapshot Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a pure-Markdown capability snapshot panel to the Chinese and English README hero area so the public homepage feels more like a strong capability surface and less like plain prose.

**Architecture:** Reuse already-verified repository facts and reformat the existing `At A Glance` zone into a more visual capability panel. Keep the current headline and narrative structure intact, but insert a stronger display layer between the headline block and the comparison section.

**Tech Stack:** Markdown, repository docs, git verification, PowerShell node audit scripts

---

### Task 1: Freeze traceability for the capability-snapshot pass

**Files:**

- Create: `docs/requirements/2026-03-19-public-readme-capability-snapshot.md`
- Create: `docs/plans/2026-03-19-public-readme-capability-snapshot-design.md`
- Create: `docs/plans/2026-03-19-public-readme-capability-snapshot-plan.md`
- Modify: `docs/requirements/README.md`
- Modify: `docs/plans/README.md`

**Step 1: Write the frozen requirement and design documents**

Document the chosen “capability battle report panel” approach, the constraints, and the evidence sources.

**Step 2: Update plan and requirement indexes**

Insert the new requirement and plan as current-entry items so this pass stays traceable.

**Step 3: Verify docs exist**

Run: `ls docs/requirements/2026-03-19-public-readme-capability-snapshot.md docs/plans/2026-03-19-public-readme-capability-snapshot-design.md docs/plans/2026-03-19-public-readme-capability-snapshot-plan.md`
Expected: all three files listed

### Task 2: Rewrite the capability panel in both READMEs

**Files:**

- Modify: `README.md`
- Modify: `README.en.md`

**Step 1: Replace the plain `At A Glance` bullet block with a panel-like snapshot**

Create a short section that visually groups:

- scale metrics
- governed execution traits
- a short concluding line

**Step 2: Keep the rest of the hero flow intact**

Do not move installation upward. Do not weaken the existing title and subtitle. Keep the downstream difference section readable.

**Step 3: Verify first-screen readability**

Run: `sed -n '1,80p' README.md && echo '---' && sed -n '1,80p' README.en.md`
Expected: title -> subtitle -> capability snapshot -> difference section order is visible

### Task 3: Verify facts and phase hygiene

**Files:**

- None created intentionally beyond audit receipts

**Step 1: Verify snapshot facts**

Run:

```bash
find bundled/skills -mindepth 1 -maxdepth 1 -type d | wc -l
node -e "const x=require('./config/upstream-corpus-manifest.json'); console.log((x.entries||[]).length)"
ls config/*.json | wc -l
```

Expected:

- `340`
- `19`
- `129`

**Step 2: Verify diff scope**

Run: `git diff --stat -- README.md README.en.md docs/requirements/2026-03-19-public-readme-capability-snapshot.md docs/plans/2026-03-19-public-readme-capability-snapshot-design.md docs/plans/2026-03-19-public-readme-capability-snapshot-plan.md docs/requirements/README.md docs/plans/README.md`
Expected: only the intended README and doc-trace files appear

**Step 3: Run phase hygiene evidence**

Run:

```bash
pwsh -File scripts/governance/Invoke-NodeProcessAudit.ps1
pwsh -File scripts/governance/Invoke-NodeZombieCleanup.ps1
```

Expected: `0` node processes and `0` cleanup candidates

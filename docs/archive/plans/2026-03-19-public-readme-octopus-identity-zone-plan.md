# Public README Octopus Identity Zone Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a simple, memorable octopus identity zone to the Chinese and English README hero without introducing image assets.

**Architecture:** Insert a compact ASCII/Markdown “cute octopus core” block directly under the README title so it acts like a lightweight brand mark. Keep the current propagation headline, capability snapshot, and comparison sections intact, using the octopus block as a recognition layer rather than a replacement.

**Tech Stack:** Markdown, repository docs, git verification, PowerShell node audit scripts

---

### Task 1: Freeze the branding pass

**Files:**

- Create: `docs/requirements/2026-03-19-public-readme-octopus-identity-zone.md`
- Create: `docs/plans/2026-03-19-public-readme-octopus-identity-zone-plan.md`
- Modify: `docs/requirements/README.md`
- Modify: `docs/plans/README.md`

**Step 1: Write the requirement doc**

Capture the approved “cute octopus core” direction, constraints, and acceptance criteria.

**Step 2: Register the plan in the indexes**

Add the requirement and plan to the current-entry surfaces so the pass stays traceable.

**Step 3: Verify the docs exist**

Run: `ls docs/requirements/2026-03-19-public-readme-octopus-identity-zone.md docs/plans/2026-03-19-public-readme-octopus-identity-zone-plan.md`
Expected: both files listed

### Task 2: Insert the octopus identity block in both READMEs

**Files:**

- Modify: `README.md`
- Modify: `README.en.md`

**Step 1: Add the octopus block below `# VibeSkills`**

Use the approved “cute octopus core” layout, keeping it short and easy to scan.

**Step 2: Preserve hero hierarchy**

Keep the order readable:

- title
- octopus identity zone
- tagline / explanation
- capability snapshot
- comparison section

**Step 3: Verify first-screen order**

Run: `sed -n '1,60p' README.md && echo '---' && sed -n '1,60p' README.en.md`
Expected: the octopus identity zone appears immediately after the title in both files

### Task 3: Verify and clean up

**Files:**

- None intentionally beyond receipts

**Step 1: Verify diff scope**

Run: `git diff --stat -- README.md README.en.md docs/requirements/2026-03-19-public-readme-octopus-identity-zone.md docs/plans/2026-03-19-public-readme-octopus-identity-zone-plan.md docs/requirements/README.md docs/plans/README.md`
Expected: only README and governance trace files appear

**Step 2: Verify worktree state**

Run: `git status --short --branch`
Expected: only expected local documentation changes remain

**Step 3: Run phase hygiene evidence**

Run:

```bash
pwsh -File scripts/governance/Invoke-NodeProcessAudit.ps1
pwsh -File scripts/governance/Invoke-NodeZombieCleanup.ps1
```

Expected: `0` node processes and `0` cleanup candidates

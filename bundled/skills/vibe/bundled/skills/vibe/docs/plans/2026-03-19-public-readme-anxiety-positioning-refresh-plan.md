# Public README Anxiety Positioning Refresh Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Remove the octopus Markdown identity zone and reframe the README hero around AI-era anxiety, choice overload, and VibeSkills as the governed answer to that problem.

**Architecture:** Keep the strong headline and capability snapshot, but replace the mascot-style identity layer with two short narrative paragraphs: first the present-day AI anxiety and fragmentation problem, then VibeSkills as the system-level response. Preserve the downstream comparison and installation ordering.

**Tech Stack:** Markdown, repository docs, git verification, PowerShell node audit scripts

---

### Task 1: Freeze the refresh pass

**Files:**

- Create: `docs/requirements/2026-03-19-public-readme-anxiety-positioning-refresh.md`
- Create: `docs/plans/2026-03-19-public-readme-anxiety-positioning-refresh-plan.md`
- Modify: `docs/requirements/README.md`
- Modify: `docs/plans/README.md`

**Step 1: Write the requirement doc**
Capture the approved “remove octopus, use anxiety + response” direction.

**Step 2: Register the plan in the indexes**
Add the new requirement and plan to the current-entry surfaces.

**Step 3: Verify the docs exist**
Run: `ls docs/requirements/2026-03-19-public-readme-anxiety-positioning-refresh.md docs/plans/2026-03-19-public-readme-anxiety-positioning-refresh-plan.md`
Expected: both files listed

### Task 2: Rewrite the README hero in both languages

**Files:**

- Modify: `README.md`
- Modify: `README.en.md`

**Step 1: Remove the octopus Markdown block**
Delete the mascot-style ASCII identity zone from both READMEs.

**Step 2: Add the anxiety paragraph and response paragraph**
Insert two short blocks after the main headline area:

- AI-era anxiety and overload
- VibeSkills as the governed response

**Step 3: Preserve the rest of the hero flow**
Keep:

- main judgment headline
- capability snapshot
- difference section
- installation still below the core narrative

**Step 4: Verify first-screen order**
Run: `sed -n '1,70p' README.md && echo '---' && sed -n '1,70p' README.en.md`
Expected: no octopus block; anxiety + response paragraphs appear before the capability snapshot

### Task 3: Verify and clean up

**Files:**

- None intentionally beyond receipts

**Step 1: Verify diff scope**
Run: `git diff --stat -- README.md README.en.md docs/requirements/2026-03-19-public-readme-anxiety-positioning-refresh.md docs/plans/2026-03-19-public-readme-anxiety-positioning-refresh-plan.md docs/requirements/README.md docs/plans/README.md`
Expected: only README and governance trace files appear

**Step 2: Verify worktree state**
Run: `git status --short --branch`
Expected: only expected documentation changes remain

**Step 3: Run phase hygiene evidence**
Run:

```bash
pwsh -File scripts/governance/Invoke-NodeProcessAudit.ps1
pwsh -File scripts/governance/Invoke-NodeZombieCleanup.ps1
```

Expected: `0` node processes and `0` cleanup candidates

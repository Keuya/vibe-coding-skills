# Public README Poster Hero Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rebuild the public Chinese and English README into a poster-style landing surface with a reusable octopus logo and GitHub-safe HTML/SVG layout.

**Architecture:** Keep the repo public homepage GitHub-native. Use SVG assets for the hero layer, HTML tables for horizontal information cards, and Markdown for the long-lived narrative and navigation links. Preserve the current positioning message while upgrading the visual hierarchy.

**Tech Stack:** Markdown, GitHub-safe inline HTML, SVG assets, governed docs indexes, git verification commands

---

### Task 1: Freeze the poster-hero pass

**Files:**
- Create: `docs/requirements/2026-03-19-public-readme-poster-hero.md`
- Create: `docs/plans/2026-03-19-public-readme-poster-hero-design.md`
- Create: `docs/plans/2026-03-19-public-readme-poster-hero-plan.md`
- Modify: `docs/requirements/README.md`
- Modify: `docs/plans/README.md`

**Step 1: Write the frozen requirement**

Capture the approved `Hybrid` visual direction, GitHub rendering constraints, and asset scope.

**Step 2: Write the design document**

Record the visual system, content hierarchy, and rationale for `SVG + HTML + Markdown`.

**Step 3: Register the pass in current-entry indexes**

Add the new requirement and plan to the README indexes so the pass remains traceable.

**Step 4: Verify the docs exist**

Run: `ls docs/requirements/2026-03-19-public-readme-poster-hero.md docs/plans/2026-03-19-public-readme-poster-hero-design.md docs/plans/2026-03-19-public-readme-poster-hero-plan.md`
Expected: all three files listed

### Task 2: Create the visual assets

**Files:**
- Create: `docs/assets/vibeskills-octopus-mark.svg`
- Create: `docs/assets/readme-poster-hero-cn.svg`
- Create: `docs/assets/readme-poster-hero-en.svg`

**Step 1: Create the reusable octopus logo**

Draw a minimal cute octopus mark with a professional palette and transparent background.

**Step 2: Create the Chinese poster hero**

Build a horizontal SVG hero that combines title, supporting line, scale stats, and the octopus visual field.

**Step 3: Create the English poster hero**

Mirror the Chinese composition with English copy while preserving the same visual weight.

**Step 4: Verify the assets exist**

Run: `ls docs/assets/vibeskills-octopus-mark.svg docs/assets/readme-poster-hero-cn.svg docs/assets/readme-poster-hero-en.svg`
Expected: all three SVG files listed

### Task 3: Rebuild the README surfaces

**Files:**
- Modify: `README.md`
- Modify: `README.en.md`

**Step 1: Insert the poster hero and logo**

Place the hero SVG at the top of each README, followed by the reusable octopus mark and a centered title block.

**Step 2: Upgrade the capability snapshot**

Replace the plain first-screen table feeling with HTML cards while keeping the verified numbers.

**Step 3: Preserve and tighten the narrative**

Keep the existing positioning message, but reflow it around the new poster-style hierarchy.

**Step 4: Add clear quick paths**

Present `quick-start`, `manifesto`, and install entry points as landing-page-style navigation panels.

**Step 5: Verify the first-screen structure**

Run: `sed -n '1,120p' README.md && echo '---' && sed -n '1,120p' README.en.md`
Expected: language link, hero image, logo/title block, capability cards, and quick-path structure all appear in order

### Task 4: Verify scope and finish cleanly

**Files:**
- None intentionally beyond receipts

**Step 1: Verify diff scope**

Run: `git diff --stat -- README.md README.en.md docs/assets/vibeskills-octopus-mark.svg docs/assets/readme-poster-hero-cn.svg docs/assets/readme-poster-hero-en.svg docs/requirements/2026-03-19-public-readme-poster-hero.md docs/plans/2026-03-19-public-readme-poster-hero-design.md docs/plans/2026-03-19-public-readme-poster-hero-plan.md docs/requirements/README.md docs/plans/README.md`
Expected: only README, assets, and governance trace files appear

**Step 2: Verify worktree state**

Run: `git status --short --branch`
Expected: only the intended poster-hero changes remain

**Step 3: Preserve cleanup evidence**

Check the latest governed cleanup receipt under `outputs/runtime/vibe-sessions/.../hook-stop-cleanup.json`
Expected: phase cleanup evidence exists for the turn

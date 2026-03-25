# Public README Philosophy And Source Image Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Update the public README to lead with the philosophy of standardization, embed the author-provided Gemini SVG directly, and rewrite the capability explanation in simpler language.

**Architecture:** Keep the README in standard GitHub Markdown/HTML. Add the original SVG as a repo asset, rewrite the top-of-page philosophy and capability snapshot, and document the pass in governed requirement / plan traces.

**Tech Stack:** Markdown, GitHub-safe HTML image embedding, governed docs indexes, local SVG asset management, git verification

---

### Task 1: Freeze the README philosophy + source-image pass

**Files:**
- Create: `docs/requirements/2026-03-19-public-readme-philosophy-and-source-image.md`
- Create: `docs/plans/2026-03-19-public-readme-philosophy-and-source-image-design.md`
- Create: `docs/plans/2026-03-19-public-readme-philosophy-and-source-image-plan.md`
- Modify: `docs/requirements/README.md`
- Modify: `docs/plans/README.md`

**Step 1: Write the frozen requirement**

Capture the user request to stop poster design, embed the original Gemini SVG directly, and foreground the philosophy of standardization.

**Step 2: Write the design document**

Record why the README should now become more direct and philosophy-led instead of art-directed.

**Step 3: Register the pass in indexes**

Add the new requirement and plan to the current-entry indexes.

### Task 2: Add the source image to the repo

**Files:**
- Create: `docs/assets/Gemini_Generated_Image_75f8n575f8n575f8.svg`

**Step 1: Copy the source SVG into repo assets**

Use the user-provided file directly without redesigning it.

**Step 2: Verify the file exists**

Run: `ls -l docs/assets/Gemini_Generated_Image_75f8n575f8n575f8.svg`
Expected: the SVG file is present in repo assets

### Task 3: Rewrite README top sections

**Files:**
- Modify: `README.md`
- Modify: `README.en.md`

**Step 1: Replace the opening positioning**

Lead with the philosophy that standardization is the core principle.

**Step 2: Embed the original Gemini SVG**

Place the image after the philosophy framing and before the capability snapshot.

**Step 3: Rewrite the capability snapshot**

Use simpler language that explains skills, upstream inspirations, governance contracts, and the role of MCP / plugin / workflow integration.

**Step 4: Name the upstream projects**

Explicitly mention representative integrated inspirations such as `superpower`, `claude-scientific-skills`, `get-shit-done`, `aios-core`, `OpenSpec`, `ralph-claude-code`, and `SuperClaude_Framework`.

### Task 4: Verify and prepare release

**Step 1: Verify README order**

Run: `sed -n '1,120p' README.md && echo '---' && sed -n '1,120p' README.en.md`
Expected: philosophy first, image second, simplified capability table third

**Step 2: Verify diff scope**

Run: `git diff --stat -- README.md README.en.md docs/assets/Gemini_Generated_Image_75f8n575f8n575f8.svg docs/requirements/README.md docs/plans/README.md docs/requirements/2026-03-19-public-readme-philosophy-and-source-image.md docs/plans/2026-03-19-public-readme-philosophy-and-source-image-design.md docs/plans/2026-03-19-public-readme-philosophy-and-source-image-plan.md`
Expected: only intended README, asset, and governed-trace files appear

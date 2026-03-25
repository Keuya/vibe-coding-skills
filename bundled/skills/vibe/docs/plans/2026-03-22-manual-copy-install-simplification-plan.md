# 2026-03-22 Manual Copy Install Simplification Plan

## Goal

Rewrite the manual copy install guide into a short, checklist-style explanation of what to copy and what remains manual.

## Grade

- Internal grade: M

## Work Batches

### Batch 1: Governance freeze
- Create requirement doc
- Create execution plan

### Batch 2: Chinese guide rewrite
- Rewrite `docs/install/manual-copy-install.md`
- Remove shell command examples
- Keep only the essential copy checklist and post-install boundaries

### Batch 3: English guide alignment
- Rewrite `docs/install/manual-copy-install.en.md`
- Match the simplified Chinese structure and meaning

### Batch 4: Verification
- spot-check both docs for command-block removal
- verify hook-freeze and supported-host wording remains correct
- run `git diff --check`

### Batch 5: Phase cleanup
- confirm no temp artifacts were created
- leave only intended doc changes in the working tree

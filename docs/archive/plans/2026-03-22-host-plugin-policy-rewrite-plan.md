# 2026-03-22 Host Plugin Policy Rewrite Plan

## Goal

Replace the historical host-plugin-policy documents with concise current-state policy docs that match the repo's real support surface.

## Grade

- Internal grade: M

## Work Batches

### Batch 1: Governance freeze
- Create requirement doc
- Create execution plan

### Batch 2: Chinese policy rewrite
- Rewrite `docs/install/host-plugin-policy.md`
- Structure it around current support boundary, host-managed actions, and honest defaults

### Batch 3: English policy rewrite
- Rewrite `docs/install/host-plugin-policy.en.md`
- Keep structure equivalent to the Chinese doc
- Ensure it reads like a native policy document, not a literal translation artifact

### Batch 4: Verification
- grep both files for stale historical terms and unsupported-host claims
- spot-check links and core wording consistency
- run `git diff --check`

### Batch 5: Phase cleanup
- confirm no temp files were created
- leave only intentional documentation edits in git status

## Rollback Rules

- If the rewrite accidentally drops an important truthful boundary, restore that boundary in a shorter form rather than reintroducing historical narrative debt.
- If the English and Chinese files drift semantically, align the English file to the approved Chinese policy intent before completion.

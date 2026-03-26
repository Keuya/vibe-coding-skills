# 2026-03-26 OpenCode PR Delivery Plan

## Goal

Re-verify the OpenCode compatibility work, isolate the intended file set, and submit a pull request with evidence-backed release notes.

## Grade

- Internal grade: L

## Batches

### Batch 1: Freeze and traceability
- Create requirement doc
- Create execution plan
- Emit skeleton and intent receipts for this PR-delivery pass

### Batch 2: Verification
- Run `git diff --check`
- Run adapter closure and target-root guard gates
- Run host adapter and dist manifest gates
- Run OpenCode preview smoke verification
- Run direct shell and PowerShell install/check smoke against temp OpenCode roots

### Batch 3: Commit boundary isolation
- Enumerate task-relevant files
- Create a branch for the OpenCode preview work
- Stage only the OpenCode implementation, doc refresh, proof docs, and governed artifacts
- Create a non-amended commit

### Batch 4: Publish
- Push the branch to `origin`
- Open a PR against `main`
- Include verification evidence and remaining preview limitations in the PR body

### Batch 5: Cleanup
- Emit phase execution and cleanup receipts
- Leave unrelated worktree changes untouched

## Verification Commands

- `git diff --check`
- `pwsh -NoProfile -File ./scripts/verify/vgo-adapter-closure-gate.ps1 -WriteArtifacts`
- `pwsh -NoProfile -File ./scripts/verify/vgo-adapter-target-root-guard-gate.ps1 -WriteArtifacts`
- `pwsh -NoProfile -File ./scripts/verify/vibe-host-adapter-contract-gate.ps1`
- `pwsh -NoProfile -File ./scripts/verify/vibe-dist-manifest-gate.ps1 -WriteArtifacts`
- `python3 ./scripts/verify/runtime_neutral/opencode_preview_smoke.py --repo-root . --write-artifacts`
- `bash ./install.sh --host opencode --target-root <temp>`
- `bash ./check.sh --host opencode --target-root <temp>`
- `pwsh -NoProfile -File ./install.ps1 -HostId opencode -TargetRoot <temp>`
- `pwsh -NoProfile -File ./check.ps1 -HostId opencode -TargetRoot <temp>`

## Rollback Rules

- If verification fails, do not create or update the PR until the failure is explained and resolved.
- If a file cannot be cleanly attributed to this task, leave it unstaged.
- If GitHub auth or push rights fail, stop after preparing the branch and report the blocker with the verified local state.

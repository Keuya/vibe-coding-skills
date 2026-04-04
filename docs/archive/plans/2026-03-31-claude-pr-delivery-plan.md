# 2026-03-31 Claude Adaptation PR Delivery Plan

## Goal

Ship a clean pull request containing the Claude adaptation work and nothing accidental.

## Grade

- Internal grade: L

## Batches

### Batch 1: Freeze scope and inspect repository state
- Record the PR-delivery requirement
- Inspect current branch, remote, dirty files, and upstream status
- Identify the Claude-specific change set that should be carried into the PR

### Batch 2: Isolate a clean delivery branch
- Create a clean worktree or equivalent isolated branch from the latest base
- Copy or patch only the Claude-related files into that isolated branch
- Confirm the resulting diff does not contain unrelated host work

### Batch 3: Verify the isolated branch
- Run the targeted unit tests
- Run the relevant truth and manifest gates
- Recheck any live Linux Claude smoke evidence needed to support the claim set

### Batch 4: Deliver the PR
- Commit with a truthful message
- Push the branch to origin
- Open a PR with a bounded summary, verification notes, and explicit non-claims

## Verification Commands

- `python3 -m unittest tests.runtime_neutral.test_claude_preview_scaffold tests.runtime_neutral.test_installed_runtime_uninstall`
- `pwsh -NoProfile -ExecutionPolicy Bypass -File ./scripts/verify/vibe-host-adapter-contract-gate.ps1`
- `pwsh -NoProfile -ExecutionPolicy Bypass -File ./scripts/verify/vibe-cross-host-route-parity-gate.ps1`
- `pwsh -NoProfile -ExecutionPolicy Bypass -File ./scripts/verify/vibe-dist-manifest-gate.ps1`
- `bash ./install.sh --host claude-code --profile full --target-root <temp-root>`
- `bash ./check.sh --host claude-code --profile full --target-root <temp-root> --deep`
- `CLAUDE_HOME=<temp-root> claude agents`

## Rollback Rules

- If the isolated branch cannot be made cleanly without guessing, stop before commit
- If upstream moved and creates merge ambiguity, rebase only in the isolated branch
- If verification fails on the isolated branch, fix or narrow scope before PR creation

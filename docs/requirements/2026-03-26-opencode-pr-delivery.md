# 2026-03-26 OpenCode PR Delivery Requirement

- Topic: verify the OpenCode compatibility work, isolate the task-relevant change set, and submit a pull request.
- Mode: interactive_governed
- Goal: turn the implemented OpenCode preview adapter and the refreshed documentation into a proof-backed PR without bundling unrelated worktree changes.

## Deliverable

A PR-ready change set that:

1. re-verifies the OpenCode preview adapter and documentation truth against the current repo state
2. keeps only the OpenCode compatibility and doc-refresh files inside the commit boundary
3. preserves unrelated local changes outside the PR
4. creates a branch, commit, and pull request with a concise proof-backed summary

## Constraints

- No regression to Codex or Claude Code truth surfaces
- No false promotion above `preview`
- Do not stage unrelated local changes or historical scratch docs outside the task scope
- Do not amend old commits
- Completion language must be backed by fresh verification output

## Acceptance Criteria

- OpenCode install/check entrypoints still pass on shell and PowerShell paths
- OpenCode adapter/doc gates pass
- OpenCode preview smoke passes
- `git diff --check` passes before commit
- The branch contains only the OpenCode implementation and documentation files plus governed artifacts for this task
- A PR is opened against `main` with verification evidence in the body

## Non-Goals

- Rebasing or updating the local `main` branch
- Cleaning unrelated historical requirement/plan notes from the repo
- Promoting OpenCode to `supported-with-constraints`

## Inferred Assumptions

- The repository owner is the authenticated GitHub user or accessible with existing credentials
- The current dirty worktree includes both task-relevant and unrelated local changes, so staging must be explicit
- The current OpenCode proof bundle is sufficient for a truthful preview PR

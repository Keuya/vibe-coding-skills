# 2026-03-31 Claude Adaptation PR Delivery Requirement

- Topic: collect the Claude-related adaptation changes already prepared in the repository, reconcile them against the latest repository state, and deliver them as a reviewable pull request.
- Mode: interactive_governed
- Goal: produce one truthful PR for the Claude adaptation lane without accidentally bundling unrelated host work.

## Deliverable

A PR-ready branch that:

1. includes the Claude-related adaptation changes that belong together
2. excludes unrelated worktree changes from other hosts or unfinished experiments
3. keeps Linux truth at `supported-with-constraints` only where the frozen evidence supports it
4. keeps Windows and macOS below promotion unless their own proof exists
5. contains an accurate PR title and body that match the actual diff

## Constraints

- No overclaim that Claude reaches Codex official-runtime parity
- No accidental inclusion of unrelated OpenCode, OpenClaw, or generic repo churn
- No destructive cleanup of the user's existing dirty worktree
- Use the latest reachable repository base truth before opening the PR
- Verification must be rerun on the final staged branch before PR creation

## Acceptance Criteria

- A governed requirement doc and plan doc exist for this PR-delivery task
- The Claude PR branch is isolated from unrelated local modifications
- The final staged diff is explainable as one coherent Claude adaptation change set
- Targeted tests and truth gates pass on the branch that is pushed
- A pull request is opened against the repository with a truthful summary

## Non-Goals

- Solving the outstanding Windows proof blocker in this PR
- Promoting macOS in this PR
- Rewriting unrelated repository history

## Inferred Assumptions

- The current dirty worktree contains both Claude-related and unrelated modifications, so isolation is required
- `origin/main` is the intended PR base unless a newer tracked base is discovered during fetch
- GitHub authentication is available either through local git/gh or the configured GitHub integration

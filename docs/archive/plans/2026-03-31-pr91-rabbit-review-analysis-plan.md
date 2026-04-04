# 2026-03-31 PR91 Rabbit Review Analysis Plan

## Goal

Produce a defensible maintainer-grade analysis of Rabbit's PR comments.

## Grade

- Internal grade: M

## Batches

### Batch 1: Collect review signals
- Pull PR reviews, review comments, and issue comments for PR `#91`
- Identify Rabbit-authored items or equivalent automated review outputs

### Batch 2: Validate against code
- Open the exact files and lines referenced by the comments
- Compare the comment claim to the current PR diff and surrounding implementation

### Batch 3: Synthesize maintainer guidance
- Rank comments by severity and confidence
- Mark each as valid, partially valid, or not valid
- Recommend the concrete maintainer response or code action

## Verification Inputs

- `gh pr view 91 --comments`
- `gh pr review-comments 91` if available, or equivalent PR comment APIs
- local diff/context reads for referenced files

## Rollback Rules

- If Rabbit comments are not accessible through one surface, retry through GitHub API surfaces before concluding they are missing
- If comment context and current branch diverge, say which state is being analyzed and why

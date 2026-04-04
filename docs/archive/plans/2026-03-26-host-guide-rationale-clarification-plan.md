# Plan: Clarify Why OpenClaw and OpenCode Have Dedicated Install Guides

## Internal Grade

`M`

## Execution Steps

1. Update the public install index to explain that `openclaw` and `opencode` still work with the generic install prompts.
2. Add a short rationale section to the two dedicated host guides explaining why those pages exist.
3. Sync `docs/install/` into the two bundled install-doc mirrors.
4. Verify formatting and mirror parity.

## Verification

- `git diff --check -- docs/install bundled/skills/vibe/docs/install bundled/skills/vibe/bundled/skills/vibe/docs/install docs/requirements docs/plans`
- `cmp -s` checks for updated install docs across source and bundled mirrors
- `rg -n "通用安装提示词|generic install prompts|专页|dedicated guide|supplemental"` on the updated docs

## Rollback Rule

If the added wording implies that dedicated guides are separate install lanes, rewrite it before completion.

## Cleanup Expectation

Leave only the requirement doc, plan doc, source install-doc updates, and synced bundled mirrors.

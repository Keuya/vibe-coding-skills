# VCO Local Actual-Use Update Execution Plan

- Date: 2026-03-15
- Run ID: `2026-03-15-local-update-v2345`
- Internal Grade: `M`

## Scope

Pull the latest upstream VCO release and reinstall `/home/lqf/.codex` from the updated repo.

## Steps

1. Record current repo and installed version state.
2. Fast-forward the repo to `origin/main`.
3. Inspect release metadata for the new version.
4. Run `install.sh --profile full --target-root "$HOME/.codex"`.
5. Verify installed version and run `check.sh --deep`.

## Verification Commands

- `git -C /home/lqf/table/table2/vco-skills-codex rev-parse HEAD`
- `jq -r '.release.version,.release.updated' /home/lqf/.codex/skills/vibe/config/version-governance.json`
- `bash ./install.sh --profile full --target-root "$HOME/.codex"`
- `bash ./check.sh --profile full --target-root "$HOME/.codex" --deep`

## Rollback Strategy

- if installation drifts, rerun `install.sh` from the updated repo state
- no git rollback is planned because no product code edits are involved

## Cleanup Expectations

- keep only the audit/update artifacts written for this run
- preserve pre-existing untracked requirement/plan artifacts

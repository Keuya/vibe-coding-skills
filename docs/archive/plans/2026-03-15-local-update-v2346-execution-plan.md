# VCO Local Actual-Use Update Execution Plan v2.3.46

- Date: 2026-03-15
- Run ID: `2026-03-15-local-update-v2346`
- Internal Grade: `M`

## Scope

Pull latest upstream VCO and reinstall the real runtime under `/home/lqf/.codex`.

## Steps

1. Capture current repo and installed version state.
2. Fast-forward the repo to `origin/main`.
3. Inspect release metadata for the new version.
4. Run `install.sh --profile full --target-root "$HOME/.codex"`.
5. Verify installed version and run `check.sh --deep`.

## Verification Commands

- `git -C /home/lqf/table/table2/vco-skills-codex rev-parse HEAD`
- `jq -r '.release.version,.release.updated' /home/lqf/.codex/skills/vibe/config/version-governance.json`
- `bash ./install.sh --profile full --target-root "$HOME/.codex"`
- `bash ./check.sh --profile full --target-root "$HOME/.codex" --deep`

## Cleanup Expectations

- preserve pre-existing untracked docs
- write only dedicated runtime artifacts for this run

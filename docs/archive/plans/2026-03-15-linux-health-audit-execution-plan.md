# VCO Linux Health Audit Execution Plan

- Date: 2026-03-15
- Run ID: `2026-03-15-linux-health-audit`
- Internal Grade: `L`

## Scope

Audit Linux health for the real installed runtime and the current repo release `v2.3.43`.

## Wave Structure

### Wave 1: Environment and runtime baseline

- Capture Linux environment details
- Confirm repo commit and installed version
- Confirm runtime prerequisite presence

### Wave 2: Authoritative Linux execution path

- Run installed-root health checks
- Run release/install/runtime coherence checks
- Run current-release verification gates relevant to governed runtime
- Run representative router prompts through the installed runtime

### Wave 3: Pure Linux degraded lane

- Remove `pwsh` from `PATH`
- Re-run shell health check path
- Verify degraded behavior is explicit and non-misleading

### Wave 4: Static compatibility scan

- Scan for absolute Windows paths and drive-letter assumptions
- Scan for shell/runtime assumptions that may fail on Linux
- Record issues with severity and evidence

## Ownership Boundaries

- Repo under test: `/home/lqf/table/table2/vco-skills-codex`
- Installed runtime under test: `/home/lqf/.codex`
- Evidence artifacts for this run: `outputs/runtime/vibe-sessions/2026-03-15-linux-health-audit/`

## Verification Commands

- `bash ./check.sh --profile full --target-root "$HOME/.codex" --deep`
- `pwsh -NoLogo -NoProfile -File ./scripts/verify/vibe-release-install-runtime-coherence-gate.ps1 -TargetRoot "$HOME/.codex"`
- `pwsh -NoLogo -NoProfile -File ./scripts/verify/vibe-governed-runtime-contract-gate.ps1`
- `python3 -m unittest discover -s tests/runtime_neutral -p "test_governed_runtime_bridge.py"`
- `pwsh -NoLogo -NoProfile -File "$HOME/.codex/skills/vibe/scripts/router/resolve-pack-route.ps1" ...`
- `env PATH="..." bash ./check.sh --profile full --target-root "$HOME/.codex" --deep`
- `rg` static scans for Linux-sensitive path assumptions

## Rollback Strategy

- No product code changes are planned, so rollback is not needed.
- If the installed runtime drifts during testing, restore it from the current repo using `install.sh`.

## Cleanup Expectations

- Preserve only audit artifacts created for this run
- Do not leave temporary directories outside the dedicated run folder
- Record degraded-lane and node/process observations in the cleanup receipt

# VCO Linux Health Audit Execution Plan v2.3.45

- Date: 2026-03-15
- Run ID: `2026-03-15-linux-health-v2345`
- Internal Grade: `L`

## Scope

Audit Linux health for VCO `v2.3.45` on the real local installed runtime.

## Waves

### Wave 1: Baseline

- confirm repo head, release version, installed version, and Linux environment

### Wave 2: Authoritative Linux-with-pwsh lane

- run `check.sh --deep`
- run governed runtime contract gate
- run benchmark autonomous proof gate
- run runtime-neutral Python bridge tests
- run Linux router no-pwsh gate wrapper if applicable

### Wave 3: Pure Linux no-pwsh lane

- remove `pwsh` from `PATH`
- rerun shell health check
- verify whether routing remains available through the Python bridge

### Wave 4: Findings and cleanup

- summarize failures or degradations
- write execution and cleanup receipts

## Verification Commands

- `bash ./check.sh --profile full --target-root "$HOME/.codex" --deep`
- `pwsh -NoLogo -NoProfile -File ./scripts/verify/vibe-governed-runtime-contract-gate.ps1`
- `pwsh -NoLogo -NoProfile -File ./scripts/verify/vibe-benchmark-autonomous-proof-gate.ps1`
- `python3 -m unittest discover -s tests/runtime_neutral -p "test_governed_runtime_bridge.py" -v`
- `python3 -m unittest discover -s tests/runtime_neutral -p "test_router_bridge.py" -v`
- `pwsh -NoLogo -NoProfile -File ./scripts/verify/vibe-linux-router-no-pwsh-gate.ps1`
- `env -i ... bash --noprofile --norc -c 'bash ./check.sh ...'`
- `env -i ... bash --noprofile --norc -c 'python3 scripts/router/invoke-pack-route.py --force-runtime-neutral ...'`

## Rollback Strategy

- no product code change is planned
- if the installed runtime drifts, rerun `install.sh` from the current repo state

## Cleanup Expectations

- keep only dedicated run artifacts
- leave pre-existing untracked plan/requirement docs untouched

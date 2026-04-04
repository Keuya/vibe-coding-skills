# VCO Linux Health Audit Execution Plan

Date: 2026-03-15
Requirement: docs/requirements/2026-03-15-linux-health-v2347.md
Internal Grade: L

## Waves

### Wave 1: Installed Runtime Integrity

- Verify repo and installed runtime versions match at 2.3.47
- Run the runtime-neutral freshness gate against `/home/lqf/.codex`
- Run `check.sh --profile full --target-root "$HOME/.codex" --deep`

### Wave 2: Linux Functional Proof Surface

- Run `tests/runtime_neutral/test_router_bridge.py`
- Run `tests/runtime_neutral/test_governed_runtime_bridge.py`
- Run `scripts/verify/vibe-governed-runtime-contract-gate.ps1`
- Run `scripts/verify/vibe-benchmark-autonomous-proof-gate.ps1`
- Run `scripts/verify/vibe-linux-router-no-pwsh-gate.ps1`

### Wave 3: Real-Use Router Samples

- Run installed-copy `invoke-pack-route.py` with representative planning and low-signal prompts
- Confirm route mode, pack selection, and runtime-neutral bridge metadata

### Wave 4: Verdict Synthesis

- Classify each failure, if any, as environment red, version red, or test-assumption red
- Report whether Linux operation is healthy, degraded-but-honest, or regressed
- Call out any functional downgrade introduced by the latest update

## Verification Commands

```bash
jq -r '.release.version,.release.updated' /home/lqf/.codex/skills/vibe/config/version-governance.json
python3 scripts/verify/runtime_neutral/freshness_gate.py --target-root "$HOME/.codex" --write-receipt
bash ./check.sh --profile full --target-root "$HOME/.codex" --deep
python3 -m unittest discover -s tests/runtime_neutral -p 'test_router_bridge.py' -v
python3 -m unittest discover -s tests/runtime_neutral -p 'test_governed_runtime_bridge.py' -v
pwsh -NoLogo -NoProfile -File ./scripts/verify/vibe-governed-runtime-contract-gate.ps1
pwsh -NoLogo -NoProfile -File ./scripts/verify/vibe-benchmark-autonomous-proof-gate.ps1
pwsh -NoLogo -NoProfile -File ./scripts/verify/vibe-linux-router-no-pwsh-gate.ps1
python3 /home/lqf/.codex/skills/vibe/scripts/router/invoke-pack-route.py --prompt 'create implementation plan and task breakdown' --grade L --task-type planning --force-runtime-neutral --target-root "$HOME/.codex"
python3 /home/lqf/.codex/skills/vibe/scripts/router/invoke-pack-route.py --prompt 'help me with this' --grade M --task-type research --force-runtime-neutral --target-root "$HOME/.codex"
```

## Rollback Rules

- Do not change installed runtime contents during the audit
- If a failure is caused by transient repo-generated artifacts, identify it explicitly before cleaning it
- Do not delete existing user-authored untracked audit documents

## Cleanup Expectations

- Remove only audit-generated transient artifacts if they affect health gates
- Preserve requirement and plan documents created for this governed audit

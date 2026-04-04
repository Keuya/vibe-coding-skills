# Tracked Mirror Retirement Execution Plan

## Internal Grade

- Grade: `L`
- Reason: 这是多文件基础设施重构，但关键路径集中在 config / install / release / verify，适合单线串行收口。

## Work Batches

1. Freeze governed artifacts and baseline assumptions.
2. Refactor truth contracts from tracked mirror to canonical payload + generated compatibility.
3. Refactor install / uninstall / release / coherence paths to stop depending on repo mirror closure.
4. Update targeted docs and tests, then remove `bundled/skills/vibe`.
5. Run verification and emit cleanup receipts.

## Ownership Boundaries

- Config truth: `config/version-governance.json`, `config/runtime-core-packaging*.json`, `config/dependency-map.json`
- Install / uninstall: `scripts/install/*`, `scripts/uninstall/*`
- Governance / verify: `scripts/common/*`, `scripts/governance/*`, `scripts/verify/*`
- Active docs and governed artifacts: `docs/version-packaging-governance.md`, current requirement/plan docs, runtime session receipts

## Verification Commands

- `python3 -m pytest tests/runtime_neutral/test_freshness_gate.py`
- `python3 -m pytest tests/runtime_neutral/test_coherence_gate.py`
- `python3 -m pytest tests/runtime_neutral/test_install_generated_nested_bundled.py`
- `python3 -m pytest tests/runtime_neutral/test_release_cut_operator.py`
- `bash install.sh --host codex --profile full --target-root /tmp/vibe-mirror-retirement-codex`
- `bash check.sh --host codex --profile full --target-root /tmp/vibe-mirror-retirement-codex`

## Rollback Rules

- 如果 install/check 任一主链路出现回归，优先恢复新契约字段的读取兼容，而不是重新引入 repo tracked mirror。
- 如果 nested compatibility materialization 出现回归，只回退 compatibility 生成逻辑，不回退 `bundled/skills/vibe` 删除。

## Completion Rules

- 只有在 repo 中 mirror 已删、安装链路通过且 coherence/freshness 通过时，才能使用“彻底退役 tracked mirror”表述。

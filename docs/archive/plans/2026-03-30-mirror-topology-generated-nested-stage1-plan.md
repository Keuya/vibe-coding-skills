# Mirror Topology Generated Nested Stage 1 执行计划

**日期**: 2026-03-30
**需求文档**: [../requirements/2026-03-30-mirror-topology-generated-nested-stage1.md](../requirements/2026-03-30-mirror-topology-generated-nested-stage1.md)
**上游规划**: [2026-03-30-non-regression-technical-debt-remediation-plan.md](./2026-03-30-non-regression-technical-debt-remediation-plan.md)
**Internal Grade**: `L`

## Scope

本轮只做 Wave 4 第一阶段最小闭环：

- nested target 政策改成 generated compatibility
- sync 默认不主动创建缺失 nested，但继续维护已存在 nested
- release-cut 显式请求 generated compatibility materialization
- 增加 generated nested characterization test

## Steps

### Step 1: Topology Contract Tightening

- 更新 `config/version-governance.json`
- 为 `nested_bundled` 增加 generated compatibility 语义
- 保留 `presence_policy = if_present_must_match`

### Step 2: Sync Semantics Adjustment

- 更新 `scripts/governance/sync-bundled-vibe.ps1`
- 默认只同步 `sync_enabled` targets 和已存在的 optional compatibility target
- 新增显式 materialization 开关

### Step 3: Release Path Wiring

- 更新 `scripts/governance/release-cut.ps1`
- 让 preview/apply 的 sync 调用显式请求 generated compatibility materialization

### Step 4: Verification

- 新增 `tests/runtime_neutral/test_generated_nested_bundled.py`
- 更新 `tests/runtime_neutral/test_release_cut_operator.py`
- 运行：
  - `tests/runtime_neutral/test_generated_nested_bundled.py`
  - `tests/runtime_neutral/test_release_cut_operator.py`
  - `scripts/verify/vibe-version-packaging-gate.ps1`
  - `scripts/verify/vibe-nested-bundled-parity-gate.ps1`

## Verification Commands

- `pytest -q tests/runtime_neutral/test_generated_nested_bundled.py`
- `pytest -q tests/runtime_neutral/test_release_cut_operator.py`
- `pwsh -NoProfile -File scripts/verify/vibe-version-packaging-gate.ps1`
- `pwsh -NoProfile -File scripts/verify/vibe-nested-bundled-parity-gate.ps1`
- `git diff --check`

## Stop Rules

- default sync 若开始跳过已存在 nested 的 parity 维护，停止。
- release-cut 若不能继续成功 preview/apply，停止。
- nested parity gate 若因新语义退化，停止。

## Cleanup Expectations

- 阶段结束必须执行 node audit / cleanup preview。
- 必须清理 `.tmp`。

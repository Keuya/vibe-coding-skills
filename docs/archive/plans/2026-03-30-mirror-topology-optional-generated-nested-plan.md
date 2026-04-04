# Mirror Topology Optional Generated Nested 执行计划

**日期**: 2026-03-30
**需求文档**: [../requirements/2026-03-30-mirror-topology-optional-generated-nested.md](../requirements/2026-03-30-mirror-topology-optional-generated-nested.md)
**上游规划**: [2026-03-30-non-regression-technical-debt-remediation-plan.md](./2026-03-30-non-regression-technical-debt-remediation-plan.md)
**Internal Grade**: `L`

## Scope

本轮只做 Wave 4 第一阶段：

- `nested_bundled.sync_enabled -> false`
- 新增 optional generated nested characterization test

不进入 nested tracked root 删除，不进入 release/install materialize 实现。

## Steps

### Step 1: Governance Narrowing

- 更新 canonical / bundled / nested 三份 `config/version-governance.json`
- 保持 `required = false`
- 保持 `presence_policy = if_present_must_match`

### Step 2: Characterization Proof

- 新增 `tests/runtime_neutral/test_generated_nested_bundled.py`
- 覆盖：
  - sync preview skips nested target
  - nested parity gate passes when nested target is absent
  - nested parity gate fails when nested target exists but drifts

### Step 3: Verification

- 运行：
  - `tests/runtime_neutral/test_generated_nested_bundled.py`
  - `scripts/verify/vibe-version-packaging-gate.ps1`
  - `scripts/verify/vibe-nested-bundled-parity-gate.ps1`

## Verification Commands

- `pytest -q tests/runtime_neutral/test_generated_nested_bundled.py`
- `pwsh -NoProfile -File scripts/verify/vibe-version-packaging-gate.ps1`
- `pwsh -NoProfile -File scripts/verify/vibe-nested-bundled-parity-gate.ps1`
- `git diff --check`

## Stop Rules

- 若 `sync_enabled = false` 导致 bundled parity 退化，停止。
- 若 nested 缺席场景仍被 parity gate 视为失败，停止。
- 若 nested 漂移场景无法被 gate 捕获，停止。

## Cleanup Expectations

- 阶段结束必须执行 node audit / cleanup preview。
- 必须清理 `.tmp`。

# Outputs Boundary Retro Safety Migration 执行计划

**日期**: 2026-03-30
**需求文档**: [../requirements/2026-03-30-outputs-boundary-retro-safety-migration.md](../requirements/2026-03-30-outputs-boundary-retro-safety-migration.md)
**上游规划**: [2026-03-30-non-regression-technical-debt-remediation-plan.md](./2026-03-30-non-regression-technical-debt-remediation-plan.md)
**Internal Grade**: `L`

## Scope

本轮只迁移一个 outputs family：

- `outputs/retro/compare/safety-gate/baseline-cer.json`
- `outputs/retro/compare/safety-gate/current-cer.json`
- `outputs/retro/compare/safety-gate/delta.json`
- `outputs/retro/compare/safety-gate/delta.md`

不进入 `sample-run`、`smoke-temp` 和 `external-corpus`。

## Steps

### Step 1: Policy Tightening

- 更新 `config/outputs-boundary-policy.json`
- 去掉 `retro-compare-safety-baselines` allowlisted set
- 将 `expected_tracked_output_count` 从 `19` 调整到 `15`

### Step 2: Canonical Surface Cleanup

- 从 tracked outputs 中移除旧 safety-gate artifacts
- 保留 `references/fixtures/retro-compare/safety-gate/` 作为 canonical fixture

### Step 3: Verification

- 扩展 `tests/runtime_neutral/test_outputs_boundary_migration.py`
- 运行：
  - `tests/runtime_neutral/test_outputs_boundary_migration.py`
  - `scripts/verify/vibe-output-artifact-boundary-gate.ps1`

## Verification Commands

- `pytest -q tests/runtime_neutral/test_outputs_boundary_migration.py`
- `pwsh -NoProfile -File scripts/verify/vibe-output-artifact-boundary-gate.ps1`
- `git diff --check`

## Stop Rules

- 任何消费方仍依赖旧 `outputs/retro/compare/safety-gate/*` 路径，停止。
- fixture root 文件缺失，停止。
- tracked outputs 计数与 policy 不一致，停止。

## Cleanup Expectations

- 阶段结束必须执行 node audit / cleanup preview。
- 必须清理 `.tmp`。

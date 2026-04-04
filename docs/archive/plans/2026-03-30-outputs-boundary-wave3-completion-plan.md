# Outputs Boundary Wave 3 Completion 执行计划

**日期**: 2026-03-30
**需求文档**: [../requirements/2026-03-30-outputs-boundary-wave3-completion.md](../requirements/2026-03-30-outputs-boundary-wave3-completion.md)
**上游规划**: [2026-03-30-non-regression-technical-debt-remediation-plan.md](./2026-03-30-non-regression-technical-debt-remediation-plan.md)
**Internal Grade**: `L`

## Scope

本轮只完成 Wave 3 剩余 3 个 family：

- `outputs/retro/compare/sample-run/*`
- `outputs/retro/compare/smoke-temp/*`
- `outputs/external-corpus/*`

## Steps

### Step 1: Policy Tightening

- 更新 `config/outputs-boundary-policy.json`
- 将 `allowlisted_sets` 清空
- 将 `expected_tracked_output_count` 从 `15` 调整到 `0`
- 将 `strict_requires_zero_tracked_outputs` 切到 `true`

### Step 2: Canonical Surface Cleanup

- 从 tracked outputs 中移除剩余 3 个 family 的 legacy artifacts
- 保留 `references/fixtures/**` 作为唯一 canonical fixture roots

### Step 3: Verification

- 扩展 `tests/runtime_neutral/test_outputs_boundary_migration.py`
- 运行：
  - `tests/runtime_neutral/test_outputs_boundary_migration.py`
  - `scripts/verify/vibe-output-artifact-boundary-gate.ps1 -Strict`

## Verification Commands

- `pytest -q tests/runtime_neutral/test_outputs_boundary_migration.py`
- `pwsh -NoProfile -File scripts/verify/vibe-output-artifact-boundary-gate.ps1 -Strict`
- `git diff --check`

## Stop Rules

- 任何脚本/测试仍依赖旧 `outputs/**` 路径，停止。
- 任何 fixture root 文件缺失，停止。
- strict gate 无法在 `tracked outputs = 0` 下通过，停止。

## Cleanup Expectations

- 阶段结束必须执行 node audit / cleanup preview。
- 必须清理 `.tmp`。

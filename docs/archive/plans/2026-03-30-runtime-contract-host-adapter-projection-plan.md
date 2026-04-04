# Runtime Contract Host Adapter Projection 执行计划

**日期**: 2026-03-30
**需求文档**: [../requirements/2026-03-30-runtime-contract-host-adapter-projection.md](../requirements/2026-03-30-runtime-contract-host-adapter-projection.md)
**上游规划**: [2026-03-30-non-regression-technical-debt-remediation-plan.md](./2026-03-30-non-regression-technical-debt-remediation-plan.md)
**Internal Grade**: `L`

## Scope

本轮只做 Wave 2 的最小安全批次：

- 抽取 host adapter identity / projection helper
- 用 helper 替换 runtime packet、execution manifest、specialist adapter resolution 中的重复字段拼装
- 补 characterization tests

不进入更大的 runtime schema 改造。

## Steps

### Step 1: Shared Helper Extraction

- 在 `scripts/runtime/VibeRuntime.Common.ps1` 中新增：
  - host adapter identity normalizer
  - runtime packet host adapter projection builder
  - frozen runtime packet alignment projection helper

### Step 2: Consumer Adoption

- 更新 `scripts/runtime/Freeze-RuntimeInputPacket.ps1`
- 更新 `scripts/runtime/Invoke-PlanExecute.ps1`
- 更新 `scripts/runtime/VibeExecution.Common.ps1`

要求：

- 字段名不变
- fallback 逻辑不变
- specialist execution 结果字段不变

### Step 3: Verification

- 新增 `tests/runtime_neutral/test_runtime_contract_schema.py`
- 继续运行：
  - `tests/runtime_neutral/test_multi_host_specialist_execution.py`
  - `tests/runtime_neutral/test_l_xl_native_execution_topology.py`

## Verification Commands

- `pytest -q tests/runtime_neutral/test_runtime_contract_schema.py tests/runtime_neutral/test_multi_host_specialist_execution.py tests/runtime_neutral/test_l_xl_native_execution_topology.py`
- `git diff --check`

## Stop Rules

- 任何字段 rename 或字段缺失导致现有 runtime-neutral tests 回归，立即停止扩大范围。
- 如果 helper 抽取需要改动 route selection 或 large-file modularization，则推迟到后续波次。

## Cleanup Expectations

- 阶段结束必须执行 node audit / cleanup preview。
- 必须清理 `.tmp`。
- 不保留额外调试文件。

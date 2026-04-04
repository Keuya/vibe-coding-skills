# Runtime Summary Projection 执行计划

**日期**: 2026-03-30
**需求文档**: [../requirements/2026-03-30-runtime-summary-projection.md](../requirements/2026-03-30-runtime-summary-projection.md)
**上游规划**: [2026-03-30-non-regression-technical-debt-remediation-plan.md](./2026-03-30-non-regression-technical-debt-remediation-plan.md)
**Internal Grade**: `L`

## Scope

本轮只做 runtime summary projection 共享 helper：

- summary hierarchy
- summary artifacts / artifacts_relative
- summary memory_activation / delivery_acceptance 摘要
- helper-level compatibility tests

不处理 payload 外层结构，不进入 outputs boundary 或 mirror topology 收口。

## Steps

### Step 1: Shared Helper Extraction

- 在 `scripts/runtime/VibeRuntime.Common.ps1` 新增 runtime summary projection helpers

### Step 2: Consumer Adoption

- 更新 `scripts/runtime/invoke-vibe-runtime.ps1`

### Step 3: Verification

- 扩展 `tests/runtime_neutral/test_runtime_contract_schema.py`
- 继续运行：
  - `tests/runtime_neutral/test_governed_runtime_bridge.py`
  - `tests/runtime_neutral/test_memory_runtime_activation.py`
  - `tests/runtime_neutral/test_root_child_hierarchy_bridge.py`

## Verification Commands

- `pytest -q tests/runtime_neutral/test_runtime_contract_schema.py`
- `pytest -q tests/runtime_neutral/test_governed_runtime_bridge.py`
- `pytest -q tests/runtime_neutral/test_memory_runtime_activation.py`
- `pytest -q tests/runtime_neutral/test_root_child_hierarchy_bridge.py`
- `git diff --check`

## Stop Rules

- 任何 summary 字段 rename，停止。
- 任何 artifact 绝对/相对路径策略变化，停止。
- bridge 或 memory activation tests 退化，停止。
- 如果需要同时改 payload 外层结构，推迟到后续波次。

## Cleanup Expectations

- 阶段结束必须执行 node audit / cleanup preview。
- 必须清理 `.tmp`。

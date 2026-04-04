# Runtime Contract Hierarchy Projection 执行计划

**日期**: 2026-03-30
**需求文档**: [../requirements/2026-03-30-runtime-contract-hierarchy-projection.md](../requirements/2026-03-30-runtime-contract-hierarchy-projection.md)
**上游规划**: [2026-03-30-non-regression-technical-debt-remediation-plan.md](./2026-03-30-non-regression-technical-debt-remediation-plan.md)
**Internal Grade**: `L`

## Scope

本轮只做 hierarchy projection 共享 helper：

- runtime packet hierarchy
- execution manifest hierarchy
- helper-level compatibility tests

不处理 runtime summary hierarchy，不进入 authority / route / custom admission 收口。

## Steps

### Step 1: Shared Helper Extraction

- 在 `scripts/runtime/VibeRuntime.Common.ps1` 新增 `New-VibeHierarchyProjection`

### Step 2: Consumer Adoption

- 更新 `scripts/runtime/Freeze-RuntimeInputPacket.ps1`
- 更新 `scripts/runtime/Invoke-PlanExecute.ps1`

### Step 3: Verification

- 扩展 `tests/runtime_neutral/test_runtime_contract_schema.py`
- 继续运行：
  - `tests/runtime_neutral/test_governed_runtime_bridge.py`
  - `tests/runtime_neutral/test_l_xl_native_execution_topology.py`

## Verification Commands

- `pytest -q tests/runtime_neutral/test_runtime_contract_schema.py`
- `pytest -q tests/runtime_neutral/test_governed_runtime_bridge.py`
- `pytest -q tests/runtime_neutral/test_l_xl_native_execution_topology.py`
- `git diff --check`

## Stop Rules

- 任何字段名变化，停止。
- packet 与 execution manifest hierarchy 语义出现不一致，停止。
- 如果需要同时修改 runtime summary schema，推迟到后续波次。

## Cleanup Expectations

- 阶段结束必须执行 node audit / cleanup preview。
- 必须清理 `.tmp`。

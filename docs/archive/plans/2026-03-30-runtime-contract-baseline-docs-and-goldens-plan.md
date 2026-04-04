# Runtime Contract Baseline Docs And Goldens 执行计划

**日期**: 2026-03-30
**需求文档**: [../requirements/2026-03-30-runtime-contract-baseline-docs-and-goldens.md](../requirements/2026-03-30-runtime-contract-baseline-docs-and-goldens.md)
**上游规划**: [2026-03-30-non-regression-technical-debt-remediation-plan.md](./2026-03-30-non-regression-technical-debt-remediation-plan.md)
**Internal Grade**: `L`

## Scope

本轮只做 Runtime Contract Wave 2 剩余 baseline：

- runtime contract field documentation
- packet/manifest curated golden snapshot fixture
- golden-based runtime neutral test

不进入 outputs boundary、mirror topology、router large-file refactor。

## Steps

### Step 1: Contract Field Documentation

- 新增长期 contract schema 文档
- 明确 packet / manifest / summary 的 required / optional compatibility / deprecation 状态

### Step 2: Curated Goldens

- 新增 packet/manifest curated golden fixture
- 只冻结稳定字段，动态字段做归一化

### Step 3: Verification

- 新增 golden-based runtime neutral test
- 继续运行：
  - `tests/runtime_neutral/test_runtime_contract_schema.py`
  - `tests/runtime_neutral/test_governed_runtime_bridge.py`
  - `tests/runtime_neutral/test_l_xl_native_execution_topology.py`

## Verification Commands

- `pytest -q tests/runtime_neutral/test_runtime_contract_goldens.py`
- `pytest -q tests/runtime_neutral/test_runtime_contract_schema.py`
- `pytest -q tests/runtime_neutral/test_governed_runtime_bridge.py`
- `pytest -q tests/runtime_neutral/test_l_xl_native_execution_topology.py`
- `git diff --check`

## Stop Rules

- 如果 golden 需要冻结 run id、时间戳或绝对 artifact path，停止并缩小冻结面。
- 如果 contract 文档需要重新解释现有运行语义，而不是描述现状，停止。
- 如果 golden 与已有 bridge/schema 测试冲突，先修 normalization，不直接改 runtime 行为。

## Cleanup Expectations

- 阶段结束必须执行 node audit / cleanup preview。
- 必须清理 `.tmp`。

# Release Operator Closure 实施计划

**日期**: 2026-03-30
**需求文档**: [../requirements/2026-03-30-release-operator-closure-implementation.md](../requirements/2026-03-30-release-operator-closure-implementation.md)
**上游规划**: [2026-03-30-non-regression-technical-debt-remediation-plan.md](./2026-03-30-non-regression-technical-debt-remediation-plan.md)
**Internal Grade**: `XL`

## Wave Structure

### Wave 1: Freeze Scope And Analyze

- 固定范围到 release operator closure。
- 并行分析：
  - `release-cut` 缺口
  - release notes 质量规则
  - phase cleanup / node hygiene 执行方式

### Wave 2: Implement Operator Closure

- 更新 `release-cut.ps1`：
  - preview 包含 release README / dist manifest surfaces
  - apply 自动更新 release README / dist manifests
  - 自动生成 release note 时不写 `TODO`
- 新增 release note 质量 gate。

### Wave 3: Verification

- 新增并运行：
  - `tests/runtime_neutral/test_release_cut_operator.py`
  - `tests/runtime_neutral/test_release_notes_quality.py`
- 运行相关现有 gate / targeted tests。
- 修正失败项直到通过。

### Wave 4: Phase Cleanup

- 运行 node audit / cleanup（安全、报告优先）。
- 清理本轮临时文件。
- 保留 governed docs 与必要 receipts，避免仓库脏化。

## Ownership Boundaries

- Root lane:
  - requirement / plan 冻结
  - `release-cut.ps1` 主实现
  - 最终验证与收敛
- Child lane A:
  - release-cut 行为缺口分析
- Child lane B:
  - release notes 质量策略分析
- Child lane C:
  - node hygiene / cleanup 命令策略分析

## Verification Commands

- `git diff --check`
- `pytest -q tests/runtime_neutral/test_release_cut_operator.py tests/runtime_neutral/test_release_notes_quality.py`
- `pwsh -NoProfile -File scripts/verify/vibe-release-notes-quality-gate.ps1`
- `pwsh -NoProfile -File scripts/verify/vibe-dist-manifest-gate.ps1`
- `pwsh -NoProfile -File scripts/verify/vibe-version-consistency-gate.ps1`

## Delivery Acceptance Plan

- 本轮 only-if:
  - release-cut preview/apply 行为被测试覆盖
  - release README 和 dist manifest 更新逻辑进入 operator 主路径
  - 新增 release note 质量校验
  - 阶段清理已执行

## Completion Language Rules

- 只能宣称 Wave 1 完成，不能宣称整套技术债修复全部完成。

## Rollback Rules

- 如果 release-cut 的 preview 与 apply 语义失配，则回滚到上一个稳定版本，不并入其他结构改动。
- 如果新 gate 导致当前 `v2.3.53` 仓库状态不通过，则先修 gate 或缩小其约束范围，不扩大改动面。

## Cleanup Expectations

- 阶段结束必须执行 node 审计/清理和临时文件清理。
- 不保留无用的临时测试目录或手写调试文件。

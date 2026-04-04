# Release Operator Closure Wave 1 执行计划

**日期**: 2026-03-30
**需求文档**: [../requirements/2026-03-30-release-operator-closure-wave1.md](../requirements/2026-03-30-release-operator-closure-wave1.md)
**Internal Grade**: `XL`

## Wave Structure

### Wave 1A: Freeze And Characterize

- 读取 `release-cut.ps1`、`docs/releases/README.md`、`dist/*/manifest.json`、`dist/manifests/*.json` 的当前结构。
- 明确 operator 需要新增的最小 helper。
- 冻结本波 non-goals，避免 scope 漂移到 runtime/mirror/outputs。

### Wave 1B: Operator Implementation

- 为 `release-cut.ps1` 增加：
  - release README current/recent surface update
  - lane/public manifest release field update
  - release note minimal section completion guard
- 把 `vibe-dist-manifest-gate.ps1` 纳入 release-cut gate family。

### Wave 1C: Test Coverage

- 新增 `tests/runtime_neutral/test_release_cut_operator.py`
- 新增 `tests/runtime_neutral/test_release_notes_quality.py`
- 用临时 repo fixture 验证 preview/apply 的文件更新面。

### Wave 1D: Verification And Cleanup

- 运行最小 tests/gates。
- 若失败则迭代修复。
- 阶段结束后执行 node audit / cleanup 与临时文件清理。

## Ownership Boundaries

- Root governed lane:
  - requirement/plan truth
  - operator implementation
  - verification and final claim
- Test surface:
  - 只验证本波引入的 release operator 行为，不扩展到下一波债务收敛。

## Verification Commands

- `git diff --check`
- `pytest -q tests/runtime_neutral/test_release_cut_operator.py tests/runtime_neutral/test_release_notes_quality.py`
- `pwsh -NoProfile -File scripts/verify/vibe-version-consistency-gate.ps1`
- `pwsh -NoProfile -File scripts/verify/vibe-dist-manifest-gate.ps1`

## Delivery Acceptance Plan

- preview receipt 能看见新增 surfaces
- apply 能更新 README/manifest/release note
- tests 证明 operator 与质量规则有效
- gates 不因本波修改而退化

## Completion Language Rules

- 只有 tests 和指定 gates fresh 通过，才允许说 Wave 1 完成。
- 如果 gate 因环境不可用未执行，必须明确写出。

## Rollback Rules

- 若 operator 行为不稳定，先保留手工补面兼容，不删除任何现有手工编辑路径。
- 若质量检查导致历史版本被误伤，限制校验范围到当前 release note 或 operator 触达面。

## Cleanup Expectations

- 不保留临时 fixture 目录。
- 阶段结束运行 node audit，并仅在安全范围内执行 report-first cleanup。

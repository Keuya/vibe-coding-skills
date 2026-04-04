# Install Generated Nested Compatibility 执行计划

**日期**: 2026-03-30
**需求文档**: [../requirements/2026-03-30-install-generated-nested-compatibility.md](../requirements/2026-03-30-install-generated-nested-compatibility.md)
**上游规划**: [2026-03-30-non-regression-technical-debt-remediation-plan.md](./2026-03-30-non-regression-technical-debt-remediation-plan.md)
**Internal Grade**: `L`

## Scope

本轮只做 Wave 4 第二阶段的 install-time materialization 收口：

- runtime-core install 在 installed canonical vibe root 上显式生成 nested compatibility target
- 新增 integration test，证明 repo 缺失 nested baseline 时 install 仍可 materialize nested

不进入 repo tracked nested root 删除，不进入 router/runtime 大脚本拆分。

## Steps

### Step 1: Install-Time Materialization

- 在 runtime-core authoritative install path 上新增 nested compatibility materialization
- source 使用 installed canonical vibe root
- target 使用 `skills/vibe/bundled/skills/vibe`

### Step 2: Focused Proof

- 新增 `tests/runtime_neutral/test_install_generated_nested_bundled.py`
- fixture repo 明确不提供 nested baseline
- 断言 install 后：
  - nested root 存在
  - governance/config mirror 内容来自 installed canonical root
  - nested skill entrypoint 已 sanitize

### Step 3: Mirror Sync And Verification

- canonical 变更完成后同步 bundled/nested mirrors
- 运行 install-time focused test 与现有 Wave 4/Release tests

## Verification Commands

- `pytest -q tests/runtime_neutral/test_install_generated_nested_bundled.py`
- `pytest -q tests/runtime_neutral/test_generated_nested_bundled.py`
- `pytest -q tests/runtime_neutral/test_installed_runtime_scripts.py -k "nested_runtime_skill_entrypoints_sanitized or installed_shell_scripts_work_without_repo_level_adapter_registry"`
- `pytest -q tests/runtime_neutral/test_release_cut_operator.py`
- `pwsh -NoProfile -File scripts/verify/vibe-version-packaging-gate.ps1`
- `pwsh -NoProfile -File scripts/verify/vibe-nested-bundled-parity-gate.ps1`
- `git diff --check`

## Stop Rules

- 如果 install-time materialization 仍然依赖 repo 内 nested baseline，停止。
- 如果 sanitize contract 因 materialization 退化，停止。
- 如果 bundled/nested parity gate 因 install-time 逻辑漂移而失败，停止。

## Cleanup Expectations

- 阶段结束必须执行 node audit / cleanup。
- 必须清理 `.tmp`。

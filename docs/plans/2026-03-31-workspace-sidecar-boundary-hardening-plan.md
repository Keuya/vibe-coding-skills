# Workspace Sidecar Boundary Hardening 执行计划

**日期**: 2026-03-31
**需求文档**: [2026-03-31-workspace-sidecar-boundary-hardening.md](../requirements/2026-03-31-workspace-sidecar-boundary-hardening.md)

## 执行步骤

1. 用测试锁定 `host_sidecar_root` 未写入和卸载 guard 过窄两个问题
2. 为 runtime session / project descriptor 初始化链路补齐 `Runtime` 透传
3. 将 uninstall workspace sidecar guard 扩展为 `project.json` 或 runtime artifact tree 任一命中即保护
4. 清理 runtime contract tests 中的 `/tmp/workspace` 硬编码
5. 运行定向回归测试验证修复

## 验证命令

```bash
python3 -m unittest tests.runtime_neutral.test_runtime_contract_schema
python3 -m unittest tests.runtime_neutral.test_uninstall_vgo_adapter
```

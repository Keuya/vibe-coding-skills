# Workspace Sidecar Boundary Hardening 需求文档

**日期**: 2026-03-31
**任务类型**: 运行时与卸载修复
**优先级**: 高

## 目标

修复 workspace sidecar 与 host sidecar 分层中的两个残留问题：

1. 运行时生成 `.vibeskills/project.json` 时必须落盘 `host_sidecar_root`
2. host uninstall 在识别到 workspace sidecar 产物时必须退化为定向清理，不能整删 `.vibeskills`

## 交付物

1. `project.json` 初始化链路补齐 runtime 透传
2. 卸载 sidecar 边界识别从仅 `project.json` 扩展到 runtime artifact tree
3. 回归测试覆盖 host marker + workspace artifact 的混合场景
4. 运行时契约测试去掉 `/tmp/workspace` 硬编码

## 验收标准

1. 默认 workspace sidecar 模式下，`project.json.host_sidecar_root` 与当前 host sidecar 一致
2. 当 `.vibeskills` 下存在 `project.json` 或 runtime artifact tree 时，host uninstall 不会整删 `.vibeskills`
3. host marker 仍会被定向删除，不影响 workspace-owned 文档与输出
4. 相关测试在非 `/tmp` 假设下仍可运行

# 需求冻结: PR #102 冲突消解与审查问题修补

- 日期: 2026-04-04
- 任务入口: 用户指出当前提交与 `main` 存在较多冲突，且 CodeRabbit 审查发现多个问题，需要整理、修复并保持 PR 可合并

## 目标

在不扩大本次变更范围的前提下，修复 PR #102 与 `main` 的真实冲突，并处理已验证成立的 review 问题，使该 PR 回到可审阅、可验证、可继续合入的状态。

## 交付物

- `feat/opencode-preview-lane` 合入最新 `main` 之后不再保留未解决冲突
- 与 `OpenCode` 隔离根 / preview 检查相关的 shell、PowerShell、Python 安装器逻辑与当前主线保持一致
- CodeRabbit 已确认成立的问题得到修复，误报或无效建议不盲从
- 镜像副本与 canonical 文件保持同步

## 约束

- 不回退用户未授权的无关变更
- 不扩大到与本 PR 无关的主线功能重写
- 不改变“默认安装到隔离根、原生配置面仍由宿主管理”的决策
- 仅在证据充分时修改测试或文档

## 验收标准

- `git merge origin/main` 后无未解决冲突残留
- CodeRabbit 指出的有效问题在 canonical 与 bundled 镜像中均被修复
- 相关定向测试通过
- `git diff --check` 通过

## 非目标

- 不处理当前工作树中既有的历史未跟踪文档
- 不在本轮内处理与本 PR 无关的 CodeRabbit 泛化建议

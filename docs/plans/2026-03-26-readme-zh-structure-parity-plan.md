# 中文 README 与英文新版结构对齐执行计划

## 范围

只修正 `README.zh.md` 相对英文新版的结构性偏差，不扩散到其他文档。

## 执行步骤

1. 对照 [`README.md`](../../../README.md) 与 [`README.zh.md`](../../../README.zh.md) 的路由章节结构。
2. 在中文 README 主线中补齐“为什么这样设计？”部分。
3. 删除中文路由 FAQ 中重复承载的旧说明。
4. 将中文安装章节从旧的“双入口”表格改成“单一公开入口 + 两种公开版本”表格。
5. 运行差异与格式校验，确认仅发生预期变更。

## 校验

- `git diff -- README.zh.md docs/requirements/2026-03-26-readme-zh-structure-parity.md docs/plans/2026-03-26-readme-zh-structure-parity-plan.md`
- `git diff --check -- README.zh.md docs/requirements/2026-03-26-readme-zh-structure-parity.md docs/plans/2026-03-26-readme-zh-structure-parity-plan.md`
- `rg -n "为什么这样设计|一个入口，两种公开版本|唯一公开入口" README.zh.md`

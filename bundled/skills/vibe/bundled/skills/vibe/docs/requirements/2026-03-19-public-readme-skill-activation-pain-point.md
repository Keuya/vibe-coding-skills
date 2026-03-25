# 2026-03-19 Public README Skill Activation Pain Point

## Goal

在 README 中补充一个更贴近真实使用的痛点：不是 skills 不够多，而是很多 skills 激活率低、真实任务里调不起来；同时明确说明 `VCO` 生态如何通过路由、MCP / 插件入口、工作流编排与治理规则提高能力激活率，并将当前版本发布到 GitHub。

## Deliverables

- 更新 `README.md`，加入“skills 激活率低”痛点与 `VCO` 生态解法
- 更新 `README.en.md`，保持对应语义一致
- 新增本轮 governed requirement / plan 文档
- 更新 requirement / plan 索引
- 将当前版本发布到 GitHub 远端仓库

## Constraints

- 保持现有 capability-first README 结构不变
- 不能把问题描述成“skills 数量不足”，而是“skills 很多但激活率低”
- 解法必须落在当前仓库真实能力边界内：路由、MCP / 插件入口、受管工作流、治理规则、上下文编排
- 发布时避免对当前脏工作区做破坏性 git 历史操作

## Acceptance Criteria

- README 痛点列表中明确出现“skills 激活率低”
- README 正文明确说明 `VCO` 生态如何提高技能被真正调用的概率
- 中英文 README 保持结构与含义一致
- 当前版本成功发布到 GitHub

## Frozen User Intent

用户本轮明确要求：

- 添加一个痛点：`skills` 激活率低
- 说明通过 `VCO` 生态也能解决这个问题
- 修改完成后，把现前版本推送到 GitHub

## Evidence Strategy

- 检查 `README.md` 和 `README.en.md` 中是否新增对应痛点与解法表述
- 检查 diff 只覆盖目标文档与 governed 记录
- 检查远端 GitHub 仓库对应文件内容已更新

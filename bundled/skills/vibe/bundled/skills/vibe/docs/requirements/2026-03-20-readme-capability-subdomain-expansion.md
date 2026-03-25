# 2026-03-20 README Capability Subdomain Expansion

## Goal

在现有 README 顶部能力矩阵的基础上，继续把 20 个能力域往下拆成更细的子领域说明，让读者不仅知道仓库“分成哪些板块”，还知道每个板块下面更具体覆盖哪些工作类型。

## Deliverables

- 扩写 `README.md` 中文能力介绍
- 保留现有 20 个能力域总表
- 在总表后新增更细的子领域分组展开说明
- 更新 governed requirement / plan 索引

## Constraints

- 不推翻现有 capability-first 结构
- 不把首页改成冗长的 340 skills 罗列
- 细化说明必须继续服务公开 README，而不是写成内部开发文档
- 仍然要优先保证中文自然、完整、易读

## Acceptance Criteria

- `README.md` 在现有总表之外，新增更细的子领域拆解
- 读者能看懂每个能力域下面进一步覆盖的工作面
- 新内容保持信息密度高，但不破坏首屏阅读节奏
- diff / diff --check 通过

## Frozen User Intent

用户明确选择继续深化中文 README，而不是先推送或先同步英文版：

- “我继续把中文 README 再往下做一轮”
- “进一步把 20 个能力域再展开成更细的子领域说明”

## Evidence Strategy

- 对比 `README.md`，确认在能力矩阵后新增子领域展开区块
- 检查新说明确实细化到能力域内部，而不是重复原表
- 使用 `git diff --check` 验证格式

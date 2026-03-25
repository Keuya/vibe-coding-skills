# 2026-03-19 Public README Capability-First Opening

## Goal

重排 README 首页叙事顺序，让读者一打开仓库就先看到项目已经整合了哪些能力、资源和覆盖领域，再在结尾收束到“规范化”这一核心理念。

## Deliverables

- 重写 `README.md` 顶部结构，前置整合规模、能力资源与覆盖领域
- 重写 `README.en.md` 对应开场结构，保持中英文语义一致
- 新增一段更直接的上游整合说明，明确 `skills`、`MCP`、插件、工作流与上游项目的协同关系
- 将项目理念从开头移动到 README 结尾作为收束段落
- 更新 requirement / plan 索引以记录本轮 governed pass

## Constraints

- 保留作者提供的 Gemini 原始 SVG 作为现有视觉资产，不新增海报或二次设计
- README 开头必须优先表达“整合了什么、能覆盖什么工作”
- README 结尾必须明确表达“规范化”是项目核心理念
- 所有能力描述需保持在当前仓库真实边界内，不虚增功能范围
- 中英文 README 必须保持结构和含义一致

## Acceptance Criteria

- README 开头在理念之前先说明项目整合规模与资源层次
- README 顶部明确出现 `skills`、`MCP`、插件、上游项目、治理规则和覆盖领域
- README 结尾出现单独的理念段，明确“规范化”与稳定性、维护性、技术债的关系
- 中英文版本都体现相同的 capability-first narrative

## Frozen User Intent

用户本轮明确要求：

- 一开始强调项目整合了多个项目、多个技能
- 先让读者知道“我们有什么能力、有什么资源”
- 在 README 开头说明这些 `skills`、`MCP`、项目能覆盖哪些领域的工作
- 最后再说项目理念

## Evidence Strategy

- 检查 README 顶部顺序：标题/定位 -> 资源与能力说明 -> 覆盖领域 -> 上游整合 -> 其余正文
- 检查 README 尾部是否以“项目理念 / Project Philosophy”收束
- 检查中英文 README 都包含 `skills`、`MCP`、插件、上游项目、治理规则与领域覆盖描述

# 2026-03-20 README Detailed Capability Matrix

## Goal

重写 README 顶部的能力覆盖介绍，把当前过于泛泛、中文可读性不足的能力描述改成一张更全面、更细致、更容易理解的能力矩阵表，让读者一眼看清这个仓库到底能做哪些类型的工作。

## Deliverables

- 重写 `README.md` 顶部能力覆盖区块，改为详实表格
- 重写 `README.en.md` 对应区块，保持结构一致
- 保留 capability-first 叙事，但移除当前过于笼统的短列表
- 新增本轮 governed requirement / plan 记录

## Constraints

- 不能把 340 个 skills 生硬罗列成冗长清单
- 必须按领域和能力板块组织内容，而不是泛泛写几条抽象概括
- 中文版要以自然、直接、信息密度高但仍可读的表达为主
- 表格描述必须与仓库真实能力边界相符

## Acceptance Criteria

- `README.md` 的中文能力介绍明显更自然、更具体
- 能力覆盖不再只是 5-6 条泛泛 bullet，而是分板块详实说明
- 表格至少覆盖产品/规划、工程开发、文档、数据/ML、科研/生命科学、自动化/部署等核心方向
- `README.en.md` 保持对应语义

## Frozen User Intent

用户明确要求：

- 当前“这些能力能够覆盖哪些工作”写得不好
- 中文读起来有点看不懂
- 介绍过于泛泛而谈
- 希望在开头详细列出仓库能干什么、有哪些方面的技能
- 希望改成一个详实的表格

## Evidence Strategy

- 对比 README 顶部新旧结构，确认已将泛泛 bullet 改成详实表格
- 检查中英文 README 顶部是否都完成对应重写
- 用 diff / diff --check 验证范围与格式

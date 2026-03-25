# 2026-03-19 Public README Propagation Optimization

## Goal

将公开首页首屏从“清晰介绍型入口”进一步优化为“传播优先、价值冲击更强”的首页入口，在极小篇幅内同时传达项目的全面性、治理安全性、稳定性与整合价值。

## Deliverables

- 重写 `README.md` 首屏结构与开头主叙事
- 重写 `README.en.md` 首屏结构与开头主叙事
- 新增首屏 proof / highlights 区块，使用仓库内可验证事实支撑传播文案
- 更新 `docs/requirements/README.md` 与 `docs/plans/README.md` 的 current entry

## Constraints

- 首屏主轴必须是“这是什么，以及为什么它值得被立刻注意”，不是“马上安装”
- 安装入口保留，但必须后移，不能抢走首屏宣传重心
- 叙事上必须有机结合三种冲击：判断冲击、数字冲击、对比冲击
- 不得伪造无法在仓库内验证的数量、能力或外部声誉数据
- 公开主名称仍为 `VibeSkills`，`VCO` 作为背后的 governed runtime 解释
- 文风允许更锋利，但不能滑向夸张、空泛或不可证实的营销措辞

## Acceptance Criteria

- 用户在阅读 README 前 30-60 秒内就能感知到：项目不只是 skill 列表，而是整合系统
- 首屏能明确打出项目的全面性、治理性和稳定性，而不是只讲抽象理念
- proof / highlights 区块中的数量与能力表述都能追溯到仓库内事实
- 安装入口仍可见，但退到第二优先级
- 中英文 README 首屏保持同等级别的传播力度，而不是英文仅做直译兜底

## Non-Goals

- 不在本轮重写 manifesto、quick-start 或安装页主体内容
- 不新增图像、徽标素材或截图资产
- 不修改 runtime、router、install、check 的实现行为

## Frozen User Intent

用户明确希望：

- 首页以宣传传播为重，而不是安装转化为重
- 在极小篇幅内就让用户感知到项目价值并产生冲击感
- 重点突出全面性、架构的安全性与稳定性、整合了大量优质上游项目
- 首屏表达方式采用三者联合：判断冲击 + 数字冲击 + 对比冲击
- 具体气质选择 `版本 A`：更锋利、更有宣传冲击

## Evidence Strategy

- `bundled/skills/` 顶层目录数量用于支撑 skill 规模叙事
- `config/upstream-corpus-manifest.json` 的 `entries` 数量用于支撑上游整合规模叙事
- `config/*.json` 数量用于支撑治理 / contract / policy 密度叙事
- 通过 `git diff --stat` 验证本轮只改动预期公开入口文档与索引
- 通过 Node audit / cleanup receipts 保留阶段卫生证据

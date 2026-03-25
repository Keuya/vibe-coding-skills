# 2026-03-19 Public README Capability Snapshot

## Goal

在 README 中英双语首屏标题区后新增一个纯 Markdown 的能力展示区，用无图片素材的方式强化首屏的“能力规模、治理密度、稳定执行”感知。

## Deliverables

- 在 `README.md` 首屏新增能力展示面板
- 在 `README.en.md` 首屏新增对应英文能力展示面板
- 新增设计文档与实现计划文档
- 更新 `docs/requirements/README.md` 与 `docs/plans/README.md` 的 current entry

## Constraints

- 不能引入图片、徽标、截图等新素材依赖
- 展示区必须明显偏“能力展示”，不是品牌口号区
- 展示区必须建立在仓库内可验证事实之上
- 不能破坏上一轮已确定的首屏主轴：宣传优先，安装后置
- 视觉语气允许有控制台 / 战报质感，但必须保持普通用户可读

## Acceptance Criteria

- 用户在标题区之后立刻看到一个高辨识度的能力展示区
- 展示区同时传达规模感、治理感和可执行感
- 展示区与下方“为什么它会让人立刻感到不一样”不重复抢话
- 中英文版本都保持同等级别的展示强度

## Non-Goals

- 不新增真实图片资产
- 不修改 manifesto、quick-start 或安装页正文
- 不修改 runtime、router、install、check 行为

## Frozen User Intent

- 方向：`能力展示`
- 方案：`方案 1：能力战报面板`
- 目标：用纯 Markdown 做出更有辨识度的首屏能力展示，不依赖图片素材

## Evidence Strategy

- `bundled/skills` 顶层目录数支撑能力规模
- `config/upstream-corpus-manifest.json` entries 支撑上游整合规模
- `config/*.json` 数量支撑治理 / contract 密度
- `git diff --stat` 与 Node audit / cleanup 支撑本轮变更和阶段卫生证据

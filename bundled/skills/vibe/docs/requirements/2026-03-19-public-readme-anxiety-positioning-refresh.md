# 2026-03-19 Public README Anxiety Positioning Refresh

## Goal

移除 README 首屏中不理想的章鱼 Markdown 识别区，改为更强的时代焦虑与系统回应叙事，让首页更直接地说明：为什么当下人们会需要 `VibeSkills`，以及它如何通过整合最前沿工具集合与严格治理制度来回应这种焦虑。

## Deliverables

- 重写 `README.md` 首屏前部叙事
- 重写 `README.en.md` 首屏前部叙事
- 删除章鱼 Markdown 识别区
- 新增本轮 requirement 与 plan 文档
- 更新 `docs/requirements/README.md` 与 `docs/plans/README.md` 当前入口

## Constraints

- 不保留当前章鱼 Markdown 图形
- 首屏必须突出当下 AI 工具爆炸、工作流繁多、学习与融合困难、害怕被时代抛弃的现实困境
- `VibeSkills` 的回应必须明确落在：整合最前沿工具集合、以完整稳定严苛的治理制度来管理这些优秀工具和资源
- 保持“宣传优先、安装后置”主轴不变
- 文风可以有冲击力，但不能流于焦虑营销或夸张失真
- 中英文版本都要保持同级别的表达力度

## Acceptance Criteria

- 首屏不再出现章鱼图形
- 用户在前几段就能读到时代焦虑与选择困境，而不是只看到抽象的系统说明
- `VibeSkills` 的价值主张更像“对时代困境的回应”，而不是单纯工具介绍
- 现有 capability snapshot 仍保留，用于承接事实层证明
- 首页整体仍清晰可读，不会因为情绪化叙事变得浮夸

## Non-Goals

- 不修改 manifesto、quick-start 或安装页正文
- 不新增图片、logo 或 mascot 方案
- 不修改 runtime、router、install、check 行为

## Frozen User Intent

用户明确要求：

- 删除当前章鱼 Markdown 图标
- 在首页前部加入关于当下工具参差不穷、AI 工作流过多、如何选择与融合、如何学习和收集、以及害怕被快速发展时代抛弃的焦虑叙事
- 强调这个工具正是为此而生
- 强调它整合的是最前沿工具集合，并用完整、稳定、严苛的治理制度管理这些优秀工具和资源
- 采用此前讨论的 `C 方案：双段切入`

## Evidence Strategy

- 通过 README 首屏结构验证“焦虑 -> 回应 -> capability snapshot -> 差异说明”的顺序
- 通过 `git diff --stat` 验证本轮只改动 README 与治理索引
- 通过 Node audit / cleanup receipts 保留阶段卫生证据

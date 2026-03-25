# 2026-03-19 Public Docs Entrypoint Restructure

## Goal

将公开入口文档从“分散、冗长、偏 operator 叙事”收敛为一组明显偏向普通用户、但仍能被重度用户快速理解的公开文档。

## Deliverables

- 重写 `README.md`
- 重写 `docs/manifesto.md`
- 重写 `docs/install/one-click-install-release-copy.md`
- 新增 `docs/quick-start.md`
- 重写 `README.en.md`
- 重写 `docs/manifesto.en.md`
- 重写 `docs/install/one-click-install-release-copy.en.md`
- 新增 `docs/quick-start.en.md`
- 更新 `docs/requirements/README.md` 与 `docs/plans/README.md` 的 current entry

## Constraints

- 对外名称采用 `VibeSkills / VCO` 并列语义：`VibeSkills` 为对外主名称，`VCO` 为核心运行时解释
- 文风必须明显偏向普通用户，避免 operator-first 术语淹没主叙事
- README 不追求讲全，只追求让第一次进入仓库的人快速理解“这是什么、为什么值得用、怎么开始”
- manifesto 不再维持“大宣言”口气，改为短心路历程加少量核心原则
- 安装入口以“复制给 AI 的一步式提示词”为主，不以命令列表为主
- 必须保留诚实边界：不得把宿主插件、外部 MCP、provider secrets 伪装成已经自动完成

## Acceptance Criteria

- 普通用户在 3-5 分钟内能从 `README.md` 理解项目定位与开始方式
- `README.md`、`docs/manifesto.md`、安装文案之间职责清晰，不再互相抢话
- 新增 `docs/quick-start.md` 能承接 README 之后的第二跳导航
- 文档整体调性降低，不再把项目包装成过度宏大的抽象宣言
- 保留作者真实动机：面对优质但分散、互相冲突、难组合的 skills / 插件 / 工作流生态，尝试通过整合、路由、治理和留痕把使用门槛降下来

## Non-Goals

- 不在本轮重写全站所有安装、release、operator、proof 文档
- 不改变现有安装脚本、检查脚本和运行时行为

## Frozen User Intent

用户希望公开入口文档具备以下属性：

- 受众：普通用户与重度用户都要覆盖，但明显偏向普通用户
- 气质：平衡型，先讲清楚项目是什么、为什么值得用，再保留短心路与方法论
- 安装位置：靠后，先建立理解和信任，再给出开始方式
- manifesto 角色：短心路历程加少量核心原则
- 名称：`VibeSkills / VCO` 并列，对外优先 `VibeSkills`

## Evidence Strategy

- 通过中英文文件级重写确认公开入口职责收敛
- 通过索引更新确认新 requirement / plan 已进入 canonical surfaces
- 通过阶段结束前的 git diff 与 Node 审计确认本轮只留下预期文档改动与清理证据

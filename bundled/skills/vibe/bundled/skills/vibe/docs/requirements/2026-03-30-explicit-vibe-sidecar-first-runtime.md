# Explicit Vibe Sidecar-First Runtime Requirement

**日期**: 2026-03-30
**目标**: 为 Vibe 设计一套“未显式调用时完全沉默、显式 `$vibe` / `/vibe` 以 skill 形式调用时完整启用”的 sidecar-first 架构，并彻底移除对宿主原生配置文件的默认依赖。

## Intent Contract

- Goal: 冻结一套统一架构，使 Vibe 的路由层与 runtime 只在显式 `vibe` skill 调用时完整启用，且默认与目标宿主的原生配置文件完全解耦。
- Deliverable:
  - 单一需求文档
  - 单一设计/迁移计划文档
  - 明确的状态分层、入口分层、宿主适配边界与迁移策略
- Constraints:
  - 默认路径必须是 `sidecar-first + skills-only activation`，而不是继续向任何宿主真实配置文件写入 `vibeskills`。
  - “未显式调用 `vibe` 时保持沉默”必须被视为正确行为，而不是能力缺陷。
  - “显式调用 `vibe` 时完整启用”必须同时覆盖路由层与 runtime 层，不允许只启用其一。
  - 不能把“宿主 skill 调用入口”与“Vibe 主状态存储”混为一谈。
  - 对目标宿主，安装器不得修改 `settings.json`、`opencode.json` 或其他宿主原生配置文件。
  - 设计必须以“目标宿主原生支持 skill 调用”为前提，不得偷偷回退到 command/agent/config 桥接。
  - 必须保留安装/卸载安全性，不能让 sidecar-first 迁移破坏现有 owned-only uninstall 合同。
- Acceptance Criteria:
  - 明确区分以下三层：
    - 宿主 skill 调用入口层
    - Vibe canonical runtime state
    - 安装/审计收据层
  - 明确回答：
    - 为什么 sidecar 可以承担运行时主状态
    - 为什么显式 skill 调用可以替代默认注入/常驻激活
    - 哪些宿主可以直接迁移到 skills-only sidecar-first
    - 哪些现有 install/test truth 需要同步收缩
  - 给出可执行迁移波次，而不是只给抽象原则。
- Product Acceptance Criteria:
  - 用户能够得到一个清晰结论：Vibe 在未来应当“默认沉默 + 显式 skill 启用 + sidecar-first + 零宿主配置写入”。
  - 后续实现可以直接按该设计推进，而不需要重新争论 `settings.json` / `opencode.json` 是否应参与默认安装。
- Manual Spot Checks:
  - 核对当前 runtime 是否读取 `.vibeskills/host-closure.json`
  - 核对当前安装器对 `claude-code` / `cursor` / `windsurf` / `openclaw` 的真实写面
  - 核对安装矩阵与 host capability matrix 中的宿主 truth wording
- Completion Language Policy:
  - 不得把“零宿主配置写入”弱化成“默认关闭但仍保留桥接”。
  - 若某个宿主当前证据不足以证明 skill-only 激活可用，必须标注为“需要迁移验证”，不能直接宣称零退化。
- Delivery Truth Contract:
  - 本轮交付设计，不默认宣称实现已完成。
  - 本轮允许冻结需求与计划文档，不要求同步修改安装器实现。
- Non-goals:
  - 不在本轮直接实现全部宿主迁移。
  - 不在本轮提升任何宿主支持等级。
  - 不把 sidecar-first 错写成“宿主会在未显式调用时主动读取 `.vibeskills` 状态”。
- Autonomy Mode: `interactive_governed`
- Inferred Assumptions:
  - 用户认可“未显式调用 `vibe` 时完全沉默”是正确行为。
  - 用户希望显式 `vibe` skill 调用时，所有 Vibe 路由/治理/runtime 功能完整启用。
  - 目标宿主原生支持 skill 调用，因此不需要通过原生配置文件注入 `vibe`。
  - `.vibeskills/host-settings.json` 比宿主真实配置文件更适合作为跨宿主统一状态面。

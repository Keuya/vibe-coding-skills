# Cross-Host Startup Regression Audit Requirement

**日期**: 2026-03-30
**目标**: 对 `opencode` 之外的宿主适配器逐一排查，确认是否存在与 OpenCode 相同或同类的“安装器写入宿主真实配置后导致宿主启动、配置解析或基础命令失效”的回归风险。

## Intent Contract

- Goal: 基于仓库当前代码与本机可用宿主 CLI，对 `claude-code`、`cursor`、`windsurf`、`openclaw` 逐个完成真实验证，给出每个宿主是否存在同类启动回归的结论与证据。
- Deliverable:
  - 单一需求文档与执行计划
  - 每个宿主的配置写面审计结论
  - 每个宿主可获得的真实 CLI 证据或无法验证时的边界说明
  - 若发现问题，给出根因、修复方案与必要实现
- Constraints:
  - 必须区分“写共享配置但宿主可容忍”和“写共享配置即破坏宿主解析”两类风险。
  - 任何“没有问题”的结论都必须有本地命令或结构证据支撑，不能只依据文档文案。
  - 不得把 `windsurf/openclaw` 这类 runtime-core 宿主与 `claude-code/cursor` 这类共享 `settings.json` 宿主混为一谈。
  - 若宿主 CLI 缺少可用于证明配置解析的非交互命令，必须明确标注验证边界。
- Acceptance Criteria:
  - 对 `claude-code`、`cursor`、`windsurf`、`openclaw` 各自产出明确结论：`confirmed-safe`、`confirmed-regression`、或 `not-provable-with-current-cli-surface`。
  - 每个结论都附带本地命令输出或仓库写面证据。
  - 若发现新问题，必须给出修复范围和验证方案，且不能破坏既有 OpenCode 修复。
- Product Acceptance Criteria:
  - 能回答“除了 OpenCode 以外，其他宿主是否也会因为 Vibe 写入内容而启动不了”这个问题，并能指出具体宿主与证据。
  - 用户支持可以据此给不同宿主提供不同处置建议，而不是统一口径。
- Manual Spot Checks:
  - 隔离根安装后，观察真实共享配置文件是否被写入
  - 运行宿主 CLI 的最小启动/配置探针
  - 核对现有 runtime-neutral tests 与 adapter settings-map/closure truth
- Completion Language Policy:
  - 在没有真实本地 CLI 证据时，不能说“确认安全”，只能说“当前仓库写面未见同类风险”或“当前 CLI 面不足以证明”。
  - 若发现问题但未修复完成，不能说“已解决”。
- Delivery Truth Contract:
  - 本轮允许新增需求/计划文档、验证脚本、测试与必要修复。
  - 对宿主 CLI 行为的判断必须以本机命令输出为准。
- Non-goals:
  - 不在本轮扩展新的宿主能力或重做适配器架构。
  - 不对 OpenCode 已定位问题重复做文档性复述。
- Autonomy Mode: `interactive_governed`
- Inferred Assumptions:
  - `windsurf/openclaw` 因为不写共享 `settings.json`，大概率不具备与 OpenCode 同类的配置解析风险。
  - `claude-code/cursor` 因为写共享 `settings.json` 的 `vibeskills` 节点，仍需真实 CLI 验证其宿主是否容忍该字段。

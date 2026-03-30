# VCO 文档索引

`docs/` 是 VCO 的长期治理文档与说明文档入口。

按"目的"分层组织，避免把当前执行计划、历史证明材料和制度规范混在一起。

---

## 我是谁，我该从哪里开始？

| 我的身份 | 推荐入口 |
|:---|:---|
| **普通用户，想安装使用** | [`install/one-click-install-release-copy.md`](./install/one-click-install-release-copy.md)（中文）或 [`install/one-click-install-release-copy.en.md`](./install/one-click-install-release-copy.en.md)（英文） |
| **想了解系统架构** | [`architecture.md`](./architecture.md) — VCO 总体结构与执行边界概览 |
| **想为项目贡献代码** | [`../CONTRIBUTING.md`](../CONTRIBUTING.md) — 贡献者入口与区域划分规则 |
| **想查看当前运行状态** | [`status/README.md`](./status/README.md) — 当前运行态与各阶段证明材料索引 |
| **想理解治理规则** | [`developer-change-governance.md`](./developer-change-governance.md) — 变更治理正式规则 |

---

## 当前执行入口

这些是**当前活跃**的计划和执行状态文档，如果你在追踪进行中的开发工作，从这里开始：

- [`plans/README.md`](./plans/README.md)：当前 active plan、支撑材料、时间线索引与历史背景入口
- [`plans/2026-03-11-vco-repo-simplification-remediation-plan.md`](./plans/2026-03-11-vco-repo-simplification-remediation-plan.md)：当前 repo 收敛主执行计划
- [`plans/2026-03-13-distribution-governance-plan.md`](./plans/2026-03-13-distribution-governance-plan.md)：分发治理总计划
- [`plans/2026-03-13-post-upstream-governance-repo-convergence-plan.md`](./plans/2026-03-13-post-upstream-governance-repo-convergence-plan.md)：上游治理后的仓库收敛计划
- [`plans/2026-03-13-post-upstream-governance-developer-entry-plan.md`](./plans/2026-03-13-post-upstream-governance-developer-entry-plan.md)：上游治理后的开发者入口计划

---

## 运行态入口

这些是**运行时相关**的文档——安装方式、运行机制、层级治理说明：

**安装**
- [`install/one-click-install-release-copy.md`](./install/one-click-install-release-copy.md)：面向普通用户的一键安装提示词（中文）
- [`install/one-click-install-release-copy.en.md`](./install/one-click-install-release-copy.en.md)：one-click onboarding prompt for ordinary users (English)

**运行机制规范**（这些文件定义了 `/vibe` 调用后的行为规则，不需要改动）
- [`../SKILL.md`](../SKILL.md)：vibe 技能的主合约定义（机器读取 + 人类参考）
- [`../protocols/runtime.md`](../protocols/runtime.md)：6 阶段运行时流程的完整规范
- [`../protocols/team.md`](../protocols/team.md)：XL 多代理编排规范

**层级治理说明**（解释 root/child 分工与 specialist 技能接入规则）
- [`root-child-vibe-hierarchy-governance.md`](./root-child-vibe-hierarchy-governance.md)：说明 root（协调者）与 child（执行者）代理的职责划分，以及 L/XL 执行级别下的串行/并行规则
- [`specialist-dispatch-governance.md`](./specialist-dispatch-governance.md)：说明专项技能（如 `tdd-guide`、`code-review`）如何以受限方式接入 vibe，避免技能冲突

**当前运行状态**
- [`status/README.md`](./status/README.md)：当前运行态、proof 入口与阶段回执总索引
- [`status/current-state.md`](./status/current-state.md)：当前 closure batch 的 runtime 摘要（基于 artifact 证明，非文档本身）
- [`status/non-regression-proof-bundle.md`](./status/non-regression-proof-bundle.md)：最小 closure 证明合约（non-regression proof bundle = 证明一次变更不破坏现有功能所需的最小证据集）
- [`releases/README.md`](./releases/README.md)：受治理的 release 说明与历史 release 记录

**冷启动 / 特殊环境**
- [`cold-start-install-paths.md`](./cold-start-install-paths.md)：三条冷启动路径说明（最小可用、推荐满血、企业治理）
- [`one-shot-setup.md`](./one-shot-setup.md)：一次性 bootstrap、readiness 检查与 deep doctor 说明

---

## 开发者入口

面向贡献者和维护者的变更治理规则与参考资料：

- [`../CONTRIBUTING.md`](../CONTRIBUTING.md)：开发者总入口、禁止随意编辑的区域与证明预期
- [`developer-change-governance.md`](./developer-change-governance.md)：开发者变更治理的正式规则（哪些变更需要计划、哪些需要 proof bundle）
- [`distribution-governance.md`](./distribution-governance.md)：canonical truth surface（权威内容来源）定义与 stop rules（不可绕过的停止规则）
- [`upstream-distribution-governance.md`](./upstream-distribution-governance.md)：上游来源真相、披露与本地保留规则
- [`origin-provenance-policy.md`](./origin-provenance-policy.md)：仓库内保留的上游资产溯源策略
- [`../references/contributor-zone-decision-table.md`](../references/contributor-zone-decision-table.md)：判断某个文件是否可以自由编辑的区域决策表
- [`../references/change-proof-matrix.md`](../references/change-proof-matrix.md)：不同变更类型所需证明材料的矩阵（你需要提供什么才能声称"变更成功"）
- [`../references/developer-entry-contract.md`](../references/developer-entry-contract.md)：开发者入口契约（正式的贡献者行为规范）

---

## 背景 / 治理正文

长期有效的制度规范和架构说明，不随执行计划变化而更新：

- [`docs-information-architecture.md`](./docs-information-architecture.md)：`docs/` 目录的语义划分、索引规则与维护约束
- [`architecture.md`](./architecture.md)：VCO 总体结构、执行边界与主执行面说明
- [`repo-cleanliness-governance.md`](./repo-cleanliness-governance.md)：canonical（规范）/ mirror（镜像）/ runtime（运行时）/ archive（归档）文件的清洁合约
- [`version-packaging-governance.md`](./version-packaging-governance.md)：版本打包拓扑说明（canonical / bundled / nested / installed）
- [`runtime-freshness-install-sop.md`](./runtime-freshness-install-sop.md)：安装 → 新鲜度检查 → 一致性验证的操作程序（SOP）
- [`output-artifact-boundary-governance.md`](./output-artifact-boundary-governance.md)：`outputs/**` 与 `references/fixtures/**` 的长期边界规定
- [`observability-consistency-governance.md`](./observability-consistency-governance.md)：可观测性与一致性治理规则
- [`external-tooling/README.md`](./external-tooling/README.md)：外部工具 / provider / MCP 的接入边界说明

---

## 跨层级导航

- [`../config/index.md`](../config/index.md)：机器可读的策略、路由、打包与清洁配置入口
- [`../scripts/README.md`](../scripts/README.md)：治理脚本、验证脚本、路由脚本与公共脚本入口
- [`../references/index.md`](../references/index.md)：合约、矩阵、账本、fixtures 与 overlays 的导航入口

---

## 本阶段新增的运行状态证明

- [`status/distribution-governance-baseline-2026-03-13.md`](./status/distribution-governance-baseline-2026-03-13.md)
- [`status/distribution-governance-closure-report-2026-03-13.md`](./status/distribution-governance-closure-report-2026-03-13.md)
- [`status/repo-convergence-baseline-2026-03-13.md`](./status/repo-convergence-baseline-2026-03-13.md)
- [`status/repo-convergence-closure-report-2026-03-13.md`](./status/repo-convergence-closure-report-2026-03-13.md)
- [`status/developer-entry-baseline-2026-03-13.md`](./status/developer-entry-baseline-2026-03-13.md)
- [`status/developer-entry-canary-report-2026-03-13.md`](./status/developer-entry-canary-report-2026-03-13.md)
- [`status/developer-entry-closure-report-2026-03-13.md`](./status/developer-entry-closure-report-2026-03-13.md)

---

## 维护规则

- `docs/*.md`（根目录级别）只放**长期治理正文**、集成说明和稳定操作程序，不把有日期的计划或 batch report 升格为 canonical 合约
- `docs/plans/` 负责当前执行入口与时间绑定计划；`docs/status/` 负责当前运行态与 proof 材料；`docs/releases/` 负责 release 记录
- `status/current-state.md` 只做 artifact 支撑的状态摘要；真相来源在 `outputs/verify/**` 与运行时回执中，而非文档本身
- 新增根目录级治理正文时，必须更新本索引；新增有日期的材料时，更新对应子目录的 `README.md` 即可

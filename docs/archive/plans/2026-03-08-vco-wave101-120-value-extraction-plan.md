# VCO Wave101-120 Value Extraction Continuation Plan

- Up: [../README.md](../README.md)
- Index: [README.md](README.md)

**Date:** 2026-03-08
**Mode:** XL / unattended / vibe-first
**Planning Goal:** 在 cleanup-first 已建立 hygiene / parity / freshness / archive-navigation 基线之后，把后续优质项目价值榨取重新收束为一套**先跑通治理跑道、再做深度产品化、最后进入 promotion/release 决策**的连续 wave，而不是重新回到无边界扩张。

## 1. Why Wave101-120

Wave83-100 已经把以下方向推进到“可治理、可评测、可进入 soft stage”的状态：

- memory / prompt / browser / desktop / document / connector 的 plane 级治理；
- promotion board、release train、rollback drill、ops cockpit、candidate quality board；
- upstream corpus / role-pack / discovery / capability lifecycle 的基础治理层。

本轮 cleanup-first 又进一步完成了三件关键事情：

1. `docs/` 的 plans / releases / archive-layer 导航收口；
2. `scripts/` 的 governance / verify / common surface 收口；
3. canonical -> bundled -> nested mirror 的同步与关键门禁复验通过。

因此，Wave101-120 不应重复“搭骨架”，而应解决两个更具体的问题：

1. **剩余价值还没有被榨到 product-grade**：尤其是 `mem0` / `Letta` / `Prompt-Engineering-Guide`、`browser-use` / `Agent-S`、connector ecosystem、role-pack / discovery corpus 仍有高价值切片停留在 `tracked` / `partial_absorption` / `soft`。
2. **继续扩张前仍有跑道缺口**：repo 还不是 zero-dirty，operator surface 也还没有完全统一 preview / output / execution-context 语义；如果现在直接继续大规模吸收，会重新制造漂移。

## 2. Wave101-120 Guardrails

1. **Single control plane**：VCO 仍是唯一 orchestrator、唯一默认 execution owner、唯一 canonical truth-source。
2. **Cleanup before extraction**：与继续榨取直接相关的 operator / docs / scripts runway 必须先收口，再进入新一轮 source-specific productization。
3. **Advice-first / confirm-gated**：上游项目的价值只能增强 VCO 的 contract / scorecard / replay / eval / operator assets，不能直接夺取 routing、execution、promotion 权限。
4. **No raw catalog import**：`awesome-*`、`claude-skills`、`antigravity-awesome-skills`、`awesome-mcp-servers` 等只能 selective harvest，禁止整库变 canonical runtime。
5. **No second runtime**：`browser-use`、`Agent-S`、`agent-squad`、`awesome-claude-code-subagents` 都只能沉淀为 provider / role / handoff / eval pattern，不能变第二运行时。
6. **Every absorption claim needs assets**：任何“吸收完成”都至少需要 `docs + config + references + verify gate (+ pilot/eval if applicable)`。
7. **Wave boundary must stay explicit**：Wave101-104 是 extraction runway，Wave105-116 才是 source-specific 深挖，Wave117-120 负责 board/release/closure；不得跳步。

## 3. Source Clusters and Remaining Value

| Cluster | Source projects | Current posture | Remaining high-value slice | Explicit no-go |
| --- | --- | --- | --- | --- |
| Memory / Prompt | `mem0`, `Letta`, `Prompt-Engineering-Guide` | `soft` / `partial_absorption` | memory write admission quality、memory/prompt eval、pattern distillation、compaction / contract coverage | 不形成第二 memory truth-source；不形成第二 prompt router |
| Browser / Desktop | `browser-use`, `Agent-S` | `soft` / `shadow_governed` | open-world scenario corpus、provider ranking、desktop replay coverage、cross-plane fallback traces | 不形成第二 browser/desktop orchestrator |
| Connector / MCP ecosystem | `awesome-mcp-servers`, `activepieces`, `composio` | `catalog_governed` / `shadow_governed` | connector sandbox simulation、risk-tier coverage、action rollback/replay quality | 不自动安装 catalog；不让 connector runtime takeover |
| Role pack / skill corpus | `agent-squad`, `awesome-claude-code-subagents`, `awesome-agent-skills`, `claude-skills`, `antigravity-awesome-skills`, `awesome-claude-skills-composio` | `tracked_corpus` / `partial_absorption` | role grammar、handoff patterns、harvest scoring、capability dedup against existing skills | 不引入第二 squad/subagent runtime；不整库导入 skills |
| Discovery / eval corpus | `awesome-vibe-coding`, `vibe-coding-cn`, `awesome-ai-tools`, `awesome-ai-agents-e2b` | `tracked_corpus` | multilingual workflow patterns、tool discovery scorecards、agent/eval scenario distillation | 不把 discovery list 直接变 marketplace 或 runtime plane |

## 4. Program Metrics

| Metric | Target by Wave120 | Meaning |
| --- | ---: | --- |
| `repo_cleanup_runway_closed` | 1.0 | extraction-related docs / scripts / operator surface 已收口到可持续推进状态 |
| `operator_surface_documented` | 100% | `scripts/README.md` + `scripts/governance/README.md` + `scripts/common/README.md` 可完整覆盖主要 operator surface |
| `source_cluster_productization_coverage` | >= 80% | 五大 source cluster 至少完成可核查的资产化与门禁化 |
| `duplicate_runtime_introductions` | 0 | 未引入第二 router / orchestrator / default execution owner |
| `strict_candidate_ready_surfaces` | >= 4 | 至少四个已处于 `soft`/`shadow` 的面形成 strict-candidate review 包 |
| `upstream_value_to_asset_ratio` | >= 1.5 | 每个高优先级来源至少沉淀 1 个以上 canonical 资产切片 |
| `release_ready_wave_group` | 1 | Wave117-120 能输出完整 release/board/closure evidence |

## 5. Stage Structure

### Stage A — Extraction Runway Closure (Wave101-104)
先把继续榨取所依赖的治理跑道收口，避免在脏基线与不一致 operator 语义上继续扩张：

- operator surface contract convergence
- preview / apply / output contract normalization
- execution-context / no-BOM / release registration consistency
- extraction resume gate

### Stage B — Memory / Prompt Deep Harvest (Wave105-108)
把 `mem0` / `Letta` / `Prompt-Engineering-Guide` 的剩余价值，从“有治理”推进到“有严格证据链”：

- memory quality + write admission hardening
- Letta policy / memory block / compaction contract coverage
- prompt intelligence eval + bilingual pattern distillation
- memory/prompt strict-candidate review package

### Stage C — Browser / Desktop / Connector Deep Harvest (Wave109-112)
聚焦开放式执行与外部 action plane 的高风险高价值部分：

- browser-use open-world scenario corpus 与 provider ranking
- Agent-S replay / desktop task contract enrichment
- connector sandbox simulation for MCP / Activepieces / Composio
- rollback/replay quality pack for connector actions

### Stage D — Role / Skill / Discovery Corpus Distillation (Wave113-116)
把 role-pack、skill-corpus、discovery-corpus 的“参考价值”进一步压缩成可运营资产：

- role grammar / handoff pattern pack
- selective skill harvest v3
- multilingual vibe workflow extraction
- discovery/eval scorecard pack

### Stage E — Promotion / Release / Closure (Wave117-120)
把前四个 stage 的成果整理成 board / release / closure decision material：

- upstream re-audit matrix refresh
- candidate quality board v2
- bounded promotion proposals
- Wave101-120 closure gate + release evidence bundle

## 6. Wave Backlog

| Wave | Track | Title | Primary goal | Main sources | Planned outputs | Primary gate/evidence |
| --- | --- | --- | --- | --- | --- | --- |
| 101 | runway | operator contract convergence | 统一 operator taxonomy、preview/apply 语义、machine-readable output 边界 | internal governance surface | `scripts/governance/README` 扩展、operator contract doc、run-order table | governance README + cleanliness evidence |
| 102 | runway | common helper adoption hardening | 把 no-BOM / execution-context / shared helper 的使用边界显式化 | internal governance surface | common helper API note、adoption checklist、script drift list | BOM / parity / helper audit evidence |
| 103 | runway | release/operator registration normalization | 统一 release-facing gate registration 与 operator output contract | internal governance surface | release gate registry note、operator output summary contract | release docs + release-cut linkage review |
| 104 | runway | extraction resume gate | 明确何时可从 cleanup-first 切回价值榨取主线 | all clusters | resume checklist、resume gate、workset pressure snapshot | repo cleanliness + output boundary + parity bundle |
| 105 | memory | mem0 write-quality hardening | 把 mem0 从“可选 backend”推进到“可审核 write admission + replay evidence” | `mem0` | write-admission refinements、memory eval scenarios、receipt contract | memory quality / mem0 gates |
| 106 | memory | Letta contract coverage expansion | 扩展 Letta 对 memory block / tool rule / compaction 术语覆盖 | `Letta` | conformance extension doc、contract checklist | Letta policy conformance evidence |
| 107 | prompt | prompt pattern distillation v2 | 把 Prompt-Engineering-Guide 的高价值模式压成 bilingual cards / risk slices | `Prompt-Engineering-Guide` | prompt cards v2、risk checklist v2、distillation scorecard | prompt intelligence eval |
| 108 | memory+prompt | strict-candidate review pack | 形成 memory/prompt 的 strict-candidate review 包，而非直接 promotion | `mem0`, `Letta`, `Prompt-Engineering-Guide` | review bundle、board note、rollback references | candidate quality board |
| 109 | browser | browser-use scenario corpus | 建立开放式 browser task corpus 与 provider fallback trace | `browser-use` | scenario set、provider ranking note、fallback matrix | browser openworld eval |
| 110 | desktop | Agent-S replay enrichment | 提升 desktop replay contract 与 task contract 的覆盖度 | `Agent-S` | replay pattern pack、desktop task taxonomy | desktop replay evidence |
| 111 | connector | connector sandbox simulation v2 | 把 catalog / connector risk 变成可运行的 sandbox simulation matrix | `awesome-mcp-servers`, `activepieces`, `composio` | simulation matrix、risk tier map、rollback samples | connector sandbox simulation gate |
| 112 | connector | connector replay / rollback pack | 让 connector action ledger 从“可记账”升级到“可复放、可回退、可发布” | `activepieces`, `composio`, MCP ecosystem | action ledger enrichments、replay handle contract | connector action / release evidence |
| 113 | role-pack | role grammar and handoff patterns | 提炼角色语法、handoff 模式与 XL team composition pattern | `agent-squad`, `awesome-claude-code-subagents` | role grammar pack、handoff scorecard、team composition notes | role-pack governance evidence |
| 114 | skill-corpus | selective skill harvest v3 | 对 skill corpus 做去重后 selective harvest，而非继续堆 catalog | `awesome-agent-skills`, `claude-skills`, `antigravity-awesome-skills`, `awesome-claude-skills-composio` | harvest matrix v3、dedup notes、asset shortlist | skill harvest / capability dedup evidence |
| 115 | discovery | multilingual vibe workflow extraction | 吸收中英文 vibe workflow 模式，形成 discovery/eval 参考而非第二方法论 | `awesome-vibe-coding`, `vibe-coding-cn` | multilingual workflow note、scenario prompts、anti-drift glossary | discovery intake scorecard |
| 116 | discovery | agent/tool eval distillation | 把 discovery lists 压缩为 candidate scouting + eval corpora | `awesome-ai-tools`, `awesome-ai-agents-e2b` | eval notes、tool scouting scorecard、ceiling notes | discovery/eval evidence pack |
| 117 | board | upstream re-audit matrix v3 | 刷新各来源的 ceiling、migration、remaining value、next asset | all upstream sources | re-audit matrix v3、value ledger refresh | upstream re-audit evidence |
| 118 | board | candidate quality board v2 | 把 memory/prompt/browser/desktop/connector/role/discovery 汇总到统一 board | all promoted candidate surfaces | board v2、quality summary、promotion readiness notes | candidate quality board |
| 119 | promotion | bounded promotion proposals | 只提出有 rollback / kill switch / strict review 包的 promotion proposal | selected soft surfaces | promotion proposal set、boundedness checklist | bounded proposal evidence |
| 120 | closure | Wave101-120 closure bundle | 形成可审计的 stage closure，不直接扩张到 Wave121+ | all stage outputs | closure gate、release evidence bundle、next-horizon memo | Wave101-120 closure gate |

## 7. Priority Order

### P0 — 必须优先启动

- Wave101-104：否则继续榨取会重新把 cleanup-first 打散。
- Wave105-107：`mem0` / `Letta` / `Prompt-Engineering-Guide` 属于当前最接近 product-grade，但仍最容易越界的来源。
- Wave109-111：browser / desktop / connector 是高价值也高风险的外部执行面，必须在 strict-candidate 前完成 scenario / replay / simulation 证据。

### P1 — 跑道稳定后推进

- Wave112-116：role-pack / skill harvest / discovery distillation。
- 这些方向价值高，但比 memory/browser/connector 更适合作为“跑道稳定后”的第二批增量。

### P2 — 最后执行

- Wave117-120：board / promotion / closure。
- 只有当前面 stage 的证据足够完整，才值得进入统一 board 与 bounded promotion proposals。

## 8. Explicit Non-Goals

- 不新增新的顶层 plane。
- 不把 `browser-use`、`Agent-S`、`agent-squad`、`awesome-claude-code-subagents` 升级成第二运行时。
- 不把 `awesome-*` 列表变成可直接安装/可直接执行的 marketplace。
- 不跳过 cleanup runway 直接进入 promotion / release。
- 不把“发现了有价值内容”直接等同于“已经吸收完成”。

## 9. Definition of Ready

任一 wave 在进入执行前，至少要满足：

- 对应 source cluster 的当前状态、剩余价值与 no-go 边界已经清楚写明；
- 已知它会产出哪些 canonical assets，而不是只做调研；
- 已知它依赖哪些现有 gate / board / policy；
- 已知失败时回退到哪个 stage / policy / operator command。

## 10. Definition of Done

Wave101-120 规划层面的完成，要求：

- 所有 wave 都有明确 title / source / output / evidence；
- 先跑道、再产品化、再 promotion 的顺序被固定；
- 五大 source cluster 都有具体榨取方向，而不是抽象口号；
- 明确列出哪些内容绝对不能吸收，以防再次引入冗余与控制面漂移。

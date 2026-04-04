# VCO Wave83-100 Formal Planning Horizon

- Up: [../README.md](../README.md)
- Index: [README.md](README.md)

**Date:** 2026-03-07
**Mode:** XL / unattended / vibe-first
**Program Goal:** 在 Wave64-82 已完成 plane contractization / scorecard / replay / promotion / release closure 的基础上，把后续 `83+` 收束为一个**有边界的第一规划视界**：优先消化剩余上游价值、提高 gate 与证据链可靠性、把 advisory-only 能力变成可运营的人工复核闭环，而不是继续无边界扩张新的控制面。

## 1. Why Wave83+

Wave64-82 已经完成：
- memory / browser / desktop / document / connector / prompt intelligence 的 plane 级治理落地；
- cross-plane task contract / replay ledger / promotion board v2 / ops cockpit / rollback drill / release train v2；
- Wave64-82 closure gate 通过，进入“可继续扩张但必须受控”的状态。

Wave83+ 不应该重复 64-82 的工作。新的目标应转向三件事：

1. **可靠性硬化**：把 verify / board / release evidence 链做成不易因关键词漂移、编码差异、运行壳差异而误报失败的治理基础设施。
2. **剩余价值产品化**：继续吸收 `agent-squad` / `awesome-agent-skills` / `awesome-claude-code-subagents` / `awesome-vibe-coding` / `vibe-coding-cn` / `awesome-ai-tools` / `e2b` 等尚未 fully productized 的价值，但只以 VCO-native asset 落地。
3. **人工闭环运营化**：把 advisory-first 能力进一步接到 dashboard / release evidence bundle / bounded proposal / manual apply 流程，而不是自动接管 routing 或 owners。

## 2. Guardrails

1. **VCO remains the only control plane**：不得引入第二 orchestrator、第二默认 execution owner、第二 canonical truth-source。
2. **Advisory-first still dominates**：Wave83-100 所有新增建议面都只能输出 evidence / suggestion / scorecard，不得自动写入 router / board / stage。
3. **Rollback-first remains mandatory**：所有新 proposal / eval / dashboard 必须显式带 rollback reference 或 kill switch path。
4. **No uncontrolled new top-level planes**：Wave83-100 不新增新的顶层控制平面；只允许在现有 plane、role-pack、discovery/eval、ops/release 这四条轴线上深化。
5. **Productize only after dedup**：任何来自上游的新价值必须先证明不与现有 plane / overlay / governance 重叠，才能进入 canonical backlog。
6. **Planning horizon is bounded**：本次 `83+` 规划先收敛为 `Wave83-100`；`Wave101+` 只在 `Wave83-100 closure gate` 通过后再展开。

## 3. Program Metrics

| Metric | Target by Wave100 | Meaning |
|---|---:|---|
| `gate_reliability_pass_rate` | >= 95% | 关键 verify gates 在支持环境中的可重复运行率 |
| `candidate_eval_coverage` | >= 80% | memory/browser/desktop/document/prompt 的候选质量评测覆盖率 |
| `role_pack_governed_sources` | >= 4 | role-pack 相关上游来源进入可治理 catalog / scorecard |
| `discovery_intake_scored_sources` | 4/4 | `awesome-vibe-coding` / `vibe-coding-cn` / `awesome-ai-tools` / `awesome-ai-agents-e2b` 全部进入 intake scoring |
| `connector_simulation_coverage` | >= 80% | connector 写动作有 sandbox / simulation / rollback evidence |
| `release_bundle_completeness` | 100% | release evidence bundle 字段完整 |
| `upstream_reaudit_completeness` | 15/15 | 15 个上游项目完成再审计矩阵更新 |
| `new_top_level_planes_added` | 0 | 不新增新的顶层控制平面 |

## 4. Stage Structure

### Stage A — Reliability & Candidate Evaluation (Wave83-88)
先把 Wave64-82 的治理资产变成更稳的执行基础，再建立 candidate quality evidence：
- gate reliability / keyword alias / shell robustness
- memory quality eval
- browser + desktop openworld eval
- document failure taxonomy
- prompt intelligence eval
- candidate quality board

### Stage B — Remaining Upstream Value Productization (Wave89-94)
把仍停留在 tracked/partial 的高价值来源，压缩为 VCO-native 的 role-pack / discovery / capability / connector / skill-harvest 治理资产：
- role pack v2 / subagent handoff
- discovery intake scoring
- capability lifecycle
- connector sandbox simulation
- skill harvest v2

### Stage C — Human-in-the-Loop Operations (Wave95-100)
把 advisory-first 能力接入 operator / release / bounded-proposal 闭环：
- ops dashboard
- release evidence bundle
- manual apply policy
- rollout proposal boundedness
- upstream re-audit matrix v2
- Wave83-100 closure gate

## 5. Wave Backlog

| Wave | Track | Title | Primary Goal | Upstream Value Source | Candidate Gate |
|---|---|---|---|---|---|
| 83 | reliability | gate reliability and keyword alias governance | 把 verify gate 的关键词/编码/壳兼容性纳入统一可靠性合同 | all current planes | `vibe-gate-reliability-gate.ps1` |
| 84 | candidate-eval | memory quality eval pack | 为 `mem0` / `Letta` 建立 preference-quality / retention / fallback eval 证据 | `mem0`, `Letta` | `vibe-memory-quality-eval-gate.ps1` |
| 85 | candidate-eval | openworld runtime eval harness | 统一 BrowserOps / DesktopOps 的 openworld eval / replay / confirm / rollback 场景包 | `browser-use`, `Agent-S` | `vibe-openworld-runtime-eval-gate.ps1` |
| 86 | candidate-eval | document failure taxonomy | 把 Docling document plane 的 extraction failure modes / remediation paths 制度化 | `Docling` | `vibe-document-failure-taxonomy-gate.ps1` |
| 87 | candidate-eval | prompt intelligence eval and card QA | 为 Prompt intelligence 建立 pattern-card 质量、风险标注、confirm hint 评测面 | `Prompt-Engineering-Guide` | `vibe-prompt-intelligence-eval-gate.ps1` |
| 88 | candidate-eval | candidate quality board v1 | 把 memory/browser/desktop/document/prompt 候选质量汇总进统一 quality board | multiple current planes | `vibe-candidate-quality-board-gate.ps1` |
| 89 | role-pack | role pack v2 governance | 把 role-pack 剩余价值从 reference 升格为 scorecard + boundary + landing graph | `agent-squad`, `awesome-agent-skills`, `awesome-claude-code-subagents`, `antigravity-awesome-skills`, `claude-skills` | `vibe-role-pack-v2-gate.ps1` |
| 90 | role-pack | subagent handoff governance | 把 reviewer / analyst / implementer / supervisor handoff 模式沉淀为责任矩阵与证据合同 | `agent-squad`, `awesome-claude-code-subagents` | `vibe-subagent-handoff-gate.ps1` |
| 91 | discovery | discovery intake scorecard | 为 discovery corpus 建立 source intake / dedup / usefulness scoring，停止只跟踪不排序 | `awesome-vibe-coding`, `vibe-coding-cn`, `awesome-ai-tools`, `awesome-ai-agents-e2b` | `vibe-discovery-intake-scorecard-gate.ps1` |
| 92 | discovery | capability lifecycle governance | 把 capability catalog 从静态登记推进到 intake / promote / retire 的生命周期治理 | discovery corpus + capability catalog | `vibe-capability-lifecycle-gate.ps1` |
| 93 | connector | connector sandbox simulation | 对 `composio` / `activepieces` 写动作建立 sandbox / simulation / rollback evidence contract | `Composio`, `activepieces`, `awesome-mcp-servers` | `vibe-connector-sandbox-simulation-gate.ps1` |
| 94 | skill-corpus | skill harvest v2 governance | 把剩余 skill catalog 来源压成更可审计的 harvest scorecard 与 promotion ceiling | `claude-skills`, `antigravity-awesome-skills`, `awesome-claude-skills-composio` | `vibe-skill-harvest-v2-gate.ps1` |
| 95 | operations | ops dashboard evidence pack | 把 board / telemetry / replay / rollback 证据汇总成 operator-facing dashboard pack | all promoted candidates | `vibe-ops-dashboard-gate.ps1` |
| 96 | release | release evidence bundle v3 | 把 release note / release ledger / verify evidence / board snapshot 统一成 release bundle | release train v2 inputs | `vibe-release-evidence-bundle-gate.ps1` |
| 97 | governance-loop | manual apply policy governance | 把建议输出、人工复核、显式 apply、回滚记录制度化为 manual-only policy | adaptive routing / advisory outputs | `vibe-manual-apply-policy-gate.ps1` |
| 98 | governance-loop | rollout proposal boundedness | 为所有 rollout/proposal 输出增加 delta 上界、non-goal、rollback reference 校验 | all proposal-producing surfaces | `vibe-rollout-proposal-boundedness-gate.ps1` |
| 99 | upstream | upstream re-audit matrix v2 | 对 15 个上游项目做再审计矩阵，更新 absorbability / remaining value / no-go | all tracked upstream sources | `vibe-upstream-reaudit-matrix-gate.ps1` |
| 100 | closure | wave83-100 closure gate | 形成 Wave83-100 正式 closure gate，为 Wave101+ 进入条件提供硬证据 | all tracks | `vibe-wave83-100-closure-gate.ps1` |

## 6. Track-by-Track Design Notes

### 6.1 Reliability Track (Wave83)
- 不新建 plane；只增强 verify/gate 体系的可维护性。
- 目标是把“关键词漂移 / PowerShell 编码差异 / 壳差异”变成显式治理对象。
- 必须保持 gate 仍是 evidence checker，而不是文档生成器。

### 6.2 Candidate Eval Track (Wave84-88)
- `mem0` / `Letta`：重点不再是 contract existence，而是 candidate quality、retention confidence、fallback integrity。
- `browser-use` / `Agent-S`：重点是 openworld replayable eval，不是放宽 takeover boundary。
- `Docling`：重点是 extraction failure taxonomy 与 remediation evidence，不是更换 document truth-owner。
- `Prompt-Engineering-Guide`：重点是 pattern cards / risk checklist 的质量评测，不是第二 prompt router。

### 6.3 Role Pack / Discovery / Skill Productization (Wave89-94)
- `agent-squad` / `awesome-agent-skills` / `awesome-claude-code-subagents` 的价值继续走 role-card / handoff / scorecard，不进入第二 orchestrator。
- `awesome-vibe-coding` / `vibe-coding-cn` / `awesome-ai-tools` / `awesome-ai-agents-e2b` 继续只走 discovery/eval/capability material layer，不变成 runtime surface。
- `Composio` / `activepieces` 的下一步不是升为默认 connector owner，而是建立更强的 sandbox / simulation / rollback evidence。
- `claude-skills` / `antigravity` / `awesome-claude-skills-composio` 的下一步是 skill harvest quality bar，而不是大规模 raw import。

### 6.4 Operations Loop (Wave95-100)
- dashboard / release bundle / proposal boundedness 都必须是 **manual-review-first**。
- 任何 suggestion 都必须显式包含：`scope`, `delta_limit`, `non_goals`, `rollback_reference`, `apply_policy=manual_only`。
- `Wave100` closure gate 通过前，不展开 `Wave101+` 实施。

## 7. Entry / Exit Rules

### Entry Rule for Wave83 Execution
以下条件同时满足，才允许从规划进入实施：
- Wave64-82 closure gate 已通过；
- `config/wave83-100-planning-board.json` 已落地；
- 至少明确 3 个 first execution slices（建议：83 / 89 / 95）；
- 无需新增顶层 plane 才能推进。

### Exit Rule for Wave100 Closure
满足以下条件，才允许讨论 `Wave101+`：
- `Wave83-100` planning board 全部完成；
- candidate eval / role-pack productization / ops bundle 三条主线均有 closure evidence；
- `upstream re-audit matrix v2` 完成 15/15 更新；
- `vibe-wave83-100-closure-gate.ps1` 通过。

## 8. Suggested First Execution Slices

建议优先执行以下 3 个 slice：
1. **Wave83**：先把 gate / shell / keyword alias 的可靠性层做稳，避免后续所有 wave 被验证脆弱性反复打断。
2. **Wave89**：把 role-pack 相关上游价值推进成可治理 scorecard，继续榨取 `agent-squad` / subagent catalog 系列的剩余价值。
3. **Wave95**：把 ops dashboard 做出来，提升 operator 可见性，为 96-100 的 release/manual loop 打底。

## 9. Not In Scope

以下内容明确不在 Wave83-100：
- 新的顶层控制平面；
- 自动修改 VCO router / promotion board stage 的自适应闭环；
- 直接把上游 marketplace / catalog 暴露为运行态 surface；
- 未经过 dedup 的大规模 skill 或 role 原样导入。

## 10. Deliverables for This Planning Step

本轮规划只要求形成：
- `docs/plans/2026-03-07-vco-wave83-100-execution-plan.md`
- `config/wave83-100-planning-board.json`
- `task_plan.md` / `findings.md` / `progress.md` 的 Wave83+ planning addendum

而不要求：
- 实际创建 Wave83-100 的 docs/config/gates 本体；
- 运行任何新的 verify gate；
- 进行任何 `shadow -> soft` 晋升动作。

## 11. Execution Status Companion

The planning board remains the authoritative Wave83-100 execution tracker.
The previously separate execution-status companion is no longer kept as a standalone repo document.

Execution expectations:
- execution frontier starts at `Wave83`
- sequencing remains `83 -> 89 -> 95`
- readiness should stay visible as **ready / blocked / sequenced** inside the planning board and runtime receipts

# No Silent Fallback And No Self-Introduced Fallback Governance Plan

> **For Claude:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task.

**Goal:** 把 VCO 当前“允许静默回退、允许实现期顺手补 fallback、允许把退化路径包装成正常成功”的治理口径，升级为一套可执行、可验证、可发布的强约束治理体系。该体系必须同时满足三条硬要求：默认禁止静默回退，默认禁止自发编写回退逻辑，任何回退或退化路径一旦触发都必须向用户发出独立、强烈、不可忽略的风险警报，明确说明这不是等价成功，而是能力边界变化与可信度下降。

**Architecture:** 本计划采用 `principle freeze -> policy encoding -> implementation guard -> runtime hazard alert -> proof and release truth` 五层结构。第一层冻结原则，第二层把原则转成 machine-readable policy，第三层约束代码实现和评审，第四层改造运行时与路由的告警和 truth surface，第五层以专用 gate、replay、release truth bundle 证明稳定性、可用性和智能性没有被“回退便利性”侵蚀。

**Tech Stack:** Markdown governance docs, JSON policy files, PowerShell/Python/Bash runtime scripts, router/runtime contracts, verify gates, replay fixtures, release truth documents, diff-based review enforcement.

---

## Executive Conclusion

### Final Judgment

当前仓库已经不适合继续把 `fallback` 视为一种默认工程便利。

原因不是“回退机制永远不能存在”，而是仓库里已经同时出现了四类高风险现象：

1. 运行时把 `legacy_fallback`、`fallback_provider`、`fallback_on_error`、`supported-with-constraints` 等语义混合使用，容易把“降级可运行”误叙述成“能力等价”。
2. 实现层存在“顺手补一个 fallback 先让它跑起来”的空间，容易把未解决的问题包进代码，形成长期质量债。
3. 部分协议与 overlay 把 fallback 当作正常设计项，而不是高风险例外项。
4. 用户很可能在没有被强提醒的情况下进入退化路径，最终遭遇“功能退化而不自知”。

因此，本次治理的核心不是“删除所有 fallback 词汇”，而是重建如下秩序：

- `fallback_policy = forbidden_by_default`
- `self_introduced_fallback = forbidden_by_default`
- `silent_degradation = forbidden`
- `fallback_success_is_not_authoritative_green = true`
- `degradation_budget = 0 unless explicitly approved`

### Required Outcome

完成后，VCO 必须满足以下事实：

1. 除非用户明确要求设计 fallback / degrade / rollback / compatibility rescue path，否则实现阶段禁止主动新增相关逻辑。
2. 任何运行时回退都不能静默发生，必须发出独立的高严重度警报区块。
3. 任何回退成功都不能直接记为标准成功，必须标记为 `degraded`, `non-authoritative`, `manual-review-required` 或等价状态。
4. 评审、verify gate、release note、platform truth、runtime receipt 必须对回退路径保持同一套口径。
5. 证明链必须覆盖稳定性、可用性、智能性三条维度，而不是只验证“程序还能跑”。

---

## Why This Plan Exists

用户这次要求的不是普通编码规范，而是一次治理哲学升级。

目标是让 VCO 从“默认帮你兜底”升级为“默认不替你掩盖问题”。这背后的工程判断是成立的：

- 静默回退会让真实故障隐藏在“貌似成功”的表象里。
- 自发引入 fallback 会让代码库越来越像补丁堆，而不是可验证系统。
- 如果运行时不把退化风险显式抬到用户层，用户会把退化结果当成等价结果。
- 一个强调 governed runtime 的系统，不能把“有 fallback 所以能继续”当成默认美德。

本计划的根本方向是：

- 把 fallback 从“默认可用工具”降级为“高风险例外机制”
- 把 warning 从“普通提示”升级为“风险警报”
- 把实现习惯从“先让它别报错”改成“先把真实边界说清楚”

---

## Scope Split

本计划必须同时治理两类问题，且不能混为一谈。

### Scope A: Runtime Fallback Governance

治理对象包括但不限于：

- `legacy_fallback`
- `fallback_provider`
- `fallback_on_error`
- `supported-with-constraints`
- `degraded-but-supported`
- `manual_actions_pending`
- route guard 触发后的 confirm / degrade surface
- provider / overlay / bridge 的异常兜底

目标是：

- 禁止静默回退
- 禁止把退化结果包装成等价成功
- 统一回退风险警报语义

### Scope B: Implementation-Time Fallback Governance

治理对象包括但不限于：

- 新代码里主动添加 `fallback`, `degrade`, `legacy`, `rescue`, `backup path`, `best effort`, `continue on error` 一类逻辑
- 为了让测试先过而临时加入的兼容分支
- 在用户未要求的情况下新增 retry + fallback + swallow error 组合

目标是：

- 禁止自发回退实现
- 禁止把 fallback 当作默认工程风格
- 只有在 requirement / plan 明确批准时才允许设计回退机制

### Scope C: Explicit Exception Handling

以下场景不属于“默认禁止一切”的简单粗暴治理，必须单独建模：

1. 用户明确要求存在回退策略。
2. 平台能力差异必须被诚实暴露，例如 host capability declaration。
3. 安装或接入环节的人工接管提示。
4. 迁移期 shadow path，仅用于 proof 或对比，不得作为对外默认成功路径。
5. 遥测、日志、可观测性等非主功能面的受限退化，但必须明确标记为 non-authoritative。

这些例外场景可以存在，但必须满足两条规则：

- 例外必须显式声明，不得默认生效。
- 例外一旦触发，必须发出强警报，并改变 success truth。

---

## Non-Negotiable Principles

### Principle 1: No Silent Fallback

任何回退、降级、切换到 legacy、切换到 manual path、切换到 heuristic-only、切换到 alternate provider 的行为，都不得静默发生。

### Principle 2: No Self-Introduced Fallback

除非用户明确要求，禁止在写代码、补 bug、改路由、改 overlay、改 provider、改治理脚本时自发加入回退逻辑。

### Principle 3: Fallback Is Hazard, Not Convenience

一旦进入 fallback 路径，系统必须把它视为风险事件，而不是便利特性。

### Principle 4: Fallback Success Is Not Equivalent Success

fallback path 返回结果，不代表 authoritative green。必须单独标记 truth level。

### Principle 5: Warning Must Escalate To Hazard Alert

用户要求的不是“多给一点 warning”，而是强烈、单独、不可混淆的风险提示。标准 warning 不够。

### Principle 6: Governance Must Cover Prompt, Plan, Code, Runtime, Review, Release

如果只改 README 或只改 router，治理一定会漏。必须形成全链路约束。

---

## Threat Model

### Threat 1: Hidden Functional Degradation

系统触发 fallback，但用户误以为结果等价。

后果：

- 功能能力下降
- 验证强度下降
- 可信度下降
- 用户不知情

### Threat 2: Fallback Debt Accumulation

开发者为追求短期通过率，在实现中不断加入 fallback。

后果：

- 代码路径爆炸
- 主路径责任不清
- 真实 bug 被延后
- proof 难度持续上升

### Threat 3: Release Truth Corruption

release note、platform status、runtime receipt 对 fallback 的叙述不一致。

后果：

- 用户看不懂真实状态
- 平台支持声明失真
- verification 失去公信力

### Threat 4: Intelligence Masked By Recovery

模型或路由本该暴露“不知道”或“不够确定”，却被 fallback 包装成“已经处理完”。

后果：

- 智能性评估失真
- ranking / routing 真问题被掩盖
- benchmark 指标虚高

---

## Formal Policy Design

## Policy Object 1: Runtime Fallback Policy

新增或强化统一策略对象，建议命名为：

- `config/fallback-governance.json`

其核心字段应当包含：

```json
{
  "fallback_policy": "forbidden_by_default",
  "silent_fallback": false,
  "silent_degradation": false,
  "fallback_success_is_authoritative": false,
  "require_hazard_alert": true,
  "require_user_explicit_approval_for_design": true,
  "degradation_budget_default": 0
}
```

### Required Runtime Semantics

1. 只要 route / provider / runtime / overlay 进入 fallback，receipt 必须记录。
2. route result 必须带出 truth level。
3. UI / rendered text / operator summary 必须出现风险警报。
4. verify gate 必须校验“是否警报”和“是否 truth 降级”。

## Policy Object 2: Implementation Fallback Policy

建议新增：

- `config/implementation-guardrails.json`

其核心语义：

```json
{
  "self_introduced_fallback": "forbidden_by_default",
  "allowed_only_when_requirement_explicit": true,
  "diff_must_flag_fallback_keywords": true,
  "review_requires_explicit_justification": true
}
```

### Required Implementation Semantics

1. 新增 fallback 逻辑时，必须存在 requirement-level 批准字段。
2. plan 必须写出 fallback 的适用边界、风险、验证方式、退出条件。
3. review 必须单独审 fallback 是否必要。
4. 没有 requirement 批准时，相关 diff 直接红灯。

## Policy Object 3: Hazard Alert Contract

建议统一引入强警报标准，建议使用固定标题：

- `FALLBACK HAZARD ALERT`
- `DEGRADATION HAZARD ALERT`

### Mandatory Alert Language

每次触发回退时，至少必须向用户明确说明：

1. 这不是等价成功。
2. 当前结果来自回退或退化路径。
3. 功能边界、验证强度或可信度可能下降。
4. 用户如果继续使用，可能在不自知的情况下承受功能退化。
5. 如需 authoritative 结果，必须回到主路径修复问题或补齐依赖。

---

## Repository Change Map

## Layer 1: Principle And Protocol Layer

优先修改或新增：

- `protocols/runtime.md`
- `protocols/do.md`
- `protocols/review.md`
- `protocols/think.md`
- `config/runtime-contract.json`

### Required Changes

1. 把“禁止静默回退”写成 runtime invariant。
2. 把“禁止自发回退实现”写成 implementation invariant。
3. 把“fallback success is not authoritative green”写入 runtime truth。
4. 把 review 对 fallback 的阻断条件写成正式规则。

## Layer 2: Router And Runtime Layer

重点目标文件：

- `scripts/router/resolve-pack-route.ps1`
- `scripts/router/runtime_neutral/router_contract.py`
- `config/router-thresholds.json`
- `config/router-model-governance.json`
- `config/platform-support-policy.json`

### Required Changes

1. 保留已有 fallback 机制的事实描述，但把其默认语义改为 hazard path。
2. route result 中增加 `truth_level`, `hazard_alert_required`, `degradation_state` 一类字段。
3. 如果 route mode 为 `legacy_fallback` 或等价状态，必须输出强警报，而不是普通 confirm 文本。
4. 平台 truth 文档不得把 degraded lane 叙述成 equivalent support。

## Layer 3: Implementation And Review Layer

重点目标文件：

- `protocols/do.md`
- `protocols/review.md`
- `scripts/verify/*`
- diff review / lint / governance gates

### Required Changes

1. 新增“fallback keyword introduction audit”。
2. 新增“requirement-approved fallback only” gate。
3. 新增 reviewer checklist：
   - 这个 fallback 是用户明确要求的吗
   - 没有 fallback 是否可以直接暴露真实错误
   - fallback 是否会掩盖主路径问题
   - fallback 是否改变 authoritative truth

## Layer 4: Release Truth Layer

重点目标文件：

- `docs/releases/*.md`
- `docs/status/*.md`
- `config/platform-support-policy.json`
- proof bundle docs

### Required Changes

1. release note 不得把 fallback closure 写成 capability closure。
2. platform truth 必须区分：
   - authoritative
   - degraded
   - constrained
   - manual-handoff-required
3. proof bundle 必须显式列出是否使用 fallback。

---

## Execution Program

## Wave 0: Truth Freeze

### Objective

先冻结治理目标和风险语言，避免一边改代码一边变口径。

### Actions

1. 新增本计划文档。
2. 冻结 fallback hazard vocabulary。
3. 冻结 authoritative vs degraded truth vocabulary。

### Exit Criteria

- 官方计划存在
- 警报术语固定
- truth vocabulary 固定

## Wave 1: Principle Encoding

### Objective

把原则写进 protocol 和 config，而不是停留在文档口号层。

### Actions

1. 在 runtime contract 中加入 `no_silent_fallback` invariant。
2. 在 do/review protocol 中加入 `no_self_introduced_fallback` invariant。
3. 新增 machine-readable fallback governance policy。

### Exit Criteria

- protocol 层可读
- config 层可机读
- invariant 可被 gate 调用

## Wave 2: Implementation Guard

### Objective

阻止未来继续无意识地产生 fallback 债。

### Actions

1. 新增 fallback keyword diff audit。
2. 新增 requirement-approved fallback gate。
3. 把 review checklist 固化进 verify path。

### Exit Criteria

- 无 requirement 批准时，新增 fallback diff 红灯
- review 对 fallback 有单独断言

## Wave 3: Runtime Hazard Alert

### Objective

把“回退风险”从内部语义提升到用户可见语义。

### Actions

1. route result 增加 truth and hazard fields。
2. confirm / rendered text 输出独立风险警报。
3. runtime receipt 标注 degradation state。

### Exit Criteria

- fallback 触发时一定有独立风险警报
- fallback success 不再显示成普通 green

## Wave 4: Proof Closure

### Objective

证明这套治理不是只会增加告警噪音，而是提升真实稳定性和可信度。

### Actions

1. 新增 runtime hazard proof gate。
2. 新增 implementation fallback guard gate。
3. 新增 release truth consistency gate。

### Exit Criteria

- stability proof green
- usability proof green
- intelligence proof green

## Wave 5: Release Truth Realignment

### Objective

让 release note、status、platform truth、runtime receipt 对 fallback 说同一种话。

### Actions

1. 修订 release note 模板。
2. 修订 platform truth 模板。
3. 修订 promotion bundle 输出。

### Exit Criteria

- release truth 不再夸大 fallback closure
- proof 与叙事一致

---

## Testing And Proof Program

## Stability Proof

必须证明：

1. 引入治理后，主路径不会因为“禁止 fallback”而发生无意破坏。
2. fallback 触发时，系统 truth 标记稳定、字段完整、receipt 可追踪。
3. 旧有 fallback 机制不会再以 silent 方式通过。

### Suggested Tests

- runtime contract schema tests
- route result truth-level tests
- fallback hazard alert rendering tests
- receipt completeness tests

## Usability Proof

必须证明：

1. 用户能明显区分 authoritative success 与 degraded success。
2. 风险提示足够醒目，不会与普通 warning 混淆。
3. 治理不会把正常主路径体验变成过度摩擦。

### Suggested Tests

- confirm / rendered text snapshot tests
- warning severity snapshot tests
- operator summary clarity tests
- common happy-path no-extra-alert tests

## Intelligence Proof

必须证明：

1. 模型或 router 不会靠 fallback 掩盖自身不确定性。
2. “不知道”与“退化完成”被区分开。
3. benchmark / governed runtime 的结果 truth 更诚实，而不是更虚假地乐观。

### Suggested Tests

- route decision honesty replay
- fallback trigger reason coverage
- benchmark_autonomous truth-surface proof
- authoritative vs degraded success classification tests

---

## Required Gates

建议新增以下 gates。

1. `vibe-no-silent-fallback-contract-gate.ps1`
2. `vibe-no-self-introduced-fallback-gate.ps1`
3. `vibe-fallback-hazard-alert-gate.ps1`
4. `vibe-release-truth-vs-fallback-consistency-gate.ps1`
5. `vibe-benchmark-truth-honesty-gate.ps1`

### Gate 1: No Silent Fallback Contract Gate

断言：

- fallback path 一旦出现，必须有 truth downgrade
- fallback path 一旦出现，必须有 hazard alert
- fallback path 不得被记为 authoritative green

### Gate 2: No Self-Introduced Fallback Gate

断言：

- diff 中新引入 fallback 关键词时，必须关联 requirement 批准
- 未批准则直接失败

### Gate 3: Fallback Hazard Alert Gate

断言：

- UI / receipt / runtime summary 存在独立警报区块
- 警报语句包含“不等价成功”“可能功能退化而不自知”等硬语义

### Gate 4: Release Truth Consistency Gate

断言：

- release note
- platform status
- proof bundle
- runtime receipt

对同一 fallback 事实的描述必须一致。

### Gate 5: Benchmark Truth Honesty Gate

断言：

- benchmark_autonomous 在触发 fallback 时不会把结果包装为完整闭环成功
- proof 中必须暴露 degraded truth

---

## Stop Rules

出现以下任一情况必须停止继续推进，并先修治理口径：

1. 新增告警但没有改变 truth level。
2. 新增 gate 但允许未批准 fallback diff 通过。
3. release note 继续把 degraded closure 写成 full closure。
4. benchmark proof 仍然把 fallback success 记作标准 success。
5. 用户层仍然看不到独立风险警报。

---

## Migration Cautions

这次治理不能用“全删 fallback”来粗暴完成。

必须注意：

1. 当前仓库已经大量存在 fallback / degrade 词汇，迁移需要分层分类。
2. 平台能力声明、手工接管提示、观测面降级不应与主功能 fallback 混为一谈。
3. 某些兼容桥接可能暂时保留，但必须改成 explicit hazard path。
4. 迁移期允许存在 shadow fallback proof，仅限 proof，不得当作正式主路径成功。

---

## Final Acceptance Criteria

本计划只有在以下条件全部满足时才算真正落地：

1. 默认实现路径不再允许自发添加 fallback。
2. 所有 runtime fallback 都不再静默发生。
3. 所有 fallback success 都不再被记为 authoritative green。
4. 用户在触发回退时一定会看到强烈、独立、不可忽略的风险警报。
5. review、verify、release truth、platform truth 口径统一。
6. stability、usability、intelligence 三类 proof 全部通过。

---

## Immediate Next Steps

1. 先执行 Wave 1，把原则编码进 protocol 和 config。
2. 再执行 Wave 2，先堵住“继续新增 fallback 债”的入口。
3. 然后执行 Wave 3，把 runtime truth 和 hazard alert 打通。
4. 最后执行 Wave 4 和 Wave 5，用 proof 和 release truth 收口。

Plan complete and saved to `docs/plans/2026-03-15-no-silent-fallback-and-no-self-introduced-fallback-governance-plan.md`.

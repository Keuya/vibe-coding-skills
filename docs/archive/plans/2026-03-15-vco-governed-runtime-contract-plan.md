# VCO Governed Runtime Contract Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 把 `vibe` 从“以 M/L/XL 为用户入口分流的路由器”收敛为“统一治理入口”，让 `/vibe`、`$vibe` 与 agent 调用 `vibe` 时都进入同一条官方主路径，并在 `interactive_governed` 与 `benchmark_autonomous` 两种模式下，以固定的 6 段状态机完成需求澄清、文档冻结、XL 计划、计划执行、验证与阶段清洁闭环。

**Architecture:** 本计划采用 `single governed runtime contract + internal execution grade + phase receipts + mandatory phase cleanup` 架构。用户只感知一个 `vibe` skill 入口，`M/L/XL` 降为内部执行编排等级；主状态机固定为 `skeleton_check -> deep_interview -> requirement_doc -> xl_plan -> plan_execute -> phase_cleanup`，并通过 machine-readable config、runtime scripts、phase receipts 与 verify gates 证明行为稳定、不退化、可审计。

**Tech Stack:** PowerShell / Bash, Markdown governance docs, JSON runtime contracts, VCO router/runtime scripts, verify gates, plan/requirements templates, phase cleanup / node hygiene governance.

---

## Executive Conclusion

### Final Judgment

`vibe` 现在已经不适合继续以“先判断 M/L/XL，再决定是否访谈、是否规划、是否并发”的方式承担统一入口职责。

原因不是当前分级设计无效，而是它把过多“下一步该怎么做”的认知负担转移给了用户：

1. 用户要先判断这是不是复杂任务。
2. 用户要先判断自己是否应该进入 XL。
3. 用户要自己决定要不要先访谈、先写计划、还是先执行。
4. 用户要自己约束“什么时候进入无人值守、什么时候收口、什么时候清理”。

这与 VCO / VibeSkills 想提供的“智能外骨骼”方向冲突。对用户最友好的设计应该是：

- 只要调用 `vibe`，就进入统一治理路径；
- 需求先被澄清和冻结；
- 计划总是先于执行；
- 执行总是带验证；
- 阶段结束总是自动收口；
- 用户只在需要做高价值决策时介入。

因此，本计划的正式目标不是继续扩展“更多路由分支”，而是把 `vibe` 重构为：

- **统一 skill 入口**
- **固定治理状态机**
- **双运行模式**
- **内部等级编排**
- **可证明闭环**

### Required Outcome

完成后，`vibe` 必须满足以下事实：

1. `/vibe`、`$vibe`、以及 agent prompt 中附加 `vibe` skill 时，进入同一运行时契约。
2. 用户不再看到 M/L/XL 作为入口选项。
3. 所有 `vibe` 任务默认走完整 6 段状态机。
4. `benchmark_autonomous` 模式下，用户给出完整要求后，不再被反复追问，但系统仍必须产出需求文档、执行计划、验证收据与 cleanup 收据。
5. 每阶段结束都必须执行 phase cleanup，且 node cleanup 保持 attribution-safe 边界。
6. 必须新增治理 gate，证明该设计的稳定性、可用性和智能性，而不是只靠文档叙述。

## Why This Plan Exists

这次改造是为了把你长期工作中的强经验规则，转写成 `vibe` 的官方运行时契约：

- 先检查骨架，而不是盲目开始。
- 先访谈和冻需求，而不是边做边猜。
- 默认按 XL 任务流规划，而不是让用户自己组织复杂度。
- 计划驱动执行，而不是边想边做。
- 每阶段结束必须清理临时状态和受控 node 进程占用。
- 在 `benchmark` 场景中，AI 要能够接收完整要求后自主完成 analyze -> plan -> execute -> verify -> cleanup 的闭环。

现有仓库已经具备部分基础：

- [`protocols/think.md`](./../protocols/think.md) 已定义 planning / analysis 流程。
- [`protocols/team.md`](./../protocols/team.md) 已定义 XL native team orchestration。
- [`scripts/router/modules/21-capability-interview.ps1`](./../scripts/router/modules/21-capability-interview.ps1) 已存在 capability interview 基础。
- [`config/deep-discovery-policy.json`](./../config/deep-discovery-policy.json) 已存在 interview / intent contract 相关策略。
- [`config/confirm-ui-policy.json`](./../config/confirm-ui-policy.json) 已存在 unattended/confirm 行为规则。
- [`config/xl-operator-checkpoints.json`](./../config/xl-operator-checkpoints.json) 已存在 XL operator checkpoint。
- [`scripts/governance/phase-end-cleanup.ps1`](./../scripts/governance/phase-end-cleanup.ps1) 已存在阶段清洁入口。

问题在于，这些能力仍然是离散的，尚未被提升为统一主链。

## Non-Negotiable Principles

### Principle 1: `vibe` Is a Skill, Not a Prefix-Specific Command

`/vibe`、`$vibe`、以及 agent 内部 prompt 附加 `vibe`，都只是不同宿主里的 skill 调用语法，不是不同治理入口。

因此，设计对象必须是 **`vibe skill runtime contract`**，而不是某个平台命令前缀。

### Principle 2: One User-Facing Path Only

`vibe` 进入后，用户不再感知 M/L/XL 分岔。

用户只看到统一主路径：

`skeleton_check -> deep_interview -> requirement_doc -> xl_plan -> plan_execute -> phase_cleanup`

### Principle 3: M/L/XL Become Internal Execution Grades

`M/L/XL` 不删除，但只能用于内部执行编排：

- 决定执行阶段是单 agent、subagent 还是 native team
- 决定验证深度和并发规模
- 决定是否启用 wave contract

它们不再作为用户入口分叉。

### Principle 4: No Silent Degeneration

禁止以下退化：

- 直接跳过需求文档
- 直接跳过计划文档
- benchmark 模式中直接执行而不留下证据链
- 因为“任务看起来简单”而静默绕过主状态机
- 因为无人值守而跳过验证与 phase cleanup

### Principle 5: Cleanup Is Part of the Runtime, Not an Afterthought

`phase_cleanup` 必须是状态机中的正式阶段，而不是“执行完记得顺手跑一下”的附加动作。

### Principle 6: Intelligence Must Be Proved, Not Claimed

必须用 scenario receipts、intent completeness、plan traceability、phase receipts、cleanup receipts 与 verify gates，来证明系统的智能性，而不是靠 README 叙述。

## Governed Runtime vNext

## Runtime Modes

### Mode A: `interactive_governed`

默认模式。

特征：

- 允许在关键阶段向用户确认
- 访谈真实发生
- 需求文档由用户确认后冻结
- 计划文档可在确认后进入执行

### Mode B: `benchmark_autonomous`

闭环模式。

特征：

- 用户给出完整任务要求后，不再继续追问
- 系统内部完成推断版 interview
- 自动生成 intent contract、requirement doc、XL plan
- 自动执行、验证、收口
- 不减少治理步骤，只减少人与系统的交互轮次

## Fixed 6-Stage State Machine

### Stage 1: `skeleton_check`

**Purpose**

确定当前任务上下文、仓库骨架、运行时边界、现有文档与活跃计划是否完整。

**Inputs**

- user task
- mode
- repo root
- current branch / worktree state
- existing requirement / plan artifacts

**Outputs**

- `outputs/runtime/vibe-sessions/<run-id>/skeleton-receipt.json`

**Mandatory Checks**

- required directories exist
- runtime contract config exists
- whether active plan already exists
- whether repo is in a conflicting dirty state
- whether required protocol/config surfaces are available

**Failure Rules**

- missing governed skeleton -> initialize minimal governed skeleton
- conflicting active plan -> require explicit takeover or fork

### Stage 2: `deep_interview`

**Purpose**

把用户需求压缩成结构化意图契约，而不是直接进入执行。

**Inputs**

- task text
- skeleton receipt
- mode

**Outputs**

- `outputs/runtime/vibe-sessions/<run-id>/intent-contract.json`

**Required Fields**

- `goal`
- `deliverable`
- `constraints`
- `acceptance_criteria`
- `non_goals`
- `risk_tolerance`
- `autonomy_mode`
- `open_questions`
- `inference_notes`

**Behavior by Mode**

- `interactive_governed`: 开门见山、直击核心、细致深入访谈；必要时多轮，但必须收敛。
- `benchmark_autonomous`: 不向用户继续提问，改为内部推断访谈，并记录不确定项与默认决策依据。

### Stage 3: `requirement_doc`

**Purpose**

冻结唯一需求源。

**Inputs**

- intent contract

**Outputs**

- `docs/requirements/YYYY-MM-DD-<topic>.md`

**Rules**

- 后续计划只能引用 requirement doc，不得直接以聊天历史为唯一需求源。
- benchmark 模式必须写出“推断项”和“默认决策”。

### Stage 4: `xl_plan`

**Purpose**

默认按 XL 任务流做计划，形成统一执行蓝图。

**Inputs**

- requirement doc

**Outputs**

- `docs/plans/YYYY-MM-DD-<topic>-execution-plan.md`

**Required Sections**

- task classification
- internal execution grade
- wave / batch / phase breakdown
- ownership map
- verification commands
- rollback plan
- no-regression proof plan
- phase cleanup policy

### Stage 5: `plan_execute`

**Purpose**

基于计划推进实现，不允许脱离计划直接写代码。

**Inputs**

- execution plan
- mode

**Outputs**

- code / docs / configs / receipts

**Rules**

- internal grade controls execution topology
- XL/native team is preferred for parallelizable batches
- every spawned subagent prompt must end with `$vibe`
- each milestone must produce evidence and phase receipts

### Stage 6: `phase_cleanup`

**Purpose**

完成阶段收口，保持仓库与 runtime 整洁。

**Inputs**

- current phase result
- execution receipts

**Outputs**

- `outputs/runtime/vibe-sessions/<run-id>/cleanup-receipt.json`
- process audit / cleanup artifacts

**Required Actions**

- remove temp files generated by the phase
- refresh local excludes if needed
- run repo hygiene checks
- run report-safe node audit / cleanup
- freeze cleanup receipt

## Planned Repository Changes

## Layer 1: Protocol Layer

### Add

- `protocols/runtime.md`

### Modify

- `SKILL.md`
- `protocols/think.md`
- `protocols/do.md`
- `protocols/team.md`
- `protocols/retro.md`

### Target Effect

把当前“grade-first entry”重写为“governed-runtime-first entry”，并把 `M/L/XL` 降级为内部 execution grade。

## Layer 2: Config Layer

### Add

- `config/runtime-contract.json`
- `config/runtime-modes.json`
- `config/requirement-doc-policy.json`
- `config/plan-execution-policy.json`
- `config/phase-cleanup-policy.json`

### Modify

- `config/deep-discovery-policy.json`
- `config/confirm-ui-policy.json`
- `config/xl-operator-checkpoints.json`
- `config/vco-overlays.json` if needed for runtime exposure

### Target Effect

把 6 段状态机、双模式、文档契约、cleanup 契约全部 machine-readable 化。

## Layer 3: Runtime Script Layer

### Add

- `scripts/runtime/invoke-vibe-runtime.ps1`
- `scripts/runtime/Invoke-SkeletonCheck.ps1`
- `scripts/runtime/Invoke-DeepInterview.ps1`
- `scripts/runtime/Write-RequirementDoc.ps1`
- `scripts/runtime/Write-XlPlan.ps1`
- `scripts/runtime/Invoke-PlanExecute.ps1`
- `scripts/runtime/Invoke-PhaseCleanup.ps1`

### Modify

- `scripts/router/resolve-pack-route.ps1` only where necessary to hand off to governed runtime

### Target Effect

`vibe` 有一个统一 runtime dispatcher，router 不再直接承担全部运行时职责。

## Layer 4: Document / Template / Receipt Layer

### Add

- `docs/requirements/README.md`
- `templates/requirements/governed-requirement-template.md`
- `templates/plans/governed-execution-plan-template.md`
- `outputs/runtime/vibe-sessions/.gitkeep` if needed

### Target Effect

需求文档、计划文档、阶段收据都成为一等公民。

## Execution Program

## Batch 0: Plan Freeze and Entry Registration

**Objective**

把本计划冻结为官方入口之一，并让后续改造以此为唯一设计源。

**Actions**

1. Add this plan under `docs/plans/`
2. Update `docs/plans/README.md`
3. Record this as current entry in plan index

**Exit Criteria**

- plan file exists
- plans index updated

## Batch 1: Unified Runtime Contract

**Objective**

先重写入口语义，再动执行逻辑。

**Files**

- `SKILL.md`
- `protocols/runtime.md` (new)
- `protocols/think.md`
- `protocols/do.md`
- `protocols/team.md`

**Actions**

1. Add governed runtime protocol
2. Redefine `vibe` as governed runtime entry
3. Move grade-first behavior behind runtime contract
4. Document the two official modes

**Exit Criteria**

- `vibe` entry semantics are documented consistently
- 6-stage state machine is formalized
- M/L/XL are documented as internal grades only

## Batch 2: Machine-Readable Runtime Config

**Objective**

把主状态机、双模式和 mandatory artifacts 配置化。

**Files**

- `config/runtime-contract.json`
- `config/runtime-modes.json`
- `config/requirement-doc-policy.json`
- `config/plan-execution-policy.json`
- `config/phase-cleanup-policy.json`

**Actions**

1. Encode stage sequence
2. Encode stage inputs/outputs
3. Encode mode-specific question/confirm behavior
4. Encode required artifacts and failure fallbacks

**Exit Criteria**

- all runtime stages exist in config
- both modes exist in config
- mandatory artifacts are declared

## Batch 3: Deep Interview and Requirement Freeze

**Objective**

把 capability interview 升级为正式需求契约入口。

**Files**

- `scripts/router/modules/21-capability-interview.ps1`
- `config/deep-discovery-policy.json`
- `templates/requirements/governed-requirement-template.md`
- `docs/requirements/README.md`

**Actions**

1. Extend interview output to full intent contract
2. Add benchmark-mode inference behavior
3. Materialize requirement doc from intent contract
4. Define requirement doc as single source of task truth

**Exit Criteria**

- intent contract includes required fields
- requirement doc can be generated
- benchmark mode no longer requires live questioning

## Batch 4: XL Plan Generation

**Objective**

统一由 requirement doc 驱动 XL 计划生成。

**Files**

- `scripts/runtime/Write-XlPlan.ps1`
- `templates/plans/governed-execution-plan-template.md`
- `config/plan-execution-policy.json`
- related protocol updates

**Actions**

1. Generate plan from requirement doc
2. Enforce wave / batch / phase structure
3. Add verify commands, rollback rules, and cleanup stage requirements

**Exit Criteria**

- plan generated from requirement doc only
- plan contains wave / batch / phase / verify / rollback / cleanup sections

## Batch 5: Plan-Driven Execution

**Objective**

让执行变成由计划驱动的受控 runtime。

**Files**

- `scripts/runtime/Invoke-PlanExecute.ps1`
- execution-related configs / protocol touchpoints

**Actions**

1. Internalize grade selection
2. Run native XL team when needed
3. Inject `$vibe` suffix into spawned agent prompts
4. Produce phase receipts for each completed stage

**Exit Criteria**

- subagent prompts are governed and suffixed with `$vibe`
- execution advances only after planned checkpoints
- phase receipts exist

## Batch 6: Mandatory Phase Cleanup

**Objective**

把 cleanup 收口从 operator habit 升级为 runtime contract。

**Files**

- `scripts/runtime/Invoke-PhaseCleanup.ps1`
- `config/phase-cleanup-policy.json`
- existing governance / cleanup integration files

**Actions**

1. Wrap `phase-end-cleanup.ps1`
2. Require cleanup after each phase
3. Emit cleanup receipt
4. Keep node cleanup attribution-safe

**Exit Criteria**

- cleanup is mandatory in runtime contract
- cleanup receipt exists
- node audit / cleanup remains safe and reportable

## Batch 7: Governed Runtime Verification

**Objective**

用 gate 与场景证明该设计已经真正落地。

**Files**

- `scripts/verify/vibe-governed-runtime-gate.ps1`
- `scripts/verify/vibe-governed-runtime-scenarios.ps1`
- `tests/` fixtures if needed

**Actions**

1. Add contract gate
2. Add scenario-driven behavior gate
3. Cover both modes and fallback behavior
4. Ensure no-regression against current router/runtime obligations

**Exit Criteria**

- governed runtime contract gate PASS
- governed runtime scenarios PASS
- no-regression evidence exists

## Verification Matrix

## Stability

Must prove:

- stage order is fixed
- missing prerequisite artifacts block forward progress
- cleanup always runs after phase completion
- benchmark and interactive modes never cross wires

## Usability

Must prove:

- `vibe` behavior is host-syntax neutral
- requirement doc and execution plan are readable and predictable
- benchmark mode can accept one-shot task descriptions and close the loop

## Intelligence

Must prove:

- interview extracts actionable deliverables and constraints
- benchmark mode can infer missing but necessary execution defaults
- internal grade selection matches task complexity
- plan structure is traceable back to requirement doc

## No Regression

Must prove:

- existing router behavior is not silently broken
- current confirm/unattended capabilities still work inside the governed runtime
- cleanup and node hygiene protections remain intact

## Proof Artifacts

Expected new proof surface:

- `outputs/runtime/vibe-sessions/<run-id>/skeleton-receipt.json`
- `outputs/runtime/vibe-sessions/<run-id>/intent-contract.json`
- `docs/requirements/YYYY-MM-DD-<topic>.md`
- `docs/plans/YYYY-MM-DD-<topic>-execution-plan.md`
- `outputs/runtime/vibe-sessions/<run-id>/phase-*.json`
- `outputs/runtime/vibe-sessions/<run-id>/cleanup-receipt.json`
- `outputs/verify/vibe-governed-runtime-gate.json`
- `outputs/verify/vibe-governed-runtime-scenarios.json`

## Rollback Strategy

If any batch destabilizes existing routing or cleanup safety:

1. keep governed runtime docs/config but disable runtime takeover
2. fall back to existing `vibe` entry behavior
3. preserve new proof artifacts for diagnosis
4. do not ship silent partial takeover

## Phase-End Hygiene Rules

At the end of every execution batch:

1. run bounded verification for the batch
2. run phase-end cleanup
3. audit managed node ownership
4. keep node cleanup report-only unless policy and ownership explicitly allow apply
5. delete temp files produced during the batch
6. keep repo clean enough for the next batch

## Immediate Next Steps

1. Complete Batch 0 by registering this plan as current entry.
2. Execute Batch 1 and Batch 2 first; do not jump straight into runtime execution scripts without freezing the contract.
3. After each batch, run verification plus phase cleanup before advancing.


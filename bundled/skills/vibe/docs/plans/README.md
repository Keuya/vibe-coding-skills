# Plans

- Up: [`../README.md`](../README.md)

## What Lives Here

`docs/plans/` stores dated execution plans, staged programs, triage notes, and closure reports.

This directory is responsible for:

- current execution entry points
- historical planning context
- staged implementation order

This directory is **not** the canonical home for:

- live runtime truth
- the sole proof contract
- the single current-state summary

Those surfaces live under [`../status/README.md`](../status/README.md).

## Start Here

### Current Entry

- [`2026-03-15-vco-governed-runtime-contract-plan.md`](./2026-03-15-vco-governed-runtime-contract-plan.md): `vibe` 统一治理入口正式方案；将 `vibe` 收敛为固定 6 段状态机、双运行模式、内部等级编排与 mandatory phase cleanup 的官方运行时契约。
- [`2026-03-14-single-core-dual-adaptation-dual-proof-dual-release-plan.md`](./2026-03-14-single-core-dual-adaptation-dual-proof-dual-release-plan.md): 单核心、双适配、双证明、双发行正式方案；聚焦平台差异去分叉、installed runtime 行为证明、统一版本线与双发行治理。
- [`2026-03-13-linux-full-authoritative-migration-plan.md`](./2026-03-13-linux-full-authoritative-migration-plan.md): Linux 满血权威迁移专项计划；聚焦去 PowerShell 中心化、runtime-neutral authoritative core、Linux 证明链闭环，以及严格零退化推广边界。
- [`2026-03-13-next-platform-promotion-execution-plan.md`](./2026-03-13-next-platform-promotion-execution-plan.md): 下一阶段平台推进执行文档；聚焦 Windows 权威路径、Linux 强路径、Linux 降级路径与平台 promotion 证据闭环。
- [`2026-03-13-universal-vibeskills-execution-program.md`](./2026-03-13-universal-vibeskills-execution-program.md): 通用化主执行程序；定义官方运行时冻结、host/platform capability contract 与 no-regression proof 主骨架。
- [`2026-03-13-universal-vibeskills-no-regression-migration-plan.md`](./2026-03-13-universal-vibeskills-no-regression-migration-plan.md): 通用化迁移总规划；解释为何可以做通用化，但必须以前提不退化。
- [`2026-03-13-distribution-governance-plan.md`](./2026-03-13-distribution-governance-plan.md): 分发治理总计划；覆盖 upstream provenance、license/notice、repo-local retention 和 proof-bundle 分发边界。
- [`2026-03-13-post-upstream-governance-repo-convergence-plan.md`](./2026-03-13-post-upstream-governance-repo-convergence-plan.md): 上游治理后的仓库收敛计划；聚焦 repo cleanliness、fixture/output 闭合和导航收敛。
- [`2026-03-13-post-upstream-governance-developer-entry-plan.md`](./2026-03-13-post-upstream-governance-developer-entry-plan.md): 上游治理后的开发者入口计划；聚焦 CONTRIBUTING、禁改区、proof 预期和 canary contributor journey。
- [`2026-03-13-one-shot-full-setup-closure-plan.md`](./2026-03-13-one-shot-full-setup-closure-plan.md): 一键安装闭环计划；聚焦 bootstrap、doctor、MCP profile 物化和冷启动入口收敛。
- [`2026-03-11-vco-repo-simplification-remediation-plan.md`](./2026-03-11-vco-repo-simplification-remediation-plan.md): repo 收敛与治理简化主计划。

### Supporting Current

- [`2026-03-11-node-zombie-guardian-implementation-plan.md`](./2026-03-11-node-zombie-guardian-implementation-plan.md): 阶段卫生与僵尸 Node 防误杀实现计划。
- [`2026-03-08-repo-cleanliness-batch2-4-triage.md`](./2026-03-08-repo-cleanliness-batch2-4-triage.md): cleanup-first 剩余工作拆分、stop rules 与批次顺序。

### Runtime / Proof Handoff

- [`../status/README.md`](../status/README.md): 当前运行态、proof 入口与 operator handoff。
- [`../status/current-state.md`](../status/current-state.md): 当前 live 状态摘要。
- [`../status/non-regression-proof-bundle.md`](../status/non-regression-proof-bundle.md): 最小 proof contract。

## Background Entry

- [`2026-03-09-batch0-9-closure-report.md`](./2026-03-09-batch0-9-closure-report.md): Batch 0-9 收口报告与剩余 governed backlog。
- [`2026-03-08-repo-full-cleanup-master-plan.md`](./2026-03-08-repo-full-cleanup-master-plan.md): 仓库全域 cleanup umbrella plan。
- [`2026-03-07-repo-cleanliness-next-wave-plan.md`](./2026-03-07-repo-cleanliness-next-wave-plan.md): 早期 repo cleanliness 下一波规划。
- [`2026-03-07-nested-bundled-root-parity-governance-plan.md`](./2026-03-07-nested-bundled-root-parity-governance-plan.md): nested bundled root parity 与 version topology 历史治理计划。

## Wave Horizons

- [`2026-03-08-vco-wave121-140-operatorized-value-extraction-plan.md`](./2026-03-08-vco-wave121-140-operatorized-value-extraction-plan.md): 较新的 continuation horizon。
- [`2026-03-08-vco-wave101-120-value-extraction-plan.md`](./2026-03-08-vco-wave101-120-value-extraction-plan.md): 上一阶段 continuation horizon。
- Historical wave material kept for context:
  - `2026-03-07-vco-wave83-100-execution-plan.md`
  - `2026-03-07-vco-wave83-100-execution-status.md`
  - `2026-03-07-vco-wave64-82-execution-plan.md`
  - `2026-03-07-vco-wave40-63-execution-plan.md`
  - `2026-03-07-vco-deep-value-extraction-drift-closure-plan.md`
  - `2026-03-07-vco-full-spectrum-integration-plan.md`

## Design Spikes

- [`2026-03-04-gpt52-llm-acceleration-design.md`](./2026-03-04-gpt52-llm-acceleration-design.md)
- [`2026-03-04-turbomax-vector-context-design.md`](./2026-03-04-turbomax-vector-context-design.md)

## Full Chronological Index

| Date | Type | File | Focus |
| --- | --- | --- | --- |
| 2026-03-15 | runtime contract plan | [2026-03-15-vco-governed-runtime-contract-plan.md](./2026-03-15-vco-governed-runtime-contract-plan.md) | `vibe` 统一治理入口、固定 6 段状态机、interactive / benchmark 双模式、内部等级编排与 mandatory phase cleanup |
| 2026-03-14 | architecture plan | [2026-03-14-single-core-dual-adaptation-dual-proof-dual-release-plan.md](./2026-03-14-single-core-dual-adaptation-dual-proof-dual-release-plan.md) | 单核心、双适配、双证明、双发行；统一 root、shell、replay、release contract，避免平台双分叉 |
| 2026-03-13 | migration plan | [2026-03-13-linux-full-authoritative-migration-plan.md](./2026-03-13-linux-full-authoritative-migration-plan.md) | Linux 满血权威迁移、runtime-neutral authoritative core、PowerShell-only gate 去中心化、零退化 promotion proof |
| 2026-03-13 | execution plan | [2026-03-13-next-platform-promotion-execution-plan.md](./2026-03-13-next-platform-promotion-execution-plan.md) | Windows 权威路径重证明、Linux + pwsh 强路径 proof、Linux 无 pwsh 降级诚实化、平台 promotion 证据闭环 |
| 2026-03-13 | execution plan | [2026-03-13-universal-vibeskills-execution-program.md](./2026-03-13-universal-vibeskills-execution-program.md) | 通用化主执行程序、官方运行时冻结、host/platform capability contract、no-regression 骨架 |
| 2026-03-13 | migration plan | [2026-03-13-universal-vibeskills-no-regression-migration-plan.md](./2026-03-13-universal-vibeskills-no-regression-migration-plan.md) | 不退化通用化迁移总规划与阶段边界 |
| 2026-03-13 | governance plan | [2026-03-13-distribution-governance-plan.md](./2026-03-13-distribution-governance-plan.md) | upstream 联合清点、repo-local retention、license/provenance 闭环与分发治理 |
| 2026-03-13 | convergence plan | [2026-03-13-post-upstream-governance-repo-convergence-plan.md](./2026-03-13-post-upstream-governance-repo-convergence-plan.md) | 上游治理后的仓库收敛、fixture/output 闭合、proof-bundle 稳定性 |
| 2026-03-13 | developer-entry plan | [2026-03-13-post-upstream-governance-developer-entry-plan.md](./2026-03-13-post-upstream-governance-developer-entry-plan.md) | 开发者入口、CONTRIBUTING、贡献分区、PR 模板与 developer-entry gate |
| 2026-03-13 | setup plan | [2026-03-13-one-shot-full-setup-closure-plan.md](./2026-03-13-one-shot-full-setup-closure-plan.md) | 一键安装、bootstrap、doctor、MCP profile 物化与冷启动入口 |
| 2026-03-11 | remediation plan | [2026-03-11-vco-repo-simplification-remediation-plan.md](./2026-03-11-vco-repo-simplification-remediation-plan.md) | repo 收敛与治理简化主计划 |
| 2026-03-11 | implementation plan | [2026-03-11-node-zombie-guardian-implementation-plan.md](./2026-03-11-node-zombie-guardian-implementation-plan.md) | 僵尸 Node 识别、安全清理边界与阶段卫生 |
| 2026-03-09 | closure report | [2026-03-09-batch0-9-closure-report.md](./2026-03-09-batch0-9-closure-report.md) | Batch 0-9 执行收口、gate snapshot、剩余 governed backlog |
| 2026-03-08 | master plan | [2026-03-08-repo-full-cleanup-master-plan.md](./2026-03-08-repo-full-cleanup-master-plan.md) | full-repo cleanup umbrella plan |
| 2026-03-08 | planning horizon | [2026-03-08-vco-wave121-140-operatorized-value-extraction-plan.md](./2026-03-08-vco-wave121-140-operatorized-value-extraction-plan.md) | post-W120 operatorized continuation horizon |
| 2026-03-08 | planning horizon | [2026-03-08-vco-wave101-120-value-extraction-plan.md](./2026-03-08-vco-wave101-120-value-extraction-plan.md) | value extraction continuation |
| 2026-03-08 | triage | [2026-03-08-repo-cleanliness-batch2-4-triage.md](./2026-03-08-repo-cleanliness-batch2-4-triage.md) | cleanup-first 剩余工作与 stop rules |
| 2026-03-07 | status | [2026-03-07-vco-wave83-100-execution-status.md](./2026-03-07-vco-wave83-100-execution-status.md) | Wave83-100 状态收敛 |
| 2026-03-07 | execution plan | [2026-03-07-vco-wave83-100-execution-plan.md](./2026-03-07-vco-wave83-100-execution-plan.md) | Wave83-100 bounded planning horizon |
| 2026-03-07 | execution plan | [2026-03-07-vco-wave64-82-execution-plan.md](./2026-03-07-vco-wave64-82-execution-plan.md) | Wave64-82 promotion / release-train program |
| 2026-03-07 | execution plan | [2026-03-07-vco-wave40-63-execution-plan.md](./2026-03-07-vco-wave40-63-execution-plan.md) | Wave40-63 reliability / packaging hardening |
| 2026-03-07 | governance plan | [2026-03-07-vco-full-spectrum-integration-plan.md](./2026-03-07-vco-full-spectrum-integration-plan.md) | 全谱系 integration 路线 |
| 2026-03-07 | governance plan | [2026-03-07-vco-deep-value-extraction-drift-closure-plan.md](./2026-03-07-vco-deep-value-extraction-drift-closure-plan.md) | 剩余价值萃取与 drift closure |
| 2026-03-07 | cleanup plan | [2026-03-07-repo-cleanliness-next-wave-plan.md](./2026-03-07-repo-cleanliness-next-wave-plan.md) | repo cleanliness next wave |
| 2026-03-07 | packaging plan | [2026-03-07-nested-bundled-root-parity-governance-plan.md](./2026-03-07-nested-bundled-root-parity-governance-plan.md) | nested parity / version topology |
| 2026-03-04 | design spike | [2026-03-04-gpt52-llm-acceleration-design.md](./2026-03-04-gpt52-llm-acceleration-design.md) | GPT-5.2 / LLM acceleration overlay |
| 2026-03-04 | design spike | [2026-03-04-turbomax-vector-context-design.md](./2026-03-04-turbomax-vector-context-design.md) | vector-first context design |

## Rules

- `Current Entry` only keeps a small set of currently active plans.
- Runtime truth and proof contracts stay under `docs/status/`, not duplicated indefinitely in `docs/plans/`.
- Historical wave plans and closure reports move to context sections instead of competing with active entry points.
- Any new `docs/plans/*.md` file must update this index in the same change.

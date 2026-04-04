# VCO Status

`docs/status/` 只保留当前状态入口、proof contract 和必要 guardrails，不承担长期历史堆积。

## Start Here

- live summary: [`current-state.md`](current-state.md)
- current closure receipt: [`closure-audit.md`](closure-audit.md)
- architecture sign-off proof: [`../proof/2026-04-04-owner-consumer-consistency-proof.md`](../proof/2026-04-04-owner-consumer-consistency-proof.md)
- batch order / next hop: [`roadmap.md`](roadmap.md)
- minimum proof contract: [`non-regression-proof-bundle.md`](non-regression-proof-bundle.md)
- transitional blockers: [`path-dependency-census.md`](path-dependency-census.md)

## Cross-Layer Handoff

- plans and historical batch context: [`../plans/README.md`](../plans/README.md)
- operator scripts: [`../../scripts/README.md`](../../scripts/README.md)
- verify run order: [`../../scripts/verify/gate-family-index.md`](../../scripts/verify/gate-family-index.md)
- long-term promotion contracts: [`../universalization/platform-promotion-criteria.md`](../universalization/platform-promotion-criteria.md)

## Reading Boundary

- [`current-state.md`](current-state.md)、[`closure-audit.md`](closure-audit.md)、[`../proof/2026-04-04-owner-consumer-consistency-proof.md`](../proof/2026-04-04-owner-consumer-consistency-proof.md) 是当前优先阅读面。
- 历史 dated baseline / ledger / closure 文档已经从 live surface 中移除；当前目录只保留仍有运行态消费者的最小集合。

## Rules

- [`current-state.md`](current-state.md) 是唯一 live summary；数值和 PASS/FAIL 必须回指 `outputs/verify/**`、回归结果或当前 closure receipt。
- [`closure-audit.md`](closure-audit.md) 是当前批次回执，不维护平行摘要。
- 结构性 sign-off 证明统一收束到 [`../proof/2026-04-04-owner-consumer-consistency-proof.md`](../proof/2026-04-04-owner-consumer-consistency-proof.md)。
- 历史状态正文不再长期保留在 repo 内。

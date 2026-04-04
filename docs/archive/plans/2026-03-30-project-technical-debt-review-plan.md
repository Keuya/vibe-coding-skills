# 项目问题与技术债审查执行计划

**日期**: 2026-03-30
**需求文档**: [2026-03-30-project-technical-debt-review.md](../requirements/2026-03-30-project-technical-debt-review.md)
**Internal Grade**: `L`

## Wave Structure

### Wave 1: Freeze Audit Scope

- 固定审查基线到最新 `main`。
- 确认 `vibe` 审查范围：发布治理、镜像拓扑、runtime 契约、outputs 边界、历史 release surface、脚本维护性。
- 采集需求/计划/报告所需的最小上下文。

### Wave 2: Evidence Collection

- 检查 `config/version-governance.json` 与 `scripts/governance/release-cut.ps1` / `sync-bundled-vibe.ps1`。
- 检查 `scripts/runtime/Freeze-RuntimeInputPacket.ps1`、`Invoke-PlanExecute.ps1`、`VibeExecution.Common.ps1` 的字段传播形态。
- 检查 `docs/releases/*`、`.gitignore`、`config/outputs-boundary-policy.json`、`scripts/router/*` 与相关测试覆盖线索。

### Wave 3: Review Consolidation

- 按严重度排序形成 findings。
- 区分“当前风险”与“承认中的迁移债”。
- 写入审查报告并更新 `docs/requirements/README.md` 与 `docs/plans/README.md` 索引。

## Ownership Boundaries

- Root governed lane: 负责 requirement / plan / report 的唯一冻结面，以及最终 findings 排序与措辞。
- Repo source evidence: 仅作为审查输入，不做产品代码行为修改。

## Verification Commands

- `git status --short --branch`
- `git log --oneline --decorate -n 5`
- `rg -n "TODO|FIXME|placeholder|stub" docs/releases scripts/governance scripts/runtime`
- `git ls-files outputs`
- `wc -l scripts/runtime/Invoke-PlanExecute.ps1 scripts/runtime/Freeze-RuntimeInputPacket.ps1 scripts/router/resolve-pack-route.ps1 scripts/router/legacy/resolve-pack-route.legacy.ps1 scripts/governance/release-cut.ps1 scripts/governance/sync-bundled-vibe.ps1`

## Delivery Acceptance Plan

- 报告必须覆盖至少五个以上 distinct findings。
- 每个 finding 必须能追溯到仓库中的具体路径与证据片段。
- 若某项被归类为“技术债而非现行 bug”，报告中要显式写明原因。

## Completion Language Rules

- 只有 requirement / plan / report 三个文档都落地，且最终 findings 已按严重度写清，才允许说“本轮审查完成”。
- 如果未跑全量 gate，需要明确写成“未执行”。

## Rollback Rules

- 本轮仅新增审查文档与索引更新；若文档结构与仓库现有索引规则冲突，则回退到最小文档集合，不触碰产品逻辑。

## Cleanup Expectations

- 不生成无关运行产物。
- 不修改 `outputs/`、`dist/`、`scripts/runtime/` 等产品面文件。

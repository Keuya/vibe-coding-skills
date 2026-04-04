# 2026-04-01 Status History Index Closure Plan

## Internal Grade

`M`

## Objective

在不动历史文件路径的情况下，为 `docs/status/` 增加一个明确的历史索引，把目录阅读体验从“混合目录”收口为“active surfaces + archival-by-default index”。

## Target Files

- `docs/status/README.md`
- `docs/status/history-index.md`

## Execution Steps

1. 按角色把现有 dated status 文件分成 baselines、closure reports、evidence ledgers、specialized proof snapshots。
2. 新建 `history-index.md`，集中承接这些历史材料。
3. 更新 `docs/status/README.md`，把历史文件入口统一指向新的索引页。
4. 跑 targeted diff/format 检查，确认未破坏现有路径稳定性。

## Verification

```bash
git -C /home/lqf/table/table5/runtime-sandboxes/vibe-skills-main-audit diff --check -- \
  docs/status/README.md \
  docs/status/history-index.md \
  docs/requirements/2026-04-01-vibe-status-history-index-closure.md \
  docs/plans/2026-04-01-vibe-status-history-index-closure-plan.md
```

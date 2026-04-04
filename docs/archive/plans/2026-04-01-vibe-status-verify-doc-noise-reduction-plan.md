# 2026-04-01 Status And Verify Doc Noise Reduction Plan

## Internal Grade

`M`

## Objective

降低 `status` 和 `verify` 两个入口面的阅读噪音，让操作者先看到当前有效入口，再按需深钻。

## Target Files

- `docs/status/README.md`
- `scripts/verify/README.md`

## Execution Steps

1. 为 `status` 首页补清晰边界，明确 dated baselines / closure reports 默认按归档阅读。
2. 重写 `scripts/verify/README.md`，只保留常用运行顺序、最常见 quick start 和跨层跳转。
3. 把 family 级展开、专题 gate、长命令清单交回 `gate-family-index.md` 和相关专题文档。
4. 运行 targeted diff/grep 检查，确认格式与叙事都稳定。

## Verification

```bash
git -C /home/lqf/table/table5/runtime-sandboxes/vibe-skills-main-audit diff --check -- \
  docs/status/README.md \
  scripts/verify/README.md \
  docs/requirements/2026-04-01-vibe-status-verify-doc-noise-reduction.md \
  docs/plans/2026-04-01-vibe-status-verify-doc-noise-reduction-plan.md
```

```bash
rg -n "mirror-only drift|canonical to bundled packaging parity|镜像同步|bundled 镜像同步策略" \
  /home/lqf/table/table5/runtime-sandboxes/vibe-skills-main-audit/docs \
  /home/lqf/table/table5/runtime-sandboxes/vibe-skills-main-audit/scripts \
  --glob '!**/docs/releases/**' \
  --glob '!**/docs/requirements/**'
```

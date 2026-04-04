# 2026-04-01 Historical Doc Noise Reduction Plan

## Internal Grade

`M`。单代理串行文档收口，无需并行实现。

## Objective

把高频索引页压缩成短入口文档，降低维护者扫描成本，同时避免继续传播 mirror-first 历史叙事。

## Target Files

- `docs/README.md`
- `docs/status/README.md`
- `docs/plans/README.md`
- `config/index.md`
- `scripts/README.md`
- `scripts/verify/gate-family-index.md`
- `references/index.md`

## Execution Steps

1. 识别当前入口页中的重复导航、超长清单和过时表述。
2. 把每个入口页改成“用途 + Start Here + 边界 + 最小规则”的短结构。
3. 保留核心锚点，删去不必要的展开说明和长历史列表。
4. 运行文档级检查与 targeted grep，确认没有引入格式问题或重新扩大 mirror-first 叙事。

## Verification

```bash
git -C /home/lqf/table/table5/runtime-sandboxes/vibe-skills-main-audit diff --check -- \
  docs/README.md \
  docs/status/README.md \
  docs/plans/README.md \
  config/index.md \
  scripts/README.md \
  scripts/verify/gate-family-index.md \
  references/index.md
```

```bash
rg -n "canonical to bundled packaging parity|mirror-only drift|镜像同步|bundled 镜像同步策略" \
  /home/lqf/table/table5/runtime-sandboxes/vibe-skills-main-audit/docs \
  /home/lqf/table/table5/runtime-sandboxes/vibe-skills-main-audit/scripts \
  /home/lqf/table/table5/runtime-sandboxes/vibe-skills-main-audit/config \
  --glob '!**/docs/releases/**' \
  --glob '!**/docs/requirements/**'
```

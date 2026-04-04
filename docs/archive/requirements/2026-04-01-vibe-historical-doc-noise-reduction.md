# 2026-04-01 Historical Doc Noise Reduction

## Goal

继续在 tracked `bundled/skills/vibe` mirror 退役之后，压缩高频入口文档，减少重复导航、历史噪音和 mirror-first 叙事。

## In Scope

- 精简活跃入口页，只保留维护者和操作者真正需要的核心信息。
- 统一入口页对 canonical-only packaging / generated compatibility 的口径。
- 保留必要链接，但不再在索引页重复展开大段历史列表或解释。

## Out of Scope

- 大规模重写 dated reports、release notes、requirements 历史文档。
- 变更 runtime、install、verify、router 的执行逻辑。
- 删除仍被引用的历史材料。

## Constraints

- 改动必须低风险、以文档为主。
- 继续保留 legacy gate 名称，但不能让索引页误导维护者回到 mirror-first 维护模式。
- 优先压缩入口文档，而不是扩散到整仓历史材料。

## Acceptance Criteria

- `docs/README.md`、`docs/status/README.md`、`docs/plans/README.md`、`scripts/README.md`、`scripts/verify/gate-family-index.md`、`config/index.md`、`references/index.md` 等入口页明显更短、更易扫读。
- 入口页不再罗列过多 dated items，只保留当前常用入口和清晰边界。
- 文档语义与 canonical-only runtime contract 一致。

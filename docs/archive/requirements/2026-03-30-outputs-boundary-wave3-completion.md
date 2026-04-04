# Outputs Boundary Wave 3 Completion 实施需求

**日期**: 2026-03-30
**目标**: 在 routing-stability 与 retro safety 两批迁移已验证通过的前提下，完成 Wave 3 剩余 outputs family 的退役，把 tracked outputs 从 `15` 收敛到 `0`，并切换到严格零 tracked outputs 模式。

## Intent Contract

- Goal: 完成 `sample-run`、`smoke-temp`、`external-corpus` 三个剩余 family 的迁移收口。
- Deliverable:
  - `outputs-boundary-policy.json` 移除全部剩余 allowlisted sets。
  - 旧 `outputs/retro/compare/sample-run/`、`outputs/retro/compare/smoke-temp/`、`outputs/external-corpus/` tracked 文件全部退役。
  - `strict_requires_zero_tracked_outputs` 切换到 `true`。
  - migration characterization test 扩展覆盖所有已退役 family，并断言 tracked outputs 为 `0`。
- Constraints:
  - 不改变 `references/fixtures/**` 下现有 canonical fixture 内容。
  - 不改变 `migration-map.json` 的已存在镜像映射记录。
  - 不改变 verify/runtime 行为，只迁移 truth surface。
- Acceptance Criteria:
  - tracked outputs 计数从 `15` 下降到 `0`。
  - policy 中 `allowlisted_sets` 为空。
  - policy 中 `strict_requires_zero_tracked_outputs = true`。
  - 仓库内不再跟踪任何 `outputs/**` 历史 fixture 文件。
  - `references/fixtures/external-corpus/`、`references/fixtures/retro-compare/sample-run/`、`references/fixtures/retro-compare/smoke/` 仍存在并保持 canonical。
- Product Acceptance Criteria:
  - outputs boundary 完成从 legacy tracked outputs 到 fixture-only canonical surface 的迁移。
  - 后续 gate 可以在 strict 模式下要求仓库不再保留 tracked outputs。
- Manual Spot Checks:
  - 检查 `git ls-files outputs` 为空。
  - 检查 `references/fixtures/**` 对应 family 文件仍存在。
- Completion Language Policy:
  - 只能宣称“Wave 3 outputs boundary migration 完成”，不能外推为整个大项目完成。
- Delivery Truth Contract:
  - 必须有 fresh test/gate evidence，且 strict gate 通过。
- Non-goals:
  - 不进入 mirror topology reduction。
  - 不修改 `migration-map.json` 的历史记录。
  - 不改动 runtime contract / release operator 逻辑。
- Autonomy Mode: `interactive_governed`
- Inferred Assumptions:
  - 三个剩余 family 都没有脚本/测试消费旧路径，且 legacy outputs 与 fixture 内容一致，因此可以作为同一收官批次完成。

# Outputs Boundary Retro Safety Migration 实施需求

**日期**: 2026-03-30
**目标**: 作为 Wave 3 第二批迁移，把 `outputs/retro/compare/safety-gate/` 的 4 个 tracked legacy outputs 退役，只保留 `references/fixtures/retro-compare/safety-gate/` 作为 canonical fixture root。

## Intent Contract

- Goal: 用最小安全批次继续验证 outputs boundary migration 路径，收敛 retro compare family。
- Deliverable:
  - `outputs-boundary-policy.json` 不再把 `retro-compare-safety-baselines` 视为 tracked allowlisted output。
  - 旧 `outputs/retro/compare/safety-gate/` 4 个 tracked 文件从仓库 surface 移除。
  - migration characterization test 扩展覆盖 safety-gate family。
- Constraints:
  - 不改变 `references/fixtures/retro-compare/safety-gate/` 现有 fixture 内容。
  - 不改变 `migration-map.json` 的已存在镜像映射记录。
  - 不同时迁移 `sample-run`、`smoke-temp` 或 `external-corpus` family。
- Acceptance Criteria:
  - tracked outputs 计数从 `19` 下降到 `15`。
  - policy 不再包含 `retro-compare-safety-baselines` allowlisted set。
  - 仓库内不再跟踪 `outputs/retro/compare/safety-gate/` 下 4 个 legacy 文件。
  - fixture root 中对应 4 个文件仍存在且保持 canonical。
- Product Acceptance Criteria:
  - outputs boundary 继续朝“fixture 为真源、generated output 不进入 tracked outputs”收敛。
  - 本批迁移不影响现有 verify/runtime 行为。
- Manual Spot Checks:
  - 检查仓库中不再有 tracked `outputs/retro/compare/safety-gate/*`。
  - 检查 `references/fixtures/retro-compare/safety-gate/` 4 个 fixture 文件仍存在。
- Completion Language Policy:
  - 只能宣称“retro safety outputs family 迁移完成”，不能外推为整个 Wave 3 完成。
- Delivery Truth Contract:
  - 必须有 fresh gate/test evidence。
- Non-goals:
  - 不迁移 `sample-run`。
  - 不迁移 `smoke-temp`。
  - 不迁移 `external-corpus`。
  - 不切换 `strict_requires_zero_tracked_outputs`。
- Autonomy Mode: `interactive_governed`
- Inferred Assumptions:
  - safety-gate family 是最安全的下一批对象，因为 fixture 已存在、内容与旧 tracked outputs 一致，且没有脚本/测试消费旧路径。

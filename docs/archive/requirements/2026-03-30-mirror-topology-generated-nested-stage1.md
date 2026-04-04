# Mirror Topology Generated Nested Stage 1 实施需求

**日期**: 2026-03-30
**目标**: 作为 Wave 4 第一阶段，把 `nested_bundled` 从默认常驻同步目标降为 generated compatibility target，同时保留“若存在则必须匹配”的非退化约束。

## Intent Contract

- Goal: 先把 nested mirror 的默认同步语义变成“存在则维护、缺失不主动创建”，再由 release/install-time 显式 materialize。
- Deliverable:
  - `config/version-governance.json` 为 `nested_bundled` 增加 generated compatibility 语义。
  - `sync-bundled-vibe.ps1` 默认不再为缺失的 nested target 创建目录，但在 nested 已存在时仍保持 parity。
  - `release-cut.ps1` 显式请求 materialize generated compatibility targets。
  - 新增 `tests/runtime_neutral/test_generated_nested_bundled.py`。
- Constraints:
  - 不删除 repo 内现有 nested tracked mirror。
  - 不修改 bundled mirror 作为长期 repo 内唯一必需 mirror 的地位。
  - 不改变 installed runtime freshness contract。
- Acceptance Criteria:
  - 当 nested target 缺失时，默认 `sync-bundled-vibe.ps1` 只同步 bundled，不创建 nested。
  - 当显式传入 generated-compatibility materialization 开关时，`sync-bundled-vibe.ps1` 可以创建并同步 nested。
  - `release-cut.ps1` preview/apply 流程继续成功。
  - 若 nested 已存在，default sync 仍保持其与 canonical/bundled 的 parity。
- Product Acceptance Criteria:
  - nested topology 从“长期 tracked parity target”开始收敛到“按需 compatibility target”。
  - 不引入 release/install/runtime 行为退化。
- Manual Spot Checks:
  - 在临时仓库中验证 default sync 不创建缺失 nested。
  - 在临时仓库中验证显式 materialize 开关可以创建 nested。
- Completion Language Policy:
  - 只能宣称“Wave 4 第一阶段 generated nested baseline 已落地”，不能宣称整个 mirror topology reduction 完成。
- Delivery Truth Contract:
  - 必须有新测试与 packaging/release 相关验证。
- Non-goals:
  - 不删除 repo 中现有 nested tracked payload。
  - 不做 manifest-driven packaging copy 全量重构。
  - 不变更 installed runtime target layout。
- Autonomy Mode: `interactive_governed`
- Inferred Assumptions:
  - 当前 repo 仍保留 nested tracked mirror，因此 default sync 必须继续维护“若存在则匹配”，否则会立刻引入 drift。

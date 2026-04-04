# Mirror Topology Optional Generated Nested 实施需求

**日期**: 2026-03-30
**目标**: 作为 Wave 4 第一阶段，把 `nested_bundled` 从 repo 内持续同步目标降级为 optional generated compatibility target，同时保留“存在时必须匹配”的兼容语义。

## Intent Contract

- Goal: 在不删除 repo 内 nested mirror 的前提下，先停止把它当作长期同步目标。
- Deliverable:
  - `version-governance.json` 的 `nested_bundled.sync_enabled` 切换到 `false`。
  - canonical / bundled / nested 三份 governance 配置保持一致。
  - 新增 characterization test，证明：
    - `sync-bundled-vibe.ps1 -Preview` 不再计划 materialize nested target；
    - `vibe-nested-bundled-parity-gate.ps1` 在 nested 缺席时仍可通过；
    - nested 若存在但不匹配，仍然失败。
- Constraints:
  - 不删除 repo 内 nested tracked mirror。
  - 不改变 `presence_policy = if_present_must_match`。
  - 不改 install-time runtime contract。
- Acceptance Criteria:
  - `nested_bundled` 不再属于持续 sync target。
  - 现有 parity / packaging gates 不退化。
  - 新 characterization test 通过。
- Product Acceptance Criteria:
  - nested compatibility 从“常驻同步镜像”开始收敛到“按需生成兼容面”。
  - 后续 release/install materialize 可以在不依赖 repo 常驻同步的前提下推进。
- Manual Spot Checks:
  - 检查 `config/version-governance.json` 与 bundled mirrors 的 `sync_enabled` 一致。
  - 检查 sync preview 中不再出现 `target_id = nested_bundled`。
- Completion Language Policy:
  - 只能宣称“Wave 4 第一阶段 optional generated nested 已落地”，不能宣称 nested mirror 已移除。
- Delivery Truth Contract:
  - 必须有 fresh test/gate evidence。
- Non-goals:
  - 不删除 nested tracked root。
  - 不修改 `presence_policy` 为新枚举。
  - 不修改 installed runtime freshness/coherence contract。
- Autonomy Mode: `interactive_governed`
- Inferred Assumptions:
  - helper/gate 已经支持 optional + if_present_must_match 语义，因此第一阶段只需要收敛 sync surface 和 characterization proof。

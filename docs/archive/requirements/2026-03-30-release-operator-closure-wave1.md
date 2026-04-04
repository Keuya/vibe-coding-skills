# Release Operator Closure Wave 1 需求

**日期**: 2026-03-30
**目标**: 在不改变现有发布语义、不弱化 install/runtime/packaging 行为的前提下，把 `scripts/governance/release-cut.ps1` 提升为覆盖当前主要 release surfaces 的 authoritative operator，并补齐对应的自动化验证。

## Intent Contract

- Goal: 完成 non-regression technical debt remediation plan 的 Wave 1。
- Deliverable:
  - `release-cut.ps1` 能自动更新 `docs/releases/README.md` 与 `dist/*/manifest.json` 的 release-facing truth surfaces。
  - 新增 release operator integration tests。
  - 新增 release notes 质量测试，阻止 `TODO` 和重复 major headings 进入合并面。
- Constraints:
  - 不重写发布流程整体架构。
  - 不修改 runtime/router 行为。
  - 不在本轮改变 mirror topology 或 outputs policy。
  - 不删除人工 release note 补充能力，但 operator 必须成为 authoritative path。
- Acceptance Criteria:
  - `release-cut.ps1 -Preview` 能显示新增的 release surface file actions。
  - `release-cut.ps1` apply 后会对齐 `docs/releases/README.md` 当前 release surface 与 recent release 列表中的当前版本项。
  - `release-cut.ps1` apply 后会对齐 `dist/*/manifest.json` 与 `dist/manifests/*.json` 的 release version/updated 字段。
  - 自动生成的 release note 不能再落成 `TODO` 模板。
  - 至少有一组自动化测试覆盖 operator 行为，且至少有一组测试覆盖 release notes 质量约束。
- Product Acceptance Criteria:
  - 发布动作与发布真相面更一致，减少手工补面。
  - 新增校验不会把历史 release notes 一次性全部判死，但会约束当前被 operator 触达的 release note。
- Manual Spot Checks:
  - 检查 preview receipt 中是否列出 release README 与 dist manifests。
  - 检查 apply 后 `docs/releases/README.md` 的 current release surface 和 recent release 首项是否一致。
  - 检查一个 lane manifest 与一个 public manifest 的 release 字段已对齐。
- Completion Language Policy:
  - 只有在相关测试和最小 gate 通过后，才允许说本波已完成。
- Delivery Truth Contract:
  - 本波只声称实现了 Wave 1 的 release operator closure。
  - 不把后续 runtime/output/mirror 波次的目标混入完成声明。
- Non-goals:
  - 不实现 runtime contract schema extraction。
  - 不迁移 tracked outputs。
  - 不收缩 nested mirror。
- Autonomy Mode: `interactive_governed`
- Inferred Assumptions:
  - `docs/releases/README.md` 的当前版本项应由 operator 自动保持一致。
  - 当前 `dist/*/manifest.json` 与 `dist/manifests/*.json` 的 release 字段是纯派生面，适合由 operator 自动更新。

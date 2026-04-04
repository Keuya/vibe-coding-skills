# 非退化技术债修复执行计划

**日期**: 2026-03-30
**需求文档**: [../requirements/2026-03-30-non-regression-technical-debt-remediation.md](../requirements/2026-03-30-non-regression-technical-debt-remediation.md)
**审查输入**: [2026-03-30-project-technical-debt-review-report.md](./2026-03-30-project-technical-debt-review-report.md)
**Internal Grade**: `XL`

## Strategy

本次修复不能按“哪里最乱先动哪里”执行，而要按“哪里最能降低后续改造风险”排序。

推荐总策略：

1. 先补 non-regression harness，再动结构。
2. 先修 release/operator truth surface，再缩镜像面。
3. 先收口 runtime contract 生成方式，再拆超大脚本。
4. 先迁移 outputs 到明确 fixture/canonical surface，再收紧 outputs policy。
5. 所有高风险路径都使用阶段迁移，而不是一次性切换。

## Priority Order

### Priority 0: Freeze Proof Before Refactor

这是所有后续修复的前提，不是可选项。

必须先补或强化以下 proof：

- `release-cut` 的端到端测试，至少覆盖：
  - release note 生成/禁止 TODO stub 的行为
  - `docs/releases/README.md` 当前 release surface 更新
  - `dist/*/manifest.json` 的 `source_release` 对齐
- runtime contract characterization tests，至少冻结：
  - runtime input packet
  - execution manifest
  - host adapter requested/effective id
- outputs boundary migration tests：
  - 旧 allowlist fixture
  - 新 fixture root
  - dual-read compatibility
- mirror topology proof：
  - canonical -> bundled
  - nested mirror presence/absence 两种模式
  - release/install-time generated nested compatibility

没有这些 proof，不要开始删除 nested mirror、不要开始收紧 outputs、不要开始抽 runtime schema。

## Wave Structure

### Wave 1: Release Surface Closure

**Why first**

`release-cut` 现在不是完整 operator，却被当成完整 operator 使用。这会让后续每一波重构都承担额外的 release truth 风险。

**Change set**

- 把 `release-cut.ps1` 升级为完整 release surface operator：
  - 更新 `config/version-governance.json`
  - 更新 maintenance markers
  - 更新 changelog / ledger
  - 更新 `docs/releases/README.md`
  - 更新 `dist/*/manifest.json`
  - 仅允许在 preview/apply 中生成“待填充 release note 草稿”，但禁止合并前保留 `TODO`
- 把 `vibe-dist-manifest-gate.ps1` 纳入正式 release-cut gate family
- 新增 release note quality checks：
  - no `TODO`
  - no duplicated top-level section titles
  - required sections present

**Migration mode**

- 先保留手工补面能力，但 operator 变成 authoritative path。
- 第一个版本只做“operator 自动补齐 + gate fail on mismatch”，不立即删除人工 fallback。

**Verification**

- 现有 gates：
  - `scripts/verify/vibe-version-consistency-gate.ps1`
  - `scripts/verify/vibe-version-packaging-gate.ps1`
  - `scripts/verify/vibe-dist-manifest-gate.ps1`
  - `scripts/verify/vibe-release-install-runtime-coherence-gate.ps1`
- 必须新增：
  - `tests/runtime_neutral/test_release_cut_operator.py`
  - `tests/runtime_neutral/test_release_notes_quality.py`

**Stop rules**

- 如果 release-cut 无法在 preview 中准确显示派生改动，就不进入 apply。
- 如果 operator 与当前手工发布面出现分歧，先修 operator，不做镜像/outputs 收敛。

### Wave 2: Runtime Contract Schema Extraction

**Why second**

release 面稳定后，最值得优先收口的是 runtime contract 手工映射，因为它影响后续 runtime / router / host adapter 的所有改造。

**Change set**

- 引入单一 contract builder/normalizer：
  - runtime input packet shared builder
  - execution manifest shared projection
  - host adapter shared projection
- 用 helper + schema 替换散落在多个脚本里的重复字段组装
- 把关键 contract 显式文档化：
  - required fields
  - optional compatibility fields
  - allowed deprecations

**Migration mode**

- 第一阶段使用 dual-write：
  - 新 helper 产出新结构
  - 旧字段名继续保留
  - tests 对两者同时校验
- 第二阶段才删除旧的散落复制逻辑

**Verification**

- 现有 tests：
  - `tests/runtime_neutral/test_multi_host_specialist_execution.py`
  - `tests/runtime_neutral/test_governed_runtime_bridge.py`
  - `tests/runtime_neutral/test_l_xl_native_execution_topology.py`
- 必须新增：
  - `tests/runtime_neutral/test_runtime_contract_schema.py`
  - packet/manifest golden snapshots

**Stop rules**

- 任何字段 rename 如果没有 compatibility alias，不允许落地。
- 任何 host adapter 相关字段如果不能同时通过 runtime packet 和 execution manifest 断言，不允许继续拆脚本。

### Wave 3: Outputs Boundary Migration

**Why third**

`outputs/` 债务是噪音源，但直接清理很危险，因为它和历史 fixture / baseline / gate 读取路径交织在一起。必须先迁移 truth source，再收紧 policy。

**Change set**

- 把 21 个 tracked outputs 分批迁移到 `references/fixtures/**`
- 更新 gates，让它们优先读取 `references/fixtures/**`
- 在过渡期保留 dual-read：
  - 优先读新路径
  - 旧路径存在时只作兼容，不再作为 canonical baseline
- 迁移完成后：
  - `expected_tracked_output_count` 递减到 0
  - `strict_requires_zero_tracked_outputs` 切到 `true`

**Migration mode**

- 一次只迁一个 family：
  - external-corpus
  - retro compare
  - verify routing stability
- 每迁完一个 family 就更新 gate 和 policy，不做大包迁移。

**Verification**

- 现有 gate：
  - `scripts/verify/vibe-output-artifact-boundary-gate.ps1`
- 必须新增：
  - `tests/runtime_neutral/test_outputs_boundary_migration.py`

**Stop rules**

- 旧路径删掉前，必须先证明所有消费方已读新路径。
- 任何一个 fixture family 迁移失败，都不继续减少 tracked count。

### Wave 4: Mirror Topology Reduction

**Why fourth**

镜像拓扑是最大结构债，但风险也最高。只有在 release operator 和 runtime/output 边界稳定后，才适合收镜像。

**Change set**

- 目标状态：
  - canonical root 仍是唯一真源
  - `bundled/skills/vibe` 保留为唯一长期 repo 内镜像
  - `nested_bundled` 从“长期 tracked mirror”降级为“install-time / release-time generated compatibility surface”
- `sync-bundled-vibe.ps1` 从“整目录复制”逐步收敛为“manifest-driven packaging copy”
- `config/version-governance.json` 中的 nested target 改成可生成 compatibility target，而不是长期 parity target

**Migration mode**

- 第一步：nested root 改成 optional generated target，但 gate 继续允许存在时必须匹配
- 第二步：release/install 流程负责 materialize nested compatibility
- 第三步：从 repo 常驻结构中移除 nested tracked mirror

**Verification**

- 现有 gates：
  - `scripts/verify/vibe-version-packaging-gate.ps1`
  - `scripts/verify/vibe-nested-bundled-parity-gate.ps1`
  - `scripts/verify/vibe-mirror-edit-hygiene-gate.ps1`
- 必须新增：
  - `tests/runtime_neutral/test_generated_nested_bundled.py`
  - release/install parity integration test

**Stop rules**

- 在 release/install-time 生成 nested compatibility 之前，不允许删除 repo 内 nested baseline。
- 如果 manifest-driven packaging 还没稳定，就不要同时改 mirror topology policy。

### Wave 5: Router / Runtime Large-File Refactor

**Why last**

大脚本拆分是高可见度工作，但不是最先该做的。没有前四波护栏，拆分只会把风险扩散。

**Change set**

- 对 `Invoke-PlanExecute.ps1`、`Freeze-RuntimeInputPacket.ps1` 做 helper extraction
- 对 router 做两段式收口：
  - 先继续保留 legacy contract baseline
  - 再逐步缩小 legacy surface 的活跃职责
- 不追求“一步删掉 legacy”，只追求“主路径越来越模块化、legacy 越来越只做 contract comparison”

**Migration mode**

- 每次只提一个 cohesive helper/module
- 每个 PR 只允许一个主维度变化：
  - contract extraction
  - routing module extraction
  - legacy surface retirement prep

**Verification**

- 现有 gates/tests：
  - `scripts/verify/vibe-router-contract-gate.ps1`
  - `tests/runtime_neutral/test_router_bridge.py`
  - `tests/runtime_neutral/test_governed_runtime_bridge.py`
- 必须新增：
  - helper-level unit tests
  - file-size / complexity advisory report

**Stop rules**

- 在 legacy contract 仍是 required baseline 时，不允许跳过 contract comparison 直接改核心 routing semantics。
- 如果拆分导致路由行为需要重新解释，就应作为独立 feature/change wave，而不是伪装成 maintenance。

### Wave 6: Historical Truth Surface Hardening

**Why last**

历史 release note 和历史计划文档问题是真相面质量债，但对当前运行风险最低，放在最后处理更合理。

**Change set**

- 建立历史文档质量 lint：
  - no `TODO`
  - no duplicate major headings
  - required release note skeleton
- 对最关键的历史版本做补齐，而不是全量美化

**Verification**

- release note lint
- targeted historical truth audit

## Recommended First 3 PRs

### PR 1: Release Operator Closure

只做以下事情：

- `release-cut.ps1` 补齐 release README + dist manifests
- 把 `vibe-dist-manifest-gate.ps1` 纳入 release-cut gate family
- 新增 release operator integration tests

**Why this first**

- 风险低于 mirror/runtime 重构
- 价值高
- 能减少后续每一波修改的发布面人工成本

### PR 2: Runtime Contract Builder Introduction

只做以下事情：

- 引入 shared contract helper
- 保留旧字段
- 新增 schema/golden tests

**Why second**

- 它是 runtime 与大脚本拆分的基础设施
- 可以在行为不变下显著降低后续 drift 风险

### PR 3: Outputs Family-by-Family Migration Start

只迁移一个 outputs family 到 `references/fixtures/**`，不同时处理 nested mirror。

**Why third**

- 能验证迁移机制是否可靠
- 不会和更高风险的镜像拓扑变更互相缠绕

## Ownership Boundaries

- Root governed lane:
  - 决定整体顺序
  - 冻结 requirement / plan
  - 决定每波 stop/go
- Release lane:
  - 负责 `release-cut`、release notes、dist manifests
- Runtime lane:
  - 负责 contract helper 与 schema consolidation
- Packaging lane:
  - 负责 mirror topology 和 packaging manifest
- Cleanliness lane:
  - 负责 outputs migration 和 policy tightening

## Verification Commands

### Current reusable verification

- `git diff --check`
- `pytest -q tests/runtime_neutral/test_governed_runtime_bridge.py tests/runtime_neutral/test_multi_host_specialist_execution.py tests/runtime_neutral/test_installed_runtime_scripts.py tests/runtime_neutral/test_coherence_gate.py`
- `pwsh -NoProfile -File scripts/verify/vibe-version-consistency-gate.ps1`
- `pwsh -NoProfile -File scripts/verify/vibe-version-packaging-gate.ps1`
- `pwsh -NoProfile -File scripts/verify/vibe-dist-manifest-gate.ps1`
- `pwsh -NoProfile -File scripts/verify/vibe-release-install-runtime-coherence-gate.ps1`
- `pwsh -NoProfile -File scripts/verify/vibe-output-artifact-boundary-gate.ps1`
- `pwsh -NoProfile -File scripts/verify/vibe-nested-bundled-parity-gate.ps1`
- `pwsh -NoProfile -File scripts/verify/vibe-router-contract-gate.ps1`

### Required new verification before structural waves

- `pytest -q tests/runtime_neutral/test_release_cut_operator.py`
- `pytest -q tests/runtime_neutral/test_release_notes_quality.py`
- `pytest -q tests/runtime_neutral/test_runtime_contract_schema.py`
- `pytest -q tests/runtime_neutral/test_outputs_boundary_migration.py`
- `pytest -q tests/runtime_neutral/test_generated_nested_bundled.py`

## Delivery Acceptance Plan

本规划被接受的标准不是“看起来完整”，而是满足以下逻辑：

1. 最大风险项没有被提前执行。
2. 每波都能独立 merge/release，不依赖一次性大切换。
3. 每个结构收敛动作前，都有 proof strengthening wave。
4. 能清楚回答“如果某波失败，在哪个边界停下来且不影响当前功能”。

## Completion Language Rules

- 当前只允许说“修复路线已规划完成”。
- 在任何一波未实际执行前，都不允许说“技术债已开始被修复”。

## Rollback Rules

- 每波必须可单独回滚，不能把多个结构债捆绑在同一 PR。
- 对 release/runtime/packaging 的重构必须保留 compatibility window，直到新旧路径都被证明稳定。
- 如果某波新增 gate 仍未稳定，则只允许停留在 dual-read/dual-write 状态，不允许删除旧路径。

## Cleanup Expectations

- 本轮只产出 requirement / plan 文档与索引更新。
- 不修改产品逻辑。
- 不生成新的 runtime outputs。

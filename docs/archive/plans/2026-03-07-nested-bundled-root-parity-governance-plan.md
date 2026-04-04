# 2026-03-07 Nested Bundled Root Parity & Version Governance Plan

- Up: [../README.md](../README.md)
- Index: [README.md](README.md)

## 1. 目标

本规划聚焦两个结果：

1. 为 `nested bundled root` 建立专门的 parity gate，消灭“旧脚本副本可被误执行但未被门禁覆盖”的治理盲区。
2. 把当前 `canonical -> bundled` 的版本治理，升级为面向整个镜像拓扑（mirror topology）的统一治理体系，减少版本漂移、镜像漂移、发布口径漂移与重复 cut 歧义。

## 2. 当前问题定义

### 2.1 已确认的事实

- `config/version-governance.json` 目前只显式声明：
  - `source_of_truth.canonical_root = .`
  - `source_of_truth.bundled_root = bundled/skills/vibe`
- `scripts/governance/sync-bundled-vibe.ps1` 内部会额外推导并同步：
  - `bundled/skills/vibe/bundled/skills/vibe`
- `scripts/verify/vibe-version-packaging-gate.ps1` 只校验 `canonical_root <-> bundled_root`。
- `docs/version-packaging-governance.md` 只把 repo root、bundled mirror、installed runtime copy 作为一级治理对象，没有把 nested bundled root 纳入正式契约。

### 2.2 风险结果

这意味着当前系统存在“脚本知道 nested root，治理合同不知道 nested root，release gate 也不检查 nested root”的结构性不一致。只要有人误跑旧副本、历史 bundled 副本残留、或 nested root 被局部修改，现有门禁可能仍然通过。

## 3. 根因分析

| 根因 | 表现 | 后果 |
|---|---|---|
| 关键镜像目标被脚本硬编码，而非配置声明 | sync 能同步 nested root，但 config 与 docs 没有把它声明为治理对象 | 工具行为与治理合同分离 |
| 可执行副本未全部纳入 gate | packaging gate 只校验 primary bundled root | 旧副本漂移不能被及时阻断 |
| 镜像治理仍是“单镜像思维” | 只有 canonical 与 bundled 的一对一校验 | 不能表达一主多镜像、可选镜像、条件镜像 |
| release cut 语义未完全制度化 | 同版本重复 cut、ledger/release note/changelog 一致性约束不完整 | 发布审计解释成本高 |
| 漂移识别规则不够严格 | bundled/nested mirror 的独立改动没有被显式定义为异常 | 容易形成“镜像即分叉” |

## 4. 治理设计原则

### 4.1 单一真源

- repo root (`.`) 是唯一 canonical source。
- `bundled/skills/vibe` 与任何 nested bundled root 都是派生镜像，不是人工维护源。
- 任何直接发生在 mirror root 的手工修改，默认都应被视为 drift，而不是正常开发行为。

### 4.2 所有可执行副本都必须可审计

只要某个目录内的脚本/配置/协议文件可能被人误执行，它就必须：

- 被配置层显式声明；
- 被 sync 层显式处理；
- 被 gate 层显式验证；
- 被 release 层纳入阻断条件。

### 4.3 镜像拓扑必须配置化

不允许在脚本内部继续隐式推导关键 mirror target。镜像路径、角色、是否必需、是否允许缺失、是否参与 gate，都必须进入机器可读配置。

### 4.4 发布是管线，不是人工拼装

release cut 的本质应是：

1. 写版本；
2. 同步全部镜像；
3. 运行全部治理 gates；
4. 记录 ledger / changelog / release note；
5. 只有全部通过时才形成可交付版本。

### 4.5 漂移优先判定

当发现 mirror-only diff 时，默认结论应为“派生镜像漂移”，而不是“这是另一个合法维护面”。

## 5. 目标拓扑模型

建议把版本治理从当前的 `source_of_truth` 二元结构，升级为显式的 mirror topology。

### 5.1 目标角色

| Target ID | 路径 | 角色 | 是否必需 | 预期策略 |
|---|---|---|---|---|
| `canonical` | `.` | 唯一真源 | 是 | 不参与 sync，被所有镜像引用 |
| `bundled` | `bundled/skills/vibe` | 主镜像 / 发布镜像 | 是 | 必须与 canonical 保持 full parity |
| `nested_bundled` | `bundled/skills/vibe/bundled/skills/vibe` | 次镜像 / 历史兼容执行面 | 条件必需 | 若存在则必须与 canonical 和 bundled 一致 |
| `installed_runtime` | `${TARGET_ROOT}/skills/vibe` | 安装态运行副本 | 外部态 | 不纳入 repo parity，但保留 install-time force-copy 保护 |

### 5.2 推荐的 presence policy

对 `nested_bundled` 推荐采用：

- `presence_policy = if_present_must_match`

含义是：

- 如果 nested root 不存在，gate 可通过；
- 如果 nested root 存在，则必须满足完整 parity；
- 一旦团队确认 nested root 是长期保留的兼容层，再升级为 `required`。

这样可以先收口漂移，再逐步硬化，不会因为历史副本尚未完全清理而一次性打断所有流程。

## 6. 配置合同升级方案

建议在 `config/version-governance.json` 内新增一个面向镜像拓扑的结构，保留现有字段做兼容过渡。

### 6.1 建议新增字段

```json
{
  "mirror_topology": {
    "targets": [
      {
        "id": "canonical",
        "path": ".",
        "role": "canonical",
        "required": true,
        "sync_enabled": false
      },
      {
        "id": "bundled",
        "path": "bundled/skills/vibe",
        "role": "mirror",
        "required": true,
        "sync_enabled": true,
        "parity_policy": "full"
      },
      {
        "id": "nested_bundled",
        "path": "bundled/skills/vibe/bundled/skills/vibe",
        "role": "mirror",
        "required": false,
        "presence_policy": "if_present_must_match",
        "sync_enabled": true,
        "parity_policy": "full"
      }
    ]
  }
}
```

### 6.2 配置层规则

- 现有 `source_of_truth.canonical_root` 与 `source_of_truth.bundled_root` 可以暂时保留，用于兼容旧脚本。
- 所有新脚本优先读取 `mirror_topology.targets`。
- 当所有脚本都完成迁移后，再决定是否逐步废弃旧字段。

## 7. 专门 parity gate 设计

### 7.1 新 gate 名称

新增：

- `scripts/verify/vibe-nested-bundled-parity-gate.ps1`

### 7.2 该 gate 的职责

1. 从 `config/version-governance.json` 读取 `nested_bundled` 目标，而不是脚本内硬编码路径。
2. 根据 `presence_policy` 判断 nested root 的缺失是否允许。
3. 若 nested root 存在，则执行以下校验：
   - mirrored files 是否齐全；
   - mirrored directories 是否齐全；
   - nested-only 文件是否全部在 allowlist；
   - canonical 与 nested 的文件 hash parity；
   - bundled 与 nested 的文件 hash parity；
   - 关键版本标记是否一致（例如 `SKILL.md`、`references/changelog.md` 头部、ledger 最新版本）。
4. 产出标准化 artifacts，写入：
   - `outputs/verify/vibe-nested-bundled-parity-gate.json`
   - `outputs/verify/vibe-nested-bundled-parity-gate.md`

### 7.3 判定等级

| 失败类型 | 说明 | 建议级别 |
|---|---|---|
| `missing_target` | 配置要求存在，但 nested root 缺失 | blocking |
| `unexpected_extra` | nested root 出现未声明额外文件 | blocking |
| `content_drift` | nested 与 canonical/bundled hash 不一致 | blocking |
| `version_marker_drift` | nested 版本标记落后 | blocking |
| `policy_mismatch` | gate 读取到的 topology 配置与旧字段冲突 | blocking |

### 7.4 为什么不能只扩展原 packaging gate

虽然也可以把 nested root 直接塞进 `vibe-version-packaging-gate.ps1`，但建议单独设 gate，原因有三点：

1. 这是一类“历史兼容执行面”问题，不应和主 bundled packaging 逻辑完全混在一起；
2. 单独 artifacts 更利于 CI 与 drift 审计；
3. 未来若 nested root 被移除或升级为 required，独立 gate 更容易切换策略。

## 8. Sync 脚本治理升级

### 8.1 当前问题

`sync-bundled-vibe.ps1` 当前通过脚本变量硬编码推导 nested root，这会导致：

- 实际行为与 config contract 分离；
- 新增 mirror target 时必须继续改脚本；
- 无法统一表达“某镜像允许不存在”“某镜像暂时 advisory”等策略。

### 8.2 升级目标

把 `sync-bundled-vibe.ps1` 改成 topology-driven：

- 遍历 `mirror_topology.targets`；
- 对所有 `sync_enabled = true` 的 mirror，从 canonical 直接同步；
- 不再从 bundled 推导 nested，也不再在脚本内写死镜像路径；
- `-PruneBundledExtras` 升级为对所有 mirror target 生效。

### 8.3 关键约束

- 所有 mirror 必须从 canonical 直接复制，而不是 mirror -> mirror 级联复制；
- 这样即便 bundled 已经脏了，nested 也不会被继续“传染”。

## 9. Release 与版本治理规则

### 9.1 版本变更入口统一

建议明文规定：

- 版本号与更新日期，只允许通过 `scripts/governance/release-cut.ps1` 变更；
- 不允许手工编辑 `config/version-governance.json` 中的 `release.version` / `release.updated` 作为常规流程；
- 若确需人工修复，必须把修复动作记录到 changelog 与 progress 文档。

### 9.2 release-cut 幂等语义必须制度化

当前重复运行同版本 cut 会追加 ledger，但不更新已有 release note，容易造成账本与说明分叉。推荐改成二选一：

#### 方案 A：默认禁止重复 cut（推荐）

- 同一 `version` 只能 cut 一次；
- 若需要重新发布，必须 bump patch 版本；
- 好处是审计口径最清晰。

#### 方案 B：显式 `-AmendRelease`

- 普通模式禁止同版本重复 cut；
- 只有显式传入 `-AmendRelease` 才允许同版本重切；
- 且必须同步更新 release note 的 `Commit(base)` 与 ledger 最新记录。

推荐采用 **方案 B**，因为它既保留修复空间，也把歧义控制在显式参数内。

### 9.3 发布阻断链

release-cut 的 `-RunGates` 建议升级为至少包含：

1. `vibe-version-consistency-gate.ps1`
2. `vibe-version-packaging-gate.ps1`
3. `vibe-nested-bundled-parity-gate.ps1`
4. `vibe-config-parity-gate.ps1`

后续再逐步增加：

5. `vibe-release-note-coherence-gate.ps1`（新）
6. `vibe-ledger-coverage-gate.ps1`（新）
7. `vibe-mirror-edit-hygiene-gate.ps1`（新）

## 10. 项目级版本控制与漂移治理规范

### 10.1 开发规范

- 日常开发只能改 canonical root。
- `bundled/skills/vibe/**` 与 nested bundled root 一律视为派生物。
- PR 中若出现 mirror-only diff，默认判为异常，除非该 PR 明确包含同步脚本输出并附带对应 gate 结果。

### 10.2 提交流程规范

建议采用以下提交序列：

1. 修改 canonical；
2. 运行 `sync-bundled-vibe.ps1 -PruneBundledExtras`；
3. 运行 parity / consistency / config gates；
4. 再提交 mirror 结果；
5. 由 CI 复跑 gates。

### 10.3 CI 规范

建议把治理校验拆成三级：

#### Level 1: PR 必跑

- `vibe-version-consistency-gate.ps1`
- `vibe-version-packaging-gate.ps1`
- `vibe-nested-bundled-parity-gate.ps1`
- `vibe-config-parity-gate.ps1`

#### Level 2: Release 必跑

- 包含 Level 1 全部；
- 再加 release note / ledger coherence gates。

#### Level 3: Nightly 审计

- 对 repo 中全部 mirror target 生成 drift 报告；
- 输出 `outputs/verify/nightly-mirror-audit.*`；
- 用于发现“没有触发 release，但镜像悄悄变脏”的问题。

### 10.4 所有权规范

建议把以下文件纳入明确的治理 owner：

- `config/version-governance.json`
- `scripts/governance/release-cut.ps1`
- `scripts/governance/sync-bundled-vibe.ps1`
- `scripts/verify/vibe-version-packaging-gate.ps1`
- `scripts/verify/vibe-nested-bundled-parity-gate.ps1`
- `docs/version-packaging-governance.md`

目的不是加流程负担，而是保证治理链条由固定责任人维护，避免“有人改 sync、没人改 gate”。

## 11. 建议的实施顺序（P0 / P1 / P2）

### P0：立即收口（必须做）

1. 在 `config/version-governance.json` 中显式声明 nested bundled target。
2. 新增 `vibe-nested-bundled-parity-gate.ps1`。
3. 让 `release-cut.ps1 -RunGates` 接入新 gate。
4. 更新 `docs/version-packaging-governance.md` 与 `scripts/verify/README.md`。

### P1：结构硬化（建议紧随其后）

5. 把 `sync-bundled-vibe.ps1` 改为 topology-driven。
6. 增加 `vibe-mirror-edit-hygiene-gate.ps1`：识别“只改 mirror 不改 canonical”的脏修改。
7. 增加 `vibe-release-note-coherence-gate.ps1`：校验 release note / ledger / git head 一致性。
8. 把 `normalized_json_ignore_keys` 从全局规则升级为按路径或按文件类型的精细规则。

### P2：运维级治理（中期增强）

9. 增加 `vibe-ledger-coverage-gate.ps1`：检查 ledger 与 changelog 覆盖关系。
10. 引入 nightly drift audit。
11. 为治理文件建立 CODEOWNERS / reviewer 责任矩阵。
12. 评估是否最终移除 nested bundled root，或保留但强制 required。

## 12. 成功判据

当以下条件同时成立时，说明本轮治理收口成功：

1. nested bundled root 不再是脚本隐式行为，而是 config 合同中的一级对象；
2. release-cut 会在 nested parity 失败时明确阻断；
3. sync、gate、docs 三层对 mirror topology 的定义一致；
4. mirror-only drift 能被 PR 或 release 过程稳定识别；
5. 同版本重复 release 的语义被明确约束，不再出现 ledger / release note 解释冲突。

## 13. 推荐的最终治理结论

本次不建议只做一个“散点补丁式”的 nested 校验，而应把它提升为 **mirror topology governance** 的第一项落地：

- 先显式声明所有镜像目标；
- 再给每个可执行镜像一个对等 gate；
- 再把 release-cut 变成统一阻断入口；
- 最后逐步补齐 release coherence、mirror edit hygiene、nightly audit 等强化机制。

这样不仅能解决这次的 nested bundled root 漂移问题，也能把整个项目的版本控制与派生镜像管理从“脚本约定”升级为“制度化治理”。
## 14. 执行上下文漂移治理（必须纳入本次方案）

子代理补充审计确认：本次 nested bundled root 风险的最高优先级根因，不只是“存在第二份镜像”，而是 **治理脚本按自身物理位置推导 repoRoot，而 scripts 又被镜像进 bundled 与 nested**。

### 14.1 风险机制

当前 `sync-bundled-vibe.ps1` 与 `vibe-version-packaging-gate.ps1` 都采用“以 `$PSScriptRoot/../..` 推导 repoRoot”的模式。只要这些脚本从 `bundled/skills/vibe/scripts/...` 或 `bundled/skills/vibe/bundled/skills/vibe/scripts/...` 被执行，脚本眼中的：

- `repoRoot`
- `canonical_root = .`
- `bundled_root = bundled/skills/vibe`

就会全部重新解释。

最危险的情况是：

- 在 bundled 副本内执行 gate；
- 此时脚本会把 `bundled/skills/vibe` 视为 repo root；
- 进而把 `bundled/skills/vibe/bundled/skills/vibe` 视为 bundled root；
- 最终形成 bundled ↔ nested 的“闭环自洽”校验，而不再校验最外层 canonical ↔ bundled。

这会产生一种**假通过**：实际仓库根已经漂移，但 gate 仍然 PASS，因为它在错误的执行上下文里验证了错误的对象。

### 14.2 对 nested parity gate 的新增硬性要求

因此，新的 `vibe-nested-bundled-parity-gate.ps1` 不能只做文件 hash 对比，还必须增加 **执行上下文断言**：

1. 当前执行上下文必须能锁定到最外层仓库根；
2. 若脚本被从 bundled 或 nested 副本路径直接执行，默认 FAIL；
3. 输出明确提示：当前执行的是 mirror 副本，不是 canonical repo 的治理脚本；
4. 校验 `canonical_root` 与 `bundled_root` 的解析结果必须落到预期的 outer canonical / outer bundled，而不是 bundled ↔ nested 闭环。

### 14.3 对 config 的补充建议

建议在 `config/version-governance.json` 中再增加两类字段：

- `packaging.execution_context_policy`
  - `require_outer_git_root = true`
  - `fail_if_repo_root_is_bundled = true`
- `packaging.top_level_structure_policy`
  - `allowed_top_level_extras = []`
  - `prune_top_level_extras = true`

目的有两个：

- 把“必须从 outer canonical 执行治理脚本”写成机器可读规则；
- 把 `bundled_root` 顶层出现的额外 `bundled/` 递归结构，纳入显式治理而不是放任其成为系统外残留。

### 14.4 对 sync / packaging gate 的联动要求

本轮规划应把以下改动视为同一治理闭环，而不是彼此独立的小修补：

1. `sync-bundled-vibe.ps1` 不再用硬编码推导 nested root；
2. `vibe-version-packaging-gate.ps1` 增加 outer-root 锁定逻辑；
3. `vibe-nested-bundled-parity-gate.ps1` 覆盖执行上下文、最大嵌套深度、canonical/bundled/nested 三方 parity；
4. release-cut 统一串联上述门禁。

只有这样，才能真正防止“跑到旧脚本副本”导致的伪校验通过。

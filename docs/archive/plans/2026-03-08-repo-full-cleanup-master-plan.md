# Repo Full Cleanup Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 把 `vco-skills-codex` 从“可运行但高漂移/高噪声/高认知负担”的状态，收口为一个对 AI 与人类都可快速理解、可安全维护、可稳定发布、可持续扩展的整洁仓库。

**Architecture:** 本计划采用 `canonical-first + plane-governance + cleanup-before-expansion` 路线：先冻结并解释脏区，再按 canonical / mirror / runtime / reference / archive 五个平面分域清扫，最后用 parity/freshness/gate/README/index 把结构与运行时一起收口。它不是一次性“大搬家”，而是先建立信息架构与治理边界，再做归档、规范化、镜像收敛与长期保洁自动化。

**Tech Stack:** Git, PowerShell gates, Markdown governance docs, JSON policy/config manifests, bundled mirror sync pipeline, runtime freshness / parity gates.

---

## Status

- **Target repo:** `_ext/vco-skills-codex`
- **Plan role:** 这是 2026-03-08 起的全仓清扫总纲；它吸收并上位管理此前的局部清扫文档，而不是替代历史记录。
- **Upstream inputs:**
  - `docs/plans/2026-03-07-repo-cleanliness-next-wave-plan.md`
  - `docs/plans/2026-03-08-repo-cleanliness-batch2-4-triage.md`
  - `docs/docs-information-architecture.md`
  - `references/reference-asset-taxonomy.md`
  - `references/mirror-topology.md`

## Scope Boundary

- `D:\table\new_ai_table` 当前是 **workspace-of-workspaces**，不是单一 git repo；它包含多个独立仓库、镜像、scratch 与 runtime 目录。
- 本计划的**直接治理对象**是 VCO canonical repo：`_ext/vco-skills-codex`。
- 根工作区层面的目录重构（例如统一 `projects/` / `third_party/` / `artifacts/` / `.cache/`）应在 canonical repo 清扫收口后，单独立项为 **workspace hygiene plan**，避免把“仓库治理”和“工作区搬迁”混成一件事。
## Objective

本轮不是“删文件求干净”，而是同时完成四件事：

1. **仓库干净**：`git status --short` 可归零，或至少每一条脏项都能被归类为受控工作集。
2. **结构清晰**：任何人和 AI 进入仓库后，都能立刻区分 canonical、mirror、runtime、reference、archive、workspace metadata。
3. **漂移可控**：不再出现“改错平面 / 跑错脚本副本 / 把运行态产物当真源”的问题。
4. **后续可持续**：清扫完成后仍能靠 SOP、README、index、gate 维持整洁，而不是靠一次人工突击。

## Audit Snapshot

### Repo-wide dirty snapshot

| Metric | Count | Meaning |
| --- | ---: | --- |
| Total dirty paths | 888 | 当前总脏项 |
| Modified tracked | 119 | 已跟踪文件被改动 |
| Untracked | 769 | 新文件未纳入版本控制 |
| Top dirty prefix `bundled/` | 594 | 镜像扩散最严重 |
| Top dirty prefix `docs/` | 92 | 文档面新增较多 |
| Top dirty prefix `scripts/` | 90 | 脚本面新增较多 |
| Top dirty prefix `config/` | 52 | 机器治理资产持续新增 |
| Top dirty prefix `references/` | 52 | 支撑资产平面持续新增 |

### Plane split snapshot

| Plane | Total | Modified | Untracked | Interpretation |
| --- | ---: | ---: | ---: | --- |
| `canonical` | 294 | 38 | 256 | 真源本体仍有大量未收口资产 |
| `mirror:bundled` | 292 | 36 | 256 | canonical 新增内容已扩散进 bundled |
| `mirror:nested` | 302 | 45 | 257 | nested mirror 继续放大漂移与认知负担 |

### Canonical untracked concentration

| Prefix | Count |
| --- | ---: |
| `scripts/` | 83 |
| `docs/` | 80 |
| `references/` | 47 |
| `config/` | 46 |

### Structural interpretation

- 问题不是单点脏文件，而是 **canonical 未收口 → sync 扩散 → bundled/nested 同步复制脏项** 的平面级污染。
- 运行态产物主要在 `outputs/`、`.tmp/`、`.serena/`，它们应继续 `ignore`，不应与 canonical workset 混淆。
- 目前最需要治理的不是“功能代码”，而是 **信息架构、工作区边界、镜像纪律、文档入口、脚本家族目录、编码规范（BOM / EOL）**。

## Cleanup Domain Model

| Domain | Scope | Role | Editing Rule |
| --- | --- | --- | --- |
| Canonical Source | `config/`, `scripts/`, `docs/`, `protocols/`, `references/`, root files | 唯一真源 | **允许编辑** |
| Mirrors | `bundled/skills/vibe/**`, `bundled/skills/vibe/bundled/skills/vibe/**` | 打包/兼容镜像 | **禁止手改，只能 sync** |
| Runtime Artifacts | `outputs/`, `.tmp/`, `.serena/` | 运行证据、缓存、临时产物 | **默认不入 git** |
| Reference Library | `references/**` | 合同、矩阵、目录、scorecard、overlay 参考资产 | 允许编辑，但必须纳入 index |
| Archive Layer | 历史 report/audit/draft/batch docs | 保留历史语义 | 不和 governance spine 混堆 |
| Workspace Metadata | `.internal/`, tool-local state | 本地工具状态 | 不应进入公共契约 |

## End State Definition

### Clean enough

满足以下条件即可认为“可恢复开发节奏”：

- canonical 非镜像工作集没有未知 `??`；
- `outputs/`, `.tmp/`, `.serena/` 不再进入 `git status`；
- parity / packaging / runtime freshness gates 继续全绿；
- `docs/`, `references/`, `scripts/verify/`, `scripts/governance/`, `scripts/common/` 至少有可导航入口；
- 不再发生“手改 mirror”或“从 mirror root 执行治理脚本”。

### Fully clean

满足以下条件才算“全仓清扫完成”：

- `git -C _ext/vco-skills-codex status --short` 为空；
- canonical / bundled / nested 的 package scope 全量可由 sync 再生产；
- `.gitattributes` 与 BOM/EOL gate 生效，文本资产不再产生结构性换行噪声；
- 文档、reference、脚本、config 形成稳定导航骨架；
- runtime artifact 边界、安装 SOP、freshness gate、execution-context lock 均已成文并已验证；
- 新人/AI 能通过少量入口文档完成 repo 定位，而不需要“猜哪里才是真源”。

## Guiding Principles

1. **Canonical first**：所有治理与内容修改先落 canonical，再通过 sync 进入 mirror。
2. **No mirror authorship**：mirror 是派生物，不是维护面。
3. **Cleanup before renames**：先补目录契约、README、index，再做大范围移动/重命名。
4. **Runtime stays runtime**：运行证据可以存在，但必须与长期资产分层。
5. **Index before scale**：任何新 family 新增前，先有索引与入口说明。
6. **No hidden ownership**：每一类资产都要有“属于哪个平面、由谁维护、如何验证”。
7. **BOM/EOL are governance issues**：编码与换行不是小问题，而是解析与 parity 的上游风险。
8. **One batch, one closure**：每批只解决一个主矛盾，并给出明确 exit criteria。

## Stop Rules

- 在 canonical workset 未清理前，**不允许**继续大规模扩张 wave backlog。
- 在 mirror parity 规则未满足前，**不允许**手工修 mirror 目录。
- 在 README/index 未补齐前，**不做**大规模 rename/move。
- 在 `.gitattributes` / BOM / EOL 策略未明确前，**不做**大范围文本再生成。
- 在 runtime / archive / reference 未分层前，**不把**时间绑定材料提升为长期治理正文。

## Execution Backlog

### Batch 0 — Freeze, Inventory, and Classification

**Objective:** 建立唯一可信的清扫盘点，冻结“什么是 canonical backlog、什么是 mirror 扩散、什么是 runtime 噪声”。

**Primary scope:**
- `git status --porcelain`
- `git ls-files --others --exclude-standard`
- `git clean -ndX`
- plane-level 分类台账

**Actions:**
- 生成 repo cleanliness inventory（按 canonical / bundled / nested / runtime / archive 分类）。
- 为 top prefixes 建立解释：为什么脏、该 track/ignore/archive/sync 哪一类。
- 固化当前 snapshot，作为后续 batch 的对照基线。

**Deliverables:**
- `outputs/governance/` 或等价 ignore 目录中的 inventory 报告
- 每个 plane 的 dirty ledger

**Exit criteria:**
- 每条脏项都能落入固定分类；
- 不再使用“感觉上很乱”描述仓库状态。

### Batch 1 — Runtime Noise Separation

**Objective:** 把运行态噪声从 canonical 认知面彻底剥离。

**Primary scope:**
- `outputs/`
- `.tmp/`
- `.serena/`
- 其它工具缓存目录

**Actions:**
- 复查 `.gitignore` 与 runtime artifact boundary。
- 明确哪些 `outputs/` 是允许长期保留的证据目录，哪些是可周期清理的缓存/临时结果。
- 把 runtime 目录的 install / usage / cleanup SOP 文档化。

**Deliverables:**
- runtime artifact allowlist / denylist
- cleanup SOP / retention policy

**Exit criteria:**
- runtime 目录不再出现在 `git status`；
- `outputs/` 的存在不再被误判为“仓库不干净”。

### Batch 2 — Encoding, BOM, and EOL Normalization

**Objective:** 清掉结构性文本噪声，避免 frontmatter / parser / parity 再次受损。

**Primary scope:**
- `.md`, `.json`, `.yml`, `.yaml`, `.ps1`, `.sh`
- `.gitattributes`
- BOM / EOL quick gates

**Actions:**
- 引入统一 `.gitattributes`，对关键文本资产固定 `eol=lf`（按仓库实际策略微调）。
- 明确 no-BOM contract，尤其覆盖 `SKILL.md` / manifest / gate config / scripts。
- 为 BOM / EOL 添加快速 gate 或将其并入现有 verify family。

**Deliverables:**
- `.gitattributes`
- 文本编码 / 换行策略文档
- BOM/EOL 验证脚本或 gate 文档入口

**Exit criteria:**
- 不再因 BOM 导致 frontmatter 失效；
- mirror diff 不再被换行噪声污染。

### Batch 3 — Canonical Workset Triage

**Objective:** 先把 canonical 的 256 条 untracked 变成受控资产，再考虑 mirror。

**Primary scope:**
- `config/`
- `scripts/`
- `docs/`
- `references/`

**Actions:**
- 逐目录执行三分法：`must-track` / `must-ignore` / `must-archive`。
- 优先处理 `config/` 与 `scripts/verify/`，因为它们决定后续治理能否自动化。
- 对 root files (`README.md`, `SKILL.md`, `install.*`, `check.*`) 的变更做真源确认。

**Deliverables:**
- canonical workset closure 清单
- 目录级 admission rule

**Exit criteria:**
- canonical 非 mirror 域不再存在未知 `??`；
- 每个未跟踪项都有明确去向。

### Batch 4 — Docs and References Information Architecture

**Objective:** 让人类与 AI 都能用固定入口理解仓库，而不是靠文件名搜索生存。

**Primary scope:**
- `docs/README.md`
- `docs/plans/README.md`
- `references/index.md`
- taxonomy / archive-layer / governance spine

**Actions:**
- 按 `docs/docs-information-architecture.md` 稳定 root `docs/` 与 `docs/plans/` 的边界。
- 按 `references/reference-asset-taxonomy.md` 把 registry / matrix / contract / ledger / overlay 梳成导航骨架。
- 明确哪些历史报告留在 archive layer，哪些升级为长期治理正文。

**Deliverables:**
- 更新后的 docs/readme/index spine
- archive-layer policy

**Exit criteria:**
- `docs/` 与 `references/` 不再是“平铺文本森林”；
- 新人/AI 可以从 README/index 进入主要资产面。

### Batch 5 — Scripts and Config Governance Spine

**Objective:** 把脚本与配置从“文件集合”升级成“家族化 operator surface”。

**Primary scope:**
- `scripts/verify/`
- `scripts/governance/`
- `scripts/common/`
- `config/`

**Actions:**
- 为 verify/governance/common/config 建立 family 级 README 与目录契约。
- 补清“哪些脚本是 gate、哪些是 operator、哪些是 common primitive、哪些是 batch sidecar”。
- 对 manifest/board/contract/config family 做命名与入口统一。

**Deliverables:**
- `scripts/verify/README.md`
- `scripts/governance/README.md`
- `scripts/common/README.md`
- `config` family index / contract map

**Exit criteria:**
- 不再需要只靠文件名记忆脚本用途；
- AI 能从目录级入口理解调用关系与执行顺序。

### Batch 6 — Mirror Convergence and Drift Closure

**Objective:** 在 canonical clean 后，再把 bundled 与 nested bundled 一次性收敛回正确状态。

**Primary scope:**
- `bundled/skills/vibe/**`
- `bundled/skills/vibe/bundled/skills/vibe/**`
- sync / parity / packaging / runtime coherence gates

**Actions:**
- 禁止 mirror 手改，所有差异回 canonical 解决。
- 执行标准 sync，必要时 prune mirror extras。
- 复跑 parity / packaging / release-install/runtime coherence gates。

**Deliverables:**
- 干净的 bundled/nested mirror
- mirror closure evidence

**Exit criteria:**
- mirror 的差异只能由 canonical sync 解释；
- nested bundled 不再成为“旧副本误执行”的风险面。

### Batch 7 — Archive, Historical Debt, and Third-Party Compliance

**Objective:** 把历史材料与合规材料从“杂物堆”变成稳定边界。

**Primary scope:**
- `docs/` archive-layer 文档
- `third_party/`, `NOTICE`, `THIRD_PARTY_LICENSES.md`
- 历史 backup / report / audit / draft 资产

**Actions:**
- 给历史报告建立 archive 层导航，而不是混在 governance spine。
- 清理不再需要的 backup 命名模式；保留必须长期留档的 evidence。
- 审查 third-party license 清单与镜像策略的一致性。

**Deliverables:**
- archive policy
- third-party compliance map

**Exit criteria:**
- 历史材料可找、可解释、不可误认成真源；
- 第三方边界清楚，不与 canonical 资产混淆。

### Batch 8 — Repository Entry Spine for Humans and AI

**Objective:** 把“如何理解这个仓库”收口成稳定入口，而不是把理解负担推给搜索。

**Primary scope:**
- root `README.md`
- root `SKILL.md`
- package entry docs
- install/check/runtime SOP

**Actions:**
- 在 root README 中强调 plane model、core entry path、how-to-run / how-not-to-edit。
- 在 `SKILL.md` 与治理文档之间建立清晰反向锚点。
- 明确“第一次进入仓库应该看什么”的 AI/human reading path。

**Deliverables:**
- repo entry map
- installation / runtime / governance reading path

**Exit criteria:**
- 新人和 AI 都能在极少上下文里完成 repo 定位；
- 入口文档与实际目录职责一致。

### Batch 9 — Recurring Hygiene Automation

**Objective:** 把清扫成果从“一次性工程”变成持续治理机制。

**Primary scope:**
- preflight scripts
- verify gates
- release/install SOP
- freshness/parity automation

**Actions:**
- 把 cleanliness inventory、BOM/EOL check、runtime boundary、mirror parity 纳入周期性检查。
- 把 release/install/runtime freshness 与 cleanup governance 串联到同一 operator story。
- 形成“新增资产如何进入 repo”的 admission checklist。

**Deliverables:**
- hygiene checklist
- recurring gate cadence
- maintenance SOP

**Exit criteria:**
- 清扫完成后新增工作不会立即重新污染仓库；
- 任何新漂移都能在 batch 早期被 gate 捕获。

## Human / AI Readability Contract

完成清扫后，仓库至少要满足以下可理解性契约：

- **1 hop discoverability:** 从 root README 出发，1 次跳转内能找到 docs spine、reference spine、scripts spine、config spine。
- **plane clarity:** 任一文件都能判断自己属于 canonical / mirror / runtime / reference / archive 哪个平面。
- **entry discipline:** `docs/README.md`, `docs/plans/README.md`, `references/index.md`, `scripts/*/README.md` 形成稳定入口层。
- **no hidden generated truth:** 生成物不再被当作治理源；治理源不再藏在 mirror。
- **operator path clarity:** 人类与 AI 都能知道“先改哪里、再 sync 哪里、最后验什么”。

## Definition of Done Checklist

- [ ] canonical / bundled / nested 的脏项完成分域解释
- [ ] runtime artifact 完全隔离并文档化
- [ ] `.gitattributes` 与 no-BOM / EOL 策略落地
- [ ] canonical `??` workset 全部归类并收口
- [ ] docs / references / scripts / config 有稳定入口与 family README
- [ ] mirror parity / packaging / runtime freshness gates 继续通过
- [ ] archive / third-party / compliance 边界完成治理
- [ ] root README / SKILL / install / check 的阅读路径一致
- [ ] `git status --short` 为空

## Explicit Non-Goals

- 不把本轮清扫变成新一轮 feature wave。
- 不在 mirror 侧做人工结构创新。
- 不为了“视觉干净”删除仍然有审计/发布价值的 evidence。
- 不在没有 taxonomy / README / index 的情况下做大搬迁。
- 不一次性重写整个仓库历史。

## Recommended Immediate Sequence

1. 以本文件为 umbrella，冻结“继续扩张 wave”行为。
2. 先完成 Batch 0–3，优先把 canonical 脏区解释并收口。
3. 再完成 Batch 4–6，让信息架构与 mirror 一起稳定。
4. 最后完成 Batch 7–9，把 archive / compliance / automation 封闭成长期治理层。

## Success Signal

当这份计划执行完成后，`vco-skills-codex` 不只是 “git status 为空”，而是一个具有以下特征的仓库：

- 真源唯一，镜像纪律清晰；
- 运行态输出有边界，历史材料有归档；
- 文档、脚本、配置、reference 都有稳定入口；
- AI 与人类都能用同一套路径快速理解并安全操作；
- 后续再做 value extraction / wave 扩张时，不会把旧漂移重新带回来。

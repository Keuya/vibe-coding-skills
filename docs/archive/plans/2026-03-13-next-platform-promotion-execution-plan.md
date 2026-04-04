# Next Platform Promotion Execution Plan

> Companion documents:
> - `docs/plans/2026-03-13-universal-vibeskills-execution-program.md`
> - `docs/plans/2026-03-13-universal-vibeskills-no-regression-migration-plan.md`
> - `docs/universalization/platform-support-matrix.md`
> - `docs/universalization/platform-parity-contract.md`
> - `docs/universalization/platform-install-matrix.md`
> - `docs/universalization/official-runtime-baseline.md`
> - `docs/universalization/no-regression-proof-standard.md`
> - `docs/universalization/host-capability-matrix.md`
> - `docs/status/non-regression-proof-bundle.md`

**Goal:** 在已经完成第一轮通用化合同、truth docs、distribution lanes、host capability 和 no-regression proof 链的基础上，把下一步工作收敛成一个只围绕平台推进的执行批次。重点不是继续扩张 host 叙事，而是把 `Windows authoritative lane`、`Linux + pwsh strong lane`、`Linux without pwsh degraded lane` 三条路径做成可验证、可推广、可回滚的执行闭环，并且在整个过程中严格保持官方运行时零退化。

**Why now:** 当前仓库已经具备“诚实表达支持边界”的能力，但还没有把这组边界推进成“可用于 promotion 的平台证据包”。如果下一步继续横向扩张 host 适配或继续新增治理层，平台真实性会重新失焦，最终又回到“README 先宣传，证据之后补”的老问题。

**Core judgment:** 下一阶段的成功标准不是“把 Linux 宣传成和 Windows 一样强”，而是把平台真相变成可执行的工程纪律。允许最终结论仍然是“Windows 仍然最强，Linux 仍然带约束”，但不允许继续停留在“理论上支持，实际缺少 fresh-machine proof”的状态。

---

## 1. Current Baseline

截至当前批次，以下事项已经成立：

- `Windows` 是当前唯一已经被证明的权威参考路径。
- `Linux + pwsh` 已经被定义为 `supported-with-constraints`，但 promotion 证据尚未闭环。
- `Linux without pwsh` 已经被定义为 `degraded-but-supported`，但降级报告与冷启动体验仍需要更严格的实机证明。
- `Codex` 是当前最强宿主路径。
- `Claude Code` 仍是 `preview`。
- `OpenCode` 仍是 `not-yet-proven`。
- 当前仓库已经具备 replay / contract / honesty / installed-runtime freshness / version packaging 这些不退化裁判面。

这意味着下一步不应该再做的事情是：

- 不继续扩大 host 范围。
- 不新增新的“默认 fully supported”叙事。
- 不把 macOS 拉进同一优先级。
- 不重写 router 主链来换取平台叙事上的整齐。

---

## 2. Non-Negotiable Constraints

### 2.1 Windows lane first

- `Windows` 仍然是 release authority。
- 任何 Linux 推进都必须建立在 Windows 官方链持续全绿的前提下。
- 不允许为了让 Linux 看起来更完整而削弱或改写 PowerShell-first 的官方治理链。

### 2.2 Promotion is evidence-gated

- 支持等级升级不是目标本身，证据闭环才是目标。
- 如果 Linux 证据不足，允许保持当前标签不变。
- 不允许用文案升级替代工程证明。

### 2.3 Host and platform remain separate axes

- 不允许把“Codex supported”偷换成“所有平台都一样 supported”。
- 不允许把“Linux supported”偷换成“所有 host 在 Linux 上都 ready”。
- 所有对外表述必须维持 `<host> on <platform> => <status>` 这一表达方式。

### 2.4 Scope discipline

本轮默认不进入以下区域做结构性改造：

- `scripts/router/**`
- `install.ps1`
- `check.ps1`
- `install.sh`
- `check.sh`
- `scripts/bootstrap/**`
- `bundled/skills/vibe/**`
- `config/version-governance.json`

允许的动作是：

- 补充平台 proof 文档。
- 新增平台 promotion gate。
- 修复平台 bridge、doctor 报告、shell/pwsh 一致性问题。
- 修复安装说明与真实行为不一致的问题。

---

## 3. Next-Step Scope

本轮执行只做五件事：

1. 冻结平台 promotion 的判定标准。
2. 把 Windows 参考路径重新做成带收据的 release authority baseline。
3. 把 Linux + `pwsh` 做成真实的强路径候选，并建立 gap ledger。
4. 把 Linux 无 `pwsh` 的降级路径做成明确、诚实、可复现的 operator lane。
5. 把平台 truth 同步回安装入口、冷启动文档和版本治理流程。

本轮明确不做：

- 不新增新的 host adapter。
- 不提升 `OpenCode` 状态。
- 不推进 macOS promotion。
- 不新增新的治理 overlay。
- 不做 router 语义重构。

---

## 4. Execution Batches

## Batch A: Freeze Platform Promotion Criteria

**Objective:** 把“什么情况下可以升级平台支持等级”写成正式 contract，而不是散落在 README、matrix 和对话中。

**Planned outputs:**

- `docs/universalization/platform-promotion-criteria.md`
- `docs/status/platform-promotion-baseline-2026-03-13.md`
- `references/platform-gap-ledger.md` 更新为当前平台推进 ledger
- `scripts/verify/vibe-platform-promotion-bundle.ps1`

**Actions:**

- 定义平台 promotion 的最低证据清单。
- 把 `Windows`、`Linux + pwsh`、`Linux without pwsh` 的 expected surfaces 列成统一判定表。
- 明确“标签可以保持不变但 batch 仍然算成功”的条件。
- 明确“哪些 gap 是 blocker，哪些 gap 只是 advisory”。

**Exit conditions:**

- promotion criteria 有唯一文档入口。
- platform gap ledger 可以明确区分 `open`、`blocked`、`proved`、`not-in-scope`。
- platform promotion bundle 有可执行入口。

## Batch B: Re-Prove Windows as Release Authority

**Objective:** 重新证明 `Windows` 仍然是当前唯一权威参考路径，并把它变成 Linux 推进的裁判面。

**Planned outputs:**

- `docs/status/platform-windows-authority-closure-report-2026-03-13.md`
- `outputs/verify/**` 中对应平台 proof 收据
- `dist/manifests/*` 中与平台 truth 相关的版本戳若有变更则同步

**Actions:**

- 在当前官方环境重新跑完整 baseline。
- 重新收集 installed runtime freshness / version consistency / release-install coherence 收据。
- 确认 `one-shot setup`、`check.ps1 -Profile full -Deep`、平台 truth gates 仍与当前 README 承诺一致。
- 如无必要，不改实现，只收据化。

**Mandatory verification:**

```powershell
git diff --check
pwsh -NoProfile -File .\check.ps1 -Profile full -Deep
pwsh -NoProfile -File .\scripts\verify\vibe-official-runtime-baseline-gate.ps1 -WriteArtifacts
pwsh -NoProfile -File .\scripts\verify\vibe-platform-support-contract-gate.ps1 -WriteArtifacts
pwsh -NoProfile -File .\scripts\verify\vibe-platform-doctor-parity-gate.ps1 -WriteArtifacts
pwsh -NoProfile -File .\scripts\verify\vibe-version-consistency-gate.ps1 -WriteArtifacts
pwsh -NoProfile -File .\scripts\verify\vibe-version-packaging-gate.ps1 -WriteArtifacts
pwsh -NoProfile -File .\scripts\verify\vibe-installed-runtime-freshness-gate.ps1 -WriteArtifacts
pwsh -NoProfile -File .\scripts\verify\vibe-release-install-runtime-coherence-gate.ps1 -WriteArtifacts
```

**Exit conditions:**

- Windows baseline 全绿。
- 新平台推进没有引入任何 Windows regression。
- 后续 Linux 任何结论都可以回指这组 Windows 收据。

## Batch C: Promote Linux + `pwsh` from Theory to Proof Candidate

**Objective:** 把 `Linux + pwsh` 从“逻辑上接近 authoritative”推进成“有 fresh-machine proof 的强路径候选”。

**Planned outputs:**

- `docs/status/platform-linux-pwsh-baseline-2026-03-13.md`
- `docs/status/platform-linux-pwsh-closure-report-2026-03-13.md`
- `references/platform-gap-ledger.md` 中 Linux + `pwsh` 细分 gap
- `scripts/verify/vibe-linux-pwsh-proof-gate.ps1`

**Actions:**

- 至少在两个独立 clean workspace 做 Linux + `pwsh` fresh-machine 演练。
- 执行 `one-shot setup`、`deep check`、platform truth gates。
- 收集 shell 路径、PowerShell follow-up 路径、doctor 结果、manual action 分类。
- 只修 bridge 层问题：
  - `bash` 到 `pwsh` 的衔接不一致
  - readiness classification 漂移
  - profile materialization 漂移
  - 文档与真实行为不一致
- 不借机重写官方 Windows 实现。

**Mandatory verification:**

```bash
bash ./scripts/bootstrap/one-shot-setup.sh
bash ./check.sh --profile full --deep
pwsh -NoProfile -File ./scripts/verify/vibe-platform-support-contract-gate.ps1 -WriteArtifacts
pwsh -NoProfile -File ./scripts/verify/vibe-platform-doctor-parity-gate.ps1 -WriteArtifacts
pwsh -NoProfile -File ./scripts/verify/vibe-cross-host-degrade-contract-gate.ps1 -WriteArtifacts
pwsh -NoProfile -File ./scripts/verify/vibe-universalization-no-regression-gate.ps1 -WriteArtifacts
```

**Promotion rule:**

- 只有在连续三次完整跑通、覆盖至少两个 clean workspace、且没有新增 Windows regression 时，才允许讨论是否把 `Linux + pwsh` 从 `supported-with-constraints` 提升。
- 如果仍存在 blocker，允许继续保持原标签，但必须把 blocker 记入 gap ledger。

## Batch D: Close the Honest Degraded Lane for Linux without `pwsh`

**Objective:** 让 Linux 无 `pwsh` 的路径不是“能跑但说不清”，而是“明确降级、结果可信、用户可预期”。

**Planned outputs:**

- `docs/status/platform-linux-degraded-baseline-2026-03-13.md`
- `docs/status/platform-linux-degraded-closure-report-2026-03-13.md`
- `scripts/verify/vibe-linux-degraded-honesty-gate.ps1`
- `docs/universalization/platform-degraded-lane-contract.md`

**Actions:**

- 实机验证无 `pwsh` 情况下的安装、check、doctor、manual follow-up 输出。
- 确认 warning 文案与状态分类一致。
- 确认不会把 `warn-and-skip` 伪装成 success。
- 确认 README、cold-start docs、install matrix 明确写出：
  - 能装什么
  - 什么被跳过
  - 怎么升级到强路径

**Mandatory verification:**

```bash
bash ./scripts/bootstrap/one-shot-setup.sh
bash ./check.sh --profile full --deep
```

Windows 控制面必须补跑：

```powershell
pwsh -NoProfile -File .\scripts\verify\vibe-cross-host-degrade-contract-gate.ps1 -WriteArtifacts
pwsh -NoProfile -File .\scripts\verify\vibe-platform-support-contract-gate.ps1 -WriteArtifacts
pwsh -NoProfile -File .\scripts\verify\vibe-universalization-no-regression-gate.ps1 -WriteArtifacts
```

**Exit conditions:**

- Linux degraded lane 的输出可以稳定得到显式降级结论。
- 不存在“表面 ready、实则 authoritative gates 被静默跳过”的情况。
- 升级路径被写清楚。

## Batch E: Converge Public Surface, Release Governance, and Version Sync

**Objective:** 把平台 truth 收束到用户真正会看的入口，并把本地仓库、installed runtime、GitHub 版本治理重新对齐。

**Planned outputs:**

- `README.md`
- `README.en.md`
- `docs/cold-start-install-paths.md`
- `docs/universalization/platform-support-matrix.md`
- `docs/universalization/platform-install-matrix.md`
- `docs/status/current-state.md`
- `docs/status/roadmap.md`

**Actions:**

- 仅在 proof 已经落地后，更新 README 的平台 truth block。
- 把最小可用、推荐满血、企业治理三条安装路径和平台差异显式关联起来。
- 把版本同步动作纳入 batch close：
  - repo version
  - bundled mirror version
  - installed runtime marker
  - GitHub 远端主分支
- 如果 Linux 未达到 promotion 标准，则同步的是“truthful docs”，不是“更高标签”。

**Exit conditions:**

- 用户入口文档与平台真相一致。
- 本地仓库、运行时副本、远端主分支版本一致。
- 没有因为发布而把预览能力说成正式支持。

---

## 5. Test Matrix

### 5.1 Mandatory matrix

每个 batch 结束后至少覆盖以下矩阵：

| Surface | Windows | Linux + `pwsh` | Linux without `pwsh` | Expected |
| --- | --- | --- | --- | --- |
| Official runtime baseline | required | compare-to-Windows | compare-to-Windows | Windows remains green |
| One-shot setup | required | required | required | status must match documented lane |
| Deep check / doctor | required | required | required | no silent drift |
| Provider-missing degrade | required | required | required | explicit abstention only |
| Installed runtime freshness | required | required when runtime installed | advisory | no stale packaged runtime |
| Version consistency / packaging | required | required | required | one source of version truth |
| Platform truth docs | required | required | required | wording matches evidence |

### 5.2 Zero-regression budget

本轮 regression budget 仍然是零容忍：

- `0` 个 Windows official-runtime regression
- `0` 个 silent degrade
- `0` 个 false-ready doctor result
- `0` 个 host/platform overclaim

### 5.3 Stability proof bundle

任一平台路径若要升级或被用于 release 文案，必须提供：

1. 命令清单
2. 原始输出或 machine-readable receipt
3. support-level judgment
4. gap ledger 状态
5. rollback point

---

## 6. Batch-End Hygiene

每个 batch 结束后都必须执行：

```powershell
pwsh -NoProfile -File .\scripts\governance\phase-end-cleanup.ps1 -WriteArtifacts
pwsh -NoProfile -File .\scripts\verify\vibe-node-zombie-gate.ps1 -WriteArtifacts
```

只有在审计输出明确证明目标进程是 `vco-managed` 时，才允许执行：

```powershell
pwsh -NoProfile -File .\scripts\governance\phase-end-cleanup.ps1 -WriteArtifacts -ApplyManagedNodeCleanup
```

同时必须清理：

- 当前 batch 产生的临时文件
- 未被引用的本地演练输出
- 过期的对照日志副本

禁止把临时 proof 物料长期堆放在 repo 根目录。

---

## 7. Stop Rules and Rollback

出现以下任一情况，立即停止当前 batch：

- `Windows` baseline 新增失败
- platform truth gate 与 README 文案冲突
- Linux 路径需要修改 router 主链才能跑通
- 版本同步后出现 canonical / bundled / installed runtime 漂移
- degraded lane 输出重新出现“静默跳过但最终成功”式假阳性

回滚顺序必须是：

1. 先撤回对外文案和 support-level 升级。
2. 再撤回本 batch 新增的 proof / adapter / promotion 文件。
3. 如非 Windows baseline 自身记录错误，不回滚官方运行时主链。

---

## 8. Completion Standard

只有满足以下全部条件，这一轮“下一步平台推进”才算完成：

1. Windows 官方参考路径重新收据化并保持全绿。
2. Linux + `pwsh` 拥有真实 fresh-machine proof，且其 blocker 被明确 ledger 化。
3. Linux 无 `pwsh` 的降级路径被证明是诚实、可复现、可升级的。
4. README / cold-start / install matrix / status docs 与真实支持等级一致。
5. 本地仓库、bundled mirror、installed runtime、GitHub 主分支版本重新对齐。
6. 全程没有引入官方运行时退化。

**Important:** 本轮可以在不提升任何支持等级的情况下成功收口。只要平台 truth 更完整、证据链更强、入口文档更诚实，这一轮就算完成。平台 promotion 必须是结果，不能是前提。

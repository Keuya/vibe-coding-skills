# Single-Core Dual-Adaptation Dual-Proof Dual-Release Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 在不做 Linux / Windows 双分叉、不牺牲当前官方运行时能力、不制造“名义通用、实际退化”的前提下，把 `vco-skills-codex` 收敛为“单核心、双适配、双证明、双发行”的正式架构。

**Architecture:** 本计划采用 `single canonical core + platform adapters + behavior-first proof + release stratification` 架构。核心思想不是把现有仓库拆成两个平台仓，而是把路径解析、宿主调用、安装入口、证明体系和发行物显式分层，保留一份唯一事实来源，同时为 Windows 与 Linux 建立各自权威闭环与跨平台一致性证明。

**Tech Stack:** PowerShell / pwsh, Bash, Markdown governance docs, JSON policy manifests, VCO router/runtime scripts, proof bundles, release/install/check gates.

---

## Executive Conclusion

### Final Judgment

**结论一：不能做双分叉。**  
把项目拆成 Linux 版和 Windows 版，短期看会降低局部复杂度，长期会直接引入双份 router、双份治理、双份 proof、双份回归面，最终让“通用化”退化成“并行维护两个分布式产品”。这与当前项目希望成为通用 `VibeSkills` 基座的方向相冲突。

**结论二：必须做单核心、双适配、双证明、双发行。**  
当前真实问题不是“平台太多”，而是以下几层没有被正式建模：

- 运行时根目录被写死到作者机器和 Windows 语义。
- Linux 已安装运行时行为没有进入权威证明面。
- README / protocol / config / gate 对平台边界和宿主边界表达不一致。
- 当前 proof 更像“镜像与标记一致性证明”，而不是“安装后行为可运行证明”。

**结论三：这次改造的首要对象不是功能，而是 contract。**  
要先冻结并重建：

- 路径 contract
- 平台 contract
- 宿主 shell contract
- proof contract
- release contract

在这些 contract 没冻结之前，任何“快速兼容”都会把现有稳定性吃掉。

## Why This Plan Exists

用户已经明确提出三个目标必须同时成立：

1. 不再被 Linux / Windows / 宿主差异反复拉扯。
2. 不允许为了通用化引入功能退化。
3. 必须能够严格证明稳定性、可用性和智能性，而不是靠 README 承诺。

本计划就是把这三个目标落成一个可执行的工程方案。

## Current Reality Baseline

### 1. 当前仓库仍然把默认运行根绑定到 Windows 环境变量

已确认的入口问题：

- [`check.ps1`](D:\table\new_ai_table\_ext\vco-skills-codex\check.ps1)
- [`install.ps1`](D:\table\new_ai_table\_ext\vco-skills-codex\install.ps1)

这两个入口当前都使用：

```powershell
[string]$TargetRoot = (Join-Path $env:USERPROFILE ".codex")
```

这意味着只要进入 Linux / pwsh 环境且 `USERPROFILE` 为空，入口就可能直接空路径崩溃。

### 2. Linux 已安装运行时的真实路由闭环并未被修好

关键命中点：

- [`scripts/router/modules/46-confirm-ui.ps1`](D:\table\new_ai_table\_ext\vco-skills-codex\scripts\router\modules\46-confirm-ui.ps1)

该模块直接使用：

```powershell
$userRoot = Join-Path $env:USERPROFILE ".codex\\skills"
```

这不是 README 边界问题，而是已安装运行时在 Linux 上的真实行为断点。只要 global fallback 依赖这条路径，Linux lane 就不是正式满血。

### 3. 当前 proof 体系尚未覆盖“安装后行为真相”

关键配置点：

- [`config/version-governance.json`](D:\table\new_ai_table\_ext\vco-skills-codex\config\version-governance.json)

已确认：

- 存在 `installed_runtime.target_relpath = "skills/vibe"`
- 存在 `installed_runtime.receipt_relpath = "skills/vibe/outputs/runtime-freshness-receipt.json"`
- 存在 `require_nested_bundled_root = false`

这说明现有 freshness / coherence 证明主要验证：

- 安装标记
- 镜像一致性
- receipt 完整性
- 版本一致性

但尚未把“Linux 下 installed runtime 的真实路由可运行性”纳入权威证明。

### 4. Canonical config 仍然泄漏作者机器绝对路径

关键命中点：

- [`bundled/skills/vibe/config/dependency-map.json`](D:\table\new_ai_table\_ext\vco-skills-codex\bundled\skills\vibe\config\dependency-map.json)

已确认包含：

- `C:/Users/羽裳/.codex/skills/vibe`
- `C:/Users/羽裳/.codex/skills/local-vco-roles`
- 以及一系列同类来源

这意味着 canonical truth 已被 author-machine path 污染。只要这类绝对路径继续存在，项目就不能声称自己已经具备平台中性和位置中性。

### 5. Docs 也在把 `~/.codex` 写成事实，而不是默认值

关键命中点：

- [`protocols/team.md`](D:\table\new_ai_table\_ext\vco-skills-codex\protocols\team.md)

当前仍存在：

- `Role prompts sourced from ~/.codex/skills/local-vco-roles/...`

这在本质上把“默认安装位置”写成了“架构真相”，会持续误导平台适配与宿主适配设计。

### 6. 两个关键 gate 仍然写死 `powershell.exe`

关键命中点：

- [`scripts/verify/vibe-platform-promotion-bundle.ps1`](D:\table\new_ai_table\_ext\vco-skills-codex\scripts\verify\vibe-platform-promotion-bundle.ps1)
- [`scripts/verify/vibe-universalization-no-regression-gate.ps1`](D:\table\new_ai_table\_ext\vco-skills-codex\scripts\verify\vibe-universalization-no-regression-gate.ps1)

这意味着 promotion / no-regression 在 Linux lane 上依然不是 shell-neutral proof。

## Non-Negotiable Principles

### Principle 1: One Canonical Core Only

核心运行语义只允许有一份唯一事实来源，必须统一表达以下内容：

- 路径解析规则
- skill root / external root / bundled root 解析规则
- 路由 contract
- proof contract
- release contract

不允许 Windows 和 Linux 各自维护一份“逻辑上相同、实现上不同”的 router 或 governance 真相。

### Principle 2: Platform Differences Must Live in Adapters, Not in Core Truth

平台差异只能存在于适配层，例如：

- home directory 发现方式
- shell 选择方式
- process spawning 方式
- path separator / quoting 方式
- host-managed profile materialization 方式

这些差异不能反向污染：

- canonical config
- router semantics
- skill contract
- README 对外承诺

### Principle 3: No Silent Degrade

每个能力都必须被显式标记为以下状态之一：

- `full`
- `degraded-but-supported`
- `advisory-only`
- `unsupported`

不能再出现“文档看起来支持、脚本也能跑一半，但真实安装后行为断裂”的伪支持。

### Principle 4: Proof Must Be Behavior-First

以后所有绿色结论都必须先回答一个问题：

> 这个绿色，是否证明了用户安装后的真实行为？

如果答案是否定的，那这个 gate 只能算辅助信号，不能算 promotion authority。

### Principle 5: Version Line Must Stay Unified

无论最终发行多少个产物，都只能保留一条统一版本线。例如：

- `2.3.x` 是唯一对外版本
- Windows artifact 与 Linux artifact 共享同一语义版本
- repo、本地安装目录、GitHub tag、proof bundle receipt 必须在同一版本线上对齐

不允许出现平台即版本的分裂模式。

## Target Architecture

## A. Single Canonical Core

新增或收敛出一组核心 contract，不依赖具体平台、不依赖具体宿主安装位置：

- `Resolve-VibeHome`
- `Resolve-VibeTargetRoot`
- `Resolve-VibeSkillRoot`
- `Resolve-VibeInstalledSkillRoot`
- `Resolve-VibeExternalRoot`
- `Resolve-VibeHostShell`
- `Resolve-VibePlatformProfile`

这些能力可以先以 PowerShell helper module 落地，再由 shell wrappers / bash wrappers 调用，但 contract 必须唯一。

### Unified Root Resolution Order

后续所有入口统一遵循以下优先级：

1. 显式 `--target-root`
2. 环境变量 `VIBE_TARGET_ROOT`
3. 环境变量 `CODEX_HOME`
4. settings / profile 中声明的 root
5. 平台 home fallback

平台 home fallback 只在最后一级出现，且必须封装，不允许各脚本再直接拼：

- `$env:USERPROFILE`
- `$env:HOME`
- `~/.codex`
- `C:/Users/...`

### Explicit Ban List

从 canonical runtime 中禁止以下模式继续扩散：

- 直接使用 `$env:USERPROFILE` 作为唯一 home 来源
- 直接使用 `$env:HOME` 作为唯一 home 来源
- 写死 `powershell.exe`
- 写死 `C:/Users/...`
- 在 docs / config 中把 `~/.codex` 写成架构事实

## B. Dual Adaptation

### Adapter 1: Windows Authoritative Adapter

职责：

- PowerShell 入口
- Windows path normalization
- Windows shell / process contract
- Windows install / check / promotion lane

要求：

- 继续保持当前 Windows 权威能力不退化
- 所有现有 Windows 满血能力必须在 adapter 化后保持等价

### Adapter 2: Linux Authoritative Adapter

职责：

- pwsh / bash 双入口协调
- Linux path normalization
- Linux install / check / promotion lane
- Linux 下已安装 runtime 路由闭环

要求：

- Linux 不再只是“可运行但部分降级”的 lane
- Linux authoritative lane 必须能证明 installed runtime 行为
- 没有 `pwsh` 时，必须诚实进入 degraded contract
- 有 `pwsh` 时，必须具备完整权威证明闭环

### Host Adaptation Is Separate from Platform Adaptation

宿主差异不是平台差异。需要单独抽象 host surface，例如：

- Codex
- Claude Code
- OpenCode
- Generic skill consumer

平台 adapter 解决的是 Windows / Linux。  
宿主 adapter 解决的是 settings / plugin / MCP / host-managed surfaces。

这两个维度不能混为一谈，否则后续会再次陷入多维叉乘爆炸。

## C. Dual Proof

### Proof Line 1: Platform Authoritative Proof

每个平台都需要自己的权威闭环：

- 安装证明
- 路由证明
- freshness 证明
- promotion 证明
- replay 证明

Windows 与 Linux 都必须能单独回答：

- repo runtime 是否可运行
- installed runtime 是否可运行
- bundled/global fallback 是否工作
- docs 承诺是否与真实行为一致

### Proof Line 2: Cross-Platform Consistency Proof

除了各自跑通，还必须证明以下一致性：

- 相同 prompt / 相同 router input 的 route parity
- 相同 target root contract 的 path parity
- 相同安装产物的 receipt / manifest parity
- 相同支持等级声明的 docs parity

换句话说：

- 平台 proof 证明“各自能活”
- consistency proof 证明“没有偷偷分叉”

## D. Dual Release

### Release Artifact Strategy

统一版本线下，允许双发行物：

- Windows-first release artifact
- Linux-first release artifact

必要时再加：

- generic host bundle

但这些 artifact 必须共享：

- 同一版本号
- 同一 canonical manifest
- 同一 proof family
- 同一 changelog truth

### Release Contract

每个发行物都必须回答：

- 支持哪些平台
- 支持哪些宿主
- 哪些能力是 full
- 哪些能力是 degraded-but-supported
- 哪些能力需要 operator provisioning

不允许再用“一份 README 同时覆盖所有情况”的模糊叙事。

## Scope

本计划覆盖以下面向：

- 路径解析 contract 重建
- Windows / Linux 平台适配 contract
- host shell contract
- installed runtime proof 补强
- promotion / replay 体系升级
- canonical config 去绝对路径
- README / protocol / proof 文档 truth alignment
- 统一版本线下的双发行策略

本计划暂不直接覆盖：

- 新 skill 大规模扩容
- 第三方 skill 批量引入
- 新模型能力研发
- 全量 host adapter 的完整功能实现

这些属于下一阶段，在 core contract 稳定后推进。

## Workstreams

### Workstream 1: Root Contract Freeze

输出物：

- 路径解析设计说明
- helper contract 列表
- default root 与 custom root 规范
- docs 中关于 `~/.codex` 的重新表述

完成标准：

- 所有入口统一优先级
- 不再允许脚本各自推导 root

### Workstream 2: Platform Adapter Extraction

输出物：

- Windows adapter
- Linux adapter
- host shell resolver
- process spawn abstraction

完成标准：

- `powershell.exe` 被适配层替换
- Linux / Windows 都能由同一核心 contract 驱动

### Workstream 3: Installed Runtime Repair

输出物：

- installed runtime 路由修复
- global fallback 修复
- confirm UI root resolution 修复

完成标准：

- Linux installed runtime 不再依赖 `USERPROFILE`
- custom target root 可工作
- repo runtime 与 installed runtime route parity 可验证

### Workstream 4: Proof Upgrade

输出物：

- installed-runtime behavior replay
- Linux authoritative promotion gate
- cross-platform consistency gate
- promotion bundle truth alignment

完成标准：

- 绿灯不再放过 Linux installed runtime 断裂
- proof bundle 与真实平台状态一致

### Workstream 5: Release Governance

输出物：

- dual-release manifest
- platform capability matrix
- release channel truth docs
- unified version governance update

完成标准：

- 本地安装目录、repo、GitHub 版本一致
- 每个 artifact 的支持边界可审计

## Execution Waves

### Wave 0: Baseline Freeze

目标：

- 冻结当前问题证据
- 冻结当前 Windows / Linux 差异基线
- 冻结当前 docs / config / proof 的冲突点

动作：

1. 建立单独 baseline status 文档。
2. 把当前关键命中点列为 authoritative evidence。
3. 冻结当前 promotion truth，禁止在 baseline 未记录前“顺手修”。

退出条件：

- 后续所有改造都能对照 baseline 解释“修了什么、为何修、是否退化”。

### Wave 1: Path Contract Design and Freeze

目标：

- 不写代码先定 contract

动作：

1. 列出所有入口脚本的 root 解析方式。
2. 列出所有 `USERPROFILE` / `HOME` / `~/.codex` / 绝对路径命中点。
3. 发布统一 root resolution contract。
4. 明确默认值、环境变量、参数覆盖、settings 覆盖优先级。

退出条件：

- 任意脚本都能被重新解释到统一 contract 上。

### Wave 2: Adapter Layer Landing

目标：

- 把路径、shell、spawn 差异收口到适配层

动作：

1. 落地 `Resolve-VibeHome` 系列 helper。
2. 替换入口脚本的直接拼路径逻辑。
3. 替换 hardcoded `powershell.exe`。
4. 引入 host shell 发现逻辑。

退出条件：

- core 层不再直接感知平台特有路径或 shell 名称。

### Wave 3: Installed Runtime Linux Closure

目标：

- 让 Linux 从“部分支持”推进到“权威支持”

动作：

1. 修 confirm UI / route fallback 的 root 解析。
2. 修 installed runtime 下的 global skill fallback。
3. 建立 Linux fresh-machine 安装与 replay 证明。
4. 确保 Linux + pwsh lane 可跑完 promotion。

退出条件：

- Linux installed runtime 行为被真正确认，不再只靠 repo 内 gate。

### Wave 4: Canonical Truth Cleanup

目标：

- 清除作者机器路径和文档事实污染

动作：

1. 清理 `dependency-map.json` 中的绝对路径。
2. 把 docs 中的 `~/.codex` 改写为“默认 target root”而不是“唯一事实”。
3. 对 config / protocol / README 做 truth alignment。

退出条件：

- canonical config 不再泄漏 author-machine path。
- docs 不再把默认安装目录写成唯一架构路径。

### Wave 5: Behavior-First Proof Upgrade

目标：

- 证明体系升级为行为权威

动作：

1. 为 installed runtime 增加真实 replay fixture。
2. 为 Linux / Windows 分别建立 authoritative promotion gate。
3. 新增 cross-platform consistency gate。
4. 禁止“标记一致但行为断裂”仍然绿灯。

退出条件：

- 任何 promotion green 都意味着用户安装后真实可运行。

### Wave 6: Dual Release Formalization

目标：

- 在统一版本线下形成双发行

动作：

1. 定义 artifact family。
2. 定义 capability matrix。
3. 定义 release naming / receipt / bundle contract。
4. 更新 README 与 release governance 文档。

退出条件：

- 平台支持声明和实际产物完全对齐。

### Wave 7: Final Promotion and Freeze

目标：

- 完成正式晋升并冻结回归基线

动作：

1. 跑完整 proof bundle。
2. 跑 fresh-machine Windows 证据。
3. 跑 fresh-machine Linux 证据。
4. 对齐 repo / local runtime / GitHub version。
5. 清理临时文件与阶段性脚本产物。

退出条件：

- 形成可重复的正式版本。

## Test Matrix

### A. Root Resolution Tests

必须覆盖：

- Windows PowerShell 默认 root
- Windows PowerShell 自定义 `--target-root`
- Windows 设置 `VIBE_TARGET_ROOT`
- Linux pwsh 默认 root
- Linux pwsh 自定义 `--target-root`
- Linux bash 入口转发
- `USERPROFILE` 缺失
- `HOME` 缺失
- `CODEX_HOME` 优先级

通过标准：

- 不得出现 null-path crash
- 不得出现路径分支行为不一致

### B. Install Tests

必须覆盖：

- minimal profile
- full profile
- 默认安装路径
- 自定义安装路径
- Windows authoritative lane
- Linux authoritative lane
- Linux 无 `pwsh` 的 degraded lane

通过标准：

- 安装状态与 capability 声明一致
- degraded path 必须诚实报出边界

### C. Runtime Routing Tests

必须覆盖：

- repo runtime
- installed runtime
- bundled runtime
- global fallback
- confirm UI
- custom root install

通过标准：

- 相同输入 route 结果一致
- installed runtime 行为不能弱于 repo runtime 声明

### D. Proof and Promotion Tests

必须覆盖：

- freshness gate
- coherence gate
- promotion bundle
- no-regression gate
- replay fixture
- platform capability receipt

通过标准：

- 任一权威 gate 失败，promotion 直接阻断
- proof bundle 状态必须与真实平台状态一致

### E. Intelligence Tests

“智能性”不能只靠主观描述，至少要证明以下三件事：

1. 相同输入在 Windows / Linux 上 route parity 成立。
2. 相同输入在 repo runtime / installed runtime 上 route parity 成立。
3. provider 缺失或变化时，系统能进入明确 degrade，而不是随机偏航。

这意味着必须增加：

- router replay corpus
- provider-neutral shadow evaluation
- fallback correctness fixtures

## Stability Proof Model

### Stability

判定标准：

- 入口不崩
- 安装不崩
- 路由不崩
- proof 不虚假通过
- release 不漂移

必须满足：

- 零 null-path crash
- 零 hardcoded Windows-only spawn path in canonical proof flow
- 零 author-machine absolute path in canonical config

### Usability

判定标准：

- 普通用户能理解支持边界
- 平台安装说明能一眼分辨 full / degraded / optional
- custom root 能工作，不要求用户必须装到 `~/.codex`

必须满足：

- README 安装路径说明与真实行为一致
- Windows / Linux 两条路径的文档入口明确
- host-managed plugin / MCP surfaces 的边界讲清楚

### Intelligence

判定标准：

- VCO 的路由质量不因平台适配而漂移
- provider-neutral 设计不损失核心治理权
- 多智能体 / 路由 / fallback 行为可重复

必须满足：

- router selection 不依赖单一 provider 生死
- provider 缺失时仍有 rule-based / heuristic-safe contract
- route replay 能复现关键决策

## Risks and Mitigations

### Risk 1: 为了“通用”把现有 Windows 满血路径打坏

缓解：

- Windows 作为现有 authoritative lane，先冻结后迁移
- 任何 core 提取都先做 adapter 包裹，再做替换
- 所有替换必须跑 Windows replay baseline

### Risk 2: Linux 改造只修 repo，不修 installed runtime

缓解：

- 所有 Linux 修复必须以 installed runtime replay 为验收对象
- 任何只在 repo runtime 成立的绿灯不得视为晋升完成

### Risk 3: Docs 比代码先夸大支持

缓解：

- capability matrix 先行
- README 只能消费 capability truth
- promotion 未完成前不允许对外宣称 full-authoritative

### Risk 4: 适配层失控膨胀，重新变成隐性双分叉

缓解：

- 适配层只允许封装平台差异，不允许复制 router / governance 语义
- cross-platform consistency gate 强制阻断逻辑分叉

### Risk 5: Provider-neutral 改造削弱现有智能路由质量

缓解：

- 先做 provider 抽象，不先改 router ownership
- 先做 shadow evaluation，比对 route quality
- 只有 shadow 结果稳定后，才允许进入正式 promotion

## Stop-Ship Rules

出现以下任一情况，必须阻断正式发布：

- Linux authoritative lane 仍无法证明 installed runtime routing
- 任何 canonical config 仍残留 author-machine absolute path
- 任何核心 gate 仍写死 `powershell.exe`
- README 声称 full support，但 capability matrix 未达成
- route parity 在 Windows / Linux 间明显漂移
- repo、本地运行目录、GitHub 版本未对齐

## Completion Criteria

只有同时满足以下条件，才能判定本计划完成：

1. 单核心 contract 已冻结并进入主线。
2. Windows / Linux 均存在各自 authoritative lane。
3. Linux installed runtime 行为已被正式证明。
4. canonical config 已清除作者机器绝对路径。
5. docs / protocol / config / proof truth 已对齐。
6. dual release 已在统一版本线下落地。
7. route parity / replay / promotion 全部通过。
8. 阶段结束后的临时文件、临时脚本、僵尸 node 占用已清理。

## Implementation Order Recommendation

建议后续执行顺序固定为：

1. 基线冻结
2. 路径 contract 冻结
3. adapter 抽取
4. Linux installed runtime 修复
5. canonical truth 清理
6. proof 升级
7. dual release 落地
8. final promotion freeze

这个顺序不能反过来。  
原因很简单：如果没有先冻结 contract 和 proof，后面的每一步都无法判断是在“修通用性”还是在“制造新的不一致”。

## Immediate Next-Step Files

后续进入执行时，优先围绕以下文件族推进：

- [`check.ps1`](D:\table\new_ai_table\_ext\vco-skills-codex\check.ps1)
- [`install.ps1`](D:\table\new_ai_table\_ext\vco-skills-codex\install.ps1)
- [`scripts/router/modules/46-confirm-ui.ps1`](D:\table\new_ai_table\_ext\vco-skills-codex\scripts\router\modules\46-confirm-ui.ps1)
- [`scripts/verify/vibe-platform-promotion-bundle.ps1`](D:\table\new_ai_table\_ext\vco-skills-codex\scripts\verify\vibe-platform-promotion-bundle.ps1)
- [`scripts/verify/vibe-universalization-no-regression-gate.ps1`](D:\table\new_ai_table\_ext\vco-skills-codex\scripts\verify\vibe-universalization-no-regression-gate.ps1)
- [`config/version-governance.json`](D:\table\new_ai_table\_ext\vco-skills-codex\config\version-governance.json)
- [`bundled/skills/vibe/config/dependency-map.json`](D:\table\new_ai_table\_ext\vco-skills-codex\bundled\skills\vibe\config\dependency-map.json)
- [`protocols/team.md`](D:\table\new_ai_table\_ext\vco-skills-codex\protocols\team.md)

## Final Position

这次不是“为 Linux 打补丁”，也不是“为 Windows 保守维稳”。  
这次要完成的是一次真正意义上的架构收敛：

- 一份核心真相
- 两条平台权威闭环
- 两类证明体系
- 两份发行物
- 一条统一版本线
- 零平台双分叉

如果这套方案按顺序落地，项目才有资格同时宣称：

- 它是通用的
- 它是可治理的
- 它是可证明的
- 它是不会因通用化而退化的

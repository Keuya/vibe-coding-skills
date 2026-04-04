# Public Docs Entrypoint Restructure Execution Plan

## Execution Summary

重构公开入口文档组，使仓库首页与安装入口从“技术说明集合”收敛为“面向普通用户的清晰入口”。

## Frozen Inputs

- Requirement doc: `docs/requirements/2026-03-19-public-docs-entrypoint-restructure.md`
- Approved direction: 平衡型公开文风；普通用户优先；`VibeSkills` 为对外主名称；`VCO` 作为核心运行时解释；安装入口后置；manifesto 收缩为短心路 + 少量原则。

## Anti-Proxy-Goal-Drift Controls

### Primary Objective

让第一次进入仓库的人快速理解项目定位，并能用最简单的方式开始使用。

### Non-Objective Proxy Signals

- 不追求“看起来很宏大”的措辞
- 不追求展示尽可能多的内部组件与治理细节
- 不追求把所有安装边界都塞进 README 首屏

### Validation Material Role

现有 README、manifesto、安装文案、docs/install 与 docs/README 结构仅作为问题样本与边界参考，不作为必须保留的叙事模板。

### Declared Tier

M

### Intended Scope

仅重构公开入口文档组与相应 canonical 索引，不改 runtime / install / check 行为。

### Abstraction Layer Target

公开文档层，不进入脚本实现层。

### Completion State Target

新的公开入口文档组可直接用于 README 首屏传播和初次上手导航。

### Generalization Evidence Plan

- 中英文 `README`、`manifesto`、一步式安装文案与 `quick-start` 形成明确分工
- requirements / plans 索引更新
- `git diff --stat` 仅显示预期文档改动

## Internal Grade Decision

M。单轮单人文档重构，虽然涉及多文件，但依赖紧密，不需要多代理拆分。

## Wave Plan

### Wave 1: Canonical governance artifacts

- 新增 requirement doc
- 新增 execution plan
- 更新 requirements / plans 索引 current entry

### Wave 2: Public-facing content rewrite

- 重写 `README.md`
- 重写 `docs/manifesto.md`
- 重写 `docs/install/one-click-install-release-copy.md`
- 新增 `docs/quick-start.md`
- 重写 `README.en.md`
- 重写 `docs/manifesto.en.md`
- 重写 `docs/install/one-click-install-release-copy.en.md`
- 新增 `docs/quick-start.en.md`

### Wave 3: Verification and cleanup

- 复查关键文档职责分工
- 用 `git diff --stat` 验证修改范围
- 运行 Node 审计 / cleanup 证据

## Ownership Boundaries

- `README.md` / `README.en.md`: 项目定位、问题定义、价值主张、开始入口
- `docs/manifesto.md` / `docs/manifesto.en.md`: 作者动机与核心原则
- `docs/install/one-click-install-release-copy.md` / `docs/install/one-click-install-release-copy.en.md`: 面向普通用户的 AI 安装提示词入口
- `docs/quick-start.md` / `docs/quick-start.en.md`: README 后的二跳导航

## Verification Commands

```bash
git diff --stat -- README.md README.en.md docs/manifesto.md docs/manifesto.en.md docs/install/one-click-install-release-copy.md docs/install/one-click-install-release-copy.en.md docs/quick-start.md docs/quick-start.en.md docs/requirements/2026-03-19-public-docs-entrypoint-restructure.md docs/plans/2026-03-19-public-docs-entrypoint-restructure-plan.md docs/requirements/README.md docs/plans/README.md

git status --short

pwsh -File scripts/governance/Invoke-NodeProcessAudit.ps1
pwsh -File scripts/governance/Invoke-NodeZombieCleanup.ps1
```

## Rollback Plan

- 若文风失真或职责混乱，优先回滚单个文档到改写前版本，而不是整体放弃公开入口收敛方向
- 若 README 与安装页发生信息冲突，以 requirement doc 的用户定位与边界说明为准重新收敛

## Phase Cleanup Contract

- 不产生临时生成文件
- 阶段完成前补做 git diff 验证
- 阶段完成前补做 Node 审计与 cleanup 证据

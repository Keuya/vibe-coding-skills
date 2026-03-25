# Public README Propagation Optimization Plan

## Execution Summary

将 README 中英双语首页首屏从“解释型公开入口”升级为“传播优先、价值冲击优先”的首屏入口，同时保留事实边界与 governed traceability。

## Frozen Inputs

- Requirement doc: `docs/requirements/2026-03-19-public-readme-propagation-optimization.md`
- Approved direction: 首屏宣传优先；安装后置；联合使用判断冲击、数字冲击、对比冲击；采用更锋利的 Version A 气质。

## Anti-Proxy-Goal-Drift Controls

### Primary Objective

让第一次进入 README 的用户在极短时间内被项目价值击中，并清楚理解它和普通 skills 仓库的本质差异。

### Non-Objective Proxy Signals

- 不把 README 首屏写成安装说明页
- 不用空泛形容词代替事实支撑
- 不把 manifesto 的心路叙事重新塞回首屏
- 不为追求冲击感而写入无法证明的外部声誉信息

### Declared Tier

M

### Intended Scope

只改 `README.md`、`README.en.md` 与 requirements / plans 索引；不改其他公开文档主体内容。

### Completion State Target

README 首屏形成“定义项目 -> 量化证明 -> 差异说明 -> 次级入口”的传播型结构。

## Wave Plan

### Wave 1: Governance trace

- 新增 requirement doc
- 新增 execution plan
- 更新 requirements / plans 索引 current entry

### Wave 2: README first-screen rewrite

- 重写 `README.md` 首屏标题、副标题、proof bar、差异段和入口顺序
- 重写 `README.en.md` 对应首屏，不做弱化直译

### Wave 3: Verification and cleanup

- 复查 README 首屏信息密度与职责边界
- 用事实计数核对 proof bar 文案
- 运行 `git diff --stat`、`git status --short --branch`
- 运行 Node audit / cleanup 生成阶段卫生证据

## Ownership Boundaries

- `README.md`: 中文公开首页首屏传播主入口
- `README.en.md`: 英文公开首页首屏传播主入口
- `docs/requirements/*.md`: 冻结需求与事实边界
- `docs/plans/*.md`: 执行计划与验证路径

## Verification Commands

```bash
git diff --stat -- README.md README.en.md docs/requirements/2026-03-19-public-readme-propagation-optimization.md docs/plans/2026-03-19-public-readme-propagation-optimization-plan.md docs/requirements/README.md docs/plans/README.md

git status --short --branch

find bundled/skills -mindepth 1 -maxdepth 1 -type d | wc -l
node -e "const x=require('./config/upstream-corpus-manifest.json'); console.log((x.entries||[]).length)"
ls config/*.json | wc -l

pwsh -File scripts/governance/Invoke-NodeProcessAudit.ps1
pwsh -File scripts/governance/Invoke-NodeZombieCleanup.ps1
```

## Rollback Plan

- 若首屏过度营销或失去可信度，优先回退标题、副标题与 proof bar，而不是整体回滚本轮传播优化
- 若安装入口被压得过深影响可用性，恢复到 README 中部而不是首屏顶部

## Phase Cleanup Contract

- 不生成临时素材或截图资产
- 阶段完成前补做 git diff / status 验证
- 阶段完成前补做 Node audit / cleanup receipts

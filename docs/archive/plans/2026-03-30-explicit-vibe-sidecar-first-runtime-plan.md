# Explicit Vibe Sidecar-First Runtime Plan

**日期**: 2026-03-30
**需求文档**: [../requirements/2026-03-30-explicit-vibe-sidecar-first-runtime.md](../requirements/2026-03-30-explicit-vibe-sidecar-first-runtime.md)
**Internal Grade**: `L`

## Design Decision

冻结以下主设计：

- `entry is skill-native, state is sidecar-native`
- 默认行为是：
  - 未显式调用 `vibe` 时，Vibe 不主动注入、不主动启动、不抢宿主默认控制权
  - 显式调用 `$vibe` / `/vibe` / 宿主 skill 入口时，完整装载 Vibe 路由与 runtime
- 默认不写入宿主真实配置文件

## Canonical Layering

### 1. Host Entry Layer

职责：

- 只负责把显式 `vibe` skill 调用转交给 Vibe runtime entry
- 不承载 Vibe 主状态
- 不承载复杂治理配置

允许形式：

- `skills/vibe/**`
- 宿主原生支持的 skill 调用目录
- Vibe skill 内部引用的本地运行入口

设计要求：

- 这是最薄的一层
- 未显式调用 `vibe` 时不应产生运行时副作用
- 不允许依赖宿主原生配置文件完成 skill 注册

### 2. Canonical Runtime State Layer

canonical 文件：

- `.vibeskills/host-settings.json`

职责：

- 承载显式 `vibe` 调用所需的宿主本地 runtime state
- 作为 Vibe 路由层与 runtime 层的首选输入面

建议字段：

- `schema_version`
- `host_id`
- `managed`
- `skills_root`
- `runtime_skill_entry`
- `commands_root`
- `agents_root`
- `workflow_root`
- `mcp_config_path`
- `specialist_wrapper`
- `runtime_mode_defaults`
- `explicit_vibe_skill_invocation`
- `feature_flags`

关键规则：

- 宿主原生配置文件不是 canonical truth
- sidecar 中缺失字段时可以降级报错，但不能自动回退为宿主配置桥接

### 3. Install / Audit Receipt Layer

canonical 文件：

- `.vibeskills/host-closure.json`
- `.vibeskills/install-ledger.json`

职责：

- 记录安装产物
- 记录 wrapper readiness
- 支撑 uninstall / doctor / audit / support

关键规则：

- `host-closure.json` 不再承担长期 canonical runtime state 角色
- 它保留为 receipt / reconciliation / proof surface

## Runtime Activation Contract

### Idle State

- 未显式调用 `vibe` 时：
  - Vibe 不应抢占宿主默认路由
  - Vibe 不应要求宿主主动读取 `.vibeskills/host-settings.json`
  - 宿主保持自然静默是正确行为

### Explicit Vibe State

- 当用户显式输入 `$vibe` / `/vibe` / 宿主等价入口时：
  - Host Entry Layer 通过宿主 skill 调用把请求交给 Vibe runtime entry
  - wrapper 读取 `.vibeskills/host-settings.json`
  - Vibe 再装载：
    - 路由策略
    - runtime context
    - specialist bridge
    - commands / agents / workflow pointers
  - 若 `host-settings.json` 缺失，则输出明确的 install / repair guidance，而不是回退到宿主原生配置猜测

## Host Classification Under This Design

### Group A: 优先迁移到 sidecar-first

- `claude-code`
- `cursor`
- `opencode`
- `windsurf`
- `openclaw`

原因：

- 用户已明确要求这些宿主不再触碰原生配置文件
- 这些宿主被假定原生支持 skill 调用
- 可显著降低共享配置 schema 风险与启动回归风险

### Group B: 范围外宿主

- `codex`

原因：

- 本轮新设计以“目标宿主原生支持 skill 调用”为前提
- `codex` 是否按完全相同方式收缩，不在本轮强制冻结

## Migration Waves

### Wave 1: Runtime Truth Freeze

- 冻结原则：
  - `.vibeskills/host-settings.json` 升为 canonical runtime state
  - `.vibeskills/host-closure.json` 降为 receipt
  - 宿主原生配置文件退出默认安装面
- 更新文档 truth：
  - install matrix
  - host capability matrix
  - uninstall governance
  - install docs

### Wave 2: Runtime Reader Migration

- 调整 runtime 读取顺序：
  1. `host-settings.json`
  2. `host-closure.json` 仅作 receipt / readiness / reconciliation
  3. 明确错误，不隐式猜测宿主真实 settings

### Wave 3: Preview Host Installer Migration

- `claude-code` / `cursor`：
  - 不再写真实 `settings.json`
  - 改写 `.vibeskills/host-settings.json`
  - 仅安装 `skills/vibe/**` 与 Vibe-owned sidecar/receipt/runtime payload

- `opencode`：
  - 不再写真实 `opencode.json`
  - sidecar 承载 runtime state
  - 仅安装 `skills/vibe/**` 与 Vibe-owned sidecar/receipt/runtime payload

- `windsurf` / `openclaw`：
  - 对齐统一 sidecar schema
  - 保持 skill-native 入口模型

### Wave 4: Verification And Safety Gates

- 新增验证点：
  - 未显式调用 `vibe` 时不产生宿主启动副作用
  - 显式 `vibe` 调用时能从 sidecar 完整装载 runtime
  - uninstall 只删 owned-only surfaces
  - 缺少 sidecar 时报错清晰

### Wave 5: Codex Decision Gate

- 单独评估 `codex`
- 只在以下条件满足后才考虑迁移：
  - skill-native activation 有真实证据
  - sidecar-first 不降低当前 closure
  - route/runtime activation 不退化

## Risks

### Risk 1: 入口存在，但 sidecar 缺失

处置：

- wrapper 明确报 bootstrap missing
- 指向安装/doctor/repair

### Risk 2: sidecar 与 receipt 漂移

处置：

- `host-closure.json` 保留 readiness / artifact proof
- 引入 doctor / check 一致性检查

### Risk 3: 宿主没有稳定的显式入口挂载位

处置：

- 标记该宿主不满足本设计前提
- 不允许偷偷回退到宿主配置文件写入

### Risk 4: 测试仍绑定真实 `settings.json`

处置：

- 将相关测试改为：
  - canonical sidecar assertions
  - skill-native activation assertions
  - zero-native-config-write assertions

## Verification

设计冻结后，后续实现至少应验证：

```bash
pytest -q tests/runtime_neutral/test_claude_preview_scaffold.py
pytest -q tests/runtime_neutral/test_cursor_managed_preview.py
pytest -q tests/runtime_neutral/test_windsurf_runtime_core.py
pytest -q tests/runtime_neutral/test_openclaw_runtime_core.py
pytest -q tests/runtime_neutral/test_installed_runtime_uninstall.py
git diff --check
```

并新增：

- explicit vibe skill activation tests
- host-settings canonical read tests
- idle-no-side-effects tests
- zero-native-config-write tests

## Completion Rules

- 不能把“skill-native activation”写成“宿主会在未显式调用时主动读取 sidecar”。
- 不能把“零宿主配置写入”写成“默认不写但允许静默回退”。
- 设计完成的标准是：
  - canonical state
  - receipt layer
  - skill-native entry
  - host grouping
  - migration waves
  - verification strategy
  全部明确。

## Cleanup

阶段结束后执行：

```powershell
pwsh -NoProfile -File scripts/governance/Invoke-NodeProcessAudit.ps1 -RepoRoot .
pwsh -NoProfile -File scripts/governance/Invoke-NodeZombieCleanup.ps1 -RepoRoot .
```

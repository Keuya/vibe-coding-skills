# Cross-Host Startup Regression Audit Plan

**日期**: 2026-03-30
**需求文档**: [../requirements/2026-03-30-cross-host-startup-regression-audit.md](../requirements/2026-03-30-cross-host-startup-regression-audit.md)
**Internal Grade**: `L`

## Audit Frames

将宿主分成两组：

1. 共享配置组
   - `claude-code`
   - `cursor`
   - 风险点：安装器会向真实 `settings.json` 写入 `vibeskills`

2. 非共享配置组
   - `windsurf`
   - `openclaw`
   - 风险点：主要是 runtime-core 写面是否误触 undocumented settings surface

## Execution Waves

### Wave 1: 静态写面审计

- 检查：
  - `scripts/install/install_vgo_adapter.py`
  - `scripts/install/Install-VgoAdapter.ps1`
  - `adapters/*/settings-map.json`
  - `adapters/*/closure.json`
  - 相关 runtime-neutral tests

目标：

- 明确每个宿主到底写哪些真实宿主面
- 先判断谁存在与 OpenCode 同类的“共享配置被修改”风险前提

### Wave 2: 真实 CLI 隔离探针

- 对 `claude-code`、`cursor`、`windsurf`、`openclaw` 分别建立隔离 HOME / host root
- 先跑宿主 CLI baseline
- 再执行对应 `install.* --host ...`
- 再跑同一宿主 CLI 的最小探针，观察是否出现配置解析失败或基础命令失效

优先证明面：

- `claude-code`: 能证明配置加载的最小非交互命令
- `cursor`: 能证明配置加载的最小非交互命令
- `windsurf`: 基础 CLI 启动/帮助 + 结构写面核对
- `openclaw`: `config validate` / `skills` / `agent` 之类不会触发外部依赖的探针

### Wave 3: 结论与必要修复

- 若无问题：
  - 输出逐宿主结论与证据
  - 标明验证边界

- 若发现问题：
  - 立即实现修复
  - 补测试/验证
  - 更新文档 truth

## Verification

至少执行：

```bash
pytest -q tests/runtime_neutral/test_claude_preview_scaffold.py
pytest -q tests/runtime_neutral/test_cursor_managed_preview.py
pytest -q tests/runtime_neutral/test_windsurf_runtime_core.py
pytest -q tests/runtime_neutral/test_openclaw_runtime_core.py
git diff --check
```

若新增审计脚本或修复，再补对应验证。

## Completion Rules

- 只有当每个宿主都拿到明确证据后，才能做“逐一排查完成”的表述。
- 对 CLI 面不足的宿主，必须用 `not-provable-with-current-cli-surface` 明示，而不是默认安全。

## Cleanup

阶段结束后执行：

```powershell
pwsh -NoProfile -File scripts/governance/Invoke-NodeProcessAudit.ps1 -RepoRoot .
pwsh -NoProfile -File scripts/governance/Invoke-NodeZombieCleanup.ps1 -RepoRoot .
```

并清理隔离 HOME / host root 临时目录。

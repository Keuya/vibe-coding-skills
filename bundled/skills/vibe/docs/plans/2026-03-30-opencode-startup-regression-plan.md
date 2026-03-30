# OpenCode Startup Regression Plan

**日期**: 2026-03-30
**需求文档**: [../requirements/2026-03-30-opencode-startup-regression.md](../requirements/2026-03-30-opencode-startup-regression.md)
**Internal Grade**: `L`

## Root Cause Snapshot

已在本地隔离环境稳定复现：

- 安装 `--host opencode` 后，安装器会写入真实 `opencode.json`
- 文件内容包含顶级 `vibeskills`
- OpenCode CLI 在读取该文件时直接报错：
  - `Configuration is invalid ...`
  - `Unrecognized key: "vibeskills"`

在同一目录里删除该文件后：

- `opencode debug config` 恢复正常
- `opencode debug skill` 恢复正常
- `opencode debug agent vibe-plan` 恢复正常

因此修复方向已经收敛：**停止接管真实 `opencode.json`，让它继续保持 host-managed。**

## Execution Waves

### Wave 1: 修安装写面

- 修改 `scripts/install/install_vgo_adapter.py`
- 修改 `scripts/install/Install-VgoAdapter.ps1`

目标：

- `materialize_host_settings` 不再为 `opencode` 写真实 `opencode.json`
- 保留：
  - `commands/**`
  - `command/**`
  - `agents/**`
  - `agent/**`
  - `opencode.json.example`
  - `.vibeskills/host-closure.json`
  - specialist wrapper

### Wave 2: 修测试与 smoke

- 修改 `tests/runtime_neutral/test_opencode_managed_preview.py`
- 修改 `tests/runtime_neutral/test_installed_runtime_uninstall.py`（如果依赖真实 `opencode.json`）
- 修改 `scripts/verify/runtime_neutral/opencode_preview_smoke.py`

目标：

- 不再把真实 `opencode.json` 视为安装成功条件
- 如果本机存在 `opencode` CLI，则 smoke 必须验证：
  - `debug config`
  - `debug skill`
  - `debug agent vibe-plan`

### Wave 3: 收口文档与 truth

- 修改 `docs/install/opencode-path.en.md`
- 修改 `docs/install/opencode-path.md`
- 必要时修改 README / install docs 中提到 OpenCode 写面的表述

目标：

- 确保文档与实际写面一致
- 明确真实 `opencode.json` 不由安装器创建或改写

## Verification

至少执行：

```bash
pytest -q tests/runtime_neutral/test_opencode_managed_preview.py
pytest -q tests/runtime_neutral/test_installed_runtime_uninstall.py -k opencode
python3 ./scripts/verify/runtime_neutral/opencode_preview_smoke.py --repo-root .
git diff --check
```

若本机可用 PowerShell，也补一轮：

```powershell
pwsh -NoProfile -File .\scripts\verify\vibe-uninstall-coherence-gate.ps1
```

## Cleanup

阶段结束后执行：

```powershell
pwsh -NoProfile -File scripts/governance/Invoke-NodeProcessAudit.ps1 -RepoRoot .
pwsh -NoProfile -File scripts/governance/Invoke-NodeZombieCleanup.ps1 -RepoRoot .
```

并清理 `.tmp` / 临时隔离目录残留。

# 安装路径：高级 host / lane 参考

> 普通用户优先看：
>
> - [`one-click-install-release-copy.md`](./one-click-install-release-copy.md)
> - [`manual-copy-install.md`](./manual-copy-install.md)

这份文档只解释当前真实支持边界，以及四个宿主对应的安装命令。

## 当前支持面

| 宿主 | 模式 | 默认根目录 | 当前口径 |
| --- | --- | --- | --- |
| `codex` | governed | `~/.codex` | 当前最完整路径 |
| `claude-code` | preview guidance | `~/.claude` | 预览指导，不是 full closure |
| `cursor` | preview guidance | `~/.cursor` | 预览指导，不是 full closure |
| `windsurf` | preview runtime-core | `~/.codeium/windsurf` | runtime-core 预览，不是 full closure |

`TargetRoot` 只是路径。
`HostId` / `--host` 才决定宿主语义。

## 推荐命令

默认全量安装：

### Codex

```powershell
pwsh -File .\scripts\bootstrap\one-shot-setup.ps1 -HostId codex -Profile full
pwsh -File .\check.ps1 -HostId codex -Profile full -Deep
```

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host codex --profile full
bash ./check.sh --host codex --profile full --deep
```

### Claude Code

```powershell
pwsh -File .\scripts\bootstrap\one-shot-setup.ps1 -HostId claude-code -Profile full
pwsh -File .\check.ps1 -HostId claude-code -Profile full -Deep
```

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host claude-code --profile full
bash ./check.sh --host claude-code --profile full --deep
```

### Cursor

```powershell
pwsh -File .\scripts\bootstrap\one-shot-setup.ps1 -HostId cursor -Profile full
pwsh -File .\check.ps1 -HostId cursor -Profile full -Deep
```

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host cursor --profile full
bash ./check.sh --host cursor --profile full --deep
```

### Windsurf

```powershell
pwsh -File .\scripts\bootstrap\one-shot-setup.ps1 -HostId windsurf -Profile full
pwsh -File .\check.ps1 -HostId windsurf -Profile full -Deep
```

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host windsurf --profile full
bash ./check.sh --host windsurf --profile full --deep
```

如果你要装“仅核心框架 + 可自定义添加治理”，把上面的 `full` 改成 `minimal`。

## 更新方式

如果本地还保留仓库，先更新仓库再重跑同一组命令：

```bash
git pull origin main
```

如果你跟随 tag 发布版本而不是 `main`，则：

```bash
git fetch --tags --force
git checkout vX.Y.Z
```

## 必须保持真实的边界

### Codex

- 这是 governed 路径
- hook 当前冻结；这不是安装失败
- `OPENAI_*` 只代表 Codex 基础在线 provider
- `VCO_AI_PROVIDER_*` 才是治理 AI 在线层的可选增强项

### Claude Code

- 这是 preview guidance
- 不覆盖真实 `~/.claude/settings.json`
- hook 当前冻结；这不是安装失败

### Cursor

- 这是 preview guidance
- 不覆盖真实 `~/.cursor/settings.json`
- 当前不接管 Cursor 的 host-native provider / MCP / hook 闭环

### Windsurf

- 这是 preview runtime-core
- 默认根目录是 `~/.codeium/windsurf`
- repo 当前只负责 shared runtime payload，以及按需物化 `mcp_config.json` 与 `global_workflows/`
- 不要把它描述成已完成登录、账号、provider、插件或 workspace-native 闭环

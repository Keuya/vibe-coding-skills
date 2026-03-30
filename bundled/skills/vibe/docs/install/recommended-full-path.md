# 多宿主安装命令参考

> 普通用户优先看：
>
> - [`one-click-install-release-copy.md`](./one-click-install-release-copy.md)
> - [`manual-copy-install.md`](./manual-copy-install.md)
> - [`openclaw-path.md`](./openclaw-path.md)
> - [`opencode-path.md`](./opencode-path.md)

这份文档汇总六个支持宿主对应的安装命令与默认根目录。

Linux / macOS 公共前置条件：

- shell 入口按 **macOS 自带 Bash 3.2** 兼容维护
- `python3` / `python` 需要满足 **Python 3.10+**
- 从 `zsh` 启动不是问题本身；真正关键是解析到的 `bash` / `python3` 版本

## 支持宿主与安装方式

| 宿主 | 安装方式 | 默认根目录 | 说明 |
| --- | --- | --- | --- |
| `codex` | one-shot setup + check | `~/.codex` | 默认推荐路径 |
| `claude-code` | one-shot setup + check | `~/.claude` | 支持安装与使用 |
| `cursor` | one-shot setup + check | `~/.cursor` | 支持安装与使用 |
| `windsurf` | one-shot setup + check | `~/.codeium/windsurf` | 支持安装与使用 |
| `openclaw` | one-shot setup + check | `OPENCLAW_HOME` 或 `~/.openclaw` | 宿主细节见 [`openclaw-path.md`](./openclaw-path.md) |
| `opencode` | direct install + check | `OPENCODE_HOME` 或 `~/.config/opencode` | 宿主细节见 [`opencode-path.md`](./opencode-path.md) |

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

### OpenClaw

```powershell
pwsh -File .\scripts\bootstrap\one-shot-setup.ps1 -HostId openclaw -Profile full
pwsh -File .\check.ps1 -HostId openclaw -Profile full -Deep
```

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host openclaw --profile full
bash ./check.sh --host openclaw --profile full --deep
```

### OpenCode

```powershell
pwsh -NoProfile -File .\install.ps1 -HostId opencode -Profile full
pwsh -NoProfile -File .\check.ps1 -HostId opencode -Profile full
```

```bash
bash ./install.sh --host opencode --profile full
bash ./check.sh --host opencode --profile full
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

## 安装后仍需你本地处理的内容

### Codex

- hook 当前冻结；这不是安装失败
- AI 治理 advice 的常见配置路径，优先使用：
  - `VCO_INTENT_ADVICE_API_KEY`
  - 可选 `VCO_INTENT_ADVICE_BASE_URL`
  - `VCO_INTENT_ADVICE_MODEL`
- 向量 diff（可选）：添加 `VCO_VECTOR_DIFF_API_KEY`/`VCO_VECTOR_DIFF_MODEL`（base URL 同样可选），缺失时 diff 会退化为文本片段

### Claude Code

- 当前提供支持的安装与使用路径
- 不覆盖真实 `~/.claude/settings.json`
- hook 当前冻结；这不是安装失败
- 如需 AI 治理 advice 的常见配套路径，优先使用 `VCO_INTENT_ADVICE_API_KEY` + 可选 `VCO_INTENT_ADVICE_BASE_URL` + `VCO_INTENT_ADVICE_MODEL`

### Cursor

- 当前提供支持的安装与使用路径
- 不覆盖真实 `~/.cursor/settings.json`
- Cursor 的宿主原生设置与扩展面仍按 Cursor 自身方式管理
- AI 治理 advice 使用 `VCO_INTENT_ADVICE_*` 及可选 `VCO_VECTOR_DIFF_*`，旧 `OPENAI_*` 不再自动回填

### Windsurf

- 默认根目录是 `~/.codeium/windsurf`
- repo 当前只负责 shared runtime payload，以及 `.vibeskills/host-settings.json` / `.vibeskills/host-closure.json` 这类 sidecar 状态
- Windsurf 宿主自身的本地设置仍按 Windsurf 自身方式管理

### OpenClaw

- 默认目标根目录是 `OPENCLAW_HOME` 或 `~/.openclaw`
- 宿主专页会展开 attach / copy / bundle 等细节
- OpenClaw 宿主自身的本地配置仍按 OpenClaw 自身方式管理

### OpenCode

- 默认目标根目录是 `OPENCODE_HOME`，否则是 `~/.config/opencode`
- direct install/check 会写入 skills、`.vibeskills/*` sidecar 与 `opencode.json.example`
- 真实 `opencode.json`、provider 凭据、plugin 安装和 MCP 信任仍按宿主自身方式管理
- 如需项目内隔离安装，使用 `--target-root ./.opencode`

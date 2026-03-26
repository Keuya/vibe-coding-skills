# 安装路径：高级 host / lane 参考

> 大多数用户先看三条主路径：
>
> - [`one-click-install-release-copy.md`](./one-click-install-release-copy.md)
> - [`manual-copy-install.md`](./manual-copy-install.md)
> - [`opencode-path.md`](./opencode-path.md)

这份文档只解释当前真实支持边界。

## 当前支持面

当前公开安装面覆盖三个宿主：

- `codex`
- `claude-code`
- `opencode`

其中：

- `codex`：正式推荐路径
- `claude-code`：preview guidance 路径
- `opencode`：preview adapter 路径

`TargetRoot` 只是安装路径。
`HostId` / `--host` 才决定宿主语义。

## 推荐命令

### Codex

```powershell
pwsh -File .\scripts\bootstrap\one-shot-setup.ps1 -HostId codex
pwsh -File .\check.ps1 -HostId codex -Profile full -Deep
```

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host codex
bash ./check.sh --host codex --profile full --deep
```

### Claude Code

```powershell
pwsh -File .\scripts\bootstrap\one-shot-setup.ps1 -HostId claude-code
pwsh -File .\check.ps1 -HostId claude-code -Profile full -Deep
```

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host claude-code
bash ./check.sh --host claude-code --profile full --deep
```

### OpenCode

```powershell
pwsh -NoProfile -File .\install.ps1 -HostId opencode
pwsh -NoProfile -File .\check.ps1 -HostId opencode
```

```bash
bash ./install.sh --host opencode
bash ./check.sh --host opencode
```

> OpenCode 当前不走 `one-shot-setup`。这条 lane 目前是 preview adapter，入口是 direct install + check。

## 必须说清楚的边界

### Codex

- 当前是最完整的 repo-governed 路径
- 建议范围只包括本地 `~/.codex` 设置、官方 MCP 注册和可选 CLI 依赖
- hook 当前因兼容性问题被冻结，不属于标准安装内容
- 如果需要在线模型能力，去 `~/.codex/settings.json` 的 `env` 或本地环境变量里配置 provider 字段
- 不要要求用户把密钥贴到聊天里

### Claude Code

- 这是 preview guidance，不是 full closure
- hook 当前因兼容性问题被冻结
- 安装器不再写 `settings.vibe.preview.json`
- 用户应自己打开 `~/.claude/settings.json`，只在 `env` 下补所需字段
- 常见字段：
  - `VCO_AI_PROVIDER_URL`
  - `VCO_AI_PROVIDER_API_KEY`
  - `VCO_AI_PROVIDER_MODEL`
- 如宿主连接需要，再补 `ANTHROPIC_BASE_URL`、`ANTHROPIC_AUTH_TOKEN`
- 不要要求用户把密钥贴到聊天里

### OpenCode

- 这是 preview adapter，不是 full closure
- 当前仓库会写 skills、command/agent 包装器以及 `opencode.json.example`
- 默认目标根目录是 `OPENCODE_HOME`，否则是 `~/.config/opencode`
- 如果你想把 preview 载荷隔离在项目目录，使用 `--target-root ./.opencode`
- 真正的 `opencode.json`、provider 凭据、plugin 安装和 MCP 信任仍然是 host-managed
- 如需细节，直接看 [`opencode-path.md`](./opencode-path.md)

## AI 治理层提示

对 `claude-code` 和 `opencode`，如果本地还没配置好 `url`、`apikey`、`model` 或等价 provider 字段，就不能描述成“已完成 online readiness”。

这些值必须由用户自己填进本地宿主配置或本地环境变量。

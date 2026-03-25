# 冷启动安装路径

这份文档只回答冷启动阶段最重要的问题：当前支持哪个宿主，以及每个宿主最短的 truth-first 安装路径。

## 一句话结论

当前公开支持四个宿主：

- `codex`
- `claude-code`
- `cursor`
- `windsurf`

其中：

- `codex`：governed 正式路径
- `claude-code`：preview guidance
- `cursor`：preview guidance
- `windsurf`：preview runtime-core

其他宿主当前都不应被描述成“已支持安装”。

## Codex

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host codex --profile full
bash ./check.sh --host codex --profile full --deep
```

你会得到：

- governed runtime payload
- 可选的 Codex 本地 settings / MCP 建议
- deep health check

你不会得到：

- hook 自动安装
- 自动完成治理 AI online readiness

后续动作：

- 看 `~/.codex/settings.json`
- 区分 `OPENAI_*` 与 `VCO_AI_PROVIDER_*`

## Claude Code

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host claude-code --profile full
bash ./check.sh --host claude-code --profile full --deep
```

你会得到：

- preview guidance payload
- preview health check

你不会得到：

- full closure
- 覆盖真实 `~/.claude/settings.json`
- hook 自动安装

## Cursor

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host cursor --profile full
bash ./check.sh --host cursor --profile full --deep
```

你会得到：

- preview guidance payload
- preview health check

你不会得到：

- full closure
- 覆盖真实 `~/.cursor/settings.json`
- Cursor host-native provider / MCP / hook 闭环

## Windsurf

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host windsurf --profile full
bash ./check.sh --host windsurf --profile full --deep
```

你会得到：

- shared runtime payload
- `~/.codeium/windsurf` 下的 runtime-core 预览安装结果
- 按需物化 `mcp_config.json`
- 按需物化 `global_workflows/`

你不会得到：

- full closure
- 宿主登录 / 账号 / provider / 插件闭环

## 冷启动阶段必须守住的边界

- `HostId` / `--host` 决定宿主语义
- hook 当前在公开支持面里统一冻结；这不是安装失败
- 本地 provider 字段没配好时，不能说环境已 online ready
- 不要要求用户把密钥贴到聊天里

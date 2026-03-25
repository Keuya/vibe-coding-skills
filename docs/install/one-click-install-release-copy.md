# 提示词安装（默认推荐）

这是当前默认推荐的公开安装入口。

## 先做两件事

1. 先确认宿主：`codex`、`claude-code`、`cursor`、`windsurf`
2. 再确认版本：`全量版本 + 可自定义添加治理` 或 `仅核心框架 + 可自定义添加治理`

对应的真实 profile 映射是：

- `全量版本 + 可自定义添加治理` -> `full`
- `仅核心框架 + 可自定义添加治理` -> `minimal`

## 直接复制的提示词

- [`prompts/full-version-install.md`](./prompts/full-version-install.md)
- [`prompts/framework-only-install.md`](./prompts/framework-only-install.md)
- [`prompts/full-version-update.md`](./prompts/full-version-update.md)
- [`prompts/framework-only-update.md`](./prompts/framework-only-update.md)

## 四个宿主的真实语义

| 宿主 | 模式 | 默认根目录 | 仓库当前负责什么 | 不应伪装成什么 |
| --- | --- | --- | --- | --- |
| `codex` | governed | `~/.codex` | governed runtime、settings/MCP 建议、deep check | hook 已自动完成、治理 AI online readiness 已完成 |
| `claude-code` | preview guidance | `~/.claude` | preview guidance、health check | full closure、真实 settings 已被接管 |
| `cursor` | preview guidance | `~/.cursor` | preview guidance、health check | full closure、Cursor host-native 闭环 |
| `windsurf` | preview runtime-core | `~/.codeium/windsurf` | shared runtime payload、按需物化 `mcp_config.json` / `global_workflows/`、health check | 登录/账号/provider/插件/workspace-native 闭环 |

## 你应该期待 AI 怎么做

AI 安装助手应当：

- 先问宿主，再问版本
- 只对四个已支持宿主执行安装
- 只把两个公开版本映射到真实 profile：`full` 或 `minimal`
- 按系统类型选择 `bash` 或 `pwsh`
- 不要求你把密钥贴到聊天里
- 区分“安装完成”和“在线能力就绪”
- 安装后给出简洁结果摘要和手动后续动作

## 常见 truth-first 口径

- `codex`：最完整，但 hook 仍冻结；`OPENAI_*` 与 `VCO_AI_PROVIDER_*` 不是一回事
- `claude-code`：preview guidance，不覆盖真实 `~/.claude/settings.json`
- `cursor`：preview guidance，不接管真实 `~/.cursor/settings.json`
- `windsurf`：preview runtime-core，只落地 runtime payload 与必要物化文件

## 安装完之后再做什么

如果你后面还要接自己的 workflow / skill：

- [`custom-workflow-onboarding.md`](./custom-workflow-onboarding.md)
- [`custom-skill-governance-rules.md`](./custom-skill-governance-rules.md)

如果你要看更底层的命令和边界：

- [`recommended-full-path.md`](./recommended-full-path.md)
- [`manual-copy-install.md`](./manual-copy-install.md)
- [`host-plugin-policy.md`](./host-plugin-policy.md)

# 宿主插件与宿主配置策略

这份文档只回答三件事：

- 哪些宿主在当前公开支持面内
- 仓库当前自动处理什么
- 哪些能力仍必须由宿主侧本地完成

## 当前公开支持面

- `codex`
- `claude-code`
- `cursor`
- `windsurf`

其他代理当前不应被描述成“已有官方安装闭环”。

## 总体原则

- 先把 repo-governed payload 安装好
- 再按真实需求补宿主侧配置
- 没有被仓库稳定、公开、可验证接管的能力，不要写成默认安装要求

## Codex

- 当前最完整路径
- 围绕本地 settings、MCP 和可选 CLI 做建议
- hook 当前冻结；这不是安装失败

## Claude Code

- preview guidance
- 不靠“补一堆宿主插件”来完成接入
- 不覆盖真实 `~/.claude/settings.json`
- hook 当前冻结；这不是安装失败

## Cursor

- preview guidance
- 不覆盖真实 `~/.cursor/settings.json`
- 不接管 Cursor host-native plugin / provider / MCP 闭环
- hook 当前冻结；这不是安装失败

## Windsurf

- preview runtime-core
- 默认根目录是 `~/.codeium/windsurf`
- repo 当前只负责 shared runtime payload，以及按需物化 `mcp_config.json` 和 `global_workflows/`
- 不接管登录、账号、provider、插件或 workspace-native 闭环

## 推荐的社区表述

- 当前版本支持 `codex`、`claude-code`、`cursor`、`windsurf`
- `codex` 走 governed 路径
- `claude-code` / `cursor` 走 preview guidance
- `windsurf` 走 preview runtime-core
- hooks 在当前公开支持面里统一冻结；这不是用户安装失败
- provider 的 `url` / `apikey` / `model` 由用户在本地配置，不要要求用户贴到聊天里

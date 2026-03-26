# 提示词安装（默认推荐）

这是当前默认推荐的公开安装入口。

## 先选两件事

1. 先确认宿主：`codex`、`claude-code`、`cursor`、`windsurf`、`openclaw`、`opencode`
2. 再确认版本：`全量版本 + 可自定义添加治理` 或 `仅核心框架 + 可自定义添加治理`

公开版本映射到：

- `全量版本 + 可自定义添加治理` -> `full`
- `仅核心框架 + 可自定义添加治理` -> `minimal`

## 复制对应提示词

- [`prompts/full-version-install.md`](./prompts/full-version-install.md)
- [`prompts/framework-only-install.md`](./prompts/framework-only-install.md)
- [`prompts/full-version-update.md`](./prompts/full-version-update.md)
- [`prompts/framework-only-update.md`](./prompts/framework-only-update.md)

## 宿主专用说明

- `openclaw` 继续按 preview runtime-core 路径处理，细节看 [`openclaw-path.md`](./openclaw-path.md)
- `opencode` 当前走独立的 preview adapter 路径，不复用这组 one-shot 提示词；直接看 [`opencode-path.md`](./opencode-path.md)

## 需要时再继续看

- 仅核心框架命令路径：
  - [`minimal-path.md`](./minimal-path.md)
- 更底层的命令和边界：
  - [`recommended-full-path.md`](./recommended-full-path.md)
  - [`manual-copy-install.md`](./manual-copy-install.md)
  - [`host-plugin-policy.md`](./host-plugin-policy.md)
  - [`openclaw-path.md`](./openclaw-path.md)
  - [`opencode-path.md`](./opencode-path.md)
- 后续接自己的 workflow / skill：
  - [`custom-workflow-onboarding.md`](./custom-workflow-onboarding.md)
  - [`custom-skill-governance-rules.md`](./custom-skill-governance-rules.md)

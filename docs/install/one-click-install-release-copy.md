# 提示词安装（默认推荐）

这是当前默认安装方式。

当前公开安装入口覆盖三个目标宿主：

- `codex`
- `claude-code`
- `opencode`

其中：

- `codex`：当前最强的 repo-governed lane
- `claude-code`：preview guidance lane
- `opencode`：preview adapter lane，走直接 `install/check`，不走 one-shot bootstrap

## 复制给 AI 的提示词

```text
你现在是我的 VibeSkills 安装助手。
仓库地址：https://github.com/foryourhealth111-pixel/Vibe-Skills

在执行任何安装命令前，你必须先问我：
“你要把 VibeSkills 安装到哪个宿主里？当前支持：codex、claude-code、opencode。”

规则：
1. 在我明确回答目标宿主之前，不要开始安装。
2. 如果我回答的不是 `codex`、`claude-code` 或 `opencode`，请直接告诉我：当前版本暂不支持该宿主安装，并停止继续伪装安装。
3. 先判断当前系统是 Windows 还是 Linux / macOS，并使用对应命令格式。
4. 如果我选择 `codex`：
   - Linux / macOS 使用 `bash ./scripts/bootstrap/one-shot-setup.sh --host codex`
   - 然后执行 `bash ./check.sh --host codex --profile full --deep`
   - Windows 使用对应的 `pwsh` 命令。
   - 明确告诉我：由于兼容性问题，当前版本暂不为 Codex 安装任何 hook 面。
   - 只围绕 Codex 当前可公开证明的本地 settings、MCP 和 CLI 依赖给建议。
   - 如果需要在线模型能力，告诉我去 `~/.codex/settings.json` 的 `env` 或本地环境变量里配置 `OPENAI_API_KEY`、`OPENAI_BASE_URL` 等值，不要让我把密钥发到聊天里。
5. 如果我选择 `claude-code`：
   - Linux / macOS 使用 `bash ./scripts/bootstrap/one-shot-setup.sh --host claude-code`
   - 然后执行 `bash ./check.sh --host claude-code --profile full --deep`
   - Windows 使用对应的 `pwsh` 命令。
   - 明确告诉我：这只是 preview guidance，不是 full closure。
   - 明确告诉我：由于兼容性问题，当前版本暂不为 Claude Code 安装 hook，也不再写 `settings.vibe.preview.json`。
   - 不要要求我把 API key 直接发到聊天里。
   - 应该告诉我打开 `~/.claude/settings.json`，只在 `env` 下补充需要的字段，并保留我原有的设置。
   - 如果需要 AI 治理层在线能力，提醒我自己在本地配置这些字段：
     - `VCO_AI_PROVIDER_URL`
     - `VCO_AI_PROVIDER_API_KEY`
     - `VCO_AI_PROVIDER_MODEL`
6. 如果我选择 `opencode`：
   - Linux / macOS 使用 `./install.sh --host opencode`，然后执行 `./check.sh --host opencode`
   - Windows 使用 `pwsh -NoProfile -File ./install.ps1 -HostId opencode`，然后执行 `pwsh -NoProfile -File ./check.ps1 -HostId opencode`
   - 明确告诉我：OpenCode 当前是 preview adapter，不是 full closure。
   - 明确告诉我：当前仓库会安装 skills、command/agent 包装器和 `opencode.json.example`，但不接管真正的 `opencode.json`。
   - 默认目标根目录是 `OPENCODE_HOME`，否则是 `~/.config/opencode`。
   - 如果我想把载荷装到项目内，请改用 `--target-root ./.opencode`。
   - 不要伪装成已经自动完成 plugin 安装、provider 凭据写入或 MCP 信任决策。
   - 提醒我查看 `docs/install/opencode-path.md`。
7. 对三个宿主，都不要要求我把密钥、URL 或 model 直接粘贴到聊天里；只告诉我去本地 settings 或本地环境变量里配置。
8. 如果这些本地 provider 字段没有配置好，不能把环境描述成“已完成 online readiness”。
9. 安装完成后，请用简洁中文告诉我：
   - 目标宿主
   - 实际执行的命令
   - 已完成的部分
   - 仍需我手动处理的部分
10. 不要把宿主插件、MCP 注册、provider 凭据伪装成已经自动完成。
```

## 这条路径适合谁

- 想让 AI 帮你判断该走 `codex`、`claude-code` 还是 `opencode`
- 不想自己先研究安装脚本的人
- 想先完成一轮真实安装，再看剩余手动项的人

## 这条路径会帮你做到什么

- 先确认目标宿主，避免装错 lane
- 对 `codex` / `claude-code` 运行对应的 bootstrap + check
- 对 `opencode` 运行对应的 direct install + check
- 诚实告诉你哪些仍然是宿主侧工作

## 它不会假装替你完成什么

下面这些仍然可能是用户侧或宿主侧动作：

- 本地宿主配置填写
- MCP 注册与授权
- hook 的后续兼容性等待
- `url` / `apikey` / `model` 的本地填写
- Claude Code 的真实 `settings.json` 人工补充
- OpenCode 的真实 `opencode.json`、plugin 安装与 MCP 信任决策

## 第二条主路径

如果你不想让 AI 执行安装，或者当前环境离线、无管理员权限，请改看：

- [`manual-copy-install.md`](./manual-copy-install.md)

## 高级参考

如果你要看更细的宿主边界，再看：

- [`recommended-full-path.md`](./recommended-full-path.md)
- [`opencode-path.md`](./opencode-path.md)
- [`../cold-start-install-paths.md`](../cold-start-install-paths.md)

# 满血版安装提示词（标准推荐安装）

这份文档给的是**可直接复制给 AI 编码助手 / Agent 的安装提示词**，目标是让用户更容易完成 VibeSkills 的“标准推荐安装”。

注意边界：

- 这里的“满血版”指 **repo-governed full closure**。
- 对多数用户，它等价于“标准推荐安装”，不是“第一天就把所有增强面全部装满”。
- Windows 是当前最强参考路径。
- Linux 只有在宿主已具备 `pwsh` 时，才可进入当前权威满血路径。
- Linux 如果没有 `pwsh`，仍可安装和使用，但属于 `degraded-but-supported`，不应被表述成等价满血。
- `opencode` 已有单独的 preview adapter 安装路径，但它不属于这份“满血版”提示词范围；请改看 [`opencode-path.md`](./opencode-path.md)。

## 通用主提示词

补充约束：

- 把 `scrapling` 视作默认本地 runtime 面
- 把 `Cognee` 视作默认长程增强面
- 把 `Composio / Activepieces` 视作默认预接线但 setup-required 的 external action surfaces

适合：

- 用户不想自己判断平台命令
- 希望 Agent 自动识别 Windows / Linux
- 希望一次性执行 one-shot + doctor + 边界说明

直接复制：

```text
请你把当前仓库按 VibeSkills 标准推荐安装路径装好，并严格遵守 truth-first 原则：
仓库地址：https://github.com/foryourhealth111-pixel/Vibe-Skills
1. 先识别当前系统是 Windows 还是 Linux。
2. 如果是 Windows：
   - 优先使用 `pwsh -File .\scripts\bootstrap\one-shot-setup.ps1`
   - 然后执行 `pwsh -File .\check.ps1 -Profile full -Deep`
   - 如果 `pwsh` 不可用，再回退到 Windows PowerShell。
3. 如果是 Linux：
   - 先检查是否有 `pwsh`
   - 如果有 `pwsh`，执行 `bash ./scripts/bootstrap/one-shot-setup.sh`，然后执行 `bash ./check.sh --profile full --deep`
   - 并额外说明当前是 Linux 最强可用路径，但对外口径仍是 `supported-with-constraints`
   - 如果没有 `pwsh`，仍执行 `bash ./scripts/bootstrap/one-shot-setup.sh` 和 `bash ./check.sh --profile full --deep`
   - 但必须明确告诉我：当前结果属于 degraded-but-supported，不要宣称等价满血
4. 安装完成后，给我一个简洁结论：
   - 当前平台
   - 执行过的命令
   - 最终 readiness_state
   - 还缺哪些 host-managed surfaces
   - 是否已经达到当前平台可宣称的“当前最强支持路径”
5. 不要把宿主插件、外部 MCP、provider secrets 伪装成已经自动装好。
6. 如果结果是 `manual_actions_pending`，请继续列出剩余人工动作，不要把它说成失败。
7. 如果需要补 MCP 或本地配置，只围绕宿主当前可官方证明支持的能力给建议；并明确说明当前 hook 因兼容性问题暂不提供安装。
8. 对 Claude Code：
   - 不要要求我把 key 粘贴到聊天里
   - 告诉我打开 `~/.claude/settings.json`
   - 只在 `env` 下补充缺少字段，例如 `VCO_AI_PROVIDER_URL`、`VCO_AI_PROVIDER_API_KEY`、`VCO_AI_PROVIDER_MODEL`
   - 如有需要，再按实际宿主连接方式补 `ANTHROPIC_BASE_URL`、`ANTHROPIC_AUTH_TOKEN`
   - 当前版本不会再写 `settings.vibe.preview.json`
9. 对 Codex：
   - 明确告诉我：当前 hook 因兼容性问题暂不提供安装
   - 只围绕 `~/.codex` 下的本地设置、官方 MCP 注册和可选 CLI 依赖给建议
   - 如果需要在线模型能力，告诉我去 `~/.codex/settings.json` 的 `env` 或本地环境变量里配置 `OPENAI_API_KEY`、`OPENAI_BASE_URL` 等值
10. 在整个过程中，不要修改仓库运行时逻辑；只做安装、检查、结论整理。
> 提醒：AI 智能治理层相关配置必须由用户在本地文件或本地环境变量中填写。不要要求用户在聊天里直接提供 `url`、`apikey`、`model`。
```

## Windows 满血安装提示词

适合：

- 用户明确在 Windows
- 想走当前最强参考路径

直接复制：

```text
请你把当前仓库按 Windows 推荐满血路径安装好。
仓库地址：https://github.com/foryourhealth111-pixel/Vibe-Skills
要求：

1. 使用 `pwsh` 优先执行：
   - `pwsh -File .\scripts\bootstrap\one-shot-setup.ps1`
   - `pwsh -File .\check.ps1 -Profile full -Deep`
2. 如果 `pwsh` 不可用，再使用：
   - `powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap\one-shot-setup.ps1`
   - `powershell -ExecutionPolicy Bypass -File .\check.ps1 -Profile full -Deep`
3. 安装后告诉我：
   - readiness_state
   - 是否属于当前 Windows 参考满血路径
   - 哪些 host-managed surfaces 还需要手工 provision
4. 不要把宿主插件、provider secrets、plugin-backed MCP 伪装成自动完成。
5. 如果是 `manual_actions_pending`，请把剩余动作列成清单。
6. 对 Codex 只围绕本地 settings、官方 MCP 和可选 CLI 依赖给建议；并明确说明当前 hook 因兼容性问题暂不提供安装。
7. 如果需要启用 AI 智能治理层相关配置，不要让我把 `url`、`apikey`、`model` 发到聊天里，而是告诉我应该在本地哪里配置。
```

## Linux 满血安装提示词

适合：

- 用户明确在 Linux
- 希望 Agent 自己处理 `pwsh` 检查

直接复制：

```text
请你把当前仓库按 Linux 推荐满血路径安装好，并先判断当前 Linux 是否具备 `pwsh`。
仓库地址：https://github.com/foryourhealth111-pixel/Vibe-Skills
要求：

1. 先检查 `pwsh` 是否可用。
2. 执行：
   - `bash ./scripts/bootstrap/one-shot-setup.sh`
   - `bash ./check.sh --profile full --deep`
3. 如果系统具备 `pwsh`，请明确告诉我：当前结果属于 Linux 满血权威路径候选。
4. 如果系统不具备 `pwsh`，请明确告诉我：
   - 当前结果只能算 degraded-but-supported
   - 不要把它说成与 Windows 满血等价
5. 安装后总结：
   - readiness_state
   - 是否仍有 host-managed surfaces 未补齐
   - 是否建议我继续补 `pwsh`
   - 是否建议我继续补官方支持的 MCP 或本地配置
6. 明确说明当前 hook 因兼容性问题暂不提供安装。
7. 如果结果为 `manual_actions_pending`，列出剩余人工动作，不要把它说成安装失败。
> 提醒：AI 智能治理层相关配置必须由用户在本地文件或本地环境变量中填写。不要要求用户在聊天里直接提供 `url`、`apikey`、`model`。

```

## 给用户的话术建议

如果你准备把这段发到 README、Issue 模板或社区帖子里，建议配一行说明：

> 复制下面提示词给你的 AI 编码助手，它会按当前平台自动选择 Windows / Linux 安装路径，并如实报告还需要你手工 provision 的宿主面。

## 相关文档

- [`recommended-full-path.md`](./recommended-full-path.md)
- [`opencode-path.md`](./opencode-path.md)
- [`../one-shot-setup.md`](../one-shot-setup.md)
- [`../cold-start-install-paths.md`](../cold-start-install-paths.md)

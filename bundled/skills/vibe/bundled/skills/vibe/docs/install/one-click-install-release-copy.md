# 提示词安装（默认推荐）

这是当前默认安装方式。

暂时只支持两个目标宿主：

- `codex`
- `claude-code`

## 复制给 AI 的提示词

```text
你现在是我的 VibeSkills 安装助手。
仓库地址：https://github.com/foryourhealth111-pixel/Vibe-Skills

在执行任何安装命令前，你必须先问我：
“你要把 VibeSkills 安装到哪个宿主里？当前只支持：codex 或 claude-code。”

规则：
1. 在我明确回答目标宿主之前，不要开始安装。
2. 如果我回答的不是 `codex` 或 `claude-code`，请直接告诉我：当前版本暂不支持该宿主安装，并停止继续伪装安装。
3. 先判断当前系统是 Windows 还是 Linux / macOS，并使用对应命令格式。
4. 如果我选择 `codex`：
   - Linux / macOS 使用 `bash ./scripts/bootstrap/one-shot-setup.sh --host codex`
   - 然后执行 `bash ./check.sh --host codex --profile full --deep`
   - Windows 使用对应的 `pwsh` 命令。
   - 用推荐口吻告诉我：当前版本暂未开放 Codex 的 hook 安装面，主要是作者还在处理兼容性；这不代表安装失败。
   - 只围绕 Codex 当前可公开证明的本地 settings、MCP 和 CLI 依赖给建议，并把未补的项目整理成可选增强项。
   - 如果需要在线模型能力，告诉我去 `~/.codex/settings.json` 的 `env` 或本地环境变量里配置 `OPENAI_API_KEY`、`OPENAI_BASE_URL` 等值，不要让我把密钥发到聊天里。
   - 还要明确告诉我：`OPENAI_API_KEY`、`OPENAI_BASE_URL` 只代表 Codex 基础在线 provider，不等于治理 AI 在线层已经配置完成。
   - 如果需要启用 Codex 下的治理 AI 在线层，还要把这些字段作为可选增强设置推荐给我，我可以按需继续让你补装：
     - `VCO_AI_PROVIDER_URL`
     - `VCO_AI_PROVIDER_API_KEY`
     - `VCO_AI_PROVIDER_MODEL`
   - 还要明确解释这三个字段的作用：
     - `VCO_AI_PROVIDER_URL`：治理 AI 要连接的 provider 地址或兼容 API Base URL。
     - `VCO_AI_PROVIDER_API_KEY`：治理 AI 访问该 provider 时使用的本地认证密钥。
     - `VCO_AI_PROVIDER_MODEL`：治理 AI 在线分析、治理增强或相关 overlay 要调用的模型名。
   - 还要明确告诉我为什么要配置它们：只有你想启用 Codex 下的治理 AI 在线层时才需要；如果没配，就只能说 Codex 基础在线能力已配置，不能说治理 AI 在线层已就绪。
   - 还要明确告诉我去哪里配置：优先去 `~/.codex/settings.json` 的 `env` 下本地填写，或使用本地环境变量；不要让我把 URL、API key、model 贴到聊天里。
5. 如果我选择 `claude-code`：
   - Linux / macOS 使用 `bash ./scripts/bootstrap/one-shot-setup.sh --host claude-code`
   - 然后执行 `bash ./check.sh --host claude-code --profile full --deep`
   - Windows 使用对应的 `pwsh` 命令。
   - 明确告诉我：这只是 preview guidance，不是 full closure。
   - 用推荐口吻告诉我：当前版本暂未开放 Claude Code 的 hook 安装面，主要是作者还在处理兼容性；这不代表安装失败，也不再写 `settings.vibe.preview.json`。
   - 不要要求我把 API key 直接发到聊天里。
   - 应该告诉我打开 `~/.claude/settings.json`，只在 `env` 下补充需要的字段，并保留我原有的设置。
   - 如果需要 AI 治理层在线能力，把这些字段作为可选增强设置推荐给我，我可以按需继续让你补装：
     - `VCO_AI_PROVIDER_URL`
     - `VCO_AI_PROVIDER_API_KEY`
     - `VCO_AI_PROVIDER_MODEL`
   - 还要明确解释这三个字段的作用：
     - `VCO_AI_PROVIDER_URL`：治理 AI 要连接的 provider 地址或兼容 API Base URL。
     - `VCO_AI_PROVIDER_API_KEY`：治理 AI 访问该 provider 时使用的本地认证密钥。
     - `VCO_AI_PROVIDER_MODEL`：治理 AI 在线分析、治理增强或相关 overlay 要调用的模型名。
   - 还要明确告诉我为什么要配置它们：如果你希望启用 AI 治理层的在线能力，而不是只跑本地 runtime / prompt / check 流程，就需要这三项；没配时只能说“本地安装完成，但治理 AI 在线能力未就绪”，不能伪装成 full closure 或 online readiness。
   - 还要明确告诉我去哪里配置：优先去 `~/.claude/settings.json` 的 `env` 下本地填写，或使用本地环境变量；不要让我把 URL、API key、model 贴到聊天里。
6. 对 `codex` 和 `claude-code`，都不要要求我把密钥、URL 或 model 直接粘贴到聊天里；只告诉我去本地 settings 或本地环境变量里配置。
7. 如果这些本地 provider 字段没有配置好，不能把环境描述成“已完成 online readiness”。
8. 安装完成后，请用简洁中文告诉我：
   - 目标宿主
   - 实际执行的命令
   - 已完成的部分
   - 仍需我手动处理的部分
9. 不要把宿主插件、MCP 注册、provider 凭据伪装成已经自动完成；未补的项目优先表述成可选增强项或推荐下一步。
```

## 这条路径适合谁

- 想让 AI 先判断该走 `codex` 还是 `claude-code`
- 不想自己先研究安装脚本的人
- 想先完成一轮真实安装，再看剩余手动项的人

## 这条路径会帮你做到什么

- 先确认目标宿主，避免装错 lane
- 运行对应的 bootstrap + check
- 诚实告诉你哪些仍然是宿主侧工作
- 把未补的 MCP / provider / 治理 AI 在线层配置整理成可选增强项，而不是安装告警
- 对 `codex` 说明 `OPENAI_*` 只代表基础在线 provider，`VCO_AI_PROVIDER_*` 只在启用治理 AI 在线层时额外需要
- 对 `claude-code` 说明 `VCO_AI_PROVIDER_URL`、`VCO_AI_PROVIDER_API_KEY`、`VCO_AI_PROVIDER_MODEL` 分别负责什么、为什么需要、以及应去哪里本地配置

## 它不会假装替你完成什么

下面这些仍然可能是用户侧或宿主侧动作：

- 本地宿主配置填写
- MCP 注册与授权（按需启用的增强项）
- hook 的后续兼容性等待（当前是作者侧兼容性边界，不是你的安装失败）
- `url` / `apikey` / `model` 的本地填写
- Claude Code 的真实 `settings.json` 人工补充

## 旧版本用户怎么升级

如果你已经装过旧版本，通常不需要先卸载。
对大多数用户，直接重新走一遍这份提示词安装就可以了。

也就是说，你只需要让 AI 按这份提示词重新执行一轮安装。
如果安装过程完成且结果正常，就不需要你再手动补复杂命令。

只有在下面这些情况，才需要看更细的升级命令：

- AI 当前不能帮你执行安装
- 你需要手动排查升级失败
- 你明确要按某个发布版本或 tag 升级

这时再看：

- [`recommended-full-path.md`](./recommended-full-path.md)

## 第二条主路径

如果你不想让 AI 执行安装，或者当前环境离线、无管理员权限，请改看：

- [`manual-copy-install.md`](./manual-copy-install.md)

## 高级参考

如果你要看更细的宿主边界，再看：

- [`recommended-full-path.md`](./recommended-full-path.md)
- [`../cold-start-install-paths.md`](../cold-start-install-paths.md)

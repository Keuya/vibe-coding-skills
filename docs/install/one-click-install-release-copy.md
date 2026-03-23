# 提示词安装（默认推荐）

这是当前默认推荐的公开安装方式。

对外公开版本收束为两种：

- `全量版本 + 可自定义添加治理`
- `仅核心框架 + 可自定义添加治理`

当前脚本层仍使用 lane 实现：

- `全量版本 + 可自定义添加治理` 对应 `full`
- `仅核心框架 + 可自定义添加治理` 对应 `framework-only`

`workflow` 仍保留为兼容 / 过渡 lane，但不再作为普通用户首页主推荐版本。

暂时只支持两个目标宿主：

- `codex`
- `claude-code`

## 先看结论

如果你不想先研究 lane / profile / host 细节，就按下面理解：

- 想要开箱即用，并且后面还能继续接自己的 workflow / skill governance：选 `全量版本 + 可自定义添加治理`
- 想只保留治理框架，后面自己慢慢接 workflow / skill governance：选 `仅核心框架 + 可自定义添加治理`

对外只讲这两个版本，不要求普通用户先理解 `workflow` / `full` / `framework-only`。

## 快速选择

| 公开版本 | 实际 profile | 你会得到什么 | 不会直接得到什么 | 适合谁 |
| --- | --- | --- | --- | --- |
| `全量版本 + 可自定义添加治理` | `full` | `vibe` runtime、canonical router、完整治理框架、默认 workflow core、扩展 bundled 能力面 | 自动完成的 hook、自动完成的 provider / MCP / online readiness | 想开箱即用，也想后续继续纳管自定义 workflow 的用户 |
| `仅核心框架 + 可自定义添加治理` | `framework-only` | `vibe` runtime、canonical router、install/check/doctor、路由与 overlay/policy 治理骨架 | 默认 workflow core、大量 bundled workflow / domain skills | 只想先拿治理底座，后续自己逐步接 workflow / skill 的用户 |

## 你只需要做什么

1. 选择宿主：`codex` 或 `claude-code`
2. 选择公开版本：`全量版本 + 可自定义添加治理` 或 `仅核心框架 + 可自定义添加治理`
3. 复制下面对应提示词给 AI，让 AI 执行安装

安装完成后，如果你还要接自己的 workflow / skill，再继续看：

- [`custom-workflow-onboarding.md`](./custom-workflow-onboarding.md)
- [`custom-skill-governance-rules.md`](./custom-skill-governance-rules.md)

## 版本说明

### 1. 全量版本 + 可自定义添加治理

你会得到：

- `vibe` runtime 与 canonical router
- 完整治理框架
- 默认工作流核心
- 扩展 bundled 能力面
- 后续继续接入你自己的 custom workflow / custom skill governance 的入口

适合：

- 希望开箱即用
- 希望后面继续纳管自己的工作流
- 不想先自己补太多基础 workflow skill

### 2. 仅核心框架 + 可自定义添加治理

你会得到：

- `vibe` runtime 与 canonical router
- install / check / doctor 等治理面
- 路由、执行等级、overlay / policy 治理骨架
- 后续继续接入自定义 workflow / custom governance 的底座

你不会直接得到：

- 默认工作流核心的开箱即用体验
- 大量 bundled workflow / domain skills

适合：

- 只想保留治理框架
- 希望自己决定后续接入哪些 workflow / skill
- 能接受后续自己继续补接 custom workflow manifest 与治理规则

## 复制给 AI 的提示词

### 提示词 A：全量版本 + 可自定义添加治理

适合：

- 希望先装好再用
- 不想先自己补 workflow core
- 后面还想继续接入自己的治理

安装结果应按 truth-first 口径描述为：

- lane 已完成 / 当前 lane 可用
- 哪些宿主手工项仍待补
- 哪些 online / provider / MCP 项只是可选增强
- 不能伪装成 hook、online readiness、治理 AI online layer 已全部完成

```text
你现在是我的 VibeSkills 安装助手。
仓库地址：https://github.com/foryourhealth111-pixel/Vibe-Skills

在执行任何安装命令前，你必须先问我：
“你要把 VibeSkills 安装到哪个宿主里？当前只支持：codex 或 claude-code。”

在我回答宿主后，你还必须再问我：
“你要安装哪个公开版本？当前只支持：全量版本+可自定义添加治理，或 仅核心框架+可自定义添加治理。”

规则：
1. 在我明确回答目标宿主之前，不要开始安装。
2. 在我明确回答公开版本之前，不要开始安装。
3. 如果我回答的宿主不是 `codex` 或 `claude-code`，请直接告诉我：当前版本暂不支持该宿主安装，并停止继续伪装安装。
4. 如果我回答的公开版本不是“全量版本+可自定义添加治理”或“仅核心框架+可自定义添加治理”，请直接告诉我：当前公开安装说明暂不支持该版本名，并停止继续伪装安装。
5. 先判断当前系统是 Windows 还是 Linux / macOS，并使用对应命令格式。
6. 这次如果我选择的是“全量版本+可自定义添加治理”，你必须把它映射到安装 profile：`full`。
7. 如果我选择 `codex`：
   - Linux / macOS 使用 `bash ./scripts/bootstrap/one-shot-setup.sh --host codex --profile full`
   - 然后执行 `bash ./check.sh --host codex --profile full --deep`
   - Windows 使用对应的 `pwsh` 命令。
   - 明确告诉我：由于兼容性问题，当前版本暂不为 Codex 安装任何 hook。
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
8. 如果我选择 `claude-code`：
   - Linux / macOS 使用 `bash ./scripts/bootstrap/one-shot-setup.sh --host claude-code --profile full`
   - 然后执行 `bash ./check.sh --host claude-code --profile full --deep`
   - Windows 使用对应的 `pwsh` 命令。
   - 明确告诉我：这只是 preview guidance，不是 full closure。
   - 明确告诉我：由于兼容性问题，当前版本暂不为 Claude Code 安装 hook，也不再写 `settings.vibe.preview.json`。
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
9. 对 `codex` 和 `claude-code`，都不要要求我把密钥、URL 或 model 直接粘贴到聊天里；只告诉我去本地 settings 或本地环境变量里配置。
10. 如果这些本地 provider 字段没有配置好，不能把环境描述成“已完成 online readiness”。
11. 安装完成后，请用简洁中文告诉我：
   - 目标宿主
   - 公开版本
   - 实际映射的 profile
   - 实际执行的命令
   - 已完成的部分
   - 仍需我手动处理的部分
12. 不要把宿主插件、MCP 注册、provider 凭据伪装成已经自动完成；未补的项目优先表述成可选增强项或推荐下一步。
```

### 提示词 B：仅核心框架 + 可自定义添加治理

适合：

- 只想保留框架、检查面、路由与治理骨架
- 后续准备自己接 workflow / skill governance
- 不要求默认 workflow core 立即可用

安装结果应按 truth-first 口径描述为：

- 已拿到治理框架底座
- 不等于默认 workflow core 已齐备
- 不等于自定义 workflow 已接入完成
- 不等于治理 AI online layer 已就绪

```text
你现在是我的 VibeSkills 安装助手。
仓库地址：https://github.com/foryourhealth111-pixel/Vibe-Skills

在执行任何安装命令前，你必须先问我：
“你要把 VibeSkills 安装到哪个宿主里？当前只支持：codex 或 claude-code。”

在我回答宿主后，你还必须再问我：
“你要安装哪个公开版本？当前只支持：全量版本+可自定义添加治理，或 仅核心框架+可自定义添加治理。”

规则：
1. 在我明确回答目标宿主之前，不要开始安装。
2. 在我明确回答公开版本之前，不要开始安装。
3. 如果我回答的宿主不是 `codex` 或 `claude-code`，请直接告诉我：当前版本暂不支持该宿主安装，并停止继续伪装安装。
4. 如果我回答的公开版本不是“全量版本+可自定义添加治理”或“仅核心框架+可自定义添加治理”，请直接告诉我：当前公开安装说明暂不支持该版本名，并停止继续伪装安装。
5. 先判断当前系统是 Windows 还是 Linux / macOS，并使用对应命令格式。
6. 这次如果我选择的是“仅核心框架+可自定义添加治理”，你必须把它映射到安装 profile：`framework-only`。
7. 如果我选择 `codex`：
   - Linux / macOS 使用 `bash ./scripts/bootstrap/one-shot-setup.sh --host codex --profile framework-only`
   - 然后执行 `bash ./check.sh --host codex --profile framework-only --deep`
   - Windows 使用对应的 `pwsh` 命令。
   - 明确告诉我：由于兼容性问题，当前版本暂不为 Codex 安装任何 hook。
   - 只围绕 Codex 当前可公开证明的本地 settings、MCP 和 CLI 依赖给建议。
   - 如果需要在线模型能力，告诉我去 `~/.codex/settings.json` 的 `env` 或本地环境变量里配置 `OPENAI_API_KEY`、`OPENAI_BASE_URL` 等值，不要让我把密钥发到聊天里。
   - 还要明确告诉我：`OPENAI_API_KEY`、`OPENAI_BASE_URL` 只代表 Codex 基础在线 provider，不等于治理 AI 在线层已经配置完成。
   - 如果需要启用 Codex 下的治理 AI 在线层，还要提醒我自己在本地额外配置这些字段：
     - `VCO_AI_PROVIDER_URL`
     - `VCO_AI_PROVIDER_API_KEY`
     - `VCO_AI_PROVIDER_MODEL`
   - 还要明确解释这三个字段的作用：
     - `VCO_AI_PROVIDER_URL`：治理 AI 要连接的 provider 地址或兼容 API Base URL。
     - `VCO_AI_PROVIDER_API_KEY`：治理 AI 访问该 provider 时使用的本地认证密钥。
     - `VCO_AI_PROVIDER_MODEL`：治理 AI 在线分析、治理增强或相关 overlay 要调用的模型名。
   - 还要明确告诉我为什么要配置它们：只有你想启用 Codex 下的治理 AI 在线层时才需要；如果没配，就只能说 Codex 基础在线能力已配置，不能说治理 AI 在线层已就绪。
   - 还要明确告诉我去哪里配置：优先去 `~/.codex/settings.json` 的 `env` 下本地填写，或使用本地环境变量；不要让我把 URL、API key、model 贴到聊天里。
8. 如果我选择 `claude-code`：
   - Linux / macOS 使用 `bash ./scripts/bootstrap/one-shot-setup.sh --host claude-code --profile framework-only`
   - 然后执行 `bash ./check.sh --host claude-code --profile framework-only --deep`
   - Windows 使用对应的 `pwsh` 命令。
   - 明确告诉我：这只是 preview guidance，不是 full closure。
   - 明确告诉我：由于兼容性问题，当前版本暂不为 Claude Code 安装 hook，也不再写 `settings.vibe.preview.json`。
   - 不要要求我把 API key 直接发到聊天里。
   - 应该告诉我打开 `~/.claude/settings.json`，只在 `env` 下补充需要的字段，并保留我原有的设置。
   - 如果需要 AI 治理层在线能力，提醒我自己在本地配置这些字段：
     - `VCO_AI_PROVIDER_URL`
     - `VCO_AI_PROVIDER_API_KEY`
     - `VCO_AI_PROVIDER_MODEL`
   - 还要明确解释这三个字段的作用：
     - `VCO_AI_PROVIDER_URL`：治理 AI 要连接的 provider 地址或兼容 API Base URL。
     - `VCO_AI_PROVIDER_API_KEY`：治理 AI 访问该 provider 时使用的本地认证密钥。
     - `VCO_AI_PROVIDER_MODEL`：治理 AI 在线分析、治理增强或相关 overlay 要调用的模型名。
   - 还要明确告诉我为什么要配置它们：如果你希望启用 AI 治理层的在线能力，而不是只跑本地 runtime / prompt / check 流程，就需要这三项；没配时只能说“本地安装完成，但治理 AI 在线能力未就绪”，不能伪装成 full closure 或 online readiness。
   - 还要明确告诉我去哪里配置：优先去 `~/.claude/settings.json` 的 `env` 下本地填写，或使用本地环境变量；不要让我把 URL、API key、model 贴到聊天里。
9. 对 `codex` 和 `claude-code`，都不要要求我把密钥、URL 或 model 直接粘贴到聊天里；只告诉我去本地 settings 或本地环境变量里配置。
10. 如果这些本地 provider 字段没有配置好，不能把环境描述成“已完成 online readiness”。
11. 安装完成后，请用简洁中文告诉我：
   - 目标宿主
   - 公开版本
   - 实际映射的 profile
   - 实际执行的命令
   - 已完成的部分
   - 仍需我手动处理的部分
12. 还要额外明确告诉我：当前拿到的是治理框架底座，不等于默认 workflow core 已经齐备；如果我后续要接入自己的 workflow，请引导我继续走 custom workflow governed onboarding，而不是伪装成已经开箱即用。
13. 不要把宿主插件、MCP 注册、provider 凭据伪装成已经自动完成。
```

## 安装完成后你会看到什么

无论你选哪个版本，安装完成后都应该收到一份简洁结果摘要，至少包含：

- 目标宿主
- 公开版本
- 实际映射的 profile
- 实际执行的命令
- 已完成的部分
- 仍需手动处理的部分

推荐理解口径：

- “安装完成” ≠ “hook 已安装”
- “基础 online provider 已配置” ≠ “治理 AI online layer 已就绪”
- “核心框架已安装” ≠ “默认 workflow core 已齐备”
- “技能目录存在” ≠ “custom workflow 已被 router 纳管”

## 它不会假装替你完成什么

下面这些仍然可能是用户侧或宿主侧动作：

- 本地宿主配置填写
- MCP 注册与授权（按需启用的增强项）
- hook 的后续兼容性等待（当前是作者侧兼容性边界，不是你的安装失败）
- `url` / `apikey` / `model` 的本地填写
- Claude Code 的真实 `settings.json` 人工补充
- custom workflow 的 manifest 声明与治理规则补齐

## 安装后如何继续自定义添加 skills / 治理

统一走受治理接入路径：

- 先完成当前公开版本安装
- 再看 [`custom-workflow-onboarding.md`](./custom-workflow-onboarding.md)
- 再看 [`custom-skill-governance-rules.md`](./custom-skill-governance-rules.md)

推荐理解方式：

- 全量版本：先拿到默认 workflow core 和扩展面，再接入你自己的治理
- 核心框架版本：先拿到底座，再按 manifest 逐步接入你自己的 workflow / skill governance

如果你的目标是“装完就要把自己的工作流也接进去”，建议顺序是：

1. 先装 `全量版本 + 可自定义添加治理`
2. 再按 [`custom-workflow-onboarding.md`](./custom-workflow-onboarding.md) 建立 manifest
3. 再按 [`custom-skill-governance-rules.md`](./custom-skill-governance-rules.md) 补齐治理边界
4. 最后再跑一次 `check` / doctor 验证

## 如果后续要更新版本

如果用户已经接入了自己的 workflow / skill governance，后续升级时要特别注意：

- 放在 `skills/custom/` 和 `config/custom-workflows.json` 的自定义内容，通常不会因为标准覆盖更新被直接删掉
- 但写进官方受管路径的改动，更新时可能被覆盖

高风险路径包括：

- `skills/vibe/`
- 官方 skill 目录
- 官方 `mcp/`
- 官方 `rules/`
- 官方 `agents/templates/`

升级前建议：

1. 备份 `skills/custom/`
2. 备份 `config/custom-workflows.json`
3. 记录当前 profile

升级后必须：

1. 重新跑 `check --deep`
2. 检查是否出现 `custom_manifest_invalid`
3. 检查是否出现 `custom_dependencies_missing`

最常见的问题不是“自定义治理被删了”，而是：

- 你切换了 profile
- custom workflow 的 `requires` 不再满足
- doctor/check 因此把它判定为不可用

如果你后续准备从“全量版本”降到“仅核心框架版本”，先检查自定义 workflow 是否依赖 `writing-plans`、`systematic-debugging` 等 workflow core。

## 复制给 AI 的更新提示词

### 提示词 C：全量安装 + 自定义治理的更新提示词

适合：

- 你当前走的是 `全量版本 + 可自定义添加治理`
- 你已经接入了或准备长期保留自己的 custom workflow / skill governance
- 你希望更新后继续保持全量能力面

```text
你现在是我的 VibeSkills 更新助手。
仓库地址：https://github.com/foryourhealth111-pixel/Vibe-Skills

在执行任何更新命令前，你必须先问我：
“你当前是装在哪个宿主里？当前只支持：codex 或 claude-code。”

在我回答宿主后，你还必须再问我：
“你当前要更新到哪个公开版本？当前只支持：全量版本+可自定义添加治理，或 仅核心框架+可自定义添加治理。”

规则：
1. 在我明确回答宿主和版本前，不要开始更新。
2. 先判断当前系统是 Windows 还是 Linux / macOS，并使用对应命令格式。
3. 你必须把公开版本映射到真实 profile：
   - `全量版本+可自定义添加治理` -> `full`
   - `仅核心框架+可自定义添加治理` -> `framework-only`
4. 更新前先检查以下内容是否存在：
   - `skills/custom/`
   - `config/custom-workflows.json`
5. 如果这些自定义内容存在，先提醒我：
   - 标准覆盖更新通常不会直接删除它们
   - 但如果我改过官方受管路径，例如 `skills/vibe/`、官方 skill、官方 `mcp/`、`rules/`、`agents/templates/`，这些改动可能被覆盖
6. 更新前建议先提醒我备份：
   - `skills/custom/`
   - `config/custom-workflows.json`
7. 这次更新目标必须按 `full` 处理，不要把它降成 `framework-only`。
8. 然后执行更新所需命令，并重新运行 deep check。
9. 更新后还要重点确认：
   - 默认 workflow core 仍然存在
   - custom workflow 的 `requires` 仍然满足
   - 没有把“全量能力仍在”误判成“仅框架模式”
10. 更新完成后，请用简洁中文告诉我：
   - 目标宿主
   - 公开版本
   - 实际映射的 profile
   - 实际执行的命令
   - 自定义治理是否仍然存在
   - 默认 workflow core 是否仍然齐备
   - 是否出现 `custom_manifest_invalid`
   - 是否出现 `custom_dependencies_missing`
   - 仍需我手动处理的部分
11. 如果更新后 custom workflow 目录和 manifest 还在，但依赖不满足，不要说“自定义治理被删了”，而要明确告诉我：这是依赖断裂，不是内容丢失。
12. 不要要求我把任何 API key、URL、model 粘贴到聊天里。
13. 不要把 hook、MCP 注册、provider 凭据、治理 AI online readiness 伪装成已经自动完成。
```

### 提示词 D：仅框架 + 自定义治理的更新提示词

适合：

- 你当前走的是 `仅核心框架 + 可自定义添加治理`
- 你要保留治理框架底座与自己的 custom workflow / skill governance
- 你不要求默认 workflow core 必须随更新一起保留

```text
你现在是我的 VibeSkills 更新助手。
仓库地址：https://github.com/foryourhealth111-pixel/Vibe-Skills

在执行任何更新命令前，你必须先问我：
“你当前是装在哪个宿主里？当前只支持：codex 或 claude-code。”

在我回答宿主后，你还必须再问我：
“你当前要更新到哪个公开版本？当前只支持：全量版本+可自定义添加治理，或 仅核心框架+可自定义添加治理。”

规则：
1. 在我明确回答宿主和版本前，不要开始更新。
2. 先判断当前系统是 Windows 还是 Linux / macOS，并使用对应命令格式。
3. 你必须把这次更新目标映射到真实 profile：`framework-only`。
4. 更新前先检查以下内容是否存在：
   - `skills/custom/`
   - `config/custom-workflows.json`
5. 如果这些自定义内容存在，先提醒我：
   - 标准覆盖更新通常不会直接删除它们
   - 但如果我改过官方受管路径，例如 `skills/vibe/`、官方 skill、官方 `mcp/`、`rules/`、`agents/templates/`，这些改动可能被覆盖
6. 更新前建议先提醒我备份：
   - `skills/custom/`
   - `config/custom-workflows.json`
7. 然后执行更新所需命令，并重新运行 deep check。
8. 更新后还要重点确认：
   - 自定义治理是否仍在
   - 当前确实仍是“仅核心框架”而不是被误报成 workflow/full
   - custom workflow 的 `requires` 是否仍满足
9. 更新完成后，请用简洁中文告诉我：
   - 目标宿主
   - 公开版本
   - 实际映射的 profile
   - 实际执行的命令
   - 自定义治理是否仍然存在
   - 当前是否仍是治理框架底座模式
   - 是否出现 `custom_manifest_invalid`
   - 是否出现 `custom_dependencies_missing`
   - 仍需我手动处理的部分
10. 如果更新后 custom workflow 目录和 manifest 还在，但依赖不满足，不要说“自定义治理被删了”，而要明确告诉我：这是依赖断裂，不是内容丢失。
11. 不要要求我把任何 API key、URL、model 粘贴到聊天里。
12. 不要把 hook、MCP 注册、provider 凭据、治理 AI online readiness 伪装成已经自动完成。
```

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
- [`full-path.md`](./full-path.md)
- [`framework-only-path.md`](./framework-only-path.md)
- [`../cold-start-install-paths.md`](../cold-start-install-paths.md)

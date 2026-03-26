# 宿主插件与宿主配置策略

这份文档只回答当前版本最关键的几个问题：

- 现在支持哪些宿主
- 仓库会自动处理哪些事情
- 用户还需要在宿主侧自己处理哪些事情
- 什么不应该再被描述成“标准安装要求”

## 当前支持边界

当前公开安装面包括：

- `codex`
- `claude-code`
- `opencode`

除此之外的其他代理，当前版本都不应被描述成“已支持安装”。

如果有人想把 VibeSkills 接到别的代理上，准确说法应该是：

- 当前版本没有官方支持的安装闭环
- 不应该伪装成已有可复用的宿主插件策略
- 不应该把历史实验性 lane 当成社区可依赖的默认方案

## 先分清三类东西

社区阅读时最容易混淆的，不是命令本身，而是边界。

### 1. 仓库 payload

这是仓库自己负责的部分，例如：

- `skills/`
- `commands/`
- `skills/vibe/` runtime mirror
- 安装脚本、检查脚本、doctor / verify 入口
- OpenCode preview command/agent 包装器

这些内容属于 repo-governed surface。

### 2. 宿主配置

这是用户要在宿主本地完成的部分，例如：

- `~/.codex/settings.json`
- `~/.claude/settings.json`
- `~/.config/opencode/opencode.json`
- 本地环境变量
- 宿主侧 MCP 注册或信任决策

这些不属于“仓库已经自动完成”的范围。

### 3. 可选增强项

有些 CLI、MCP、外部服务可以增强体验，但它们不是第一次安装的默认前置。

准确做法是：

- 先把支持宿主的基础路径跑通
- 再按真实需求补增强项
- 不要为了“看起来更满”一次性全装

## Codex 的默认策略

对 `codex`，当前标准安装策略应当非常克制。

### 当前默认要求

只围绕这些可证明、可解释的面：

- 本地 `~/.codex/settings.json`
- 官方支持的 MCP 注册
- 可选 CLI 依赖
- 不包含 hook 安装

### 不再作为默认要求的历史说法

下面这些历史叙事，不应该继续出现在公开安装口径里：

- “先把一串宿主插件全部装上再说”
- “Codex 默认要补一套 Claude Code 风格 hook/plugin 面”
- “某些历史插件是 Codex 标准安装前置”

### 在线能力怎么处理

如果需要在线模型能力，应该提醒用户：

- 去 `~/.codex/settings.json` 的 `env` 下配置
- 或者在本地环境变量里配置
- 不要把密钥贴到聊天里

常见字段例如：

- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`

如果这些值没有在本地配置好，就不能把环境描述成“已完成 online readiness”。

## Claude Code 的默认策略

对 `claude-code`，当前口径必须更明确。

### 当前真实状态

`claude-code` 现在是：

- preview guidance
- 不是 full closure
- hook 当前因兼容性问题被冻结
- 安装器不再生成参考 settings scaffold

### 仓库会做什么

当前仓库只会做这些事：

- 安装 runtime payload
- 运行对应的 preview 检查

### 仓库不会做什么

当前仓库不会自动完成：

- 覆盖真实 `~/.claude/settings.json`
- 自动替用户写入正式 provider 凭据
- 自动完成宿主 MCP 注册
- 自动宣称“Claude Code 已完整接入”

### 用户应当怎么做

正确方式是：

- 打开 `~/.claude/settings.json`
- 只在 `env` 下补充你需要的字段
- 保留你原有的宿主设置

常见需要本地填写的字段包括：

- `VCO_AI_PROVIDER_URL`
- `VCO_AI_PROVIDER_API_KEY`
- `VCO_AI_PROVIDER_MODEL`

如果宿主连接确实需要，再补：

- `ANTHROPIC_BASE_URL`
- `ANTHROPIC_AUTH_TOKEN`

同样，不要要求用户把这些值贴到聊天里。

如果本地还没配好这些值，也不能把环境描述成“已完成 online readiness”。

## OpenCode 的默认策略

对 `opencode`，当前口径应该描述成 preview adapter，而不是“又一个完整闭环宿主”。

### 当前真实状态

`opencode` 现在是：

- preview adapter
- 有真实的 `install/check` 入口
- 仓库会写入 skills、command/agent 包装器和 `opencode.json.example`
- 真正的 `opencode.json`、provider 凭据、plugin 安装与 MCP 信任仍由宿主管理

### 仓库会做什么

当前仓库会：

- 安装 runtime-core + VibeSkills 技能载荷
- 安装 OpenCode command/agent 包装器
- 写入 `opencode.json.example`
- 运行对应的 preview 检查

### 仓库不会做什么

当前仓库不会自动完成：

- 覆盖真实 `opencode.json`
- 写入生产 provider 凭据
- 安装宿主 plugin
- 替用户决定 MCP 信任

### 用户应当怎么做

正确方式是：

- 把 preview payload 装到 `OPENCODE_HOME`、`~/.config/opencode` 或项目内 `./.opencode`
- 自己处理真实 `opencode.json`
- 自己补 provider 凭据
- 自己决定 plugin 安装与 MCP 信任

如果要看完整路径说明，直接看：

- [`opencode-path.md`](./opencode-path.md)

## 宿主插件的当前政策结论

如果只看当前版本，公开文档应该坚持下面这组结论：

1. `codex` 没有额外的默认宿主插件前置要求。
2. `claude-code` 不是靠“补一堆宿主插件”来完成接入，而是靠 preview guidance + 用户本地配置补全。
3. `opencode` 也不是“仓库接管整个宿主”，而是 preview adapter + host-managed 正式配置。
4. 历史上出现过的某些插件名，不等于当前社区文档还应该继续推荐它们。
5. 只要某个能力没有被仓库稳定、公开、可验证地接入，就不该写成默认安装要求。

## 推荐的社区表述

如果你要在 issue、README、讨论区或安装提示词里引用这份策略，推荐用下面这种说法：

- 当前版本公开安装面包括 `codex`、`claude-code` 和 `opencode`
- `codex` 走本地 settings + MCP + 可选 CLI 的保守增强路线
- `codex` / `claude-code` 当前都不安装 hook，因为兼容性问题尚未解决
- `claude-code` 走 preview guidance 路线，不覆盖真实 `settings.json`
- `opencode` 走 preview adapter 路线，不覆盖真实 `opencode.json`
- provider 的 `url` / `apikey` / `model` 由用户在本地配置，不在聊天里提供
- 其他代理目前不在公开支持面内

## 什么时候再扩展这份文档

只有在下面条件同时成立时，才值得重新扩大宿主插件策略：

- 新宿主已经有可验证的安装闭环
- 自动化边界足够清楚
- 社区用户不需要依赖隐性历史知识才能装对
- 我们能明确说明“仓库负责什么，宿主负责什么”

在那之前，保持简单、真实、可解释，比保留历史包袱更重要。

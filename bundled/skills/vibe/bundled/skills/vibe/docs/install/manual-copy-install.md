# 手动复制安装（离线 / 无管理员权限）

如果你不想跑安装脚本，只想手动放文件，这一页只需要记住一件事：

**把 VibeSkills 的运行时目录复制到目标宿主目录里。**

当前这条路径只面向两个宿主：

- `codex`
- `claude-code`

如果你的目标不是这两个宿主，当前版本不应描述成“已支持安装”。

## 你要复制什么

把下面这些内容复制到目标宿主目录中：

- `skills/`
- `commands/`
- `config/upstream-lock.json`
- `config/skills-lock.json`（如果仓库里有这个文件）
- `skills/vibe/` 这套 runtime mirror

你可以把它理解成：

- `skills/`：能力本体
- `commands/`：命令入口
- `config/*.json`：锁文件和版本对齐信息
- `skills/vibe/`：VCO 运行时镜像

## 复制到哪里

复制到你的目标宿主根目录下。

也就是让目标目录里最终能看到这些路径：

- `<TARGET_ROOT>/skills/`
- `<TARGET_ROOT>/commands/`
- `<TARGET_ROOT>/config/upstream-lock.json`
- `<TARGET_ROOT>/config/skills-lock.json`（如果存在）

## 安装后你还要自己做什么

手动复制只解决“把仓库文件放进去”，不解决宿主本地配置。

### 如果你装到 Codex

你还需要自己去本地配置：

- `~/.codex/settings.json`
- 常见是 `env` 下的 `OPENAI_API_KEY`、`OPENAI_BASE_URL`

### 如果你装到 Claude Code

你还需要自己去本地配置：

- `~/.claude/settings.json`
- 常见是：
  - `VCO_AI_PROVIDER_URL`
  - `VCO_AI_PROVIDER_API_KEY`
  - `VCO_AI_PROVIDER_MODEL`
- 如宿主连接需要，再补：
  - `ANTHROPIC_BASE_URL`
  - `ANTHROPIC_AUTH_TOKEN`

## 当前不会自动帮你做什么

手动复制安装不会自动完成这些事：

- hook 安装
- MCP 注册
- provider 凭据写入
- Claude Code 真实 `settings.json` 修改

其中要特别注意：

- `codex` / `claude-code` 当前都**不提供 hook 安装**
- hook 目前因为兼容性问题，暂时被冻结

## 最后一个边界

如果 `url` / `apikey` / `model` 还没有在本地配置好，就不能把环境描述成“已完成 online readiness”。

这些值应该由用户自己填进本地宿主配置或本地环境变量里，不要在聊天里直接提供。

## 什么时候不要走这条路

如果你希望：

- 让 AI 帮你判断该装到哪个宿主
- 让脚本自动执行 install + check
- 少看本地配置细节

那就不要走手动复制，直接看：

- [`one-click-install-release-copy.md`](./one-click-install-release-copy.md)

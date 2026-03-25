# 安装路径：高级 host / lane 参考

> 大多数用户先看两条主路径：
>
> - [`one-click-install-release-copy.md`](./one-click-install-release-copy.md)
> - [`manual-copy-install.md`](./manual-copy-install.md)

这份文档只解释当前真实支持边界。

## 当前支持面

暂时只支持两个宿主：

- `codex`
- `claude-code`

其中：

- `codex`：正式推荐路径
- `claude-code`：preview guidance 路径

`TargetRoot` 只是安装路径。
`HostId` / `--host` 才决定宿主语义。

## 推荐命令

### Codex

```powershell
pwsh -File .\scripts\bootstrap\one-shot-setup.ps1 -HostId codex
pwsh -File .\check.ps1 -HostId codex -Profile full -Deep
```

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host codex
bash ./check.sh --host codex --profile full --deep
```

### Claude Code

```powershell
pwsh -File .\scripts\bootstrap\one-shot-setup.ps1 -HostId claude-code
pwsh -File .\check.ps1 -HostId claude-code -Profile full -Deep
```

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host claude-code
bash ./check.sh --host claude-code --profile full --deep
```

## 旧版本怎么升级

旧版本用户不需要先卸载。
对大多数用户，最简单、最推荐的做法就是重新走一遍提示词安装。

也就是说，只要让 AI 按 [`one-click-install-release-copy.md`](./one-click-install-release-copy.md) 再安装一次，通常就够了。
只有在 AI 不能代你执行、或者你需要手动排障时，下面这些命令才有必要。

### 如果你本地还保留着这个仓库

先更新仓库：

```bash
git pull
```

如果你是按发布版本使用，而不是跟着 `main` 走，可以改成：

```bash
git fetch --tags --force
git checkout vX.Y.Z
```

然后重新执行安装。

### 升级已安装的 Codex 版本

```powershell
pwsh -File .\scripts\bootstrap\one-shot-setup.ps1 -HostId codex
pwsh -File .\check.ps1 -HostId codex -Profile full -Deep
```

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host codex
bash ./check.sh --host codex --profile full --deep
```

### 升级已安装的 Claude Code 版本

```powershell
pwsh -File .\scripts\bootstrap\one-shot-setup.ps1 -HostId claude-code
pwsh -File .\check.ps1 -HostId claude-code -Profile full -Deep
```

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host claude-code
bash ./check.sh --host claude-code --profile full --deep
```

### 如果你本地已经没有仓库副本

重新 clone 最新仓库，然后按上面的命令重新安装即可。

```bash
git clone https://github.com/foryourhealth111-pixel/Vibe-Skills.git
cd Vibe-Skills
```

### 怎么确认已经升级成功

如果你只是想让 AI 帮你重装，这一步通常也不必手动做。
只有在你需要自己核对版本时，再看下面这个文件。

Codex 默认安装到 `~/.codex` 时，可以直接查看版本治理文件：

```bash
jq -r '.release.version, .release.updated' ~/.codex/skills/vibe/config/version-governance.json
```

如果你装在自定义 `TargetRoot`，把上面的 `~/.codex` 换成你自己的安装根目录。

### 升级时会覆盖什么

- 安装器会更新目标宿主下的 VibeSkills 运行时文件
- 原有宿主配置仍然应保留，用户只需要继续维护自己本地的 `env` / provider 配置
- 旧版本里已经被冻结的 hook 行为，不会因为这次升级突然重新启用

## 必须说清楚的边界

### Codex

- 当前是最完整的 repo-governed 路径
- 建议范围只包括本地 `~/.codex` 设置、官方 MCP 注册和可选 CLI 依赖
- hook 安装面当前仍在作者处理兼容性，所以暂未开放；这不是安装失败，只是当前标准安装边界
- 如果需要 Codex 基础在线模型能力，去 `~/.codex/settings.json` 的 `env` 或本地环境变量里配置 `OPENAI_API_KEY`、`OPENAI_BASE_URL`
- 如果需要启用 Codex 下的治理 AI 在线层，可按需再补这些可选增强设置：
  - `VCO_AI_PROVIDER_URL`
  - `VCO_AI_PROVIDER_API_KEY`
  - `VCO_AI_PROVIDER_MODEL`
- `OPENAI_*` 不等于 `VCO_AI_PROVIDER_*`；前者是 Codex 基础在线 provider，后者是治理 AI 在线层
- 不要要求用户把密钥贴到聊天里
- 未补的 MCP、`VCO_AI_PROVIDER_*` 或类似配置，应优先表述成推荐增强项，而不是安装告警

### Claude Code

- 这是 preview guidance，不是 full closure
- hook 安装面当前仍在作者处理兼容性，所以暂未开放；这不是安装失败
- 安装器不再写 `settings.vibe.preview.json`
- 用户应自己打开 `~/.claude/settings.json`，只在 `env` 下补所需字段
- 常见字段：
  - `VCO_AI_PROVIDER_URL`
  - `VCO_AI_PROVIDER_API_KEY`
  - `VCO_AI_PROVIDER_MODEL`
- 如宿主连接需要，再补 `ANTHROPIC_BASE_URL`、`ANTHROPIC_AUTH_TOKEN`
- 不要要求用户把密钥贴到聊天里
- 未补的 MCP、provider 或治理 AI 在线层配置，应优先表述成推荐增强项，而不是安装告警

## AI 治理层提示

对 `codex` 和 `claude-code`，如果本地还没配置好治理 AI 所需的 `url`、`apikey`、`model`，就不能描述成“已完成治理 AI online readiness”。

对 `codex`，这表示最多只能说基础在线 provider 已就绪，不能顺带宣称治理 AI 在线层也已就绪。

这些值必须由用户自己填进本地宿主配置或本地环境变量。

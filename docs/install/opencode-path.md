# OpenCode 安装路径

## 适用范围

这是一条真实的 `preview` 适配路径，不是“OpenCode 已经完全闭环”的声明。

当前仓库可安装：

- runtime-core 载荷
- Vibe-Skills 技能载荷
- OpenCode 命令包装器
- OpenCode agent 包装器
- `opencode.json` 示例配置

当前仓库不接管：

- 真正的 `~/.config/opencode/opencode.json`
- provider 凭证
- plugin 安装
- MCP 信任决策

## 全局安装

Shell：

```bash
./install.sh --host opencode
./check.sh --host opencode
```

PowerShell：

```powershell
pwsh -NoProfile -File ./install.ps1 -HostId opencode
pwsh -NoProfile -File ./check.ps1 -HostId opencode
```

默认目标根目录：

- 若设置了 `OPENCODE_HOME`，使用该目录
- 否则使用 `~/.config/opencode`

## 项目内安装

如果希望把 preview 载荷隔离在项目内部：

```bash
./install.sh --host opencode --target-root ./.opencode
./check.sh --host opencode --target-root ./.opencode
```

PowerShell 对应参数为 `-TargetRoot .\.opencode`。

## 安装内容

preview 安装会写入：

- `skills/**`
- `commands/*.md`
- `command/*.md`
- `agents/*.md`
- `agent/*.md`
- `opencode.json.example`

当前 preview 会同时写入 plural 和 singular 的 command/agent 目录，因为 OpenCode 当前文档和运行时生态仍存在路径漂移。

## 使用方式

安装后的推荐入口：

- `/vibe`
- `/vibe-implement`
- `/vibe-review`

也可以直接在对话里显式要求：

- `Use the vibe skill to plan this change.`
- `Use the vibe skill to implement the approved plan.`

preview 载荷安装的自定义 agent：

- `vibe-plan`
- `vibe-implement`
- `vibe-review`

## 验证方式

先跑仓库自带健康检查：

```bash
./check.sh --host opencode
```

再跑专用 smoke verifier：

```bash
python3 ./scripts/verify/runtime_neutral/opencode_preview_smoke.py --repo-root . --write-artifacts
```

## 当前证明状态

仓库内置的 preview smoke verifier 已经在本地 OpenCode CLI `1.2.27` 上证明：

- `opencode debug paths` 能正确解析隔离的 OpenCode 根目录
- `opencode debug skill` 能识别安装后的 `vibe` skill
- `opencode debug agent vibe-plan` 能识别安装后的 preview agent

该 lane 仍保持 `preview`，因为命令执行 replay 和平台级 proof bundle 还没有冻结完成。

# Cross-Host Startup Regression Audit

**日期**: 2026-03-30
**需求**: [../requirements/2026-03-30-cross-host-startup-regression-audit.md](../requirements/2026-03-30-cross-host-startup-regression-audit.md)
**计划**: [../plans/2026-03-30-cross-host-startup-regression-audit-plan.md](../plans/2026-03-30-cross-host-startup-regression-audit-plan.md)

## Summary

排查结论分两类：

- 与 OpenCode 同类的“真实配置被写坏后宿主直接拒绝解析并无法启动”问题，当前**只在 `opencode` 上确认复现**。
- `windsurf`、`openclaw` 在当前仓库代码下，**已确认不具备与 OpenCode 同类的故障入口**。
- `claude-code`、`cursor` 当前**不能再写成 `confirmed-safe`**：
  - `claude-code`：已证明 `claude agents` 会读取 `settings.json`，且该命令面对 `vibeskills`、明显未知键、坏 JSON 时仍返回成功；但这只能证明该命令面的容忍性，**不能外推出整个宿主都安全**。
  - `cursor`：当前 CLI 探针还**没有证明任何已测命令会读取 `settings.json`**，因此之前基于 `cursor-agent about` 的“safe”结论不成立，只能写成**未证实同类回归，但也未证实安全**。

## Host-by-Host Result

### `claude-code`

- Classification: `settings-surface-read-confirmed-command-level-tolerance-observed`
- Shared config written: `settings.json` 顶层 `vibeskills`
- Probe:
  - baseline read proof:
    - `HOME=<tmp> CLAUDE_HOME=<tmp>/.claude`
    - `printf '{}' > "$CLAUDE_HOME/settings.json"`
    - `strace -f -e trace=openat claude agents`
  - tolerance probe:
    - `claude agents` with `settings.json = {"vibeskills": {...}}`
    - `claude agents` with `settings.json = {"definitely_unknown_root_key_for_probe": 1}`
    - `claude agents` with malformed `settings.json`
  - control probe:
    - `claude --help` with the same three config variants
- Evidence:
  - `strace` 明确显示 `claude agents` 多次打开 `"$CLAUDE_HOME/settings.json"`
  - `claude agents` 在三种配置下都返回 `4 active agents`，`rc=0`
  - `claude --help` 在三种配置下也都成功返回帮助文本，`rc=0`
  - 这说明之前“`claude agents` 成功返回，所以它可能根本没读配置”的推断是错的；它**确实读了配置**
- Conclusion:
  - 可以证明的是：`claude` CLI 至少在 `agents` 这个已验证命令面上，会读取 `settings.json`，且对 `vibeskills`、明显未知键、坏 JSON 表现出容忍
  - 不能证明的是：整个 Claude Code 宿主在所有启动/运行路径上都安全接受顶层 `vibeskills`
  - 因此这里**不能再写 `confirmed-safe`**，只能写成“已确认读取 + 已观察到命令级容忍，未证实同类启动回归”

### `cursor`

- Classification: `not-proven-with-current-probe`
- Shared config written: `settings.json` 顶层 `vibeskills`
- Probe:
  - read-surface probe:
    - `HOME=<tmp> CURSOR_HOME=<tmp>/.cursor`
    - `printf '{}' > "$CURSOR_HOME/settings.json"`
    - `strace -f -e trace=openat cursor-agent about`
    - `strace -f -e trace=openat cursor-agent models`
    - `strace -f -e trace=openat cursor-agent status`
    - `strace -f -e trace=openat cursor-agent ls`
  - tolerance probe:
    - `cursor-agent about` / `cursor-agent models` with `settings.json = {"vibeskills": {...}}`
    - `cursor-agent about` / `cursor-agent models` with `settings.json = {"definitely_unknown_root_key_for_probe": 1}`
    - `cursor-agent about` / `cursor-agent models` with malformed `settings.json`
- Evidence:
  - `cursor-agent about`、`models`、`status`、`ls` 的 `strace` 结果里，目前只稳定看到 `agent-cli-state.json`，**没有抓到 `settings.json` 读取证据**
  - `cursor-agent about` 在 `vibeskills`、明显未知键、坏 JSON 下都成功返回 `About Cursor CLI`，`rc=0`
  - `cursor-agent models` 在上述三种配置下都成功返回 `No models available for this account.`，`rc=0`
  - 这说明之前“`about` 成功返回，所以 Cursor 安全接受 `vibeskills`”的结论没有证据支撑，因为**尚未证明 `about` 会读 `settings.json`**
- Conclusion:
  - 当前只能证明：已测 `cursor-agent` 命令**没有像 OpenCode 那样立刻因为顶层 `vibeskills` 或坏 JSON 报错退出**
  - 当前不能证明：这些命令真的读取了 `settings.json`
  - 因此这里**不能再写 `confirmed-safe`**，只能写成“未证实同类回归，但安全性也未被当前探针证明”

### `windsurf`

- Classification: `confirmed-safe-against-same-class-regression`
- Shared config written: 否
- Host state written:
  - `.vibeskills/host-settings.json`
  - `mcp_config.json`
  - `global_workflows/**`
- Probe:
  - baseline: `HOME=<tmp> WINDSURF_HOME=<tmp>/.codeium/windsurf windsurf --status --user-data-dir <tmp>/userdata`
  - after install: `bash ./install.sh --host windsurf --target-root <tmp>/.codeium/windsurf --profile full`
  - post-install: same `windsurf --status ...`
- Evidence:
  - baseline 与 post-install 都返回同一条警告：`--status argument can only be used if Windsurf is already running`
  - 安装根下没有 `settings.json`
  - 只写 `.vibeskills/host-settings.json` 与 `mcp_config.json`
- Conclusion:
  - 当前仓库不写 Windsurf 的共享 settings surface，因此不存在与 OpenCode 同类的“真实配置键非法”风险前提
  - 本地最小 CLI 探针前后行为一致，未见启动链退化

### `openclaw`

- Classification: `confirmed-safe-against-same-class-regression`
- Shared config written: 否
- Host state written:
  - `.vibeskills/host-settings.json`
  - `mcp_config.json`
  - `global_workflows/**`
- Probe:
  - baseline: `HOME=<tmp> OPENCLAW_HOME=<tmp>/.openclaw openclaw config validate`
  - baseline: `HOME=<tmp> OPENCLAW_HOME=<tmp>/.openclaw openclaw skills list`
  - after install: `bash ./install.sh --host openclaw --target-root <tmp>/.openclaw --profile full`
  - post-install: repeat the same two commands
- Evidence:
  - `config validate` 安装前后都返回相同结果：缺少宿主自己的 `openclaw.json`
  - `skills list` 安装前后都能正常运行并列出 skills
  - 安装根下没有 `settings.json`
  - 只写 `.vibeskills/host-settings.json` 与 `mcp_config.json`
- Conclusion:
  - 当前仓库不写 OpenClaw 的共享 settings surface，因此不存在与 OpenCode 同类的“真实配置键非法”风险前提
  - 本地 CLI 探针前后行为一致，未见启动链退化

## Overall Conclusion

- `opencode`: 已确认存在并已修复
- `claude-code`: 已确认 `settings.json` 被读取；已验证命令面未复现 OpenCode 式解析炸裂；**但不能写成 confirmed-safe**
- `cursor`: 已测 CLI 命令面未复现 OpenCode 式报错退出；**但尚未证明会读取 `settings.json`，因此不能写成 confirmed-safe**
- `windsurf`: 当前未发现同类启动回归
- `openclaw`: 当前未发现同类启动回归

更精确地说：

- 真正需要警惕的是“宿主真实配置文件语法/字段 schema 很严格，且安装器往里面写了宿主不认识的键”
- 当前这类高风险前提只在 `opencode` 上被证实
- `claude-code`：当前只证明某些已测命令会读取并容忍该配置；证据等级不足以支撑“宿主整体安全”
- `cursor`：当前只证明若干命令没有立刻炸；证据等级不足以支撑“命令已读配置且安全接受”
- `windsurf/openclaw` 当前根本不写共享 `settings.json`，所以不具备与 OpenCode 同类的故障入口

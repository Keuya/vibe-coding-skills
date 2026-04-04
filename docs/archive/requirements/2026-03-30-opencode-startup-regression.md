# OpenCode 安装后启动回归需求

**日期**: 2026-03-30
**目标**: 严肃排查并修复 `install.sh --host opencode` / `install.ps1 -HostId opencode` 安装后导致 OpenCode 无法启动的回归问题，确保安装面与仓库文档声明一致。

## Intent Contract

- Goal: 确认 OpenCode 无法启动的直接根因，修复安装器写面，并用本地可重复的 smoke 证据证明修复生效。
- Deliverable:
  - 根因定位与复现证据
  - 安装器修复
  - 针对 OpenCode 启动/配置解析的回归测试
  - 受影响说明文档的 truth 修正
- Constraints:
  - 必须保持 `opencode` lane 的现有定位：preview adapter / direct install-check。
  - 不得再写入会破坏 OpenCode 自身配置解析的宿主真实配置。
  - 必须与仓库既有 truth 对齐：真实 `opencode.json` 属于 host-managed surface。
  - 不能为了修复启动回归而删除既有 skills / commands / agents / example scaffold 的有效写面。
- Acceptance Criteria:
  - 在隔离的 OpenCode 根目录下，安装后执行 `opencode debug config` 不再报配置非法。
  - 在同一隔离目录下，`opencode debug agent vibe-plan` 能识别安装后的 agent。
  - 安装器不再把 `vibeskills` 节点写入真实 `opencode.json`。
  - 文档不再存在“真实 `opencode.json` 仍由宿主管理”与“安装器实际写入真实 `opencode.json`”之间的矛盾。
- Product Acceptance Criteria:
  - 用户执行 `install.* --host opencode` 后，OpenCode 至少能正常读取配置并进入可运行状态。
  - 预览适配器的边界表达继续保持 honest，不夸大宿主原生闭环能力。
- Manual Spot Checks:
  - 隔离环境下运行 `opencode debug config`
  - 隔离环境下运行 `opencode debug skill`
  - 隔离环境下运行 `opencode debug agent vibe-plan`
- Completion Language Policy:
  - 在本地隔离复现与修复后 smoke 未通过前，不能说“问题已修复”。
  - 如果修复结果依赖本机安装的 `opencode` CLI，应明确说明验证环境和证据。
- Delivery Truth Contract:
  - 本轮允许修改安装器、测试、verify smoke 与相关文档。
  - 任何关于 OpenCode 宿主行为的结论都必须基于本地实际命令输出，不得只凭文档猜测。
- Non-goals:
  - 不在本轮扩展 OpenCode 的 provider / MCP / plugin 自动配置能力。
  - 不把 preview adapter 重新定义为 full host closure。
- Autonomy Mode: `interactive_governed`
- Inferred Assumptions:
  - 当前最可能的回归面是安装器对真实 `opencode.json` 的写入。
  - 如果真实 `opencode.json` 不再被写坏，OpenCode 的 agent / skill 发现链应恢复正常。

# 安装与自定义接入索引

本目录用于对外公开的安装、升级与自定义接入说明。

## 快速导航

### 公开安装入口

- [`one-click-install-release-copy.md`](./one-click-install-release-copy.md)：唯一公开安装入口；先选宿主、动作和版本，再复制对应提示词

### 公开卸载入口

- [`../../uninstall.ps1`](../../uninstall.ps1) / [`../../uninstall.sh`](../../uninstall.sh)：安装完成后的对称卸载入口；参数与 `install.*` 对齐，默认直接执行，但只会按 install ledger、host closure 和保守 legacy surface 删除 Vibe 自己管理的内容
- [`../uninstall-governance.md`](../uninstall-governance.md)：卸载契约说明；明确 shared JSON 只删 `vibeskills` 受管节点，不回滚宿主登录态、provider 凭证或插件状态

### 参考说明

- [`recommended-full-path.md`](./recommended-full-path.md)：多宿主安装命令参考
- [`openclaw-path.md`](./openclaw-path.md)：OpenClaw 专用安装与使用说明
- [`opencode-path.md`](./opencode-path.md)：OpenCode 专用安装与使用说明
- [`manual-copy-install.md`](./manual-copy-install.md)：离线或无管理员权限时的手动复制路径
- [`framework-only-path.md`](./framework-only-path.md)：旧入口名兼容说明
- [`full-featured-install-prompts.md`](./full-featured-install-prompts.md)：Codex 深度路径兼容说明
- [`installation-rules.md`](./installation-rules.md)：安装助手必须遵守的 truth-first 规则
- [`configuration-guide.md`](./configuration-guide.md)：本地配置说明

说明：

- 面向普通用户时，公开安装入口只保留 [`one-click-install-release-copy.md`](./one-click-install-release-copy.md)
- 真正保留的安装提示词文档仍是 4 份：全量安装、框架安装、全量更新、框架更新
- 其他安装相关页面只作为兼容说明、宿主补充说明或命令参考，不再作为平行公开入口
- 通用安装提示词同样支持 `openclaw` 和 `opencode`
- 单独拆出 [`openclaw-path.md`](./openclaw-path.md) 与 [`opencode-path.md`](./opencode-path.md)，只是为了补充宿主特有细节，不是因为通用安装路径不能安装
- 这些宿主专页主要展开默认根目录、额外安装方式、验证方式与宿主侧本地边界，避免把公共安装文档写得过重
- provider / MCP / 宿主 settings 等补充配置，默认都按“增强建议”处理；基础安装完成后即可直接使用，需要更强集成时再按需补充

## 公开版本

当前对外公开仍是两种用户版本：

- `全量版本 + 可自定义添加治理`
- `仅核心框架 + 可自定义添加治理`

它们在当前脚本里的真实 profile 映射是：

- `全量版本 + 可自定义添加治理` -> `full`
- `仅核心框架 + 可自定义添加治理` -> `minimal`

对外继续使用友好版本名，对内执行时再映射到真实 profile。

## 当前公开支持宿主

- `codex`
- `claude-code`
- `cursor`
- `windsurf`
- `openclaw`
- `opencode`

其中：

- `codex`：默认推荐路径
- `claude-code`：支持的安装与使用路径
- `cursor`：支持的安装与使用路径
- `windsurf`：支持的安装与使用路径
- `openclaw`：支持的安装与使用路径，通用安装提示词可直接安装，宿主专页只补充细节
- `opencode`：支持的安装与使用路径，通用安装提示词可直接安装，宿主专页只补充细节

其他宿主当前不应被描述成“已支持安装”。

## 推荐阅读顺序

如果你是普通用户：

1. [`one-click-install-release-copy.md`](./one-click-install-release-copy.md)
2. 只在这一个入口里选择对应提示词
3. [`custom-workflow-onboarding.md`](./custom-workflow-onboarding.md)
4. [`custom-skill-governance-rules.md`](./custom-skill-governance-rules.md)

如果你是高级用户：

1. [`recommended-full-path.md`](./recommended-full-path.md)
2. [`manual-copy-install.md`](./manual-copy-install.md)
3. [`host-plugin-policy.md`](./host-plugin-policy.md)

## 自定义扩展

- [`custom-workflow-onboarding.md`](./custom-workflow-onboarding.md)：如何把新 workflow 纳入治理与路由
- [`custom-skill-governance-rules.md`](./custom-skill-governance-rules.md)：自定义 skill / workflow 的治理规则

# 安装与自定义接入索引

本目录用于对外公开的安装与自定义接入说明。

当前对外公开版本收束为两种：

- `全量版本 + 可自定义添加治理`
- `仅核心框架 + 可自定义添加治理`

当前脚本实现仍保留三条 lane：

- `framework-only`
- `workflow`
- `full`

但其中：

- `full` 对应公开的“全量版本 + 可自定义添加治理”
- `framework-only` 对应公开的“仅核心框架 + 可自定义添加治理”
- `workflow` 保留为兼容 / 过渡 lane，不再作为普通用户首页主选择

## 先看这里

- [`one-click-install-release-copy.md`](./one-click-install-release-copy.md)：对外默认推荐入口，含两个公开版本的提示词安装模板
- [`full-path.md`](./full-path.md)：全量版本对应的底层 `full` lane 参考
- [`framework-only-path.md`](./framework-only-path.md)：核心框架版本对应的底层 `framework-only` lane 参考
- [`workflow-path.md`](./workflow-path.md)：兼容 / 过渡 lane 参考，不再作为普通用户首页主入口

## 自定义扩展

- [`custom-workflow-onboarding.md`](./custom-workflow-onboarding.md)：如何把新工作流纳入治理与路由
- [`custom-skill-governance-rules.md`](./custom-skill-governance-rules.md)：自定义 skill/workflow 的治理规则与禁区

## 宿主边界（必须先确认）

当前公开支持宿主只有：

- `codex`
- `claude-code`

其中：

- `codex`：governed 官方路径
- `claude-code`：preview guidance（不是 full closure）

不支持的宿主不能伪装安装成功或 online readiness 完成。

## 兼容说明

在旧参数与旧 lane 仍存在的阶段：

- `minimal` 等价于 `workflow`
- `full` 仍等价于 `full`

对外沟通建议优先使用“公开版本名”，不要让普通用户先理解 lane：

- `全量版本 + 可自定义添加治理`
- `仅核心框架 + 可自定义添加治理`

## 推荐阅读顺序

如果你是普通用户，推荐按这个顺序看：

1. [`one-click-install-release-copy.md`](./one-click-install-release-copy.md)
2. [`custom-workflow-onboarding.md`](./custom-workflow-onboarding.md)
3. [`custom-skill-governance-rules.md`](./custom-skill-governance-rules.md)

如果你是高级用户，想看底层 profile / lane 对应关系，再看：

1. [`full-path.md`](./full-path.md)
2. [`framework-only-path.md`](./framework-only-path.md)
3. [`workflow-path.md`](./workflow-path.md)

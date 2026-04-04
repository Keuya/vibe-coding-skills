# 执行计划: 仓库激进瘦身与架构收敛

## 内部等级

XL

## 总体策略

采用“先审计、后删除、再压实权威入口”的方式推进。只删除有证据证明可移除的内容，不做无依据的大扫除。

## 波次

### Wave 1: 基线与依赖审计

- 统计顶层体量、tracked file 分布、历史文档密度
- 识别 source of truth / mirror / generated / archival 四类表面
- 抽取 README、CONTRIBUTING、架构文档、测试、packages 对目录的真实依赖

### Wave 2: 并行候选清单

- 文档层: `docs/plans/**`、`docs/requirements/**`、`docs/status/**`、`docs/proof/**`、零散治理文档
- 脚本层: `scripts/verify/**`、重复安装/检查/兼容脚本、已退役 shim
- 分发/镜像层: `bundled/**`、`dist/**`、`vendor/**`、`outputs/**`、其他可重建资产

### Wave 3: 高置信删除

- 先删除低风险且高体量的候选
- 同步收缩 README / CONTRIBUTING / 架构说明中的入口描述
- 若删除对象仍被测试引用，则同步改为新的权威面或重建路径

### Wave 4: 验证与第二轮收尾

- 跑定向测试、引用搜索、格式检查
- 复审仓库结构是否更贴近 package-owned 与 explicit-projection
- 清理临时文件与阶段性缓存

## 删除与保留原则

- 删除 generated 或 archival surface，保留 canonical semantic surface
- 删除 narrative duplication，保留 operator-facing authority
- 删除 broad mirror trees，优先保留 explicit projection
- 删除无人消费脚本，保留被 contract / tests / CLI / installer 消费的入口

## 验证命令

```bash
git diff --check
python3 -m pytest tests/unit tests/integration tests/runtime_neutral
rg -n "docs/(plans|requirements|status|proof)|bundled/|dist/|vendor/|scripts/verify/"
```

注: 实际执行时按删除面缩小测试范围，优先跑受影响模块的定向集。

## 回滚规则

- 若某一删除面触发真实消费者断裂，则回滚该批删除，改为“归档索引化”而不是直接移除
- 若 `bundled` / `dist` / `vendor` 中任一表面仍承担现行发布契约，则保留最小必要集合，不做全量清空
- 若无法在本轮证明历史文档可删，则改为压缩入口、建立索引、停止继续增长

## 阶段清理

- 每一波结束后审计 node / vite / npm 进程，不触碰非本任务来源进程
- 删除临时统计文件、缓存和未跟踪分析产物
- 保持工作树只包含最终需要提交的变更

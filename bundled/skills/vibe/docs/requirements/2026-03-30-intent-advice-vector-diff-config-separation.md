# Intent Advice / Vector Diff 配置分离需求文档

**日期**: 2026-03-30
**任务类型**: 配置语义收口 / 诊断可解释性修复
**优先级**: 高

## 目标

把内置意图挖掘 advice 能力与 vector diff embeddings 能力的本地配置彻底分离，避免用户把两条能力链误认为同一组配置。

## 问题陈述

当前实现里：

1. 主 advice 层默认读取 `OPENAI_API_KEY`
2. vector diff embeddings 也默认读取 `OPENAI_API_KEY`
3. 但两者使用的模型、接口、失败形态都不同

这会让用户产生错误心智模型：

1. 以为“一个 key 配好了，两层都应该正常”
2. 以为“embeddings unavailable” 等于“主 advice 挂了”
3. 难以从键名本身理解问题归属

## 设计决策

采用彻底分离方案：

1. 不再使用 `OPENAI_API_KEY` / `OPENAI_BASE_URL` / `OPENAI_API_BASE` / `VCO_RUCNLPIR_MODEL` 作为内置 advice 与 vector diff 的默认本地键名
2. 不对旧键名做默认回退
3. 用功能语义命名替代 provider 品牌命名

## 新默认键名

### 主 Intent Advice

- `VCO_INTENT_ADVICE_API_KEY`
- `VCO_INTENT_ADVICE_BASE_URL`
- `VCO_INTENT_ADVICE_MODEL`

### Vector Diff Embeddings

- `VCO_VECTOR_DIFF_API_KEY`
- `VCO_VECTOR_DIFF_BASE_URL`
- `VCO_VECTOR_DIFF_MODEL`

## 约束

1. 运行时必须默认只读取新键名
2. probe / doctor / bootstrap / settings template / 安装文档必须同步改口径
3. provider `type=openai-compatible` 可以保留，因为它是协议兼容语义，不是用户配置命名
4. vector diff 失败时仍允许主流程安全退化
5. 诊断输出必须明确区分：
   - 主 advice 未配置
   - vector diff 未配置
   - 主 advice provider 故障
   - vector diff provider 故障

## 验收标准

1. 主 advice 默认只认 `VCO_INTENT_ADVICE_*`
2. vector diff 默认只认 `VCO_VECTOR_DIFF_*`
3. 代码路径中不存在对旧 `OPENAI_*` / `VCO_RUCNLPIR_MODEL` 的默认回退
4. 配置说明与安装说明中英文都明确区分这两组键
5. 回归测试覆盖：
   - 新 advice 键可用
   - 新 vector diff 键可用
   - 仅 advice 键可用时，vector diff 单独报告未配置或不可用
   - 旧键存在但新键缺失时，不应被当作已配置

## 非目标

1. 不改动宿主 skill-only / sidecar-only 安装合同
2. 不引入新的宿主配置写入
3. 不重做整个 `llm-acceleration-policy.json` 结构
4. 不把 vector diff 从可退化增强改成强依赖

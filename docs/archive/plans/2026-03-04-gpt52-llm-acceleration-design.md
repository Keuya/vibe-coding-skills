# GPT‑5.2 × VCO：LLM Acceleration Overlay 设计（/vibe 显式启用）

- Up: [../README.md](../README.md)
- Index: [README.md](README.md)

日期：2026-03-04
状态：Implemented（v1 + TurboMax 方案A 增强已落地）

---

## 1. 背景与目标

VCO 当前的路由体系以 **deterministic + rule/threshold/overlay** 为主（pack scoring → post-route overlays → confirm UI），稳定、可解释、可离线。但在真实工程协作里仍有两个痛点：

1. **模糊需求的澄清成本**：用户描述不完整时，靠 heuristic 可能进入 confirm_required，但确认问题不够“对症”，导致多轮来回。
2. **跨域/跨 pack 的误路由**：当 top1/top2 gap 小、或者关键词重叠时，纯规则重排难以“理解真实意图”。

本设计引入一个新的路由增强层：**LLM Acceleration Overlay**。

### 目标（Goals）

- 在不破坏 VCO 现有稳定性的前提下，引入 GPT‑5.2（model 可配置，例如 `your-model-id`）做“认知增强”：
  - 生成更好的 **确认问题（confirm questions）**
  - 对 top‑K 路由候选做 **语义重排建议（rerank advice）**
  - 生成 **意图契约补全（intent contract enrichment）** 与 “缺口（unknowns）”
  - 在任何阶段都可输出 **测试/质量建议（QA advisory）**（满足“测试部门可在任何阶段推荐”）
- 支持“烧 API 换时间”的策略（并行/推测/复核），但**只在显式 `/vibe` 或 `$vibe` 前缀时启用**。
- 默认 **advice-first**：即便 LLM 运行失败，也不影响核心路由；并且不默认替换 pack/skill 选择。

### 非目标（Non‑Goals）

- 不把 LLM 变成新的“主路由器”（不引入第二控制平面）。
- 不要求一定联网、不要求一定存在 `OPENAI_API_KEY`（无 key 时必须安全 abstain）。
- 不把 GitNexus/agency‑agents 的 overlay 逻辑强耦合进 router（它们仍是 prompt overlay advice/手动注入路径；未来可由 LLM 仅做推荐，不做强制）。

---

## 2. 总体原则

### 2.1 控制平面确定性，LLM 认知增强

- **Core routing**（pack scoring + thresholds + deterministic overlays）仍是唯一“真值”来源。
- LLM overlay 只输出：
  - `llm_acceleration_advice`（结构化 JSON，包含建议、置信度、原因）
  - 可选的 `route_mode` 提升建议（例如：把 `pack_overlay` → `confirm_required`，但默认不替换 `selected`）

### 2.2 显式 /vibe 才启用

- 仅当 `promptNormalization.prefix_detected == true` 才执行 LLM acceleration。
- 普通对话/非 /vibe 任务：零额外 API 调用，保持“隐式 S 级、零开销”的体验。

### 2.3 “烧 API 换时间”是配置化策略

通过 `config/llm-acceleration-policy.json` 的 `enhancements.*` 提供 TurboMax（方案 A）能力：

- `enhancements.diff_digest`：diff 很大时先摘要再注入上下文，降低噪声和上下文腐烂风险。
- `enhancements.committee`：多成员采样（不同 focus/temperature）+ 可选 judge 裁决，提升建议质量（以更多调用换更少返工）。
- `enhancements.confirm_question_booster`：当 `confirm_required=true` 时用一次小调用生成更短更准的确认问题（≤3）。

> 备注：这些增强仍保持 advice-first；失败会安全退化，不阻断主路由。

---

## 3. 路由接入点与数据流

### 3.1 接入点（Router hook）

位置：`scripts/router/resolve-pack-route.ps1` 的 pack scoring 之后（已拿到 `ranked/topGap/confidence/routeMode`），在 confirm UI 生成之前。

理由：
- 能拿到 top‑K 候选（LLM 能做 rerank）
- 能拿到已存在的 overlay 信号（LLM 可补充确认问题）
- 不影响 pack scoring 的 determinism

### 3.2 数据流（Data flow）

1. prompt normalization（拿到 `prefix_detected`）
2. pack scoring 得到 `ranked` + `confidence` + `top1_top2_gap`
3. 若满足 gating：
   - 采集上下文（按策略：prompt + topK + 选填 git diff/status）
   - 调用 OpenAI Responses API（Structured Output，JSON schema 严格）
   - 产出 `llm_acceleration_advice`
4. 根据 `mode`：
   - `shadow`：只写入 advice
   - `soft`：允许将 `route_mode` 提升为 confirm_required（不替换 selected）
   - `strict`：在 allowlist + topK + 置信度阈值下，允许替换 selected（可选，默认关闭）

---

## 4. 配置设计：`llm-acceleration-policy.json`

关键字段（实现级，与当前代码/配置一致）：

- `enabled / mode`：`off | shadow | soft | strict`
- `activation.explicit_vibe_only = true`
- `provider`：
  - `type = openai | mock`
  - `model`：例如 `your-model-id`
  - `base_url`：例如 `https://your-openai-compatible-endpoint/v1`
  - `timeout_ms / max_output_tokens / temperature / top_p`
- `enhancements`（TurboMax 方案 A）：
  - `diff_digest`：摘要 diff 后再注入上下文（可选择是否替换 raw diff）
  - `committee`：多成员采样 + judge（可选）
  - `confirm_question_booster`：confirm_required 时二次增强确认问题
- `context`：
  - `mode = none | prompt_only | diff_snippets_ok`
  - `max_diff_chars`：截断上限（head truncate fallback）
  - `vector_diff`：大 diff 的向量挑片注入（embeddings）
    - `embedding_model`
    - `embedding_provider.type = openai | volc_ark`
    - `embedding_provider.base_url / endpoint_path / api_key_env`
- `safety`：
  - `fallback_on_error = true`
  - `require_candidate_in_top_k = true`
  - `allow_confirm_escalation / allow_route_override`
  - `min_override_confidence`（strict 用）
- `rollout`：
  - `apply_in_modes = ["soft","strict"]`
  - `max_live_apply_rate`（采样开关，deterministic）

---

## 5. OpenAI 接入设计（Responses API）

实现一个最小可复用客户端模块：

- 输入：`model + input + response_format(json_schema strict) + timeout_ms`
- 输出：解析后的对象；失败则返回 `abstained + reason`
- 无 `OPENAI_API_KEY`：直接 abstain（不抛异常，不影响路由）
- 可选 `base_url`：支持通过 policy 的 `provider.base_url` 或环境变量 `OPENAI_BASE_URL` / `OPENAI_API_BASE` 覆盖（用于自建/代理网关）。

---

## 6. 验证与门禁

新增 gate：`scripts/verify/vibe-llm-acceleration-overlay-gate.ps1`

- **不依赖真实 API**：使用 `provider.type=mock` 或在无 key 下验证 abstain 路径。
- 断言：
  - overlay advice 字段存在且可解析
  - `explicit_vibe_only` 生效（非 /vibe 不触发）
  - mode=shadow 时不改变 selected/route_mode

并将配置加入 parity gate（main vs bundled）。

---

## 7. Rollout（推荐）

1. 默认：`mode=shadow`（只建议，不改路由）
2. 观察稳定性（misroute/confirm 率）
3. 小流量 `soft`（仅升级 confirm_required，不替换 selected）
4. 最后才考虑 `strict`（需 allowlist + 高置信度）

---

## 8. 与现有生态（agency‑agents / GitNexus）的关系

- `agency‑agents`：补齐部门/岗位视角（工程/设计/产品/市场/PM/测试/XR），以 prompt overlay 的方式注入。
- `GitNexus`：补齐代码理解与影响面证据方法（同样以 overlay 或 MCP 工具增强）。
- LLM acceleration overlay **不替代** 这些能力；它只会：
  - 在需要时推荐“应该注入哪些 overlay”
  - 帮你把确认问题问得更准确、更少轮次

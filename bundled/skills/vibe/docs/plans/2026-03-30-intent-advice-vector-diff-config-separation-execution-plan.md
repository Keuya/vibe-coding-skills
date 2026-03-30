# Intent Advice / Vector Diff 配置分离执行计划

## 内部等级

`L`

本次任务涉及配置读取、诊断、文档与测试联动，但改动边界明确，适合串行收口。

## 执行步骤

1. 冻结 requirement 与 plan 文档
2. 修改 runtime 默认键名与 env 解析链路
3. 修改 connectivity probe 状态分类与 next-step 文案
4. 修改 bootstrap doctor / settings template / 安装脚本提示
5. 修改中英文安装文档与配置说明
6. 更新并运行针对性回归测试
7. 做 node 审计与临时文件清理

## 关键改动面

- `config/llm-acceleration-policy.json`
- `config/ruc-nlpir-runtime.json`
- `config/settings.template.*.json`
- `scripts/router/modules/01-openai-responses.ps1`
- `scripts/router/modules/48-llm-acceleration-overlay.ps1`
- `scripts/verify/runtime_neutral/router_ai_connectivity_probe.py`
- `scripts/verify/runtime_neutral/bootstrap_doctor.py`
- `scripts/verify/vibe-bootstrap-doctor-gate.ps1`
- `scripts/bootstrap/one-shot-setup.sh`
- `scripts/bootstrap/one-shot-setup.ps1`
- `docs/install/*.md`
- `tests/runtime_neutral/test_router_ai_connectivity_probe.py`
- `tests/runtime_neutral/test_bootstrap_doctor.py`

## 新默认键名

- Advice:
  - `VCO_INTENT_ADVICE_API_KEY`
  - `VCO_INTENT_ADVICE_BASE_URL`
  - `VCO_INTENT_ADVICE_MODEL`
- Vector diff:
  - `VCO_VECTOR_DIFF_API_KEY`
  - `VCO_VECTOR_DIFF_BASE_URL`
  - `VCO_VECTOR_DIFF_MODEL`

## 验证命令

```bash
pytest -q \
  tests/runtime_neutral/test_router_ai_connectivity_probe.py \
  tests/runtime_neutral/test_bootstrap_doctor.py
```

必要时追加：

```bash
git diff --check
```

## 回滚规则

1. 不回滚与本任务无关的用户改动
2. 若发现默认新键名导致 advice 主链完全不可测，优先修 probe / doctor / docs，再考虑代码回滚
3. 不恢复到“默认回退旧 `OPENAI_*`”的共享配置面

## 阶段清理

1. 审计 node 进程
2. 清理临时文件
3. 保持工作树仅包含本任务必要变更

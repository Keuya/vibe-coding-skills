# 执行计划: PR #102 冲突消解与审查问题修补

## 内部等级

L

## 步骤

1. 拉取最新 `origin/main`，确认 PR 的真实冲突面，并验证 CodeRabbit findings 是否成立。
2. 将 `main` 合入当前分支，优先保留主线已有架构收口，再补回本 PR 需要的 `opencode` 修复与隔离根逻辑。
3. 修复已证实的问题：
   - `check.sh` / `install.sh` 的 OpenCode 根误接收
   - `install_vgo_adapter.py` 对 `opencode.json.example` 的安装契约不一致
   - `vibe-governance-helpers.ps1` 中 `opencode` 分支的死代码
4. 同步所有 bundled 镜像副本，避免 canonical / bundled 漂移。
5. 运行定向测试与格式校验，确认没有新的回归。
6. 进行阶段清理，审计 node 进程与临时文件，最后整理提交并更新 PR。

## 验证命令

```bash
python3 -m unittest \
  tests.runtime_neutral.test_opencode_preview_parity \
  tests.runtime_neutral.test_windsurf_runtime_core \
  tests.runtime_neutral.test_openclaw_runtime_core

git diff --check
```

## 回滚规则

- 若主线合流后出现大范围 bundle 漂移，以 canonical root 为准重新同步 bundle
- 若 review 建议与主线新逻辑冲突，以实际运行验证和当前主线语义为准

## 清理要求

- 阶段结束后审计本任务启动的 node / prettier / test 相关进程
- 删除本任务新增的临时冲突分析文件（若有）
- 不触碰非本任务来源的运行进程

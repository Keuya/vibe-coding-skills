# Batch 0-9 Closure Report

- Up: [`README.md`](README.md)
- Repo docs root: [`../README.md`](../README.md)
- Master cleanup plan: [`2026-03-08-repo-full-cleanup-master-plan.md`](2026-03-08-repo-full-cleanup-master-plan.md)

## Purpose

这份报告记录 `2026-03-09` 对 cleanup umbrella plan 中 **Batch 0-9** 的一次阶段性执行收口：把 repo cleanliness、runtime boundary、encoding/BOM、mirror parity、installed runtime freshness 与说明文档统一拉通，并形成可推送的 tracked summary。这里的“收口”指治理与验证闭环已成立，不等同于整个 repo remaining dirty 已清零。

## What Was Closed

### Batch 0 — Inventory / Classification

- 修复 `scripts/governance/export-repo-cleanliness-inventory.ps1` 的 Markdown artifact 生成解析错误，使 inventory operator 可稳定执行。
- 重跑 inventory，确认 dirty workset 已可稳定分为 `canonical / mirror:bundled / mirror:nested` 三个平面。
- 补齐 `config/repo-cleanliness-policy.json` 中的治理覆盖，把 `.gitattributes` 与 `third_party/` 纳入 managed workset，清除 `other_dirty` 漏分类。

### Batch 1 — Runtime Noise Separation

- `vibe-repo-cleanliness-gate` 在 normal mode 下通过：
  - local scratch / operator noise = 0
  - runtime-generated visible = 0
  - uncategorized dirty visible = 0
- 说明当前 remaining dirty 已经不是噪音外溢，而是受治理的 canonical / mirror backlog。

### Batch 2 — Encoding / BOM / EOL

- 新增 `.gitattributes`，固定 governed text assets 的 EOL 约束。
- 修复 `check.sh` 的 UTF-8 BOM 风险，并通过 canonical -> bundled -> nested sync 统一三平面 shell 入口编码状态。
- `vibe-bom-frontmatter-gate` 对 canonical / bundled / nested / installed 的 `SKILL.md` 全部通过，frontmatter byte-0 治理链闭环成立。

### Batch 4-5 — Docs / References / Scripts / Config Spine

已落地并纳入 repo entry spine：

- `config/index.md`
- `third_party/README.md`
- `docs/external-tooling/README.md`
- `references/overlays/index.md`
- `scripts/router/README.md`
- `scripts/overlay/README.md`
- `scripts/verify/fixtures/README.md`

这些入口把 config / external-tooling / overlays / router / verify-fixtures 从“散落文件集合”提升为可导航的 family surface。

### Batch 6 — Mirror Convergence and Drift Closure

- 执行 `scripts/governance/sync-bundled-vibe.ps1 -Preview -PruneBundledExtras`。
- 执行 `scripts/governance/sync-bundled-vibe.ps1 -PruneBundledExtras` 完成 canonical -> bundled -> nested 收口。
- 以下门禁通过：
  - `vibe-mirror-edit-hygiene-gate.ps1`
  - `vibe-nested-bundled-parity-gate.ps1`
  - `vibe-version-packaging-gate.ps1`

### Batch 7-8 — Boundary / Entry Explanation

- root `README.md` 已补充 start-here / plane model / repo planes 说明。
- `third_party/README.md` 与 cleanliness policy 一起把第三方边界从“存在但未入治理”提升为显式受控平面。

### Batch 9 — Recurring Hygiene / Installed Runtime Closure

- 运行 `install-local-worktree-excludes.ps1`，把 `task_plan.md` / `findings.md` / `progress.md` 下沉到 worktree-local excludes。
- 重新执行 `install.ps1 -Profile full` 到 `$HOME/.codex`。
- 以下运行态门禁通过：
  - `vibe-installed-runtime-freshness-gate.ps1`
  - `vibe-release-install-runtime-coherence-gate.ps1`

## Gate Snapshot

| Gate | Result |
| --- | --- |
| `vibe-repo-cleanliness-gate.ps1` | PASS |
| `vibe-output-artifact-boundary-gate.ps1` | PASS |
| `vibe-bom-frontmatter-gate.ps1` | PASS |
| `vibe-mirror-edit-hygiene-gate.ps1` | PASS |
| `vibe-nested-bundled-parity-gate.ps1` | PASS |
| `vibe-version-packaging-gate.ps1` | PASS |
| `vibe-installed-runtime-freshness-gate.ps1` | PASS |
| `vibe-release-install-runtime-coherence-gate.ps1` | PASS |

> 说明：本轮没有把 **Batch 3（canonical workset admission / commit closure）** 单独做成 zero-dirty 终局；它被明确保留为下一步收口对象。Batch 0-9 closure 在本报告中表示执行闭环成立，而不是所有 governed backlog 已归零。

## Current Interpretation

Batch 0-9 的执行闭环已经成立，但 **master cleanup plan 仍未整体完结**。

剩余 backlog 的性质已经被收口为：

- 不是 runtime 噪音；
- 不是 uncategorized drift；
- 而是尚未 commit / archive / prune 的 governed canonical + mirror workset。

换言之，当前的后续工作不再是“先判断哪里脏”，而是“对已知 workset 做 admission / archive / commit closure”。

## Next Closure Step

建议后续直接进入 **canonical workset closure**：

1. 优先收口 `scripts/verify/`、`docs/`、`config/`、`references/` 的 canonical backlog；
2. 每次 canonical edit 后只通过 `sync-bundled-vibe.ps1` 触达 mirrors；
3. 继续以 repo-cleanliness / parity / runtime-freshness gates 作为 push 前闭环。

# Tracked Mirror Retirement 实施需求

**日期**: 2026-04-01
**目标**: 彻底退役 repo 中被跟踪的 `bundled/skills/vibe` 镜像，只保留 canonical `vibe` 与安装/运行时所需的生成式兼容产物，并确保 install / release / check 主链路不发生功能性回退。

## Intent Contract

- Goal: 把 `vibe` 的仓库真相面收敛到 canonical root，移除 repo-tracked bundled mirror debt。
- Deliverable:
  - `config/version-governance.json` 不再把 `bundled/skills/vibe` 作为 repo mirror target。
  - install / uninstall / runtime freshness / coherence 主链路改为基于 canonical payload 与生成式 compatibility root 工作。
  - `bundled/skills/vibe` 从仓库中删除。
  - 关键治理文档与测试更新到新契约。
- Constraints:
  - 不改变用户可见的 `skills/vibe` 安装路径。
  - 不移除 install-time nested compatibility root，除非已有链路不再需要它。
  - 不引入新的 repo-tracked generated payload surface。
- Acceptance Criteria:
  - 仓库中不存在 `bundled/skills/vibe/SKILL.md` tracked mirror root。
  - `install_vgo_adapter.py` / `Install-VgoAdapter.ps1` 不依赖 repo mirror 就能安装 `skills/vibe`。
  - coherence / freshness 链路不再要求 `sync-bundled-vibe.ps1` 或 repo mirror closure。
  - 关键非回归测试通过。
- Product Acceptance Criteria:
  - release/install/check 的外部行为保持稳定。
  - mirror debt 的根因从“repo 常驻副本”降为“canonical + generated compatibility”。
  - 后续版本迭代不再需要同步维护 `bundled/skills/vibe`。
- Manual Spot Checks:
  - 检查仓库中 `bundled/skills/vibe` 已删除。
  - 检查安装后 `target/skills/vibe` 仍完整可用。
  - 检查安装后 `target/skills/vibe/bundled/skills/vibe` 仅作为生成式兼容面存在。
- Completion Language Policy:
  - 只有在删除 tracked mirror、更新主链路并完成验证后，才能宣称“tracked mirror 已退役”。
- Delivery Truth Contract:
  - 必须给出实际测试或 gate 证据，不能只给结构性判断。
- Non-goals:
  - 不重写整个 `bundled/skills/*` 生态。
  - 不清理所有历史文档中的镜像词汇。
  - 不重构与本债务无关的 router / runtime 逻辑。
- Autonomy Mode: `interactive_governed`
- Inferred Assumptions:
  - 其他 vendored skills 仍通过 `bundled/skills/*` 分发，只有 `vibe` 需要从 tracked mirror 特判退出。
  - install-time nested compatibility 仍有保留价值，因此本轮只移除 repo mirror，不移除生成式兼容层。

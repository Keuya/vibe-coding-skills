# Install Generated Nested Compatibility 实施需求

**日期**: 2026-03-30
**目标**: 作为 Wave 4 第二阶段，把 installed runtime 的 nested compatibility surface 从“依赖 repo 常驻 nested mirror”升级为“install-time authoritative materialization”。

## Intent Contract

- Goal: 在 repo sync 已不再持续维护 `nested_bundled` 的前提下，保证 install/runtime-core 仍能稳定产出 `skills/vibe/bundled/skills/vibe` 兼容面。
- Deliverable:
  - install-time runtime-core 链路显式 materialize `skills/vibe/bundled/skills/vibe`。
  - materialized nested surface 来自 installed canonical vibe root，而不是 repo 内已有 nested baseline。
  - 新增 focused integration proof，证明 repo 中缺失 nested baseline 时，安装后仍生成 nested compatibility。
- Constraints:
  - 不改变 `nested_bundled.materialization_mode = release_install_only`。
  - 不要求 repo 常驻 nested tracked root 先被删除。
  - 不放宽 existing freshness/sanitization contract。
- Acceptance Criteria:
  - shell install 在 `--skip-runtime-freshness-gate` 场景下，可从缺失 nested baseline 的 fixture repo materialize nested compatibility。
  - installed nested `config/version-governance.json` 与 installed canonical copy 一致。
  - installed nested skill entrypoint 仍被 sanitize 为 `SKILL.runtime-mirror.md`。
- Product Acceptance Criteria:
  - 后续从 repo 常驻结构中移除 nested tracked mirror 时，不会导致 install-time compatibility 退化。
  - release-time 与 install-time 都有各自明确 proof，不再依赖 repo 历史残留结构偶然成立。
- Manual Spot Checks:
  - 检查 fixture repo 的 `bundled/skills/vibe/bundled/skills/vibe` 缺失。
  - 检查安装后 `target/skills/vibe/bundled/skills/vibe` 存在。
  - 检查 `SKILL.md` 已被重命名为 `SKILL.runtime-mirror.md`。
- Completion Language Policy:
  - 只能宣称“Wave 4 install-time nested compatibility materialization 已落地”，不能宣称 repo 内 nested tracked mirror 已移除。
- Delivery Truth Contract:
  - 必须有 fresh integration test evidence。
- Non-goals:
  - 不删除 repo 内 nested tracked root。
  - 不修改 release-cut operator 的 release-time materialization 语义。
  - 不同时推进 mirror topology 的最终 tracked-root 删除。
- Autonomy Mode: `interactive_governed`
- Inferred Assumptions:
  - runtime-core packaging 仍会先复制 `bundled/skills/**`，但 install-time nested compatibility 不能继续依赖该过程携带历史 nested baseline。

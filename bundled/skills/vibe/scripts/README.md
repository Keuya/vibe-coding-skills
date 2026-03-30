# Scripts

`scripts/` 是 VCO 的 operator surface。这个索引只负责把操作者带到正确的脚本入口，不承担 closure proof 合同或长期 reference 导航。

## Start Here

### Operator Entrypoints

### Bootstrap / Setup Highlights

- [`bootstrap/one-shot-setup.ps1`](./bootstrap/one-shot-setup.ps1): single-command bootstrap for install -> optional settings seeding -> MCP materialization -> `check.ps1 -Deep`
- [`bootstrap/one-shot-setup.sh`](./bootstrap/one-shot-setup.sh): shell-native bootstrap for Linux / macOS with the same install -> settings seed -> MCP materialization -> `check.sh --deep` flow; maintained for macOS system Bash 3.2 + Python 3.10+
- [`setup/materialize-codex-mcp-profile.ps1`](./setup/materialize-codex-mcp-profile.ps1): materialize the selected MCP profile into `~/.codex\mcp\servers.active.json`
- [`setup/persist-codex-openai-env.ps1`](./setup/persist-codex-openai-env.ps1): safely persist built-in intent-advice env values into target `settings.json`
- [`setup/sync-codex-settings-to-user-env.ps1`](./setup/sync-codex-settings-to-user-env.ps1): optionally sync configured `VCO_INTENT_ADVICE_*` / `VCO_VECTOR_DIFF_*` settings into the user environment

- [`governance/README.md`](./governance/README.md)：human-run operator surface，覆盖 sync / rollout / release / audit / policy probes。
- [`verify/README.md`](./verify/README.md)：verify surface entrypoint 与 canonical run order。
- [`verify/gate-family-index.md`](./verify/gate-family-index.md)：gate family map 与证据型运行顺序。
- [`common/README.md`](./common/README.md)：shared helper API、UTF-8 no-BOM 写入规则与 execution-context helpers。
- [`router/README.md`](./router/README.md)：router decision surface 与 module layout。
- [`overlay/README.md`](./overlay/README.md)：overlay suggestion surface，保持 advice-first。
- [`verify/fixtures/README.md`](./verify/fixtures/README.md)：verify mock / pilot / fixture navigation。

### Cross-Layer Handoff

当你已经离开“该运行哪个脚本”的问题，而需要进入合同层或证据层时，切换到：

- [`../docs/status/non-regression-proof-bundle.md`](../docs/status/non-regression-proof-bundle.md)：minimum closure proof contract。
- [`../references/index.md`](../references/index.md)：long-lived contracts、registries、ledgers 与 reference playbooks。

## Directory Roles

| Path | Role | Notes |
| --- | --- | --- |
| `scripts/governance/` | operator entrypoints | rollout、release、mirror、policy 与 audit commands |
| `scripts/verify/` | executable gates | stop-ship、advisory、plane、release 与 closure families |
| `scripts/common/` | shared primitives | UTF-8 no BOM、execution-context、parity 与 wave-runner helpers |
| `scripts/router/` | router helpers | route probing、pack routing 与 keyword audit support |
| `scripts/overlay/` | overlay helpers | advice-first overlay 与 provider suggestion helpers |
| `scripts/bootstrap/`, `scripts/setup/` | environment bootstrap | install、setup 与 compatibility helpers |
| `scripts/research/`, `scripts/learn/` | support surfaces | auxiliary surfaces，不是最小 cleanup proof bundle |

## Navigation Boundary

- This page owns operator navigation inside `scripts/`。
- [`verify/gate-family-index.md`](./verify/gate-family-index.md) owns verify-family grouping and typical evidence-producing run order。
- [`../docs/status/non-regression-proof-bundle.md`](../docs/status/non-regression-proof-bundle.md) owns the minimum closure proof contract。
- [`../references/index.md`](../references/index.md) owns long-lived contracts、registries、ledgers 与 reference playbooks。

## Rules

- topology-aware scripts must be run from the canonical repo root，不能从 mirror 或 installed runtime 副本直接执行。
- mirror、packaging 或 release 相关改动完成后，必须回到 [`verify/README.md`](./verify/README.md) 复跑对应 gates。
- shared logic belongs in `scripts/common/`，不要在单脚本里重复实现一份 ad hoc helper。
- research helpers may depend on external corpora, but those dependencies must stay explicit and parameterizable。

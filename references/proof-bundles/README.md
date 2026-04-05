# Proof Bundles

`references/proof-bundles/` 只保留仍被 adapters、tests、replay 或 verify gates 直接消费的 machine-readable bundle。

最小 live proof surface 默认只保留：

- manifest
- bundle README 或 summary
- operation record
- contract-required receipts

没有活跃消费者的 duplicated verify outputs、command audit copies、receipt inventories，以及仅供人工回放的 raw shell logs，不应继续占据 live proof surface。

## Live Bundles

- `linux-full-authoritative-candidate`
- `claude-code-managed-closure-candidate`
- `openclaw-runtime-core-preview-candidate`

## Archive

- 历史或说明型 bundle 进入 [`../archive/proof-bundles/README.md`](../archive/proof-bundles/README.md)。
- 已从 live contract 退下来的低信号补充件可按 bundle family 归入 archive，例如 `../archive/proof-bundles/claude-code-managed-closure-candidate/`。

## Rule

- 没有 manifest、没有活跃消费者、且只承担历史说明作用的 proof bundle 不应继续留在 live surface。
- 对已经缩减为 manifest + operation record + receipt 的 live bundle，额外 raw logs 默认通过 git history 恢复，而不是继续长期跟踪。

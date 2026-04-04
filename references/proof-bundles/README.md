# Proof Bundles

`references/proof-bundles/` 只保留仍被 adapters、tests、replay 或 verify gates 直接消费的 machine-readable bundle。

## Live Bundles

- `linux-full-authoritative-candidate`
- `claude-code-managed-closure-candidate`
- `openclaw-runtime-core-preview-candidate`
- `official-runtime-baseline`

## Archive

- 历史或说明型 bundle 进入 [`../archive/proof-bundles/README.md`](../archive/proof-bundles/README.md)。

## Rule

- 没有 manifest、没有活跃消费者、且只承担历史说明作用的 proof bundle 不应继续留在 live surface。

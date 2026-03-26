# 2026-03-26 OpenCode Preview Adapter Requirement

- Topic: promote OpenCode from placeholder to a truthful preview adapter.
- Mode: interactive_governed
- Goal: land a host-native OpenCode preview lane with bounded install/check behavior, wrapper payloads, proof notes, and no false closure claims.

## Deliverable

A working change that:

1. activates `opencode` in `adapters/index.json`
2. promotes the OpenCode host profile, closure contract, and dist manifests from placeholder to `preview`
3. installs OpenCode-targeted preview payload into host-native roots without taking ownership of the real `opencode.json`
4. adds OpenCode command and agent wrapper scaffolds for governed `vibe` usage
5. updates install/check entrypoints so `--host opencode` works on both shell and PowerShell paths
6. updates universalization docs so adapter, dist, and docs state the same truth
7. adds replay/proof documentation and a runnable OpenCode preview smoke verification
8. records phase execution and cleanup receipts for this governed pass

## Constraints

- No regression to Codex governed install/check behavior
- No false promotion above `preview`
- Real host config, provider credentials, plugin provisioning, and MCP trust remain host-managed
- Existing unrelated repo changes must remain untouched
- Verification must include fresh adapter/doc gates and an actual OpenCode CLI smoke pass when the local binary exists
- Phase cleanup required before completion language

## Acceptance Criteria

- `install.* --host opencode` resolves to a host-native default root and writes only preview payload plus runtime-core payload
- `check.* --host opencode` verifies the OpenCode preview payload truthfully
- `adapters/opencode/*`, `dist/host-opencode/manifest.json`, and `dist/manifests/vibeskills-opencode.json` all agree on `preview`
- `docs/universalization/*.md` and adapter manifests agree on OpenCode status and closure wording
- OpenCode command wrappers exist for `vibe`, `vibe-implement`, and `vibe-review`
- OpenCode agent wrappers exist for `vibe-plan`, `vibe-implement`, and `vibe-review`
- A committed verification script can install/check the OpenCode preview lane in a temp workspace and emit machine-readable results
- Existing core adapter closure and dist manifest gates still pass after the change

## Non-Goals

- Promoting OpenCode to `supported-with-constraints`
- Automatic provider credential provisioning
- Automatic plugin installation inside the OpenCode host
- Claiming that `opencode debug skill` is authoritative if local runtime behavior disagrees with docs

## Inferred Assumptions

- OpenCode officially exposes host-native global and project roots for skills, commands, and agents.
- The repository should prefer OpenCode-native roots over compatibility mirrors such as `.claude/skills` or `.agents/skills`.
- Local OpenCode CLI behavior may lag or diverge from official docs, so preview proof must separate install truth from unresolved runtime discovery gaps.

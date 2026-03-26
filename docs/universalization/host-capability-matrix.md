# Host Capability Matrix

> Scope: execution contract for universalization, not marketing language.

## Purpose

This matrix freezes the difference between:

- official runtime ownership
- preview scaffold support
- runtime-core-only neutral lanes
- advisory-only contract consumption

It prevents the project from collapsing all hosts into a fake "one runtime fits all" story.

## Status Vocabulary

| Status                       | Meaning                                                                                                |
| ---------------------------- | ------------------------------------------------------------------------------------------------------ |
| `supported-with-constraints` | repo has real host evidence and a bounded support claim, but some surfaces remain host-managed         |
| `preview`                    | adapter contract exists and scaffold/check proof exists, but full host closure is still incomplete     |
| `not-yet-proven`             | host is named in the migration target, but there is no verified host-native runtime contract yet       |
| `advisory-only`              | host may consume canonical contracts or runtime-core payload, but the repo makes no host closure claim |

## Host Matrix

| Host         | Status                       | Runtime Role             | Settings Contract                                                                  | Plugin/MCP Contract         | Release Closure        | Notes                                                                      |
| ------------ | ---------------------------- | ------------------------ | ---------------------------------------------------------------------------------- | --------------------------- | ---------------------- | -------------------------------------------------------------------------- |
| Codex | `supported-with-constraints` | official-runtime-adapter | repo template + materialization exist | host-managed but documented | strongest current path | current reference lane |
| Claude Code | `preview` | host-adapter-preview | repo scaffold exists | mostly host-managed | preview-scaffold | install/check can scaffold and verify preview truth |
| OpenCode | `preview` | host-adapter-preview | repo installs wrappers + example scaffold, real `opencode.json` stays host-managed | host-managed but documented | preview-scaffold | host-native roots are supported, but runtime discovery proof is incomplete |
| Generic Host | `advisory-only`              | contract-consumer        | neutral runtime-core only                                                          | host-defined                | runtime-core-only      | canonical skill truth can be consumed without host promise                 |

## Capability Guidance

### Codex

- Strongest current evidence for settings, install, health-check, and governed runtime payload.
- Still depends on host-managed plugin provisioning and credential provisioning.

### Claude Code

- The repo can now scaffold preview settings + hooks and run preview health checks.
- This is still not a full Claude Code closure claim.

### OpenCode

- The repo can install runtime-core plus command/agent wrapper scaffolds into OpenCode roots.
- The real `opencode.json`, provider credentials, plugin provisioning, and MCP trust remain host-managed.
- Local proof on OpenCode CLI `1.2.27` now confirms `opencode debug paths`, `opencode debug skill`, and `opencode debug agent vibe-plan` on the committed preview smoke path.
- The lane still remains `preview` because command replay and platform-specific proof bundles are not yet frozen.

### Generic Host

- Useful when the user wants canonical skills and runtime-core only.
- Must never be described as an official runtime or a host-native closure lane.

## Promotion Rule

No adapter may be promoted above its current status unless all of the following exist:

1. host profile
2. settings map
3. platform contracts
4. replay-backed verification
5. install isolation proof
6. wording parity between docs and measured support

# 2026-03-21 Universal Install Generalization Execution Requirement

- Topic: execute the universal install generalization program with XL-style wave planning and verification.
- Mode: benchmark_autonomous
- Goal: implement the next concrete waves of universal installation so users can explicitly target the correct host while preserving Codex baseline truth and introducing a real generic runtime-core lane.

## Deliverable

A working implementation that:

1. introduces adapter-driven install semantics
2. adds a real `generic` host lane for runtime-core installation
3. preserves Codex as the strongest official closure lane
4. keeps Claude Code truthful as preview, with scaffold-level support only
5. updates docs and verification surfaces accordingly

## Constraints

- No regression on existing Codex baseline behavior
- No silent host/path conflation
- No false full-support claims for preview hosts
- All execution must remain traceable to requirement + plan
- Stage cleanup required after each meaningful phase, including temp/node hygiene

## Acceptance Criteria

- `install/check/bootstrap` support `host + target-root` semantics
- `generic` installs runtime core without writing Codex-shaped host state
- `codex` remains installable and checkable in isolated temp roots
- `claude-code` provides preview scaffold/truthful guidance rather than false closure
- docs and manifests reflect new host model
- isolated verification commands provide fresh evidence

## Non-Goals

- Full Claude Code closure
- Full OpenCode closure
- Automatic plugin provisioning across all hosts

## Inferred Assumptions

- The most valuable concrete implementation slice is Phases 1-3 from the design: generic lane, codex formal adapter, claude preview scaffold.
- OpenCode remains contractual placeholder unless time remains after the core waves are stable.

# 2026-03-31 KVM Host Rerun Requirement

- Topic: move the Windows ISO proof lane from the current no-KVM environment onto a host that can actually provide hardware-accelerated KVM.
- Mode: interactive_governed
- Goal: make the repository ready to truthfully detect, demand, and re-run the existing Windows ISO path on a real KVM-capable host.

## Deliverable

A working change that:

1. freezes the requirement and plan for a KVM-host rerun
2. adds a repo-owned readiness check that distinguishes a real KVM host from the current nested or no-passthrough environment
3. adds a launcher guardrail so future reruns can require KVM instead of silently falling back to `tcg`
4. documents the current blocker and the exact operator handoff needed to continue on the right machine

## Constraints

- No claim that the current session can switch machines by itself if `/dev/kvm` is not exposed
- No false claim that `KVM` is available merely because `lscpu` reports a virtualized environment
- No false promotion of the Windows Claude lane before a KVM-backed guest actually reaches install/check/smoke
- The current ISO and launch path should remain reusable without inventing a new Windows flow

## Acceptance Criteria

- The repo contains a KVM readiness check script
- The VM launcher can be told to fail fast unless KVM is genuinely available
- The current environment is checked and its KVM boundary is captured truthfully
- Docs explain how to re-run the existing ISO path on the next host without ambiguity

## Non-Goals

- Claiming Claude was tested on Windows in this batch
- Claiming that the current guest can elevate itself to the physical KVM host
- Replacing the current ISO path with a different Windows install workflow

## Inferred Assumptions

- The user still wants the existing Microsoft ISO route, not a different Windows media strategy
- A future machine with real `/dev/kvm` access is available outside this current session
- The safest next step is to make the repo refuse accidental `tcg` fallback on that future rerun

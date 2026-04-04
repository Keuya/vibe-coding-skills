# 2026-03-31 Claude Linux Proof Freeze Requirement

- Topic: finish the missing Linux proof work for the Claude Code managed-closure lane so the repo can honestly stop calling `claude-code/linux` `not-yet-proven`.
- Mode: interactive_governed
- Goal: freeze fresh Linux install/check evidence plus a real Claude CLI smoke result, then synchronize the adapter, replay, and status surfaces to the lane's existing promotion target.

## Deliverable

A working change that:

1. captures fresh Linux proof artifacts for the Claude Code lane
2. includes a real Claude CLI smoke result on Linux
3. freezes those artifacts into a versioned proof-bundle surface
4. updates `claude-code/linux` truth from `not-yet-proven` to `supported-with-constraints` only if the evidence really supports that move
5. keeps Windows and macOS below promotion unless their own proof exists

## Constraints

- No claim that Claude Code becomes an official-runtime or Codex-equivalent lane
- No claim that Windows or macOS are promoted as part of this batch
- Linux promotion must stop at `supported-with-constraints`, which is the lane's declared target
- Proof artifacts must be reproducible from versioned repository contents rather than unstaged local residue
- Verification must include real command output, not doc-only synchronization

## Acceptance Criteria

- The repo contains a frozen Linux proof bundle or bundle extension for Claude Code
- The evidence includes fresh install proof, fresh check proof, and a real Claude CLI smoke result on Linux
- `adapters/claude-code/platform-linux.json` reflects the new truthful status only if the bundle is complete
- Replay truth and status docs are synchronized to the measured result
- Required gates and targeted tests pass after the status update

## Non-Goals

- Promoting `claude-code/linux` above `supported-with-constraints`
- Claiming cross-platform parity for Claude Code
- Regressing existing Codex, Windows, or macOS truth surfaces

## Inferred Assumptions

- A bounded managed Claude settings + hook surface is already implemented, so the missing work is proof freezing rather than a broad new feature build
- A temporary Linux target root and/or Docker container is acceptable evidence if it is clearly recorded as the proof environment
- The local Claude CLI binary can be used for a truthful Linux smoke result

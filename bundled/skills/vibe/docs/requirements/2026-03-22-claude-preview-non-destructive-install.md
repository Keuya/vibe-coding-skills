# 2026-03-22 Claude Preview Non-Destructive Install Requirement

- Topic: make the Claude preview install path non-destructive.
- Mode: interactive_governed
- Goal: prevent the Claude preview lane from overwriting real host settings while preserving truthful preview guidance.

## Deliverable

A working change that:

1. never overwrites an existing Claude `settings.json`
2. never writes placeholder provider URLs into the real host settings file
3. writes preview example settings into a separate preview file
4. keeps hooks scaffold behavior intact
5. updates install/check/contracts/docs to match the non-destructive behavior
6. adds regression tests proving existing settings survive preview scaffold

## Constraints

- No regression to Codex governed install behavior
- No false claim of full Claude closure
- Preview scaffold must remain clearly separated from host-managed credentials
- Verification must include fresh regression evidence
- Phase cleanup required after verification

## Acceptance Criteria

- `scaffold-claude-preview.sh` preserves existing `settings.json`
- `scaffold-claude-preview.ps1` preserves existing `settings.json`
- Claude preview writes a separate example file instead of `settings.json`
- `install_vgo_adapter.py` and `Install-VgoAdapter.ps1` follow the same rule
- `check.sh` and `check.ps1` verify the new preview artifact instead of requiring `settings.json`
- regression tests pass for shell and PowerShell preview scaffold behavior

## Non-Goals

- Full Claude Code closure
- Automatic provider credential provisioning
- Automatic merge into host-native settings formats

## Inferred Assumptions

- The original preview intent was to offer a scaffold/example, not to take ownership of real host credentials.
- A dedicated preview file is safer than merge logic for the current closure level.

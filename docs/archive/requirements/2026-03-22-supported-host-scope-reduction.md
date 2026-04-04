# 2026-03-22 Supported Host Scope Reduction Requirement

- Topic: temporarily narrow the public install and support surface to `codex` and `claude-code` only.
- Mode: benchmark_autonomous
- Goal: make the repository truthful and defensible by removing `generic` and `opencode` from active installation, bootstrap, and public support entrypoints.

## Deliverable

A working update that:

1. exposes only `codex` and `claude-code` as supported hosts in adapter resolution and install/check/bootstrap entrypoints
2. keeps host selection explicit and truthful in both shell and PowerShell bootstrap flows
3. updates public README and install docs so they no longer present `generic` or `opencode` as supported user-facing lanes
4. preserves the non-destructive Claude Code preview guidance and Codex capability boundaries
5. verifies syntax and consistency before completion

## Constraints

- No vague “future lane” claims in the main install surface
- No instructions that ask users to paste API keys or provider secrets into chat
- Claude Code guidance must remain non-destructive to the user's real `settings.json`
- Codex guidance must stay limited to supportable settings / MCP / CLI surfaces
- Historical/internal files may remain in the repo, but they must not stay on the active public install path
- Complete cleanup after verification

## Acceptance Criteria

- `adapters/index.json` only registers `codex` and `claude-code`
- `install.sh`, `check.sh`, `scripts/bootstrap/one-shot-setup.sh` reject hosts other than `codex` and `claude-code`
- `install.ps1`, `check.ps1`, and shared PowerShell host helpers only accept `codex` and `claude-code`
- bootstrap host prompts only offer `codex` and `claude-code`
- public README and primary install docs describe only two supported hosts
- no main install doc tells users to install into `generic`, `opencode`, or “other agents”
- verification confirms script syntax, JSON validity, and no lingering unsupported-host references in the targeted public surface

## Non-Goals

- Deleting historical `generic` or `opencode` assets from the repository
- Reworking deeper internal universalization design archives
- Expanding support to other agents via new adapters

## Inferred Assumptions

- The support problem is caused by both documentation drift and executable entrypoints that still accept unsupported hosts.
- Restricting the active registry is preferable to leaving dormant public lanes that continue to look installable.
- Public trust is more important than preserving a broader but unproven compatibility story.

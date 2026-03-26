# 2026-03-26 OpenCode Documentation Refresh Requirement

- Topic: refresh installation and onboarding documentation so OpenCode preview support is described truthfully and consistently across public entrypoints.
- Mode: interactive_governed
- Goal: update install, quick-start, deployment, README, and capability docs so they match the implemented OpenCode preview adapter and measured proof state.

## Deliverable

A documentation change set that:

1. updates public install entry docs to include `opencode` as a documented preview lane
2. keeps `codex` as the strongest current lane and `claude-code` / `opencode` as truthful preview lanes
3. explains that OpenCode currently uses direct `install.*` / `check.*` entrypoints rather than one-shot bootstrap
4. points OpenCode operators to the dedicated `docs/install/opencode-path*.md` pages
5. aligns README, quick-start, deployment, install policy, and host capability wording with the current measured OpenCode proof
6. records governed runtime receipts for this doc-refresh pass

## Constraints

- No false promotion above `preview`
- No change to runtime code or support claims that verification cannot defend
- Historical requirement and plan docs should remain historical records unless a clarification note is necessary
- Existing unrelated user changes must remain untouched
- Final completion language requires fresh verification evidence

## Acceptance Criteria

- Public install docs no longer say that only `codex` and `claude-code` are supported install targets
- OpenCode docs consistently describe:
  - preview lane status
  - direct `install.* --host opencode` and `check.* --host opencode` usage
  - default OpenCode target root behavior
  - host-managed ownership of the real `opencode.json`, provider credentials, plugin provisioning, and MCP trust
- README and quick-start entrypoints route OpenCode users to the correct doc
- `docs/universalization/host-capability-matrix.md` matches the current measured proof note
- Verification passes after the edits

## Non-Goals

- Promoting OpenCode to `supported-with-constraints`
- Adding one-shot bootstrap support for OpenCode
- Claiming full OpenCode host closure
- Creating or discussing a PR in this pass

## Inferred Assumptions

- OpenCode preview install/check support landed before this doc refresh pass
- The dedicated OpenCode install docs are already the most detailed source of truth and should be reused by broader entry docs
- The local proof on OpenCode CLI `1.2.27` is strong enough to justify `preview`, but not strong enough to justify wider promotion

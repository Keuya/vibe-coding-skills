# 2026-03-22 Host Plugin Policy Rewrite Requirement

- Topic: fully rewrite the Chinese and English host-plugin-policy documents so they match the current two-host support boundary and no longer carry historical plugin baggage.
- Mode: benchmark_autonomous
- Goal: make the policy readable and defensible for open-source community readers by replacing historical `manual-codex` plugin strategy with a current-state host integration policy.

## Deliverable

A documentation update that:

1. fully rewrites `docs/install/host-plugin-policy.md`
2. fully rewrites `docs/install/host-plugin-policy.en.md`
3. limits the policy to the currently supported hosts: `codex` and `claude-code`
4. clearly separates repo-installed payload, host-managed configuration, MCP registration, and optional CLI enhancements
5. removes historical recommendation ladders around `hookify`, `everything-claude-code`, `claude-code-settings`, and `ralph-loop`

## Constraints

- No false host-plugin support claims
- No advice that asks people to paste secrets into chat
- Claude Code must remain non-destructive to the real `settings.json`
- Codex guidance must remain limited to supportable settings / MCP / optional CLI surfaces
- The rewritten docs should be simpler than the historical versions, not a compressed restatement of the same baggage

## Acceptance Criteria

- both files are fully rewritten, not lightly patched
- both files describe only `codex` and `claude-code` as supported hosts
- both files explain what the repo does automatically versus what the user still configures locally
- both files explicitly reject unsupported-host installation claims
- no residual historical plugin ranking table or manual-codex policy framing remains in the rewritten files

## Non-Goals

- editing plugin manifests or runtime logic in this task
- expanding host support beyond `codex` and `claude-code`
- rewriting all install docs again

## Inferred Assumptions

- the confusion now comes more from historical narrative debt than from missing detail
- a shorter, policy-style document is better than a compatibility archaeology note
- community readers care more about truthful current-state boundaries than about previous internal migration history

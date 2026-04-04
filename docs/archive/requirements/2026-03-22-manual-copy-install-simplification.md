# 2026-03-22 Manual Copy Install Simplification Requirement

- Topic: simplify the public manual-copy-install guide so it clearly tells readers what to copy without command-heavy instructions.
- Mode: benchmark_autonomous
- Goal: make the manual copy install page easier to scan by replacing command examples with a short file-and-directory checklist.

## Deliverable

A documentation update that:

1. rewrites `docs/install/manual-copy-install.md` into a concise checklist-style guide
2. removes shell command examples from that guide
3. clearly states which directories/files to copy
4. clearly states what the user still needs to configure locally afterward
5. keeps the hook freeze and supported-host boundaries intact
6. keeps the English page aligned with the simplified structure

## Constraints

- Keep the current support boundary: `codex` and `claude-code`
- Keep hook freeze messaging intact
- Do not reintroduce install commands into the manual copy page
- Keep the page substantially shorter and easier to scan than the previous version

## Acceptance Criteria

- the Chinese page focuses on “copy what” rather than “run what command”
- the guide explicitly lists `skills/`, `commands/`, `config/upstream-lock.json`, `config/skills-lock.json`, and `skills/vibe/`
- the guide clearly explains that online provider values are still local user configuration
- the guide clearly states that hooks are not installed
- the English page follows the same structure and meaning

## Non-Goals

- changing install scripts or runtime logic
- rewriting all install docs again
- expanding support to other hosts

## Inferred Assumptions

- the current manual guide is accurate but still too procedural for public-facing reading
- users mainly want to know what content to copy, not how to write shell commands themselves
- keeping the English page aligned is cheaper than letting the two docs drift again

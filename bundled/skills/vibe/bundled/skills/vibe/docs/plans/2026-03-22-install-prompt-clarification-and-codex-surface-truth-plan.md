# Plan: install prompt clarification and Codex surface truth

- Date: 2026-03-22
- Grade: M

## Work items

1. Update prompt-based install docs in Chinese and English.
2. Update recommended path docs to explain local credential placement and Claude non-destructive merge guidance.
3. Update Codex install/truth docs to remove unsupported hook/plugin recommendations.
4. Tighten any Codex manifest or install metadata that still advertises unsupported plugin surfaces.
5. Run targeted grep and diff checks to verify the old claims are gone from install-facing documents.

## Verification

- grep install-facing docs for `hookify`, `everything-claude-code`, `claude-code-settings`, `ralph-loop`, `apikey`, and confirm wording is truthful.
- run `git diff --check`.

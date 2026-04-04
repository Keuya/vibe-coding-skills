# 2026-03-31 PR91 Rabbit Fix Batch Requirement

- Topic: fix the validated CodeRabbit findings on PR `#91` without overreacting to false positives.
- Mode: interactive_governed
- Goal: reduce merge risk by patching the real correctness, ownership, portability, and proof-artifact hygiene problems identified during review.

## Deliverable

A bounded fix batch that:

1. fixes uninstall ownership and hook-removal safety for Claude
2. fixes the real Linux/Windows helper regressions that can create false pass/fail behavior
3. sanitizes committed proof artifacts that currently leak host-specific absolute paths
4. updates stale wording that now contradicts the Linux frozen-proof state
5. leaves false-positive Rabbit comments unimplemented unless independently justified

## Constraints

- Keep Claude Linux promotion bounded to `supported-with-constraints`
- Do not broaden Windows/macOS support claims
- Do not fix bot comments that are not technically justified
- Preserve existing governed proof receipts where possible, only sanitizing unstable host-specific values

## Acceptance Criteria

- `.vibeskills` removal is gated by ownership evidence
- Claude `PreToolUse` uninstall matching no longer removes entries by description alone when a managed command exists
- `check.sh` no longer hardcodes `python3` for the Claude hook probe
- readiness wrapper scripts fail fast on probe failure instead of looping forever
- proof bundle artifacts no longer commit local absolute paths or Codex-only host wording for the Claude run
- targeted tests and gates pass after the patch set

## Non-Goals

- Implementing every minor style suggestion from CodeRabbit
- Reworking the whole Windows VM harness beyond the reviewed correctness fixes

## Inferred Assumptions

- The current PR branch is the correct place to make the fixes
- High-priority review items should be fixed before replying in-thread

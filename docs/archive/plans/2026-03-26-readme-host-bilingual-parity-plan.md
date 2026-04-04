# README Host Bilingual Parity Plan

## Scope

Apply a narrow documentation correction for the top README host banner in English and Chinese.

## Steps

1. Locate the shared host-banner wording in [`README.md`](../../../README.md) and [`README.zh.md`](../../../README.zh.md).
2. Add `OpenClaw` in the same position in both languages.
3. Verify the resulting wording and search for the updated host banner.
4. Commit and push the correction to the active PR branch.

## Verification

- `rg -n "OpenClaw" README.md README.zh.md`
- `git diff --check`
- `git diff -- README.md README.zh.md docs/requirements/2026-03-26-readme-host-bilingual-parity.md docs/plans/2026-03-26-readme-host-bilingual-parity-plan.md`

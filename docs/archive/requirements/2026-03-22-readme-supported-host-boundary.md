# 2026-03-22 README Supported Host Boundary Requirement

- Topic: add an explicit supported-host boundary to the public README install entry.
- Mode: interactive_governed
- Internal grade: M
- Goal: make readers see immediately that the current public install surface supports only `Claude Code` and `Codex`.

## Deliverable

A README update that:

1. adds a clear note near the install guide entry in `README.md`
2. mirrors the same note in `README.en.md`
3. states that the current public support surface is only `Claude Code` and `Codex`
4. does not reopen unsupported-host claims or hook-install claims

## Constraints

- Keep wording concise and public-facing
- Place the boundary close to the install section, not buried deep in the document
- Keep Chinese and English meaning aligned
- Do not overstate support beyond the current documented surface

## Acceptance Criteria

- a reader scanning the install section can immediately see the supported hosts
- the Chinese README says the current version only supports `Claude Code` and `Codex`
- the English README says the same thing
- no other install behavior is changed by this task

## Non-Goals

- changing install scripts
- changing host policy documents again
- re-expanding support to other agents

## Inferred Assumptions

- the install docs already reflect the narrowed support surface
- the root README still needs a direct boundary reminder for first-time readers

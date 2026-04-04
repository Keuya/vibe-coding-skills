# VCO Linux Health Audit Requirement

- Date: 2026-03-15
- Run ID: `2026-03-15-linux-health-audit`
- Mode: `benchmark_autonomous`
- Topic: Linux compatibility and functional health audit for VCO `v2.3.43`

## Goal

Determine whether VCO runs correctly on Linux in its real local install, identify any Linux compatibility issues that still exist, and assess whether the current upstream update causes functional regression or degradation.

## Deliverable

A repo-grounded audit with:

- real command evidence from Linux
- actual installed-root verification against `/home/lqf/.codex`
- pure Linux degraded-lane verification without `pwsh`
- static compatibility findings for Linux-sensitive pathing and shell assumptions
- a clear judgment of `healthy`, `degraded but acceptable`, or `broken`

## Constraints

- Use the current repo checkout at `/home/lqf/table/table2/vco-skills-codex`
- Use the real installed runtime at `/home/lqf/.codex`
- Prefer command evidence over inference
- Do not claim success without fresh verification evidence
- Do not change product code during this audit unless explicitly asked

## Acceptance Criteria

- The audit confirms the current repo commit and installed version under Linux.
- The audit runs the real installer/check surfaces on Linux and records results.
- The audit tests a pure Linux lane with `pwsh` removed from `PATH` and records whether degraded behavior is honest and acceptable.
- The audit runs representative router and governance checks relevant to the current release.
- The audit performs a static scan for Linux-sensitive path and shell issues.
- The audit ends with an explicit issue list and overall health judgment.

## Non-goals

- No code fixes in this run
- No Windows validation in this run
- No release or packaging changes in this run

## Inferred Assumptions

- `pwsh` is available in the actual Linux environment and is part of the supported best-effort lane.
- The user wants a comprehensive diagnosis, not a minimal smoke test.
- Existing degraded behavior for missing `pwsh` is allowed if it is explicit, truthful, and does not mask failures.

# vibe-runtime Protocol

Governed runtime contract for `vibe`.

This protocol defines the user-facing runtime path that all host syntaxes share.
It does not replace the canonical router.
It defines what must happen after `vibe` is selected.

## Runtime Identity

`vibe` is one skill contract across all hosts:

- `/vibe`
- `$vibe`
- agent-invoked `vibe`

These are syntax variants for the same governed runtime, not separate entrypoints.

## Contract Priorities

1. Canonical router authority stays intact.
2. User-facing runtime path stays fixed.
3. `M`, `L`, `XL` remain internal execution grades only.
4. Requirement freezing happens before plan execution.
5. Cleanup is mandatory before a phase is considered complete.
6. Silent fallback and silent degradation are forbidden.
7. Fallback success is non-authoritative unless a requirement explicitly approves otherwise.

## Official Runtime Modes

### `interactive_governed`

Default mode.

- ask direct high-value questions when needed
- freeze a requirement document with user-visible assumptions
- allow approval boundaries before execution

### `benchmark_autonomous`

Closed-loop mode.

- do not keep asking the user after a full requirement is given
- infer missing assumptions and record them explicitly
- still generate requirement, plan, verification, and cleanup artifacts

## Fixed 6-Stage State Machine

### Stage 1: `skeleton_check`

Purpose:

- verify repo skeleton and governed runtime prerequisites
- discover active requirement or plan artifacts
- detect conflicting dirty-state conditions

Required outputs:

- skeleton receipt
- repo-state summary

### Stage 2: `deep_interview`

Purpose:

- transform raw task text into a structured intent contract

Required fields:

- goal
- deliverable
- constraints
- acceptance criteria
- non-goals
- autonomy mode
- open questions
- inference notes

### Stage 3: `requirement_doc`

Purpose:

- freeze the single requirement source for the run

Rules:

- write under `docs/requirements/`
- execution and review trace back to this document
- benchmark mode must record inferred assumptions

### Stage 4: `xl_plan`

Purpose:

- generate the execution plan under `docs/plans/`

Required contents:

- internal execution grade
- wave or batch structure
- ownership map
- verification commands
- rollback strategy
- cleanup expectations

### Stage 5: `plan_execute`

Purpose:

- advance work strictly from the frozen plan

Rules:

- internal grade controls topology
- XL prefers Codex-native orchestration
- spawned subagent prompts must end with `$vibe`
- milestone evidence must be written before phase completion

### Stage 6: `phase_cleanup`

Purpose:

- close the phase in a clean, auditable way

Minimum actions:

- temp artifact cleanup
- repo hygiene pass
- node audit or cleanup
- cleanup receipt write

## Protocol Delegation

The runtime may delegate stage internals to existing protocols:

- `think.md` for analysis, planning, and research
- `do.md` for execution, debugging, and verification
- `review.md` for quality review
- `team.md` for XL orchestration
- `retro.md` for retrospective learning after work closure

Delegation must not bypass the fixed stage order.

## Router Integration Rules

- route authority remains in `scripts/router/resolve-pack-route.ps1`
- `confirm_required` stays on the existing white-box confirm surface
- unattended routing is interpreted as a governed runtime mode choice, not as a second runtime
- provider-backed intelligence remains advice-only
- fallback or degraded paths must emit an explicit hazard alert rather than a silent warning
- fallback or degraded paths must downgrade runtime truth to `non_authoritative`

## Artifact Contract

Expected runtime artifacts:

- `outputs/runtime/vibe-sessions/<run-id>/skeleton-receipt.json`
- `outputs/runtime/vibe-sessions/<run-id>/intent-contract.json`
- requirement document
- execution plan
- phase receipts
- cleanup receipt

## Success Criteria

The governed runtime is considered healthy only when:

- the 6-stage sequence is preserved
- requirement and plan artifacts exist
- execution traces back to the plan
- cleanup is recorded
- no success claim is made without verification evidence
- no fallback or degraded path is presented as equivalent success
- any fallback or degraded path emits a standalone hazard alert

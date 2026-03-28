# L / XL Native Execution Closure

## Summary
Close the gap between the documented `vibe` execution model and the current runtime implementation. Land a real `L` native serial execution path and a real `XL` native selective-parallel execution path so that `vibe` no longer only freezes governance artifacts and specialist accounting, but can actually orchestrate child lanes and native specialist work under root-controlled runtime authority.

## Goal
Implement a coherent governed execution model where:

- `L` runs as a true native serial workflow inside `vibe`
- `XL` runs as a true native multi-lane workflow inside `vibe`
- parallelism is selective and step-scoped rather than global and always-on
- specialist skills can be executed in their native mode as bounded work units
- root/child governance remains single-owner, auditable, and stable

## Deliverable
A repository change set and documentation bundle that adds:

- a runtime execution topology that distinguishes `M`, `L`, and `XL` in real execution behavior, not only in metadata
- a native `L` serial orchestrator with staged subagent execution and two-stage review
- a native `XL` selective-parallel orchestrator with root-controlled wave and step scheduling
- executable specialist-dispatch units that preserve native specialist workflow contracts
- tests and proof artifacts demonstrating authority preservation, stable execution, and correct bounded parallelism

## Constraints
- Do not create a second router, second requirement surface, second execution-plan surface, or second runtime authority.
- Keep `vibe` as the runtime-selected skill for explicit governed entry.
- Do not turn `XL` into always-parallel execution; only independent units inside a step may run concurrently.
- Do not flatten specialist skills into generic labels; preserve native workflow, inputs, outputs, and validation style.
- Keep root/child hierarchy rules intact: only root may freeze canonical requirement and plan truth or issue final completion claims.
- Prefer additive execution-topology changes over broad router rewrites.

## Acceptance Criteria
- `L` execution is no longer metadata-only:
  - runtime uses a native serial orchestrator
  - design/plan approval remains explicit
  - subagent units run in ordered stages
  - two-stage review is represented in execution artifacts
- `XL` execution is no longer metadata-only:
  - runtime can execute child-governed units as real delegated lanes
  - wave order stays sequential by dependency
  - independent units inside a wave or step can run in bounded parallel
  - scheduler policy exposes bounded concurrency rather than fixed `max_parallel_units=1`
- specialist-dispatch execution is no longer accounting-only:
  - approved specialist dispatch can become executable bounded units
  - child-local specialist suggestions remain advisory until root approval
  - execution evidence records native specialist runs and recovery into root manifest
- proof surfaces show:
  - one root completion authority
  - no duplicate canonical requirement or plan surfaces
  - child lanes cannot widen global scope silently
  - degraded execution remains explicit and non-authoritative when the native path is unavailable

## Primary Objective
Make the documented `L` and `XL` governed execution semantics true in the runtime.

## Proxy Signal
The runtime no longer only writes plans and manifests about serial or parallel work; it actually schedules serial `L` child units, bounded `XL` parallel units, and executable native specialist dispatch under `vibe` governance.

## Scope
In scope:
- runtime scheduler and execution-topology policy
- `L` serial orchestrator
- `XL` selective-parallel orchestrator
- root/child delegated execution wiring
- native specialist execution contracts
- execution receipts, manifests, and proof updates
- runtime-neutral tests and governed verification gates

Out of scope:
- redesigning canonical routing logic
- host auto-interception of every non-`vibe` message
- converting all specialist skills in the repository to new metadata formats
- replacing governed runtime with a separate workflow engine

## Completion
The work is complete when explicit `vibe` runs can deliver real `L` serial native execution and real `XL` selective-parallel native execution, with specialist skills executed as bounded native helpers and with root-owned governance truth preserved end to end.

## Evidence
- runtime policy and execution code changes
- updated protocol and stable docs
- passing runtime-neutral tests covering `L`, `XL`, hierarchy, and specialist execution
- governed proof artifacts showing real delegated execution rather than accounting-only shadows

## Non-Goals
- Do not make `XL` mean unconditional full parallelism.
- Do not let child lanes become recursive top-level governors.
- Do not let specialist skills take over runtime ownership from `vibe`.
- Do not hide degraded or fallback paths behind success wording.

## Autonomy Mode
interactive_governed

## Assumptions
- Existing root/child hierarchy metadata is sufficient to seed a real delegated execution engine.
- Existing specialist recommendation and dispatch fields can be extended into executable units without redesigning router scoring.
- The current benchmark execution policy can evolve into a real governed execution-topology policy rather than remaining a repo-safe sequential proof runner only.
- Proof quality can be preserved while moving from metadata-only semantics to actual orchestration.

## Evidence Inputs
- Source task: design a reasonable solution for the missing `L` native serial execution and `XL` selective-parallel native execution behavior
- Current runtime gap:
  - documented `L`/`XL` behavior is stronger than actual execution
  - scheduler remains sequential
  - specialist dispatch is surfaced and counted but not yet executed as native bounded units

# Vibe Governor + Native Specialist Skills

## Summary
Keep `vibe` as the sole governed runtime authority while enabling it to call specialist skills as bounded native assistants through an explicit host adapter bridge. Router output must remain a single canonical routing truth, but explicit `vibe` runs should freeze specialist recommendations that can be consumed by planning and execution without handing control to a second runtime or faking native execution with receipt-only artifacts.

## Goal
Implement a minimal-change governed model where:

- `vibe` remains the only runtime owner for requirement freeze, execution planning, execution receipts, verification, and cleanup.
- specialist skills can be recommended, planned, dispatched, and verified as bounded native helpers.
- specialist usage preserves each skill's native workflow expectations rather than flattening the skill into a label.
- approved specialist dispatch can cross a host adapter bridge into real native execution when the active host supports it.
- unsupported or disabled native specialist paths degrade explicitly to `degraded_non_authoritative` rather than claiming equivalent success.

## Deliverable
A repository change set that adds:

- a frozen runtime packet contract for `specialist_recommendations`
- a frozen executable contract for `approved_dispatch`
- requirement and plan surfacing for native specialist dispatch
- a host adapter execution bridge with an initial `codex` implementation path
- execution-manifest support for specialist units, degraded specialist units, and their recovery into `vibe`
- protocol and operator documentation for the governor-plus-specialists model
- regression tests and proof artifacts demonstrating authority preservation, stability, usability, and intelligent specialist selection

## Constraints
- Do not change `runtime_selected_skill` away from `vibe` during explicit `vibe` runtime entry.
- Do not create a second router, second requirement surface, second execution-plan surface, or second runtime authority.
- Reuse existing router outputs and runtime artifacts as much as possible; prefer additive contract extensions over structural rewrites.
- Preserve current host adapter boundaries; this task is a bounded runtime execution bridge project, not a host-entry auto-intercept project.
- Specialist execution must remain bounded and must feed back into `vibe` verification and cleanup surfaces.
- Specialist skills must retain native usage expectations, input contracts, workflow semantics, and validation style when dispatched.
- Child lanes may execute only root-approved specialist dispatch; they may not self-approve new global specialist usage.

## Acceptance Criteria
- Runtime input packet includes machine-readable `specialist_recommendations` for explicit `vibe` runs without changing `authority_flags.explicit_runtime_skill`.
- Runtime input packet includes machine-readable executable specialist dispatch contracts that keep `vibe` as runtime owner.
- Requirement documents surface specialist recommendations and native-usage expectations as frozen inputs.
- Execution plans include an explicit `Specialist Skill Dispatch Plan` section describing bounded specialist use.
- Execution manifests record specialist unit counts, degraded specialist unit counts, execution drivers, and recovery status while keeping `vibe` as runtime owner.
- Protocol docs define the `vibe governor + native specialist skills` model and forbid specialist takeover of runtime truth.
- Tests prove:
  - `vibe` authority is preserved
  - specialist recommendations are frozen and surfaced
  - plan/execute artifacts include specialist dispatch data
  - root-approved child specialist dispatch can execute through the host adapter bridge
  - degraded specialist paths remain explicit and non-authoritative when appropriate
  - receipt-only specialist stubs are no longer presented as native execution

> Fill the anti-drift fields once here. Downstream governed plan and completion surfaces should reuse them rather than restate them.

## Primary Objective
Enable `vibe` to orchestrate specialist skills natively without losing governed runtime authority.

## Proxy Signal
The system freezes specialist recommendations, plans them explicitly, executes them as bounded units, and records them in execution evidence.

## Scope
In scope:
- runtime packet extension
- requirement/plan surfacing
- execution manifest specialist accounting
- host adapter execution bridge for specialist units
- `codex exec` as the first supported runtime-native adapter lane
- protocol and proof documentation
- regression tests and cleanup receipts

Out of scope:
- host auto-interception of every incoming message
- automatic replacement of `vibe` with router-selected specialist skills
- global redesign of the router scoring system
- skill-by-skill metadata rewrites across the entire repository
- blanket host-native parity for every supported install host in the first slice

## Completion
The work is complete when explicit `vibe` runs can preserve runtime authority while still planning and executing native specialist assistance with traceable evidence and passing regression coverage.

## Evidence
- code changes in runtime/config/protocol/test surfaces
- new or updated governed requirement/plan docs
- passing targeted tests
- cleanup receipts and node audit output

## Non-Goals
- Do not make router-selected specialist skills authoritative runtime owners.
- Do not silently downgrade specialist usage into generic text-only hints.
- Do not let any specialist skill create or own a separate execution plan.

## Autonomy Mode
interactive_governed

## Assumptions
- Existing router ranking already provides enough signal to derive specialist candidates without redesigning pack scoring.
- The current runtime packet shadow model can be extended rather than replaced.
- A bounded host adapter bridge can be added without creating a second runtime authority.
- `codex exec` can serve as the first real specialist-native execution lane while other hosts degrade explicitly until their adapters exist.

## Evidence Inputs
- Source task: implement `vibe` governor + native specialist skills with minimal framework change

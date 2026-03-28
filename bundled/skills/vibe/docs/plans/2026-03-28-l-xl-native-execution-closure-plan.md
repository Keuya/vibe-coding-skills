# L / XL Native Execution Closure Plan

## Execution Summary
Align runtime truth with public and protocol truth. The current repository already has governance packets, hierarchy semantics, specialist recommendation contracts, and proof accounting. What is still missing is the actual orchestrator. This plan lands that orchestrator in the smallest coherent way: first `L` native serial execution, then `XL` selective-parallel execution, then executable native specialist dispatch, all under the existing single-root `vibe` authority model.

## Frozen Inputs
- Requirement doc: /home/lqf/table/table5/workspace/release-v2.3.50-main/docs/requirements/2026-03-28-l-xl-native-execution-closure.md
- Current mismatch:
  - protocol and README promise stronger `L` / `XL` execution semantics than runtime currently performs
  - scheduler policy is still sequential with `max_parallel_units=1`
  - plan execution currently runs proof units directly rather than child-lane orchestration
  - specialist dispatch is mostly surfaced as plan-shadow accounting
- Authority invariants that must remain unchanged:
  - canonical router owns route selection
  - `vibe` owns runtime authority
  - root owns canonical requirement and plan truth
  - child lanes stay subordinate

## Internal Grade Decision
- Grade: XL
- The work changes runtime topology, policy, hierarchy execution, specialist execution, proofs, and verification.
- Parallel implementation is justified by disjoint write scopes, but the resulting runtime must use selective bounded parallelism, not blanket concurrency.

## Design Overview

### Design Principle 1: Separate Governance From Scheduling
- Governance already exists and should stay stable.
- What needs to be added is a scheduler/orchestrator layer under stage 5 `plan_execute`.
- The router still decides the route.
- `vibe` still freezes requirement and plan truth.
- The new execution layer only decides how frozen units are executed.

### Design Principle 2: One Execution Topology Policy, Three Runtime Grades
- `M`: single-lane execution
- `L`: serial child-lane execution with review checkpoints
- `XL`: wave-sequential, step-selective parallel child-lane execution
- Remove the current implicit assumption that all governed execution can use one sequential benchmark profile.

### Design Principle 3: Step-Scoped Parallelism Only
- A wave may contain multiple steps.
- Steps run sequentially by dependency.
- A step may contain multiple units.
- Only units marked `parallelizable=true` and with disjoint write scopes may execute concurrently.
- This directly answers the current gap: parallelism should happen when useful inside the `vibe` serial workflow, not as an always-on mode.

### Design Principle 4: Specialist Skills Become Executable Bounded Units
- `approved_dispatch` should be convertible into real execution units.
- `local_specialist_suggestions` remain advisory until root approval.
- A specialist unit carries:
  - native skill id
  - bounded goal
  - required inputs
  - expected outputs
  - verification expectation
  - write-scope boundary
- Specialist execution results must feed back into the root execution manifest and verification bundle.

## Target Runtime Architecture

### A. Execution Topology Policy
Replace the current repo-safe benchmark-only scheduler interpretation with a topology policy that supports:

- `wave_execution`: sequential
- `step_execution`: sequential
- `unit_execution`: sequential or bounded_parallel
- `max_parallel_units`: configurable and greater than 1 only for `XL`
- `delegation_mode`: `none`, `serial_child_lanes`, `selective_parallel_child_lanes`
- `specialist_execution_mode`: `metadata_only`, `native_bounded_units`

### B. Plan Artifact Evolution
Extend the frozen plan to express executable topology:

- wave
- step
- unit
- owner
- write_scope
- parallelizable
- requires_root_approval
- specialist_skill_id when applicable
- review_stage

This should remain one canonical plan surface, not a second planner.

### C. L Native Serial Orchestrator
`L` should execute as:

1. root freezes requirement and plan
2. root emits ordered child units
3. each child unit runs as a real child-governed lane
4. lead performs stage review after each child unit or small batch
5. final two-stage review is recorded before completion

This makes `L` truly “serial native execution”, not just a line in docs.

### D. XL Selective-Parallel Orchestrator
`XL` should execute as:

1. root freezes requirement and plan
2. root walks waves sequentially
3. inside each wave, root walks steps sequentially
4. for a step marked parallelizable, root dispatches independent child lanes concurrently
5. root waits, aggregates evidence, resolves escalations, then advances to the next step

This makes parallelism local, bounded, and intelligible.

### E. Root/Child Specialist Coordination
- Root-approved specialists may execute directly inside child lanes if already frozen in the plan.
- Child lanes may suggest additional specialists.
- New specialists discovered by child lanes produce escalation artifacts, not silent activation.
- Root may accept and append them to the active dispatch surface only through explicit governed update logic.

## Wave Plan

### Wave 1: Freeze Execution-Topology Contract
- Create a dedicated execution-topology policy schema and config surface.
- Define the runtime distinction between wave, step, and unit.
- Define `parallelizable`, `write_scope`, and `review_stage` fields.
- Preserve current single-root authority semantics.

### Wave 2: Refactor Plan Generation For Executable Topology
- Update `Write-XlPlan.ps1` so the plan can express executable step/unit structure instead of only narrative bullets.
- Keep the current human-readable plan, but add machine-readable companion data for stage 5.
- Ensure specialist dispatch is represented as executable bounded units when approved.

### Wave 3: Land L Native Serial Execution
- Introduce an `L` execution path in `Invoke-PlanExecute.ps1`.
- Convert the documented `subagent execution → two-stage review` sequence into actual runtime behavior.
- Child units should be real delegated runs with inherited frozen context and subordinate receipts.
- Add explicit review receipts so `L` is not just “serial execution”, but “serial governed execution”.

### Wave 4: Land XL Selective-Parallel Execution
- Introduce a scheduler that can execute a step in bounded parallel only when:
  - units are marked parallelizable
  - write scopes do not overlap
  - global specialist approval constraints are satisfied
- Keep wave order sequential.
- Keep root aggregation and checkpoint review mandatory between steps.

### Wave 5: Convert Specialist Dispatch From Metadata To Execution
- Add an executable specialist-unit adapter shape.
- For approved dispatch:
  - spawn bounded child unit
  - preserve native specialist contract
  - collect specialist-specific outputs and verification notes
- For local suggestions:
  - emit escalation artifact
  - do not execute until root approval

### Wave 6: Proof And Verification Upgrade
- Extend tests to prove actual delegated execution behavior:
  - `L` child units execute in order
  - `XL` parallel step executes more than one unit when allowed
  - non-parallel steps remain sequential
  - overlapping write scopes block parallel execution
  - specialist units execute only when approved
- Upgrade manifests and proof bundles to distinguish:
  - metadata-only dispatch
  - executed specialist dispatch
  - serial child-lane execution
  - bounded parallel child-lane execution

### Wave 7: Cleanup And Documentation Closure
- Update `SKILL.md`, `protocols/runtime.md`, `protocols/do.md`, `protocols/team.md`, and README wording so public truth matches runtime truth.
- Remove any wording that overstates behavior before the new orchestrator ships.
- Re-run node audit and clear temp artifacts produced by the implementation wave.

## Ownership Boundaries
- Execution policy and topology config:
  - `config/benchmark-execution-policy.json`
  - new or adjacent topology policy files
- Runtime packet and dispatch metadata:
  - `scripts/runtime/Freeze-RuntimeInputPacket.ps1`
  - `config/runtime-input-packet-policy.json`
- Plan generation:
  - `scripts/runtime/Write-XlPlan.ps1`
- Execution engine:
  - `scripts/runtime/Invoke-PlanExecute.ps1`
  - `scripts/runtime/invoke-vibe-runtime.ps1`
- Hierarchy and docs:
  - `SKILL.md`
  - `protocols/runtime.md`
  - `protocols/do.md`
  - `protocols/team.md`
  - `README.md`
  - `README.zh.md`
- Verification:
  - `tests/runtime_neutral/*`
  - governed `scripts/verify/*` gates

## Verification Commands
- `git diff --check`
- `python3 -m pytest tests/runtime_neutral/test_governed_runtime_bridge.py tests/runtime_neutral/test_root_child_hierarchy_bridge.py -v`
- `python3 -m pytest tests/runtime_neutral -k "specialist or hierarchy or runtime or plan_execute" -v`
- `rg -n "spawn_agent|send_input|wait_agent|close_agent|parallelizable|write_scope|review_stage" scripts/runtime protocols docs README*`
- `pwsh -NoLogo -NoProfile -File scripts/verify/vibe-governed-runtime-contract-gate.ps1`
- `pwsh -NoLogo -NoProfile -File scripts/verify/vibe-child-specialist-escalation-gate.ps1`

## Rollback Plan
- If real delegated execution threatens root-owned authority, revert to the last state where hierarchy metadata is correct and execution remains explicit.
- If selective parallelism causes scope overlap or artifact races, keep the topology contract but temporarily force affected steps back to serial mode.
- If native specialist execution proves unstable, degrade explicitly to metadata-only specialist dispatch rather than silently pretending execution occurred.
- Never revert unrelated user changes.

## Stability Proof Strategy
- Authority:
  - only root may freeze canonical requirement and plan truth
  - only root may issue final completion claims
- Scheduling:
  - `L` remains ordered
  - `XL` runs only approved bounded parallel steps
  - overlapping scopes are blocked from concurrent execution
- Specialist safety:
  - approved specialists may execute
  - unapproved specialists remain escalation-only
- Observability:
  - manifests prove what actually executed, not only what was recommended

## Usability Proof Strategy
- Operators can explain the runtime in one sentence:
  - `L` is serial governed execution; `XL` is wave-sequential with step-level bounded parallelism.
- Plans show where concurrency happens and where it does not.
- Specialists remain understandable as bounded helpers, not hidden runtime replacements.

## Intelligence Proof Strategy
- The system should choose concurrency only where the dependency graph allows it.
- The system should preserve specialist expertise without losing `vibe` sovereignty.
- Complex composite tasks can be decomposed into sequential macro-steps with local parallel micro-steps.

## Phase Cleanup Contract
- Remove scratch artifacts, temporary logs, and simulation outputs created during the implementation wave.
- Audit managed node processes and clear stale residue after each implementation batch.
- Preserve only intended source, docs, tests, and proof artifacts.
- Emit cleanup receipts before any completion claim.

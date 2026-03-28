# Vibe Governor + Native Specialist Skills

## Execution Summary
Implement the smallest coherent extension that lets explicit `vibe` runs freeze, plan, and execute native specialist assistance without surrendering runtime authority. Reuse existing router outputs, keep `runtime_selected_skill=vibe`, add a real host adapter bridge for specialist units, and make unsupported paths degrade explicitly instead of pretending receipt-only execution is native.

## Frozen Inputs
- Requirement doc: /home/lqf/table/table5/workspace/verify-main-pr60/docs/requirements/2026-03-28-vibe-governor-native-specialist-skills.md
- Source task: `vibe` governor + native specialist skills
- Runtime authority invariant: explicit `vibe` remains the only runtime owner

## Internal Grade Decision
- Grade: XL
- User-facing runtime remains fixed; the grade is internal only.
- Parallel work is warranted because code, tests, and governance docs can advance on disjoint write scopes.

## Wave Plan
- Wave 1: freeze executable specialist contract, host adapter policy, and degrade contract
- Wave 2: implement runtime-native specialist execution bridge with `codex exec` as the first adapter lane
- Wave 3: allow child lanes to execute only root-approved specialist dispatch while keeping local suggestions escalation-only
- Wave 4: upgrade manifests, receipts, and docs so live execution and degraded execution are clearly distinct
- Wave 5: add fake-adapter regression tests, targeted runtime verification, and cleanup closure

## Ownership Boundaries
- Runtime packet and artifact contract: `config/runtime-input-packet-policy.json`, `config/native-specialist-execution-policy.json`, `scripts/runtime/Freeze-RuntimeInputPacket.ps1`
- Requirement/plan surfacing: `scripts/runtime/Write-RequirementDoc.ps1`, `scripts/runtime/Write-XlPlan.ps1`
- Execution bridge and accounting: `scripts/runtime/VibeExecution.Common.ps1`, `scripts/runtime/Invoke-DelegatedLaneUnit.ps1`, `scripts/runtime/Invoke-PlanExecute.ps1`
- Protocol/docs authority model: `SKILL.md`, `protocols/runtime.md`, `protocols/team.md`, supporting docs
- Verification: runtime tests and targeted gates
- Subagent prompts must end with `$vibe`.

## Specialist Skill Dispatch Plan
- Dispatch only bounded specialist units; keep `vibe` as the sole runtime owner.
- Preserve native specialist usage by carrying native workflow expectations, required inputs, expected outputs, and verification mode into the dispatch contract.
- Do not auto-promote specialist recommendations into runtime ownership changes.
- Specialist-owned lanes use visible specialist invocation plus injected hidden governance context; they are not receipt-only aliases for `$vibe`.
- The first live bridge is `codex exec`; unsupported hosts or disabled native execution degrade explicitly to `degraded_non_authoritative`.
- Record all specialist units in execution evidence and recover their outputs into the `vibe` manifest.

## Verification Commands
- `git diff --check`
- `python3 -m py_compile scripts/runtime/*.ps1` is not applicable; instead validate PowerShell syntax via targeted gates and JSON schema checks
- `python3 -m pytest tests/runtime_neutral -k "runtime_input_packet or plan_execute or specialist or requirement or plan"`
- targeted `rg` checks for authority invariants such as `explicit_runtime_skill`, `shadow_only`, `specialist_recommendations`
- smoke `codex exec` in a temp directory before claiming the `codex` adapter lane works
- repo cleanliness checks and node audit after each wave

## Rollback Plan
- Revert only the governor-specialist change set if authority invariants or regression tests fail.
- Do not revert unrelated user changes or existing untracked docs.
- If the live host adapter bridge proves unstable, keep the executable contract and degrade explicitly to `degraded_non_authoritative` instead of silently restoring receipt-only fake native execution.

## Phase Cleanup Contract
- Remove temporary logs or scratch files created during each wave.
- Run node audit and clean stale managed node residue when present.
- Leave the repository with only intended source, docs, tests, and proof artifacts.
- Emit a cleanup receipt after verification closure.

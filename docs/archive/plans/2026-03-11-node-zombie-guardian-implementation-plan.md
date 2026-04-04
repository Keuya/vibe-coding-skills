# Node Zombie Guardian Implementation Plan

- Up: [../README.md](../README.md)
- Index: [README.md](README.md)

**Date:** 2026-03-11
**Mode:** XL / unattended / vibe-first
**Goal:** deliver a fully-governed VCO capability that detects and safely cleans up VCO-owned stale Node processes without impacting legitimate external Node workloads.

## 1. Success Criteria

The rollout is complete only if all of the following are true:

1. a dedicated `node-zombie-guardian` skill exists inside the VCO ecosystem
2. Node launches can be registered through a canonical wrapper
3. process liveness is tracked through ledger + heartbeat artifacts
4. audit can distinguish `vco-managed` from `external`
5. cleanup only targets `cleanup_safe` managed stale processes
6. routing metadata can select the skill from zombie-node prompts
7. deterministic verify coverage exists for routing, policy, and cleanup safety
8. bundled and nested mirrors are synchronized from canonical

## 2. Alpha-to-Omega Execution Map

### Alpha: Governance Baseline

- lock canonical write root
- define safety invariants
- define runtime artifact paths

Outputs:

- design doc
- implementation plan

### Beta: Policy Contracts

- add `process-health-policy.json`
- add `process-ledger-policy.json`

Outputs:

- explicit stale thresholds
- cleanup boundary
- artifact contract

### Gamma: Ledger Core

- implement `scripts/common/ProcessLedger.ps1`
- add locking, read/write helpers, JSONL event logging, heartbeat persistence

Outputs:

- canonical ledger library
- reusable audit/cleanup helpers

### Delta: Launch Wrapper

- implement `scripts/common/NodeLaunchWrapper.ps1`
- register VCO-managed Node processes at launch
- spawn heartbeat monitor companion

Outputs:

- wrapper-based ownership registration
- heartbeat lifecycle updates

### Epsilon: Audit Surface

- implement `scripts/governance/Invoke-NodeProcessAudit.ps1`
- classify live and fixture process snapshots

Outputs:

- actionable audit JSON/markdown
- cleanup-safe candidate marking

### Zeta: Cleanup Surface

- implement `scripts/governance/Invoke-NodeZombieCleanup.ps1`
- support report-only, simulate, and explicit apply mode

Outputs:

- bounded termination workflow
- cleanup receipts

### Eta: Skill Surface

- add `bundled/skills/node-zombie-guardian/SKILL.md`
- wire the skill to wrapper, audit, and cleanup scripts

Outputs:

- reusable operator-facing skill entrypoint

### Theta: Router Surface

- extend `pack-manifest.json`
- extend `skill-keyword-index.json`
- extend `skill-routing-rules.json`

Outputs:

- pack-level discovery
- skill-level disambiguation

### Iota: Governance References

- update tool / conflict / fallback references
- optionally mention the new capability in main VCO skill text where relevant

Outputs:

- explainable coexistence rules
- bounded degraded path

### Kappa: Capability and Evidence Layer

- add a governed capability-catalog entry if the capability is promoted beyond routing-only status
- add pilot scenario documentation

Outputs:

- discovery/evidence linkage
- rollout posture record

### Lambda: Deterministic Fixtures

- add process-health fixtures under `scripts/verify/fixtures/process-health/`
- encode healthy and stale scenarios

Outputs:

- deterministic classification cases
- false-positive regression cases

### Mu: Dedicated Gate

- add `scripts/verify/vibe-node-zombie-gate.ps1`
- prove audit, cleanup filtering, and artifact generation

Outputs:

- dedicated safety proof
- regression entrypoint

### Nu: Parity and Metadata Integration

- extend parity gates for new config files
- update verify README
- regenerate `skills-lock.json` if required by skill metadata governance

Outputs:

- mirror-safe packaging
- metadata-safe routing

### Xi: Sync and Mirror Closure

- sync canonical changes into bundled mirrors
- run mirror hygiene and nested parity checks

Outputs:

- full mirror consistency

### Omicron: Functional Verification

- run dedicated node-zombie gate
- run pack routing smoke
- run config parity
- run mirror parity / hygiene
- run skill metadata if touched

Outputs:

- evidence-backed completion decision

### Pi to Omega: Reconcile and Close

- fix any parity/routing/metadata failures
- re-run failed gates
- summarize residual risks

Outputs:

- clean, bounded ship state

## 3. Batch Structure

### Batch 1: Contracts and docs

- design doc
- implementation plan
- policies

### Batch 2: Runtime core

- ledger library
- wrapper
- audit
- cleanup

### Batch 3: Skill and routing

- bundled skill
- pack metadata
- routing rules

### Batch 4: Governance and proofs

- references
- fixtures
- dedicated gate
- verify README

### Batch 5: Packaging and close-out

- parity updates
- skills lock refresh if needed
- bundled sync
- targeted verification

## 4. Safety Gates

Every batch must preserve these invariants:

1. no direct cleanup of `external` or `unknown`
2. no new control plane
3. canonical-first edits only
4. deterministic fixture coverage for stale-vs-healthy classification
5. report-only default for cleanup

## 5. Residual Risk Management

Known residual risks and responses:

- **Process discovery ambiguity through package-manager wrappers**
  Response: wrapper records launcher PID and only promotes cleanup-safe status after positive Node PID discovery.

- **Heartbeat loss because the monitor crashed**
  Response: audit marks the process stale or missing-heartbeat, but cleanup still requires positive ownership and policy approval.

- **External Node services on the same host**
  Response: always audit-only unless explicitly VCO-managed.

- **Mirror drift**
  Response: canonical-only edits followed by bundled sync and parity gates.

## 6. Definition of Done

The work is done only when:

- the dedicated skill exists
- runtime scripts work on fixture-backed verification
- routing metadata resolves the new skill
- cleanup cannot target external processes
- dedicated and shared verify gates pass
- canonical and bundled mirrors match

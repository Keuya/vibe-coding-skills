# Linux Router Host-Neutrality And Route Quality Recovery Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix the four currently dominant platform/router problems in VCO, so Linux without `pwsh` no longer loses core routing capability, common prompts stop over-falling into `confirm_required`, planning prompts route to the correct candidate packs, and remaining Windows/path leakage is reduced to non-authoritative hygiene debt.

**Architecture:** Keep one canonical router contract and one canonical runtime truth. Do not split the project into Linux and Windows forks. Extract a host-neutral routing core from the current PowerShell authority surface, keep PowerShell and shell/Python as thin adapters, then add a second proof layer for route quality so platform compatibility and routing intelligence are promoted together rather than separately.

**Tech Stack:** PowerShell, Python, Bash, existing `scripts/router/*.ps1` modules, `config/*.json` policy files, runtime-neutral tests in `tests/runtime_neutral`, replay fixtures in `tests/replay`, governed verification gates in `scripts/verify`, Markdown proof and status docs.

---

## Executive Summary

This plan addresses four real problems:

1. Linux without `pwsh` is still missing authoritative router execution.
2. Route policy is too conservative for common prompts and overuses `confirm_required`.
3. Planning and migration prompts are ranking into the wrong packs.
4. Path neutrality is incomplete because non-authoritative Windows-flavored paths still leak through docs, templates, references, and examples.

The recovery strategy is:

- freeze truth first
- extract host-neutral core second
- recover Linux routing closure third
- tune route confidence and ranking fourth
- clean remaining path leakage fifth
- promote only after proof passes

The hard rule is unchanged:

- no dual fork
- no false promotion
- no silent regression
- no “docs say supported” without behavior proof

## Why This Plan Exists

Current repo truth is internally inconsistent in a way that affects users:

- Linux with `pwsh` is usable but still constrained.
- Linux without `pwsh` can pass parts of install/check, but still lacks the same router authority as Windows.
- Common prompts are structurally biased toward `confirm_required`.
- Planning prompts can be misranked into research-like candidates instead of architecture/planning/governance candidates.

This means the project is not blocked by one bug. It is blocked by a stacked contract problem:

- platform contract
- shell/host contract
- router authority contract
- route quality contract
- proof contract

This plan rebuilds those contracts in one sequence.

## Non-Negotiable Principles

### Principle 1: One Canonical Core

The project must keep one canonical routing semantics layer.

- No Linux router fork.
- No Windows router fork.
- No separate quality thresholds by platform unless explicitly adapter-scoped and proof-backed.

### Principle 2: Adapters Own Platform Differences

Platform differences may exist only in adapters:

- home/root discovery
- shell invocation
- process spawning
- path quoting
- installed runtime location resolution

Platform differences must not leak into:

- canonical route semantics
- canonical thresholds
- proof criteria
- release truth

### Principle 3: Behavior Before Narrative

No support or promotion statement is allowed unless the installed runtime behavior is proven.

- install/check green is not enough
- static file parity is not enough
- docs alignment is not enough
- route output quality must be tested directly

### Principle 4: Stability, Usability, And Intelligence Must Be Proven Separately

The design is considered complete only when three proof families are green:

- stability proof
- usability proof
- intelligence proof

### Principle 5: No Functional Regression

Windows authoritative behavior must remain green while Linux host-neutrality is added.

- existing PowerShell route execution must remain valid
- benchmark/governed runtime changes must not reduce current proof coverage
- current route JSON contract must remain backward compatible unless versioned

## Current Baseline

### F1: Linux Without `pwsh` Lacks Core Router Authority

Observed state:

- the canonical router is still [scripts/router/resolve-pack-route.ps1](D:/table/new_ai_table/_ext/vco-skills-codex/scripts/router/resolve-pack-route.ps1)
- shell install/check can degrade honestly without `pwsh`
- but there is no equally authoritative non-PowerShell router execution path

Implication:

- Linux without `pwsh` is not full-featured
- this is a real capability boundary, not a cosmetic warning

### F2: Route Policy Is Too Conservative

Observed state:

- `auto_route = 0.7`
- `confirm_required = 0.45`
- `fallback_to_legacy_below = 0.45`
- `legacy_fallback_guard` can re-force `confirm_required`

Implication:

- many safe/common prompts stop at the white-box menu instead of routing decisively

### F3: Planning Prompt Ranking Is Off

Observed state:

- migration/planning/governance prompts can score into research-design-like candidates
- this points to pack scoring / rerank / overlay interaction problems, not platform-specific shell failure

Implication:

- route control plane works, but route quality is not sufficiently task-aligned

### F4: Path Neutrality Is Incomplete

Observed state:

- repo still contains `~/.codex`, `${CODEX_HOME}`, and Windows-flavored examples in non-core surfaces

Implication:

- the core runtime may survive, but developer/operator understanding remains polluted
- platform neutrality cannot be claimed cleanly yet

## Target State

The target state is achieved only when all of the following are true:

1. Linux without `pwsh` can execute the canonical router through a host-neutral adapter with the same route JSON contract.
2. Windows PowerShell route execution remains green and contract-compatible.
3. Common low-risk prompts that should auto-route no longer collapse to `confirm_required` by default.
4. Planning/migration/governance prompts rank into architecture/planning candidates with measurable precision improvements.
5. Path leakage is reduced so canonical and operator-facing surfaces no longer treat Windows or `~/.codex` defaults as architectural truth.
6. The repo carries explicit proof bundles showing stability, usability, and intelligence closure.

## Success Criteria

### Stability Success Criteria

- Linux no-`pwsh` route invocation returns valid route JSON for canonical smoke prompts.
- Windows `powershell.exe` and Linux shell/Python route paths produce the same schema and compatible fields.
- No existing router contract gate regresses.
- Installed runtime route closure works from a temp artifact root and from a real target root.

### Usability Success Criteria

- at least 80% of curated common prompts that are safe and high-pattern no longer fall into `confirm_required`
- route_reason for those prompts is no longer dominated by `legacy_fallback_guard`
- confirm UI remains available for ambiguous or risky prompts

### Intelligence Success Criteria

- planning/migration/governance prompts are top-ranked into the correct candidate family
- rerank improvements are measurable against a frozen gold set
- route quality improvements are stable across Windows and Linux adapters

## Workstream Map

This plan is split into eight tasks.

1. Freeze truth and requirement contract
2. Extract host-neutral path/root contract
3. Build host-neutral router core
4. Add Linux no-`pwsh` authoritative route adapter
5. Tune confidence and guard policy for common prompts
6. Repair planning prompt ranking quality
7. Clean path leakage from non-authoritative surfaces
8. Promote through proof, release truth, and rollback rehearsal

---

### Task 1: Freeze Truth And Requirement Contract

**Files:**
- Create: `docs/requirements/2026-03-15-linux-router-host-neutrality-and-route-quality-recovery.md`
- Create: `docs/status/router-platform-truth-matrix-2026-03-15.md`
- Modify: `docs/plans/README.md`

**Step 1: Write the frozen requirement document**

Record:

- current F1-F4 facts
- target behavior
- hard non-goals
- promotion criteria

**Step 2: Write a truth matrix**

The matrix must separate:

- Windows with PowerShell
- Linux with `pwsh`
- Linux without `pwsh`
- benchmark runtime
- installed runtime

**Step 3: Explicitly classify every lane**

Use only:

- `full-authoritative`
- `supported-with-constraints`
- `degraded-but-supported`
- `not-yet-proven`

**Step 4: Verify no contradiction with platform policy**

Run:

```powershell
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-cross-host-route-parity-gate.ps1
```

Expected:

- current truth is documented honestly

**Step 5: Commit**

```bash
git add docs/requirements/2026-03-15-linux-router-host-neutrality-and-route-quality-recovery.md docs/status/router-platform-truth-matrix-2026-03-15.md docs/plans/README.md
git commit -m "docs: freeze linux router host-neutrality recovery contract"
```

---

### Task 2: Extract The Host-Neutral Path And Root Contract

**Files:**
- Modify: `scripts/common/vibe-governance-helpers.ps1`
- Create: `scripts/common/runtime_neutral/path_contract.py`
- Create: `tests/runtime_neutral/test_path_contract_bridge.py`
- Modify: `config/settings.template.codex.json`
- Modify: `config/skill-metadata-policy.json`

**Step 1: Define canonical root resolution order**

Implement one shared order:

1. explicit `-TargetRoot`
2. `VIBE_TARGET_ROOT`
3. `CODEX_HOME`
4. platform home fallback

**Step 2: Port the same resolution semantics into Python**

The Python contract must produce the same normalized roots as PowerShell for:

- Windows
- Linux
- temp roots
- custom roots

**Step 3: Add bridge tests**

Test:

- same input -> same resolved root
- no direct dependency on `USERPROFILE` as sole source
- no direct dependency on `HOME` as sole source

**Step 4: Repoint templates and metadata**

Convert hard-coded defaults from “architectural truth” into “default example / fallback”.

**Step 5: Run tests**

Run:

```bash
python -m unittest discover -s tests/runtime_neutral -p "test_path_contract_bridge.py" -v
```

Expected:

- green on Windows now
- runnable on Linux later without PowerShell

**Step 6: Commit**

```bash
git add scripts/common/vibe-governance-helpers.ps1 scripts/common/runtime_neutral/path_contract.py tests/runtime_neutral/test_path_contract_bridge.py config/settings.template.codex.json config/skill-metadata-policy.json
git commit -m "feat: freeze host-neutral path contract"
```

---

### Task 3: Build The Host-Neutral Router Core

**Files:**
- Create: `scripts/router/runtime_neutral/router_core.py`
- Create: `scripts/router/runtime_neutral/router_contract.py`
- Create: `scripts/router/invoke-pack-route.py`
- Create: `tests/runtime_neutral/test_router_host_neutral_bridge.py`
- Modify: `scripts/router/resolve-pack-route.ps1`
- Modify: `scripts/router/README.md`

**Step 1: Define the route JSON contract**

Freeze:

- `route_mode`
- `route_reason`
- `confidence`
- `confirm_ui`
- candidate schema
- overlay advice schema

**Step 2: Extract semantic logic into a host-neutral core**

The target is not “rewrite everything in one shot”.

The target is:

- parse configs once
- compute route decision in one semantic core
- expose the same output schema through PowerShell and Python adapters

**Step 3: Keep PowerShell as first adapter**

`resolve-pack-route.ps1` should call into the same logical contract, not diverge into a separate truth.

**Step 4: Add Python adapter**

`invoke-pack-route.py` must provide the same route output for:

- smoke prompts
- planning prompts
- debug prompts

**Step 5: Add bridge tests**

Run a curated prompt set and assert:

- schema parity
- stable field presence
- bounded confidence deltas

**Step 6: Run tests**

Run:

```bash
python -m unittest discover -s tests/runtime_neutral -p "test_router_host_neutral_bridge.py" -v
```

Run:

```powershell
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-router-contract-gate.ps1
```

Expected:

- both green

**Step 7: Commit**

```bash
git add scripts/router/runtime_neutral/router_core.py scripts/router/runtime_neutral/router_contract.py scripts/router/invoke-pack-route.py tests/runtime_neutral/test_router_host_neutral_bridge.py scripts/router/resolve-pack-route.ps1 scripts/router/README.md
git commit -m "feat: add host-neutral router core and bridge"
```

---

### Task 4: Add Linux No-`pwsh` Authoritative Route Adapter

**Files:**
- Modify: `check.sh`
- Modify: `install.sh`
- Modify: `scripts/bootstrap/one-shot-setup.sh`
- Create: `scripts/verify/vibe-linux-router-no-pwsh-gate.ps1`
- Create: `tests/replay/linux_no_pwsh_router_smoke.json`
- Modify: `scripts/verify/README.md`

**Step 1: Wire shell entrypoints to host-neutral router**

When `pwsh` is unavailable:

- do not skip core router smoke
- do not degrade to “file exists only”
- do call the Python route adapter

**Step 2: Add installed-runtime smoke**

Verify an installed runtime under Linux-like conditions can still emit valid route JSON.

**Step 3: Add no-`pwsh` gate**

Gate must prove:

- router invocation works
- output schema is complete
- route contract is not downgraded to placeholder data

**Step 4: Add replay fixture**

Freeze a curated Linux no-`pwsh` route fixture for regression comparison.

**Step 5: Run verification**

Run:

```powershell
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-linux-router-no-pwsh-gate.ps1
```

Expected:

- green

**Step 6: Commit**

```bash
git add check.sh install.sh scripts/bootstrap/one-shot-setup.sh scripts/verify/vibe-linux-router-no-pwsh-gate.ps1 tests/replay/linux_no_pwsh_router_smoke.json scripts/verify/README.md
git commit -m "feat: add linux no-pwsh authoritative route adapter"
```

---

### Task 5: Reduce Over-Conservative `confirm_required` Bias

**Files:**
- Modify: `config/router-thresholds.json`
- Modify: `config/ai-rerank-policy.json`
- Modify: `config/exploration-policy.json`
- Modify: `scripts/router/resolve-pack-route.ps1`
- Create: `tests/replay/common_prompt_route_quality.json`
- Create: `scripts/verify/vibe-common-prompt-route-quality-gate.ps1`

**Step 1: Freeze the common-prompt benchmark set**

Include prompts such as:

- feature implementation
- bug fix
- small refactor
- plan a migration
- architecture review
- governance cleanup

**Step 2: Label expected route classes**

For each prompt, record:

- expected top candidate family
- whether auto-route is acceptable
- whether `confirm_required` is required

**Step 3: Tune guard policy**

Adjust only after replay data exists.

Targets:

- reduce false `legacy_fallback_guard`
- preserve confirmation for ambiguous/high-risk prompts

**Step 4: Add gate**

The gate must fail if:

- common prompts regress back to `legacy_fallback_guard`
- `confirm_required` rate remains above the agreed ceiling

**Step 5: Run verification**

Run:

```powershell
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-common-prompt-route-quality-gate.ps1
```

Expected:

- quality rate improves and stays bounded

**Step 6: Commit**

```bash
git add config/router-thresholds.json config/ai-rerank-policy.json config/exploration-policy.json scripts/router/resolve-pack-route.ps1 tests/replay/common_prompt_route_quality.json scripts/verify/vibe-common-prompt-route-quality-gate.ps1
git commit -m "tune: reduce over-conservative confirm bias for common prompts"
```

---

### Task 6: Repair Planning And Migration Prompt Ranking

**Files:**
- Modify: `config/skill-routing-rules.json`
- Modify: `config/skill-keyword-index.json`
- Modify: `config/system-design-overlay.json`
- Create: `tests/replay/planning_prompt_route_goldens.json`
- Create: `scripts/verify/vibe-planning-route-ranking-gate.ps1`

**Step 1: Freeze planning prompt goldens**

Must include prompts like:

- `design a migration plan for cross-module routing and governance`
- `plan a refactor for installed runtime coherence`
- `design host-neutral routing architecture`

**Step 2: Correct candidate families**

Make architecture/planning/governance packs score above research-design packs where appropriate.

**Step 3: Adjust overlay interactions**

Prevent architecture/planning prompts from being over-absorbed by exploration/research overlays.

**Step 4: Add ranking gate**

The gate must assert:

- correct top-1 family for frozen goldens
- bounded confidence improvement
- no regression in candidate schema

**Step 5: Run verification**

Run:

```powershell
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-planning-route-ranking-gate.ps1
```

Expected:

- planning prompts rank correctly

**Step 6: Commit**

```bash
git add config/skill-routing-rules.json config/skill-keyword-index.json config/system-design-overlay.json tests/replay/planning_prompt_route_goldens.json scripts/verify/vibe-planning-route-ranking-gate.ps1
git commit -m "tune: repair planning and migration prompt route ranking"
```

---

### Task 7: Clean Remaining Windows And Host Path Leakage

**Files:**
- Modify: `config/dependency-map.json`
- Modify: `config/settings.template.codex.json`
- Modify: `config/skill-metadata-policy.json`
- Modify: `protocols/team.md`
- Modify: `scripts/verify/README.md`
- Create: `scripts/verify/vibe-path-neutrality-hygiene-gate.ps1`

**Step 1: Classify leakage**

Separate:

- authoritative blocker
- developer-facing hygiene debt
- example-only path text

**Step 2: Remove or normalize authoritative/path-sensitive surfaces**

Replace “hard truth” wording with:

- explicit default
- explicit example
- explicit environment-substituted form

**Step 3: Add hygiene gate**

Gate should fail if:

- canonical config contains author-machine absolute paths
- platform-specific examples are mislabeled as architecture facts

**Step 4: Run verification**

Run:

```powershell
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-path-neutrality-hygiene-gate.ps1
```

Expected:

- no authoritative path leakage remains

**Step 5: Commit**

```bash
git add config/dependency-map.json config/settings.template.codex.json config/skill-metadata-policy.json protocols/team.md scripts/verify/README.md scripts/verify/vibe-path-neutrality-hygiene-gate.ps1
git commit -m "chore: clean remaining host/path neutrality leakage"
```

---

### Task 8: Promotion, Release Truth, And Rollback Rehearsal

**Files:**
- Modify: `config/platform-support-policy.json`
- Modify: `docs/status/router-platform-truth-matrix-2026-03-15.md`
- Modify: `references/changelog.md`
- Modify: `docs/releases/<next-version>.md`
- Create: `scripts/verify/vibe-router-promotion-bundle-gate.ps1`
- Create: `docs/status/router-promotion-proof-bundle-<date>.md`

**Step 1: Build a promotion bundle**

Bundle must aggregate:

- host-neutral bridge proof
- Linux no-`pwsh` route proof
- common prompt quality proof
- planning ranking proof
- path neutrality hygiene proof

**Step 2: Rehearse rollback**

Prove that if promotion fails:

- docs can revert cleanly
- platform labels can revert cleanly
- no runtime contract is broken

**Step 3: Update release truth only after gates are green**

Do not upgrade platform wording before promotion bundle is green.

**Step 4: Run final bundle**

Run:

```powershell
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-router-promotion-bundle-gate.ps1
```

Expected:

- green

**Step 5: Commit**

```bash
git add config/platform-support-policy.json docs/status/router-platform-truth-matrix-2026-03-15.md references/changelog.md docs/releases scripts/verify/vibe-router-promotion-bundle-gate.ps1 docs/status/router-promotion-proof-bundle-<date>.md
git commit -m "release: promote host-neutral router truth after proof closure"
```

---

## Test Matrix

### Stability Tests

- `python -m unittest discover -s tests/runtime_neutral -p "test_path_contract_bridge.py" -v`
- `python -m unittest discover -s tests/runtime_neutral -p "test_router_host_neutral_bridge.py" -v`
- `powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-router-contract-gate.ps1`
- `powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-cross-host-route-parity-gate.ps1`
- `powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-linux-router-no-pwsh-gate.ps1`

### Usability Tests

- `powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-common-prompt-route-quality-gate.ps1`
- replay diff against `tests/replay/common_prompt_route_quality.json`

### Intelligence Tests

- `powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-planning-route-ranking-gate.ps1`
- replay diff against `tests/replay/planning_prompt_route_goldens.json`

### Hygiene And Truth Tests

- `powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-path-neutrality-hygiene-gate.ps1`
- `powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-version-packaging-gate.ps1`
- `powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-nested-bundled-parity-gate.ps1`

### Final Promotion Tests

- `powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify\vibe-router-promotion-bundle-gate.ps1`

## Proof Standard

This design is not considered landed unless it proves all three dimensions below.

### Stability Proof

Required evidence:

- same route contract on Windows and Linux adapters
- no broken installed-runtime route closure
- no PowerShell-authority regression

### Usability Proof

Required evidence:

- lower `confirm_required` rate on common prompts
- fewer `legacy_fallback_guard` route reasons where ambiguity is low
- confirm UI still present for truly ambiguous prompts

### Intelligence Proof

Required evidence:

- planning/migration/governance goldens route to the right candidate family
- rerank changes improve top-1 accuracy without destabilizing schema or confidence behavior

## Rollout Rules

Rollout order must be:

1. truth freeze
2. path contract
3. router core
4. Linux no-`pwsh` adapter
5. route quality tuning
6. planning ranking repair
7. path hygiene cleanup
8. promotion bundle

No later step may begin if an earlier proof family is still red.

## Stop Rules

Stop immediately if any of the following happens:

- Windows authoritative route path regresses
- route JSON schema changes without explicit versioning
- Linux no-`pwsh` adapter produces placeholder or partial route output
- confirm bias improves by simply lowering safeguards on ambiguous prompts
- planning ranking improves only by overfitting a tiny golden set
- path cleanup changes canonical runtime behavior

## Final Acceptance Criteria

This plan is complete only when:

1. Linux without `pwsh` has a real authoritative route adapter.
2. Windows remains green on the canonical PowerShell lane.
3. Common prompts are materially less over-conservative.
4. Planning/migration prompts route to the correct candidate family with proof.
5. Authoritative path leakage is removed from canonical surfaces.
6. Promotion truth is updated only after the proof bundle is green.

## Execution Notes

- Execute in waves, not ad hoc file touching.
- Keep one canonical core and two adapters.
- Prefer replay fixtures and route goldens over anecdotal prompt checks.
- Every quality improvement must be measurable.
- Every promotion claim must be backed by fresh artifacts.

Plan complete and saved to `docs/plans/2026-03-15-linux-router-host-neutrality-and-route-quality-recovery-plan.md`.

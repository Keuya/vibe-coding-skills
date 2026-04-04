# Universal Install Generalization XL Execution Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement the first concrete waves of universal install generalization: adapter registry, real generic host lane, codex adapter formalization, and claude preview scaffold.

**Architecture:** Preserve official Codex runtime truth while extracting adapter selection into a registry-driven layer. Implement `generic` as runtime-core-only, keep `codex` as strongest adapter-backed lane, and provide `claude-code` scaffold without overclaiming closure.

**Tech Stack:** PowerShell, Bash, JSON manifests, adapter registry, verification gates, docs

---

## Wave 0: Governance Freeze and Parallel Analysis

### Batch 0.1: Freeze execution artifacts
**Files:**
- Create: `docs/requirements/2026-03-21-universal-install-generalization-execution.md`
- Create: `docs/plans/2026-03-21-universal-install-generalization-xl-execution-plan.md`

### Batch 0.2: Parallel agent lanes
**Agent lanes:**
- adapter contract reviewer
- docs consistency reviewer
- verification/gate reviewer

**Rule:** every subagent prompt must end with `$vibe`

## Wave 1: Adapter Registry and Generic Core Lane

### Batch 1.1: Adapter contracts
**Files:**
- Create: `adapters/index.json`
- Create: `adapters/generic/host-profile.json`
- Create: `adapters/generic/settings-map.json`
- Create: `adapters/generic/closure.json`
- Modify: `adapters/codex/host-profile.json`
- Create: `adapters/codex/settings-map.json`
- Create: `adapters/codex/closure.json`
- Modify: `adapters/claude-code/host-profile.json`
- Create: `adapters/claude-code/closure.json`
- Create: `adapters/opencode/host-profile.json`
- Create: `adapters/opencode/closure.json`

### Batch 1.2: Shared adapter resolvers
**Files:**
- Create: `scripts/common/Resolve-VgoAdapter.ps1`
- Create: `scripts/common/resolve_vgo_adapter.py`
- Modify: `scripts/common/vibe-governance-helpers.ps1`

### Batch 1.3: Runtime-core install semantics
**Files:**
- Create: `config/runtime-core-packaging.json`
- Modify: `install.ps1`
- Modify: `install.sh`

## Wave 2: Adapter-Driven Install / Check / Bootstrap

### Batch 2.1: Install orchestration
**Files:**
- Create: `scripts/install/Install-VgoAdapter.ps1`
- Create: `scripts/install/install_vgo_adapter.py`
- Modify: `install.ps1`
- Modify: `install.sh`

### Batch 2.2: Check orchestration
**Files:**
- Modify: `check.ps1`
- Modify: `check.sh`
- Create: `scripts/verify/vgo-adapter-closure-gate.ps1`
- Create: `scripts/verify/vgo-adapter-target-root-guard-gate.ps1`

### Batch 2.3: Bootstrap orchestration
**Files:**
- Modify: `scripts/bootstrap/one-shot-setup.ps1`
- Modify: `scripts/bootstrap/one-shot-setup.sh`

## Wave 3: Claude Preview Scaffold and Docs

### Batch 3.1: Claude scaffold
**Files:**
- Create: `scripts/bootstrap/scaffold-claude-preview.ps1`
- Create: `scripts/bootstrap/scaffold-claude-preview.sh`
- Modify: `config/settings.template.claude.json`
- Modify: `dist/host-claude-code/manifest.json`

### Batch 3.2: Docs and dist truth
**Files:**
- Modify: `docs/deployment.md`
- Modify: `docs/cold-start-install-paths.md`
- Modify: `docs/install/recommended-full-path.md`
- Modify: `docs/universalization/install-matrix.md`
- Modify: `docs/universalization/host-capability-matrix.md`
- Modify: `docs/universalization/distribution-lanes.md`

## Wave 4: Verification and Cleanup

### Batch 4.1: Syntax and isolated host tests
**Commands:**
- shell syntax checks
- PowerShell parse checks
- isolated codex install/check
- isolated generic install/check expectations
- claude preview scaffold verification
- mismatch guard verification

### Batch 4.2: Phase cleanup
**Actions:**
- temp-file cleanup
- zombie node audit/cleanup
- receipt writing
- final evidence summary

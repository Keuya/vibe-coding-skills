# 2026-03-22 Hook Install Freeze Plan

## Goal

Freeze host hook installation for supported hosts until compatibility issues are resolved, and make the docs match the new reality.

## Grade

- Internal grade: M

## Work Batches

### Batch 1: Governance freeze
- Create requirement doc
- Create execution plan

### Batch 2: Installer / bootstrap contraction
- Update `scripts/install/install_vgo_adapter.py`
- Update `scripts/install/Install-VgoAdapter.ps1`
- Update `scripts/bootstrap/scaffold-claude-preview.sh`
- Update `scripts/bootstrap/scaffold-claude-preview.ps1`
- Update `scripts/bootstrap/one-shot-setup.sh`
- Update `scripts/bootstrap/one-shot-setup.ps1`

### Batch 3: Check and adapter contract contraction
- Update `check.sh`
- Update `check.ps1`
- Update `adapters/codex/closure.json`
- Update `adapters/codex/settings-map.json`
- Update `adapters/claude-code/host-profile.json`
- Update `adapters/claude-code/closure.json`
- Update `adapters/claude-code/settings-map.json`

### Batch 4: Install-doc clarification
- Update install-facing docs to say hooks currently have compatibility issues and are not installed
- Keep non-hook supported-host guidance intact

### Batch 5: Verification
- syntax checks for edited shell / PowerShell / Python / JSON files
- grep audit for active supported-host install paths still claiming hook installation
- `git diff --check`

### Batch 6: Phase cleanup
- remove temporary verification artifacts if any
- confirm working tree only contains intentional changes

## Rollback Rules

- If removing hook install breaks unrelated supported-host installation, keep hooks disabled and relax only the unrelated verification branch.
- If any doc still implies hooks are installed, docs must be corrected before completion.

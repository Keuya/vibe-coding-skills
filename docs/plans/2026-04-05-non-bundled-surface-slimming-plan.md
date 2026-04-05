# 2026-04-05 Non-Bundled Surface Slimming Plan

## Internal Grade Decision

`L` planning-grade work. This is a sequencing and guardrail plan for future implementation, not a delete-first wave.

## Protected / Deferred Surfaces

### `apps/`

Status: protected

Reason:

- `apps/vgo-cli/**` is part of the active semantic-owner contract in runtime tests, dist manifests, and version governance.
- Moving or deleting it would be a behavior-bearing architecture change, not a safe slimming step.

Allowed near-term actions:

- enforce cache/bytecode cleanliness
- keep only source and packaging metadata under `apps/vgo-cli/**`
- add or strengthen ignore/cleanliness gates if residue starts being tracked

Deferred actions:

- any move from `apps/vgo-cli/**` into `packages/**`
- any flattening/removal of the `apps/` root

### `commands/`

Status: protected in this execution wave; conditional convergence only after install-target redesign

Reason:

- root `commands/**` is small, but uninstall/install contracts still treat it as a managed compatibility surface
- `config/opencode/commands/**` already exists, but it is installed to different OpenCode target paths while root `commands/**` is installed to `global_workflows`

Required decision before implementation:

Choose exactly one canonical source:

1. `commands/**` canonical, `config/opencode/commands/**` generated
2. `config/opencode/commands/**` canonical, root `commands/**` generated

Only after that choice:

- update runtime config manifests
- update uninstall/install tests
- generate the compatibility projection
- then remove one duplicate surface if verification passes

Current execution decision:

- do not converge `commands/**` in this wave
- treat both command roots as active compatibility consumers until a dedicated install-target redesign is approved

### `agents/`

Status: protected in this execution wave; conditional convergence only after target unification

Reason:

- `agents/templates/**` is small and not the main size problem
- docs/tests still describe it as an official template surface
- `config/opencode/agents/**` is installed to OpenCode `agents` / `agent`, while root `agents/templates/**` is installed to governed codex `agents/templates`

Safe convergence target:

- migrate to `templates/agents/**` or another explicit template root
- keep `agents/templates/**` as generated compatibility until docs/tests/install surfaces are aligned

Current execution decision:

- do not converge `agents/**` in this wave
- keep it as a protected compatibility surface until host-target unification is intentionally designed

## Safe-Now Slimming Wave

These changes should be considered low-risk and no-regression:

1. Add or maintain repo cleanliness protection so `apps/**/__pycache__`, `.pyc`, and similar build residue never become tracked.
2. Keep `apps/` structure unchanged while cleaning non-source residue.
3. Keep `commands/` and `agents/` content unchanged because current evidence shows they serve distinct install targets.
4. Add a focused regression test proving the `apps/` surface stays source-only and free of bytecode residue.

## Future Execution Waves

### Wave 1: `apps/` hygiene only

Goal:

- preserve `apps/vgo-cli/**`
- enforce source-only cleanliness

Expected changes:

- ignore/cache hygiene
- optional repo-cleanliness tests or policy tightening

Verification:

```bash
git diff --check
python3 -m pytest -q \
  tests/integration/test_runtime_script_manifest_roles.py \
  tests/integration/test_version_governance_runtime_roles.py \
  tests/runtime_neutral/test_governed_runtime_bridge.py
```

### Wave 2: `commands/` single-source convergence

Goal:

- eliminate dual maintenance between root `commands/**` and `config/opencode/commands/**`

Implementation outline:

1. freeze canonical source choice
2. convert the non-canonical surface into generated compatibility output
3. update manifests/tests/docs
4. remove duplicate authoring burden

Verification:

```bash
git diff --check
python3 -m pytest -q \
  tests/integration/test_dist_manifest_surface_roles.py \
  tests/runtime_neutral/test_uninstall_vgo_adapter.py \
  tests/runtime_neutral/test_install_profile_differentiation.py
```

Rollback rule:

- restore both command surfaces if install/uninstall or dist-manifest verification changes behavior

### Wave 3: `agents/` template-root convergence

Goal:

- move template authoring to a clearer non-root or unified template location

Implementation outline:

1. choose target template root
2. migrate docs/tests to new canonical path
3. keep compatibility copy if needed
4. prune old root surface only after proof passes

Verification:

```bash
git diff --check
python3 -m pytest -q \
  tests/runtime_neutral/test_generated_nested_bundled.py \
  tests/integration/test_dist_manifest_surface_roles.py
```

Rollback rule:

- restore `agents/templates/**` if any install/docs/test surface still depends on the root path

## Do-Not-Touch Rules

Until a dedicated refactor wave is approved:

- do not delete `apps/vgo-cli/**`
- do not remove `commands/**` outright
- do not remove `agents/templates/**` outright

## Recommended Priority

1. `apps/` hygiene gates
2. future install-target redesign for `commands/`
3. future host-target unification for `agents/`

## Phase Cleanup Expectations

- remove `.pytest_cache` and `.tmp/*` residue created during future verification waves
- do not kill node processes unless they are owned by this repo path

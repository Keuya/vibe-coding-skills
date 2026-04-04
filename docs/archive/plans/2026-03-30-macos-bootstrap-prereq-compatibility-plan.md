# Plan: macOS Bootstrap Prerequisite Compatibility

## Internal Grade

L

## Objective

Eliminate hidden macOS bootstrap failures by removing Bash 4-only usage from shell entrypoints and by enforcing an explicit Python prerequisite contract at the shell boundary.

## Execution Steps

1. Freeze the compatibility requirement and keep the scope limited to install/check/bootstrap entrypoints plus their user-facing docs.
2. Repair shell compatibility:
   - replace `mapfile` usage in `install.sh` with a Bash 3.2-safe collection pattern
   - re-scan active shell entrypoints for other Bash 4+ constructs in the critical path
3. Introduce Python version gating:
   - add a shared minimum-version rule for shell entrypoints
   - fail early with actionable messaging before calling Python helper scripts
   - keep the minimum aligned with the syntax already used in the repo helpers
4. Update docs and messaging:
   - explain the macOS `zsh` vs `bash` distinction
   - explain why the repo needs modern Python
   - separate bootstrap prerequisites from optional external runtime prerequisites
5. Verify:
   - run targeted tests
   - run diff hygiene
   - grep for remaining `mapfile` use in active install shell entrypoints
6. Cleanup:
   - audit node processes
   - remove temp artifacts if any were created

## Verification Commands

```bash
pytest -q tests/runtime_neutral/test_router_ai_connectivity_probe.py tests/runtime_neutral/test_bootstrap_doctor.py
git diff --check
rg -n "mapfile" install.sh check.sh scripts/bootstrap/one-shot-setup.sh
```

## Rollback Rule

If the new shell gate blocks a previously valid runtime or breaks non-macOS bootstrap flows, revert the specific prerequisite gate and repair it with a narrower compatibility check before continuing.

## Completion Rule

Do not claim the fix is complete until the updated shell entrypoints, docs, and verification evidence are all present in the same branch.

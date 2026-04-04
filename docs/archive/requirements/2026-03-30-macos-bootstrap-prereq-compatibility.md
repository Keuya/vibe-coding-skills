# Requirement: macOS Bootstrap Prerequisite Compatibility

## Goal

Repair the shipped install / check / bootstrap entrypoints so macOS users do not fail because of hidden Bash 4 assumptions or ambiguous Python runtime expectations.

## Problem Statement

Current shell entrypoints are advertised as standard `bash` scripts, but at least one path uses `mapfile`, which is unavailable in the Bash 3.2 version bundled with macOS. In parallel, multiple Python helper scripts already rely on Python 3.10+ syntax, but the install and health-check entrypoints do not enforce that minimum version up front. This produces misleading failures on macOS, especially when users launch from `zsh` and the runtime resolves to system `bash` / older `python3`.

## Required Outcomes

1. The primary shell entrypoints used for install / check / one-shot bootstrap must run on macOS with the default system Bash 3.2, or fail only for a different explicitly diagnosed reason.
2. The repository must stop relying on `mapfile` in these shell entrypoints unless it is guarded by a version check and a compatible fallback.
3. All shell entrypoints that dispatch into Python helper scripts must validate the Python version before invoking those helpers.
4. The Python version gate must clearly explain the actual minimum supported version and show concrete remediation guidance for macOS users.
5. The install / configuration docs must explain:
   - macOS default shell is often `zsh`, but the script compatibility issue is really about which `bash` binary is used
   - the shell entrypoints require a modern Python runtime because helper scripts use modern syntax
   - optional external runtimes such as `ruc-nlpir` are not the same thing as the bootstrap/runtime-neutral prerequisite floor
6. The doctor / check path should produce a direct, actionable message when Python is missing or below the supported minimum.

## Non-Goals

1. Do not redesign the host-adapter model.
2. Do not make `ruc-nlpir` auto-install its own Python environment.
3. Do not widen the install surface beyond the current shell / PowerShell / Python helper architecture.

## Acceptance Criteria

1. `install.sh` no longer uses macOS-incompatible `mapfile` in its active install path.
2. `check.sh` and `scripts/bootstrap/one-shot-setup.sh` share the same Python minimum-version rule as `install.sh`.
3. When only Python 3.8/3.9 is available, the shell entrypoint exits with a deterministic compatibility error before attempting Python helper execution.
4. The compatibility error names the detected version and tells the user what to install on macOS.
5. Install docs contain a dedicated explanation of macOS Bash and Python prerequisites.
6. Regression checks covering the changed install/doctor behavior pass.

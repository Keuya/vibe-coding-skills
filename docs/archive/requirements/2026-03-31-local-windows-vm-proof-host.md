# 2026-03-31 Local Windows VM Proof Host Requirement

- Topic: establish a local Windows VM host path on the current Ubuntu machine for Claude platform-proof work.
- Mode: interactive_governed
- Goal: make the repository able to prepare and launch a reproducible local Windows VM harness instead of blocking on missing hypervisor setup.

## Deliverable

A working change that:

1. installs the minimum local VM host dependencies needed for Windows QEMU guests
2. exposes a repository-owned script to prepare the host honestly on Ubuntu
3. exposes a repository-owned script to create and launch a local Windows VM from a user-supplied ISO
4. documents the truthful boundary between "VM host ready" and "Windows proof completed"
5. keeps the current Claude platform-promotion ceiling unchanged unless guest-side proof artifacts are actually captured

## Constraints

- No false claim that Windows platform proof is completed merely because the VM host exists
- No false claim that macOS proof is solved by the Windows VM host work
- If `/dev/kvm` is unavailable, the scripts must degrade honestly to TCG instead of pretending hardware acceleration exists
- The repository must not embed or redistribute Windows installation media
- Verification must include host-level dependency proof and script-level validation

## Acceptance Criteria

- The repo contains a host-install script for local QEMU Windows proof work
- The repo contains a launch script for a Windows ISO-backed VM with reproducible defaults
- The launch path can run without KVM by using a truthful slow-path fallback
- Documentation explains required ISO input, runtime expectations, and proof boundaries
- Host verification demonstrates the local machine now has the declared hypervisor tools

## Non-Goals

- Claiming Windows Claude proof is complete before guest install/check/CLI smoke artifacts exist
- Claiming macOS proof is complete
- Automatically downloading licensed Windows media into the repo
- Fully unattended Windows guest provisioning in this batch

## Inferred Assumptions

- The user accepts local host package installation on this Ubuntu machine
- A slower software-emulated Windows VM is still useful for proof scaffolding if KVM is absent
- The next practical bottleneck after host setup will be guest media acquisition and guest-side Claude login/smoke execution

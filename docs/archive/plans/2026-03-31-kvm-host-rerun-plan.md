# 2026-03-31 KVM Host Rerun Plan

## Goal

Prepare the repository to re-run the existing Windows ISO proof path on a real KVM-capable host and make the current environment's limitation explicit.

## Grade

- Internal grade: M

## Batches

### Batch 1: Freeze governed target
- Create a KVM-host rerun requirement doc
- Create a KVM-host rerun execution plan
- Reconfirm whether the current environment can expose `/dev/kvm`

### Batch 2: Guardrails and readiness checks
- Add a repo-owned KVM readiness script
- Add a `--require-kvm` option to the Windows proof launcher
- Keep the existing ISO flow intact for the future host rerun

### Batch 3: Verification on the current environment
- Run the readiness script on the current host
- Verify that the launcher help and syntax reflect the new KVM guardrail
- Verify that `--require-kvm` fails honestly on the current no-passthrough environment

### Batch 4: Documentation and handoff
- Update proof docs with the new KVM-host rerun path
- Record the current environment's exact boundary and the next operator step
- Leave Windows Claude proof status unchanged until a real KVM-backed guest run exists

## Verification Commands

- `bash -n ./scripts/setup/run-windows-proof-vm.sh`
- `bash ./scripts/setup/check-kvm-host-readiness.sh`
- `bash ./scripts/setup/run-windows-proof-vm.sh --help`
- `bash ./scripts/setup/run-windows-proof-vm.sh --require-kvm --iso /absolute/path/Windows.iso --dry-run`

## Rollback Rules

- If the current environment unexpectedly exposes `/dev/kvm`, stop and convert the plan into a direct rerun instead of a handoff
- If the guardrail weakens the existing launcher behavior, keep the readiness script but revert the launcher flag
- If verification does not prove the boundary clearly, do not claim the repo is ready for operator handoff

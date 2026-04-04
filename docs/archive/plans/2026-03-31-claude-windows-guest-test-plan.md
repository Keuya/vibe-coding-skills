# 2026-03-31 Claude Windows Guest Test Plan

## Goal

Advance the Windows proof lane from "host can launch QEMU" to "Claude was tested in a usable Windows guest" if the host allows it, otherwise pin the blocker down with evidence.

## Grade

- Internal grade: M

## Batches

### Batch 1: Freeze governed target
- Create a guest-test requirement doc
- Create a guest-test execution plan
- Reconfirm the current blocker: no-KVM host, UEFI path reaches either WinPE stop code `0x7E` or EFI execution failure

### Batch 2: Expand launcher coverage
- Add firmware selection to the Windows proof launcher
- Support an explicit BIOS / SeaBIOS path alongside the existing UEFI / OVMF path
- Keep current storage and boot-key helpers compatible with both modes where possible

### Batch 3: Real guest experiments
- Syntax-check the updated launcher
- Run at least one BIOS-backed Windows boot experiment with the existing Microsoft evaluation ISO
- Inspect VM state, serial artifacts, and any shell or firmware behavior to determine whether the installer path advances further than the current UEFI evidence

### Batch 4: Claude test gate
- If the guest becomes usable for install or shell actions, run a real Claude smoke check inside the guest and record the result
- If the guest does not become usable, stop before any proof-language inflation

### Batch 5: Truthful reporting and cleanup
- Update proof and status docs with the new evidence
- Stop any test VMs that were started for this batch
- Leave Windows promotion status unchanged unless guest-side Claude evidence exists

## Verification Commands

- `bash -n ./scripts/setup/run-windows-proof-vm.sh`
- `bash ./scripts/setup/run-windows-proof-vm.sh --help`
- `bash ./scripts/setup/check-windows-proof-vm-state.sh`
- `bash ./scripts/setup/run-windows-proof-vm.sh --iso /absolute/path/Windows.iso --firmware bios ...`
- `bash ./scripts/setup/stop-windows-proof-vm.sh`

## Rollback Rules

- If the BIOS path cannot be encoded cleanly in the launcher, stop and keep the current UEFI-only truth
- If BIOS runs but offers no better guest execution path, record that as evidence instead of stretching conclusions
- If real guest-side Claude testing is still blocked, do not upgrade any platform status or compatibility claim

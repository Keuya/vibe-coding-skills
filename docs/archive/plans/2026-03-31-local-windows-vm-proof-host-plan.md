# 2026-03-31 Local Windows VM Proof Host Plan

## Goal

Turn the current Ubuntu machine into a truthful local Windows proof host for Claude platform testing.

## Grade

- Internal grade: M

## Batches

### Batch 1: Freeze and baseline
- Create requirement doc
- Create execution plan
- Capture current host constraints: no QEMU tooling, no `/dev/kvm`, sudo available

### Batch 2: Repository-owned VM harness
- Add a host dependency installer script
- Add a Windows VM launch script with honest KVM vs TCG detection
- Add a stop script for cleanup and repeatable reruns
- Add a proof doc describing ISO input, runtime behavior, and evidence boundaries

### Batch 3: Host execution
- Install required QEMU/OVMF/swtpm packages on the current Ubuntu host
- Verify installed binary surfaces
- Verify firmware assets can be resolved by the launch script

### Batch 4: Proof boundary validation
- Run script syntax checks
- Run launch-script dry run
- If a Windows ISO is available, start the VM and verify the QEMU process comes up with the declared surfaces
- If optical boot needs manual confirmation, verify a repo-owned QMP key-injection path exists
- Probe at least one alternative guest-boot parameter set before claiming the host harness is blocked
- If no ISO is available, stop at a truthful "host ready, guest media pending" boundary

### Batch 5: Cleanup and reporting
- Stop any temporary VM processes started during verification
- Record what is complete vs still blocked
- Keep Claude Windows platform status unchanged unless real guest proof is captured

## Verification Commands

- `bash ./scripts/setup/install-local-vm-host.sh`
- `bash -n ./scripts/setup/install-local-vm-host.sh`
- `bash -n ./scripts/setup/run-windows-proof-vm.sh`
- `bash -n ./scripts/setup/stop-windows-proof-vm.sh`
- `python3 -m py_compile ./scripts/setup/send-qmp-boot-keys.py`
- `python3 -m py_compile ./scripts/setup/send-qmp-text.py`
- `bash ./scripts/setup/run-windows-proof-vm.sh --help`
- `qemu-system-x86_64 --version`

## Rollback Rules

- If package installation introduces unexpected conflicts, stop before writing any platform-promotion claim
- If firmware path resolution is ambiguous, keep the host installer but block the launch script until path selection is deterministic
- If the VM can launch only through manual local tweaks not encoded in repo scripts, completion is blocked

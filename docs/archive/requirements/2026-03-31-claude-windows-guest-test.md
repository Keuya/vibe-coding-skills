# 2026-03-31 Claude Windows Guest Test Requirement

- Topic: push the current Windows proof lane past host scaffolding and toward a real Claude test inside the target guest environment.
- Mode: interactive_governed
- Goal: determine truthfully whether the current Ubuntu host can boot a usable Windows guest far enough to run a Claude smoke check, and if not, record the exact blocker with reproducible evidence.

## Deliverable

A working change and proof batch that:

1. keeps one repo-owned path for launching Windows proof guests while expanding boot-surface coverage beyond the current UEFI-only route
2. attempts at least one new credible guest boot strategy aimed at bypassing the current UEFI and WinPE failure mode
3. captures empirical evidence for whether the guest reaches a state where Claude can actually be tested
4. performs a real Claude smoke check inside the guest only if the guest becomes usable
5. preserves truthful status language if the host still cannot produce a usable Windows guest

## Constraints

- No claim that Claude was tested on Windows unless evidence exists from inside the guest
- No claim that Windows platform proof is promoted merely because new firmware combinations were tried
- The current host has no `/dev/kvm`, so all guest results must be described as TCG-only unless that fact changes
- Media sources must stay official; do not invent credentials or bypass vendor gating
- Verification must include both script validation and real launch evidence

## Acceptance Criteria

- The Windows VM launcher supports at least one additional firmware path that was not available before
- The repository contains a frozen governed requirement and plan for guest-level Claude testing
- At least one real VM experiment is run after the launcher change and its result is recorded
- If the guest becomes interactive enough for software execution, Claude is checked in-guest and the result is documented
- If the guest still does not become usable, the blocker is narrowed to a concrete boot or media path rather than a vague "Windows does not work"

## Non-Goals

- Pretending host-side progress equals guest-side Claude proof
- Claiming macOS proof from this work
- Regressing or reverting unrelated repository work
- Fabricating fully unattended Windows installation if the current host cannot support it

## Inferred Assumptions

- The most credible next move on this host is to widen firmware and machine-boot coverage before abandoning the local VM lane
- BIOS or prepared-disk boot may behave differently enough from the current OVMF path to be worth a real probe
- If BIOS also fails under TCG, the next truthful escalation is likely different official Microsoft media rather than more undocumented parameter churn

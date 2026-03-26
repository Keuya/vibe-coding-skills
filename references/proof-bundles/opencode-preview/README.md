# OpenCode Preview Proof Bundle

## Scope

This bundle defines what the repository must prove before OpenCode can honestly remain `preview` and what is still missing before any stronger promotion.

## Required Evidence

### Contract proof

- `adapters/opencode/host-profile.json`
- `adapters/opencode/settings-map.json`
- `adapters/opencode/closure.json`
- `dist/host-opencode/manifest.json`
- `dist/manifests/vibeskills-opencode.json`
- `docs/universalization/host-capability-matrix.md`
- `docs/universalization/install-matrix.md`
- `docs/universalization/distribution-lanes.md`

### Install/check proof

- `install.* --host opencode`
- `check.* --host opencode`
- temp-root install isolation evidence
- runtime freshness/coherence receipts

### Runtime discovery proof

- OpenCode CLI path resolution evidence
- agent wrapper discovery evidence
- command wrapper file presence evidence
- explicit note when `opencode debug skill` diverges from official docs

## Current Measured State

The committed smoke verifier currently proves on local `opencode 1.2.27` that:

- isolated OpenCode path resolution works
- the installed `vibe` skill is discovered
- the installed `vibe-plan` agent is discovered

This is enough for a truthful `preview` label.

## Promotion Blockers

OpenCode must not move above `preview` until all of these are true:

1. command wrapper behavior is replay-backed, not only file-backed
2. skill and agent discovery replay stays stable across repeated clean roots
3. at least one platform-specific proof lane is frozen
4. docs, adapter contracts, and proof outputs all stay in sync after reruns

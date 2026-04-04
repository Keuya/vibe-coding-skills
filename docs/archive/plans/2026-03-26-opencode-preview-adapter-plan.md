# 2026-03-26 OpenCode Preview Adapter Plan

## Goal

Land a truthful OpenCode preview adapter that installs bounded preview payload into OpenCode roots, updates distribution/docs truth, and proves the lane with fresh verification evidence.

## Grade

- Internal grade: L

## Batches

### Batch 1: Freeze and intent traceability
- Create requirement doc
- Create implementation plan
- Emit skeleton and intent receipts for this governed pass
- Anchor execution to the approved OpenCode design and proof framework

### Batch 2: Adapter and distribution contracts
- Activate `opencode` in `adapters/index.json`
- Rewrite `adapters/opencode/host-profile.json`
- Rewrite `adapters/opencode/settings-map.json`
- Rewrite `adapters/opencode/closure.json`
- Add `adapters/opencode/platform-linux.json`
- Add `adapters/opencode/platform-macos.json`
- Add `adapters/opencode/platform-windows.json`
- Promote `dist/host-opencode/manifest.json`
- Promote `dist/manifests/vibeskills-opencode.json`
- Sync `dist/official-runtime/manifest.json` host support truth

### Batch 3: Preview payload and entrypoints
- Add OpenCode command wrapper templates
- Add OpenCode agent wrapper templates
- Add OpenCode example config scaffold
- Update `install.sh` and `check.sh` for `--host opencode`
- Update `install.ps1` and `check.ps1` for `--host opencode`
- Update shared install/helper scripts to recognize OpenCode target roots and payload rules

### Batch 4: Truth docs and proof surfaces
- Update universalization matrices and adapter README/distribution README wording
- Add dedicated OpenCode install docs in English and Chinese
- Add OpenCode preview proof-bundle documentation
- Add a runtime-neutral OpenCode preview smoke verification script
- Update verification gates that still hard-code the old OpenCode placeholder state

### Batch 5: Verification, receipts, cleanup
- Run adapter closure, host adapter, target-root guard, and dist manifest gates
- Run the OpenCode preview smoke verification
- Run `git diff --check`
- Emit phase execution receipt
- Emit cleanup receipt with verification evidence and known remaining limitations

## Verification Commands

- `pwsh -NoProfile -File ./scripts/verify/vgo-adapter-closure-gate.ps1 -WriteArtifacts`
- `pwsh -NoProfile -File ./scripts/verify/vgo-adapter-target-root-guard-gate.ps1 -WriteArtifacts`
- `pwsh -NoProfile -File ./scripts/verify/vibe-host-adapter-contract-gate.ps1`
- `pwsh -NoProfile -File ./scripts/verify/vibe-dist-manifest-gate.ps1 -WriteArtifacts`
- `python3 ./scripts/verify/runtime_neutral/opencode_preview_smoke.py --repo-root . --write-artifacts`
- `git diff --check`

## Rollback Rules

- If local OpenCode CLI behavior contradicts doc-based assumptions, keep the lane at `preview` and encode the limitation in proof artifacts rather than weakening Codex or overclaiming OpenCode closure.
- If shared helper changes risk Codex/Claude regressions, block completion until regression gates pass or the helper delta is narrowed.
- If command or agent wrapper discovery is unstable, preserve the skill payload and example config, but keep wrapper support explicitly provisional in docs and receipts.

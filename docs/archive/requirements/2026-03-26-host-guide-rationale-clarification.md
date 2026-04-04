# Requirement: Clarify Why OpenClaw and OpenCode Have Dedicated Install Guides

## Goal

Clarify in the public install docs why `openclaw` and `opencode` have dedicated host guides.

## Problem

The current install index links to `openclaw-path.*` and `opencode-path.*`, but does not explicitly explain whether:

- the generic install prompts can already install those hosts
- the dedicated guides exist because the common install flow is insufficient
- the dedicated guides are only for host-specific details

This can make readers infer the wrong thing: that the common prompts do not support those hosts.

## Required Outcome

The public docs must state clearly that:

- the generic install prompts still support `openclaw` and `opencode`
- the dedicated host guides are supplemental, not alternative install lanes
- the dedicated host guides exist because those hosts have extra root / command / boundary details that would make the common docs noisy

## Constraints

- keep `opencode` described as a supported install-and-use path
- keep `openclaw` described as a supported install-and-use path
- do not reintroduce confusing install-grade taxonomy into public docs
- do not add absolute local filesystem paths
- preserve the existing technical truth about host-local responsibilities

## Acceptance Criteria

1. The install index explains why `openclaw` and `opencode` have dedicated guides.
2. `openclaw-path.*` states that the common install prompts still work, and the page exists to expand host-specific details.
3. `opencode-path.*` states that the common install prompts still work, and the page exists to expand host-specific details.
4. Bundled mirrors stay in sync with the source docs.

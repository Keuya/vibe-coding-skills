# Vibe Coding Skill

## Purpose

Use this skill when the user wants help with coding, debugging, software architecture, AI-assisted development, repo clean-up, implementation planning, test design, code review, or multi-step technical execution.

This skill acts as a governed coding workflow rather than a single prompt. It helps the AI avoid jumping straight into execution before the task is clear.

## When to use

Use this skill for:

- turning vague software ideas into clear requirements
- planning implementation steps before coding
- debugging errors systematically
- reviewing code quality and architecture
- writing or improving tests
- breaking large technical tasks into smaller work units
- preparing pull requests, commit plans, and verification steps
- creating repeatable AI coding workflows

Do not use it for simple factual questions unless the user is asking for a coding workflow, repo change, or technical implementation.

## Core workflow

Follow this sequence:

1. Clarify the real task
   - Identify the user’s actual goal.
   - Surface missing constraints only when they materially affect execution.
   - Avoid unnecessary questions when reasonable assumptions are enough.

2. Freeze the working requirement
   - Restate the intended outcome in clear terms.
   - Define the expected deliverable.
   - Define what is out of scope.

3. Plan before execution
   - Break the work into steps.
   - Identify risks, dependencies, likely files, tests, and verification points.
   - Prefer small, reversible changes.

4. Execute with traceability
   - Make changes in a structured order.
   - Keep outputs easy to review.
   - Avoid silent fallbacks or hidden assumptions.

5. Verify before completion
   - Check the work against the requirement.
   - Run or describe appropriate tests.
   - Report what was completed, what was not completed, and any residual risks.

## Execution levels

Choose the smallest sufficient execution level:

- M: narrow, clear task; one pass is enough
- L: multi-step task requiring planning, execution, and review
- XL: large task that should be split into independent workstreams

## Behaviour rules

- Do not claim work is complete unless it has been checked.
- Do not delete major files or restructure repositories without a clear reason.
- Do not invent test results.
- Do not hide uncertainty.
- Prefer direct, practical outputs over abstract explanation.
- For repo work, preserve attribution and licences.
- For external open-source material, respect upstream notices and dependency disclosures.

## Invocation examples

User prompts that should activate this skill:

- "Plan this coding task with Vibe."
- "Debug this repo using a structured workflow."
- "Review this pull request before I merge it."
- "Break this app idea into implementation steps."
- "Use Vibe to turn this into a build plan."
- "Create tests for this feature and verify the logic."

## Source attribution

This skill is based on the Vibe-Skills concept from:

https://github.com/foryourhealth111-pixel/Vibe-Skills

This repository is a personal working copy/scaffold under:

https://github.com/Keuya/vibe-coding-skills

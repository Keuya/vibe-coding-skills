# 2026-03-22 README Supported Host Boundary Plan

## Goal

Add a short supported-host boundary note to the public install section in both root README files.

## Grade

- Internal grade: M

## Work Batches

### Batch 1: Traceability freeze
- create requirement doc
- create execution plan

### Batch 2: Chinese README update
- locate the install guide section in `README.md`
- add a concise supported-host note near the install links

### Batch 3: English README update
- locate the install guide section in `README.en.md`
- add the same boundary note in English

### Batch 4: Verification
- inspect the edited sections
- run `git diff --check`
- verify the wording is aligned across both files

### Batch 5: Phase cleanup
- confirm no temporary files were left behind
- leave only intended documentation changes in the working tree

# SDD Workflow

This repository defines the canonical Spec-Driven Development (SDD) lifecycle for local, review-based engineering work.

## Lifecycle

Specify → Clarify → Plan → Tasks → Implement → Verify

## Principles

- Target-local evidence outranks organization-wide assumptions.
- Current repository instructions, source, tests, and contracts outrank general guidance.
- Human approval is required before implementation proceeds.
- Requirements must be traceable from specification to tasks to implementation to verification.
- Test-first implementation is required for changes that change behavior.
- Behavioral preservation is required unless the requirement explicitly changes behavior.
- Explicit owner answers are required for clarification questions.
- Separate human acceptance review is required before completion claims.

## Evidence classification

Use the following labels for claims when working in the repository:

- Observed: directly verified from local source, tests, logs, or reports
- Inferred: reasonable conclusions drawn from observed evidence but not directly verified
- Proposed: design suggestion or candidate change that has not yet been accepted
- Unverified: not yet measured, not yet tested, or not yet reviewed

## Workflow details

### 1. Specify
Create or refine the requirement set in `SPEC.md`.

The specification must:
- state the product boundary and constraints,
- define requirements with unique `REQ-XXX` identifiers,
- include acceptance scenarios for each requirement,
- identify unverified assumptions and explicit unknowns.

### 2. Clarify
Resolve ambiguous scope or behavior before implementation.

The project must:
- identify multiple reasonable interpretations,
- ask for explicit owner answers when needed,
- avoid guessing when the requirement is ambiguous,
- record clarification outcomes in the artifacts or local review record.

### 3. Plan
Create or refine `PLAN.md`.

The plan must:
- describe architecture and execution steps,
- map work to requirement IDs,
- include validation strategy,
- call out risks, unsupported stacks, and evidence gaps.

### 4. Tasks
Create or refine `TASKS.json`.

The task list must:
- contain unique IDs,
- list dependencies,
- reference the requirement IDs they satisfy,
- include validation instructions and explicit status values,
- be checked for duplicates, missing references, and dependency cycles.

### 5. Implement
Implement the approved work.

Implementation must:
- preserve unrelated worktree changes,
- respect target-local evidence and existing conventions,
- maintain traceability from requirement to task to code,
- avoid changing behavior outside the approved scope,
- write or update tests before finalizing behavior changes when practical.

### 6. Verify
Verify using local evidence, not assumptions.

The verification step must:
- run the smallest relevant checks first,
- collect actual evidence from local logs, reports, tests, and coverage XML,
- report blocked, skipped, and unverified checks clearly,
- separate measured outcomes from broader claims,
- produce honest completion evidence before saying a change is ready.

## Required review gate

A human reviewer must explicitly approve the specification, plan, and tasks before the implementation phase enters production code changes.

Approval is not the same as a handoff. It is a human decision and must be recorded through the CLI approval flow.

## Local evidence priority

When materials disagree:
1. Target source/tests/contracts in the current repository
2. Local verification artifacts and logs
3. Prior project planning documents
4. General or organization-wide guidance

Do not override local evidence with generic rules.

## Completion standard

A phase is not complete because the agent says it is complete.
A phase is complete only when:
- the required artifacts are present,
- the human review gate has passed,
- implementation behavior is validated with local evidence,
- the output is recorded and reported honestly.

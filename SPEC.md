# Specification: SDD Agent for GitHub Copilot in VS Code and IntelliJ IDEA

Status: Draft for human review before implementation.

## 1. Purpose
This repository will deliver a practical, reliable Spec-Driven Development (SDD) agent for GitHub Copilot in VS Code and IntelliJ IDEA. The implementation will not depend on an external AI service or cloud provisioning. It will rely on the local GitHub Copilot coding environment and local Python/Java tooling available in the target repository.

The repository must provide a deterministic, reviewable workflow for:
- discovering and refining requirements,
- clarifying ambiguous behavior,
- planning work,
- creating and tracking tasks,
- implementing approved changes,
- verifying artifacts with local evidence,
- recording explicit human approvals, and
- presenting a local dashboard of current state.

## 2. Product boundary
The product has three interfaces:

1. Copilot-native coding agent
   - Discover requirements and constraints.
   - Clarify behavior and scope where reasonable interpretations exist.
   - Plan work and create tasks.
   - Implement only approved changes.
   - Report verification evidence.

2. Python console
   - Validate artifacts.
   - Record explicit human approvals.
   - Run trusted-target verification.
   - Behave as a deterministic CLI, not a chatbot.

3. Local browser dashboard
   - Show target prerequisites.
   - Show approval states.
   - Show verification outcomes and logs.
   - Show actual coverage measurements.

This is local development tooling. It is not an authenticated hosted execution service and does not automatically send Copilot chat or coding activity to the dashboard.

## 3. Design constraints
- No standalone model service.
- No cloud infrastructure provisioning.
- No additional AI API key requirement.
- Copilot provides the model and coding tools.
- Existing repository instructions, manifests, tests, and conventions must be honored.
- Unrelated worktree changes must be preserved.
- The repository must clearly distinguish between observed facts, inferred facts, proposed changes, and unverified claims.
- Human approval is required before implementation proceeds.
- If scope or behavior is ambiguous, behavior must be clarified before implementation.

## 4. Scope and phases
The project is organized into phases:

- Phase 1: Discovery and human review
- Phase 2: Implementation
- Phase 3: Verification and delivery

Phase 1 is mandatory and must complete with explicit human approval before any production code implementation begins.

## 5. Requirements

### REQ-001 — Phase 1 human review gate
Before changing production code, the repository must inspect existing instructions, manifests, source, tests, and documentation; preserve unrelated worktree changes; identify scope, failure cases, and constraints; and create reviewable artifacts:
- SPEC.md
- PLAN.md
- TASKS.json

Acceptance scenarios:
- GIVEN the project has existing instructions or conventions
  WHEN Phase 1 starts
  THEN the agent must inspect those before drafting or changing requirements.
- GIVEN unrelated worktree changes exist
  WHEN the agent creates the specification and plan
  THEN unrelated edits must remain untouched.
- GIVEN the artifacts are created
  WHEN they are presented for review
  THEN they must be explicit, reviewable, and complete enough for a human to approve or reject them.

### REQ-002 — Specification quality and format
The specification must include unique requirement identifiers in the format `REQ-XXX`, each with an associated acceptance scenario.

Acceptance scenarios:
- GIVEN a requirement is added to the spec
  WHEN the requirement is reviewed
  THEN it must have a unique numeric identifier and a clear acceptance criterion.
- GIVEN requirements are duplicated or empty
  WHEN validation runs
  THEN the validation must fail with a clear error.

### REQ-003 — Plan quality and architecture
The plan must include: architecture, execution steps, requirement mapping, and validation strategy.

Acceptance scenarios:
- GIVEN the plan is created
  WHEN it is reviewed
  THEN it must be structured with the required sections.
- GIVEN a plan is missing one of those sections
  WHEN validation runs
  THEN validation must fail as incomplete.

### REQ-004 — Task tracking and dependencies
The task inventory must contain unique IDs, titles, requirement references, dependencies, status, and validation instructions.

Acceptance scenarios:
- GIVEN tasks are created
  WHEN they are reviewed
  THEN each task must have a unique ID and valid dependencies.
- GIVEN duplicate task IDs or invalid fields exist
  WHEN validation runs
  THEN the task file must be rejected.
- GIVEN a requirement has no corresponding task
  WHEN traceability is validated
  THEN the validation must fail.

### REQ-005 — Explicit human approvals only
Approvals must be recorded only through a human-operated CLI command. The system must not auto-approve or infer approval from a model response.

Acceptance scenarios:
- GIVEN a user runs an approval command
  WHEN the approval is valid
  THEN the system records the approval with the target artifact fingerprint.
- GIVEN approval content is changed after approval is recorded
  WHEN the validation runs
  THEN the approval must be invalidated.

### REQ-006 — Approval fingerprint binding
Approvals must be bound to SHA-256 fingerprints for specific artifact scopes:
- Spec approval: specification
- Plan approval: specification + plan
- Task approval: specification + plan + tasks

Acceptance scenarios:
- GIVEN the specification changes after approval
  WHEN validation checks approval state
  THEN approval must be no longer valid.
- GIVEN the plan changes without changing the specification
  WHEN plan approval is checked
  THEN the system must detect the mismatch and invalidate the plan approval.

### REQ-007 — Canonical SDD workflow
The repository must provide a single canonical workflow document titled `SDD-WORKFLOW.md` governing the lifecycle:
`Specify → Clarify → Plan → Tasks → Implement → Verify`

Acceptance scenarios:
- GIVEN the canonical workflow is referenced
  WHEN a developer follows it
  THEN it must instruct them to use target-local evidence, behavioral preservation, explicit owner answers, requirement traceability, test-first implementation, and separate human acceptance review.
- GIVEN a claim is not directly observed in target source or tests
  WHEN the workflow classifies it
  THEN it must be labeled as Observed, Inferred, Proposed, or Unverified.

### REQ-008 — Copilot customization assets
The repository must create Copilot customization files for both VS Code and IntelliJ IDEA support:
- `.github/agents/sdd.agent.md`
- `.github/prompts/sdd-specify.prompt.md`
- `.github/prompts/sdd-clarify.prompt.md`
- `.github/prompts/sdd-plan.prompt.md`
- `.github/prompts/sdd-tasks.prompt.md`
- `.github/prompts/sdd-implement.prompt.md`
- `.github/prompts/sdd-verify.prompt.md`
- `.github/copilot-instructions.md`
- `AGENTS.md`
- applicable path-scoped instructions

Acceptance scenarios:
- GIVEN a Copilot-enabled IDE loads the repo
  WHEN it reads the agent and prompt files
  THEN it must find the shared phase instructions and local workflow guidance.
- GIVEN a plain-language request such as “Run the Plan phase” is used
  WHEN the IDE does not provide slash prompts or handoff buttons
  THEN the repo must still allow the corresponding prompt to be loaded via the shared prompt file.

### REQ-009 — Deterministic validation engine
The repository must provide a deterministic validation engine for artifact integrity and approval gating.

Specifically it must detect:
- missing, empty, malformed, or placeholder-filled artifacts
- unresolved clarification markers
- missing required sections
- duplicate or empty requirement definitions
- missing plan-to-requirement mapping
- duplicate task IDs and invalid task fields
- unknown requirement or dependency references
- requirements without tasks
- dependency cycles

Acceptance scenarios:
- GIVEN a malformed artifact
  WHEN validation runs
  THEN validation must fail with the specific reason.
- GIVEN a dependency cycle exists
  WHEN task graph validation runs
  THEN the system must reject the cycle.

### REQ-010 — Trusted verification target and configuration
The repository must provide a shared verification engine used by both the CLI and the web API. It must configure a trusted target at startup, and HTTP clients must not choose arbitrary paths or commands.

Acceptance scenarios:
- GIVEN a verification target is configured
  WHEN the engine starts
  THEN it must run only against the configured trusted target.
- GIVEN an unsupported stack or layout is encountered
  WHEN verification begins
  THEN the system must report the unsupported layout truthfully instead of pretending success.

### REQ-011 — Gradle verification gates
The verification engine must support a standard root Java/Gradle module on macOS/Linux and run sequentially:
1. Checkstyle main and test
2. Executable tests with JUnit XML evidence
3. JaCoCo XML report and coverage verification

Acceptance scenarios:
- GIVEN a Gradle target is valid
  WHEN the engine runs the gate sequence
  THEN it must stop on a failed gate and report the failure.
- GIVEN a required report is missing or malformed
  WHEN the engine reads it
  THEN it must fail validation.
- GIVEN a test suite has no executable tests
  WHEN verification runs
  THEN the result must be rejected as invalid evidence.

### REQ-012 — Coverage threshold and evidence
The engine must calculate coverage from the actual report-level `LINE` counter, using an inclusive default threshold of 80%. It must not weaken stricter repository rules and must never present 80% as a universal or organizational mandate.

Acceptance scenarios:
- GIVEN a JaCoCo XML report with LINE coverage below 80%
  WHEN verification runs
  THEN it must fail with the measured coverage result.
- GIVEN a report contains a malformed line counter or invalid data
  WHEN validation reads it
  THEN the verification must fail.

### REQ-013 — CLI and local API contract
The repository must provide CLI commands equivalent to:
- `python sdd_agent.py --project /trusted/target check`
- `python sdd_agent.py --project /trusted/target approve spec --reviewer "Owner"`
- `python sdd_agent.py --project /trusted/target approve plan --reviewer "Owner"`
- `python sdd_agent.py --project /trusted/target approve tasks --reviewer "Owner"`
- `python sdd_agent.py --project /trusted/target verify`
- `python sdd_agent.py --project /trusted/target --port 8080 serve`

It must also provide:
- `GET /`
- `GET /api/sdd/status`
- `POST /api/sdd/verify` with an empty JSON object

Acceptance scenarios:
- GIVEN the CLI is invoked with invalid or unsupported input
  WHEN it runs
  THEN it must exit with a nonzero status.
- GIVEN the API is bound to the loopback address
  WHEN a request is made from outside the local machine
  THEN the server must reject or not serve it.

### REQ-014 — Local dashboard
The dashboard must be a local HTML/CSS/JavaScript UI showing the trusted target, approval state, prerequisite errors, verification gate results, coverage, logs, and historical results. Logs must be rendered as text, not HTML.

Acceptance scenarios:
- GIVEN a verification run fails
  WHEN the dashboard loads
  THEN it must show the failed state and relevant log output.
- GIVEN historical evidence exists
  WHEN the dashboard renders results
  THEN it must clearly distinguish these as historical evidence rather than live streaming.

### REQ-015 — Bootstrap, templates, examples, and documentation
The repository must provide:
- idempotent bootstrap for local dependencies into a virtual environment
- specification, plan, and task templates
- reusable Java 21 Gradle example with centralized versions, Checkstyle, JUnit 5, and JaCoCo XML reporting
- isolated Java example separate from Python tooling root
- documentation for installation, VS Code and IntelliJ setup, safe adoption, phased workflow, verification, dashboard usage, and troubleshooting

Acceptance scenarios:
- GIVEN the bootstrap runs multiple times
  WHEN it executes
  THEN it must be idempotent and avoid overwriting instructions or generating a second server.
- GIVEN the Java example is used
  WHEN it is reviewed
  THEN it must be separate from the Python root and not fabricated to fake success.

### REQ-016 — Tests and CI
The repository must include deterministic tests for approval invalidation, traceability, dependency cycles, CLI/API agreement, subprocess failure and timeout handling, concurrency, skipped checks, test evidence, coverage boundaries, persistence, and dashboard behavior.

Acceptance scenarios:
- GIVEN the repository runs its test suite
  WHEN a validation condition is violated
  THEN the relevant deterministic test must fail and identify the problem.
- GIVEN CI is configured
  WHEN the repository is run in public CI
  THEN it must use public tooling and require no private infrastructure.

### REQ-017 — Delivery gate and verification discipline
Phase 3 requires the smallest applicable tests first, then broader checks when needed. Verification must be evidence-based and must not claim perfection, universal coverage, deployment readiness, or semantic parity from mechanical checks alone.

Acceptance scenarios:
- GIVEN a verification result is successful
  WHEN it is reported
  THEN the report must distinguish between observed evidence and broader claims.
- GIVEN a check cannot be performed or is blocked
  WHEN verification is summarized
  THEN it must clearly identify the blocked or unverified state.

## 6. Non-goals and constraints
- This project does not promise IDE feature parity beyond the capabilities that can be verified from current official Copilot customization documentation.
- This project does not automatically send chat or coding activity to the dashboard.
- This project does not depend on remote hosting or cloud execution.
- This project does not approve its own artifacts.
- This project does not claim a feature is complete without local verification evidence.

## 7. Human approval gate
Implementation is not allowed until a human reviews the specification, plan, and task artifacts and explicitly approves them. The approval must be recorded in the CLI using the explicit approval workflow, not by informal chat acknowledgement.

The project may continue only after the human approval step is complete.

## 8. Review checklist
Before implementation, the human reviewer should confirm:
- Requirements are complete and specific.
- The plan includes required sections and mapping.
- Tasks are uniquely identified and dependencies are valid.
- Approval rules and SHA-256 fingerprinting are acceptable.
- The verification engine is scoped to trusted targets and local evidence.
- The dashboard and CLI contracts match the described behavior.
- The Java example is realistic and separate from Python tooling.
- Test coverage and CI strategy are clear, deterministic, and limited to public tooling.

This specification is intentionally review-first and implementation-second.


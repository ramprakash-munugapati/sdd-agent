# Plan: SDD Agent for GitHub Copilot in VS Code and IntelliJ IDEA

Status: Draft for human review before implementation.

## 1. Objective
Deliver a practical SDD agent system with three interfaces:
- Copilot-native workflow for a local coding agent
- Python console for deterministic checks and approvals
- Local browser dashboard for evidence and gate status

This plan treats the requirement set in `SPEC.md` as the governing source of truth. It does not assume IDE parity beyond what is locally verifiable.

## 2. Architecture overview

### 2.1 Repository layout
The final implementation will have a clear separation between:
- Python tooling root for the CLI, API, validation, and dashboard assets
- Java/Gradle example root for an isolated example module
- GitHub Copilot customization files under `.github/`
- Canonical workflow and developer-facing guidance (`SDD-WORKFLOW.md`, `AGENTS.md`)

### 2.2 Core components
1. Artifact validator
   - Reads `SPEC.md`, `PLAN.md`, and `TASKS.json`.
   - Checks for missing sections, malformed content, placeholder text, duplicate IDs, mapping gaps, dependency cycles, and approval mismatches.

2. Approval manager
   - Records explicit reviewer approval via local CLI.
   - Stores approval status and SHA-256 fingerprints.
   - Invalidates approvals when relevant files change.

3. Verification engine
   - Configures the trusted target at startup.
   - Runs preflight checks for the trusted target and required artifacts.
   - Enforces sequential verification gates for Checkstyle, tests, and coverage.
   - Persists logs and measured results.

4. CLI and local web API
   - Provides commands for check, approve, verify, and serve.
   - Exposes the required local endpoints.
   - Binds to loopback and rejects unsafe or cross-origin execution patterns.

5. Dashboard UI
   - Fetches and displays local status, logs, coverage, and historical result data.
   - Shows truthful state labels and statements about evidence, history, and local-only execution.

6. Java/Gradle example fixture
   - Separate from the Python root.
   - Contains a realistic but minimal Java 21 module setup with centralized version management, Checkstyle, JUnit 5, and JaCoCo XML.
   - Used as an opt-in integration example rather than as a fake success path.

## 3. Execution steps

### Phase 1 — discovery and review
1. Inspect repository instructions, manifests, existing source, and tests.
2. Identify project constraints and unsupported assumptions.
3. Draft `SPEC.md` with unique `REQ-XXX` entries and acceptance scenarios.
4. Draft `PLAN.md` covering architecture, execution, mapping, and validation strategy.
5. Draft `TASKS.json` with dependencies, IDs, and validation instructions.
6. Present these to the owner for review.
7. Halt before implementation until explicit approval is recorded.

### Phase 2 — implementation after approval
1. Create canonical workflow and developer expectations (`SDD-WORKFLOW.md`).
2. Create Copilot agent/prompt files and path-scoped guidance.
3. Implement artifact validation and approval fingerprinting.
4. Implement CLI and local API with server loopback binding.
5. Implement trusted-target verification engine and persistence.
6. Implement local dashboard assets and result reporting.
7. Add bootstrap, templates, and Java example module.
8. Add deterministic tests and CI configuration.
9. Produce user documentation.

### Phase 3 — verification and delivery
1. Run smallest relevant tests first.
2. Run broader verification checks where required.
3. Validate exact behaviors and evidence rather than proxies.
4. Summarize actual commands, outcomes, measured coverage, and any unverified/blocked checks.
5. Deliver the repository without claiming more than the measured evidence supports.

## 4. Requirement mapping

| Requirement | Primary implementation area | Validation focus |
| --- | --- | --- |
| REQ-001 | Phase 1 workflow | Artifact existence and human gate |
| REQ-002 | Artifact validator | Requirement ID uniqueness and acceptance scenarios |
| REQ-003 | Plan standard | Required sections completeness |
| REQ-004 | Task validator | Unique IDs, dependencies, requirement references |
| REQ-005 | Approval manager | Human CLI approvals only |
| REQ-006 | Approval fingerprinting | SHA-256 invalidation rules |
| REQ-007 | Canonical workflow | Workflow semantics and evidence classification |
| REQ-008 | Copilot assets | Prompt and agent file integrity |
| REQ-009 | Validation engine | Artifact and dependency validation |
| REQ-010 | Trusted target config | Startup target and unsupported layout reporting |
| REQ-011 | Verification engine | Checkstyle, tests, JaCoCo execution order |
| REQ-012 | Coverage policy | LINE coverage threshold and invalid report handling |
| REQ-013 | CLI + API | Commands, routes, loopback binding, exit codes |
| REQ-014 | Dashboard | Local UI state and log rendering |
| REQ-015 | Bootstrap + templates | Idempotency, isolation, docs |
| REQ-016 | Tests + CI | Deterministic coverage of failure modes |
| REQ-017 | Verification discipline | Evidence reporting and honest gate summaries |

## 5. Validation strategy

### 5.1 Artifact validation
Validation will be implemented in a deterministic, testable form and will fail loudly on:
- malformed YAML/JSON or missing files
- placeholder content
- unresolved review markers
- duplicate requirement or task IDs
- missing plan-to-requirement mapping
- dependency cycles
- approvals that do not match the current artifact SHA-256 values

### 5.2 CLI and API validation
The CLI and REST layer will be tested for:
- matching command names and flags
- expected exit codes on failure
- correct local routes and loopback binding behavior
- server errors and cross-origin safety

### 5.3 Verification engine validation
The verification engine will validate:
- target preflight requirements
- required Gradle wrappers and Java/Gradle layout
- sequential gate execution order
- strict failure handling on skipped or malformed checks
- coverage calculation from the JaCoCo report `LINE` counter
- persistence of logs and evidence
- timeout and concurrency behavior

### 5.4 Dashboard validation
The dashboard will be validated for:
- correct state labels: `NOT_RUN`, `BLOCKED`, `RUNNING`, `PASSED`, `FAILED`
- text-only log rendering
- accurate differentiation between live and historical evidence
- error messaging for missing prerequisites and service errors

### 5.5 Test-first discipline
The implementation will follow test-first practice for each major behavior. The tests will cover:
- approval invalidation
- traceability and gap checks
- dependency cycle detection
- CLI API parity
- subprocess failure and timeout conditions
- concurrency safeguards
- skipped checks
- test evidence and coverage boundaries
- persistence and historical results
- dashboard behavior

## 6. Risks and mitigations

### Risk: Overclaiming capability
Mitigation: validation engine must only report evidence-based states, and all claims must be tied to measured artifacts.

### Risk: Ambiguous IDE support claims
Mitigation: only document features that match current official Copilot customization guidance and local verification.

### Risk: Fake success in Java example
Mitigation: keep the Java example isolated and realistic, and avoid fabricating a Spring app or database simply to satisfy empty gates.

### Risk: Approval logic drift
Mitigation: tie each approval to artifact fingerprint state and validate mismatches aggressively.

### Risk: Local server misuse
Mitigation: enforce loopback binding and reject unsafe execution contexts.

## 7. Review gate
This plan is ready for human review. Implementation must wait for explicit human approval of the specification, plan, and tasks before production code is changed.


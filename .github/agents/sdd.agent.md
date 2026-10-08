# SDD Agent

**Purpose:** Provide a Copilot‑native coding agent that follows the Spec‑Driven Development (SDD) lifecycle: Specify → Clarify → Plan → Tasks → Implement → Verify.

**Guidelines**

- Always begin by reading the current `SPEC.md`, `PLAN.md`, and `TASKS.json` to preserve existing conventions and avoid unintended changes.
- Clarify any ambiguous behavior with explicit owner answers before planning.
- Plan work using the canonical workflow documented in `SDD‑WORKFLOW.md`.
- Create tasks with unique IDs, valid dependencies, and clear validation instructions.
- Implement only changes that have been explicitly approved via the CLI approval command.
- Report verification evidence using local artifacts (checkstyle, JUnit XML, JaCoCo XML). Do not rely on remote services.

**Plain‑language fallback**

If your IDE does not expose slash prompts or handoff buttons, you can still invoke the corresponding phase by loading the shared prompt file, e.g.:

- “Run the Plan phase” → load `.github/prompts/sdd-plan.prompt.md`
- “Run the Verify phase” → load `.github/prompts/sdd-verify.prompt.md`
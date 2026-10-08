# SDD Specify Prompt

**Goal:** Create or refine `SPEC.md` following the repository's requirement format.

**Instructions**

1. Identify the product boundary and constraints (see existing `SDD-WORKFLOW.md`).
2. Add or update requirements using the `REQ-XXX` format.
3. For each requirement, write a clear acceptance scenario using the GIVEN/WHEN/THEN pattern.
4. Flag any assumptions as `Observed`, `Inferred`, `Proposed`, or `Unverified` per the evidence classification in `SDD-WORKFLOW.md`.
5. Preserve any existing requirements; do not delete or rename identifiers without a matching update in `TASKS.json` and the verification engine.
6. When scope is ambiguous, request an explicit owner answer before proceeding.

**Plain‑language fallback**

If your IDE does not provide a slash prompt, you can invoke this prompt by opening the file `.github/prompts/sdd-specify.prompt.md` and reading its contents; the prompt text above is the instruction that GitHub Copilot will use.
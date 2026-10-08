# SDD Plan Prompt

**Goal:** Create or refine `PLAN.md` with the required sections.

**Instructions**

1. Describe the architecture of the change (components, data flow, etc.).
2. List execution steps in order; each step should be actionable and tied to a requirement ID.
3. Map every requirement from `SPEC.md` to one or more tasks in `TASKS.json`; call out any mapping gaps.
4. Include a validation strategy that specifies how each gate (checkstyle, tests, coverage) will be verified.
5. Call out risks, unsupported stacks, and evidence gaps as `Proposed` or `Unverified` per `SDD-WORKFLOW.md`.
6. Ensure the plan contains the mandatory sections: Architecture, Execution Steps, Requirement Mapping, Validation Strategy. Omission of any section will cause the validation engine to reject the plan.

**Plain‑language fallback**

If your IDE does not provide a slash prompt, open `.github/prompts/sdd-plan.prompt.md` and use the text above as the instruction for the Plan phase.
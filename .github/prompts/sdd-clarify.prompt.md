# SDD Clarify Prompt

**Goal:** Resolve ambiguous scope or behavior before implementation.

**Instructions**

1. Scan the current `SPEC.md`, `PLAN.md`, and `TASKS.json` for statements that have multiple reasonable interpretations.
2. For each ambiguous point, ask for an explicit owner answer (e.g., “Do we want behavior X or Y?”).
3. Record the clarification outcome in the artifacts or a local review record; do not guess.
4. If no reasonable interpretation exists, mark the point as `Unverified` and note the unknown.
5. After all ambiguities are resolved, the plan may proceed with clear, unambiguous requirements.

**Plain‑language fallback**

If your IDE lacks slash prompts, open `.github/prompts/sdd-clarify.prompt.md` and use the text above as the instruction that Copilot should follow for the Clarify phase.
# SDD Tasks Prompt

**Goal:** Create or refine `TASKS.json` with unique IDs, dependencies, and validation instructions.

**Instructions**

1. Each task must have a unique `id` in the format `TASK‑NNN`.
2. Provide a concise `title` and list of `requirement` IDs satisfied.
3. Include `dependencies` (other task IDs) and ensure the dependency graph is acyclic.
4. Set `status` to one of `planned`, `in_progress`, `completed`, or `blocked`.
5. Add `validation` instructions that describe how the task will be verified (e.g., "run pytest with JUnit XML", "checkstyle on modified source").
6. Detect and reject duplicate task IDs, invalid fields, and references to non‑existent requirements.
7. After creating or updating tasks, run the repository's task‑validation step to confirm consistency.

**Plain‑language fallback**

If your IDE lacks slash prompts, open `.github/prompts/sdd-tasks.prompt.md` and use the text above as the instruction for the Tasks phase.
# SDD Implement Prompt

**Goal:** Implement approved changes while preserving unrelated worktree modifications and maintaining traceability.

**Instructions**

1. Only implement changes that have an explicit approval recorded via the CLI `approve <type>` command.
2. Preserve all unrelated worktree changes; do not modify files outside the approved scope.
3. Maintain traceability from requirement (`REQ‑XXX`) → task (`TASK‑NNN`) → code change.
4. Write or update tests before finalizing behavior changes when practical (test‑first discipline).
5. After implementation, run the verification engine (`python sdd_agent.py --project <trusted/target verify`) to produce evidence.
6. If any check fails, revert the related code and re‑clarify the requirement.

**Plain‑language fallback**

If your IDE does not provide a slash prompt, open `.github/prompts/sdd-implement.prompt.md` and use the text above as the instruction for the Implement phase.
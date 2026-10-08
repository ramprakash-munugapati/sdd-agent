# SDD Verify Prompt

**Goal:** Run the deterministic verification engine and report evidence.

**Instructions**

1. Ensure the trusted target is configured (via `--project <path>`).
2. The engine runs sequentially:
   a. **Checkstyle** on main and test sources.
   b. **Executable tests** using JUnit XML output.
   c. **JaCoCo XML report** and LINE‑coverage verification (default 80% inclusive threshold).
3. Reject the run if any gate is skipped, malformed, or times out.
4. Persist the results (target, timestamps, artifact fingerprints, commands, gate outcomes, logs, measured coverage).
5. Report `PASSED` only when all gates pass; otherwise report `FAILED` with the specific reason.
6. Do not auto‑approve; any approval must be recorded separately via the CLI.

**Plain‑language fallback**

If your IDE does not provide a slash prompt, open `.github/prompts/sdd-verify.prompt.md` and use the text above as the instruction for the Verify phase.
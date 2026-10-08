# sdd-agent

Spec‑Driven Development agent for GitHub Copilot in VS Code and IntelliJ IDEA. Discover requirements, plan work, implement approved changes, and verify with human approvals.

## Quick start

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-org/sdd-agent.git
   cd sdd-agent
   ```

2. **Bootstrap the local environment** (creates a venv, installs test dependencies)

   ```bash
   python bootstrap.py
   ```

3. **Trusted target** – point the agent at a repository you want to verify:

   ```bash
   python sdd_agent.py --project /path/to/target check
   ```

4. **Record a human approval** (replace `Owner` with the reviewer name)

   ```bash
   python sdd_agent.py --project /path/to/target approve spec --reviewer "Owner"
   python sdd_agent.py --project /path/to/target approve plan --reviewer "Owner"
   python sdd_agent.py --project /path/to/target approve tasks --reviewer "Owner"
   ```

5. **Run the verification engine** (checks checkstyle, JUnit tests, JaCoCo coverage)

   ```bash
   python sdd_agent.py --project /path/to/target verify
   ```

6. **Start the local dashboard API** (binds to loopback, port 8080 by default)

   ```bash
   python sdd_agent.py --project /path/to/target --port 8080 serve
   ```

   Then open <http://127.0.0.1:8080> in a browser to view status, logs, coverage, and historical evidence.

7. **View the dashboard UI**

   Open `dashboard.html` in any browser, or point the built‑in server at the appropriate URL.

## Phases (canonical workflow)

```
Specify → Clarify → Plan → Tasks → Implement → Verify
```

- **Specify** – create or edit `SPEC.md` with `REQ‑XXX` requirements and acceptance scenarios.
- **Clarify** – resolve ambiguous behavior via explicit owner answers (prompt files in `.github/prompts/`).
- **Plan** – produce `PLAN.md` with Architecture, Execution Steps, Requirement Mapping, Validation Strategy.
- **Tasks** – maintain `TASKS.json` with unique IDs, dependencies, and validation instructions.
- **Implement** – make changes only after an approval has been recorded; preserve unrelated worktree edits.
- **Verify** – the CLI runs the verification engine; the dashboard shows gate outcomes, coverage, and logs.

## Artifact validation

The agent validates:

- `SPEC.md` must contain `REQ‑XXX` identifiers and acceptance scenarios.
- `PLAN.md` must include the required sections (Architecture, Execution Steps, Requirement Mapping, Validation Strategy).
- `TASKS.json` must have unique task IDs, valid dependencies, and references to existing requirements.
- Approvals are bound to SHA‑256 fingerprints of the relevant artifacts; changing an artifact invalidates the corresponding approval.

## Approval fingerprint binding

| Approval type | Fingerprint scope |
|---------------|-------------------|
| `spec`        | SHA‑256 of `SPEC.md` |
| `plan`        | SHA‑256 of `SPEC.md` + `PLAN.md` (concatenated) |
| `tasks`       | SHA‑256 of `SPEC.md` + `PLAN.md` + `TASKS.json` |

Recorded in `.sdd/approvals.json`. If any artifact in the scope changes, the approval is automatically considered invalid.

## Dashboard

The dashboard UI (`dashboard.html`) shows:

- Trusted target path
- Current state (`NOT_RUN`, `BLOCKED`, `RUNNING`, `PASSED`, `FAILED`)
- Artifact, checkstyle, test, and coverage gate results
- Buffered execution logs (rendered as plain text)
- Historical evidence (clearly marked as past runs, not live streaming)

## Bootstrap idempotency

Running `python bootstrap.py` multiple times is safe: after the first run a marker file `.sdd_bootstrap_done` is created, and subsequent runs skip environment creation and do not overwrite existing instructions or start a second server.

## Troubleshooting & trust limitations

- The agent is **local development tooling only**; it does not authenticate users or guarantee identity.
- The dashboard binds to `127.0.0.1` and rejects cross‑origin requests.
- Verification failures return non‑zero CLI exit codes.
- Coverage defaults to an inclusive 80% threshold based on the JaCoCo `LINE` counter; this is **not** an organizational mandate.
- If your project uses a different build system or Java version, the verification engine will report the unsupported layout rather than pretending success.

## Repository layout (high‑level)

```
sdd-agent/
├─ .github/
│  ├─ agents/
│  │   └─ sdd.agent.md
│  ├─ prompts/
│  │   ├─ sdd-specify.prompt.md
│  │   ├─ sdd-clarify.prompt.md
│  │   ├─ sdd-plan.prompt.md
│  │   ├─ sdd-tasks.prompt.md
│  │   ├─ sdd-implement.prompt.md
│  │   ├─ sdd-verify.prompt.md
│  │  └─ copilot-instructions.md
│  └─ workflows/
│      └─ ci.yml
├─ sdd_agent.py          # CLI + local API
├─ dashboard.html        # browser UI
├─ bootstrap.py          # idempotent venv bootstrap
├─ tests/
│  └─ test_validation.py
├─ .sdd/                 # runtime state (approvals, evidence)
├─ .sdd_bootstrap_done   # marker for idempotent bootstrap
└─ README.md            # you are here
```

## Java 21 Gradle example (isolated)

A minimal `java-example/` directory is provided **outside** the Python tooling root. It contains a Java 21 source file, a `build.gradle` with centralized version management, Checkstyle, JUnit 5, and JaCoCo XML reporting. Use it as a reference:

```bash
cd java-example
./gradlew check   # runs checkstyle, tests, and jacocoReport
```

The example is deliberately simple – no Spring, no database – so that verification gates reflect real evidence rather than fabricated success.

---

*This repository is intentionally review‑first and implementation‑second. All production‑code changes must pass the human approval gate before they are applied.*
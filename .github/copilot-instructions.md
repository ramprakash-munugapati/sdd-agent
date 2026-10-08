# GitHub Copilot Instructions – SDD Agent

This repository provides a set of path‑scoped instructions that GitHub Copilot can use to follow the Spec‑Driven Development (SDD) workflow.

## Canonical workflow

`Specify → Clarify → Plan → Tasks → Implement → Verify`

All phase instructions are stored in `.github/prompts/`. When Copilot encounters a request such as “Run the Plan phase”, load the corresponding prompt file:

- **Specify** → `.github/prompts/sdd-specify.prompt.md`
- **Clarify** → `.github/prompts/sdd-clarify.prompt.md`
- **Plan** → `.github/prompts/sdd-plan.prompt.md`
- **Tasks** → `.github/prompts/sdd-tasks.prompt.md`
- **Implement** → `.github/prompts/sdd-implement.prompt.md`
- **Verify** → `.github/prompts/sdd-verify.prompt.md`

## Agent metadata

The agent definition is in `.github/agents/sdd.agent.md`.

## Approval workflow

Approvals are recorded exclusively via the local CLI (`python sdd_agent.py --project <path> approve <spec|plan|tasks>`). The dashboard and Copilot chat never auto‑approve.

---

*These instructions are intentionally minimal; they reference the shared prompt files so that the same guidance is used by both VS Code and IntelliJ IDEA integrations.*
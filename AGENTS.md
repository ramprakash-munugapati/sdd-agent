# AGENTS.md

This repository contains the canonical SDD workflow and Copilot customization setup for local, review-driven development.

For the official workflow, see [`SDD-WORKFLOW.md`](./SDD-WORKFLOW.md).

## Shared workflow phases

- Specify
- Clarify
- Plan
- Tasks
- Implement
- Verify

## Human approval requirement

The repository does not implement production changes before a human reviews and explicitly approves the specification, plan, and tasks.

## Local evidence requirement

All implementation and verification work must rely on current target-local evidence rather than generalized assumptions.

## Copilot customization

Use the repository prompt files under `.github/prompts/` and agent metadata under `.github/agents/` for structured phase execution.

If slash commands or handoff buttons are unavailable in the IDE, use plain-language instructions such as:

- "Run the Plan phase"
- "Run the Verify phase"
- "Load the SDD specify prompt"

This repository supports plain-language prompts by loading the corresponding shared prompt file.

## Scope

This repo is for local development tooling and human-reviewed workflow support. It is not a hosted service or a cloud deployment system.

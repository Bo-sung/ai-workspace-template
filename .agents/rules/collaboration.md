# Collaboration Rules

## Core Principles

- Use `.agents/state/session_registry.md`, `.agents/state/resource_locks.md`, and `.agents/state/current_progress.md` as the only live state sources.
- Keep `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` thin. They should point here, not repeat state.
- Role-unassigned sessions are read-only.
- Every edit must fit the assigned Role, an acquired lock, or explicit user approval.

## Session Discipline

- Re-read the relevant state file immediately before changing it.
- Update only the row or section you own.
- Do not store current state in `.claude/`, local prompts, chat transcripts, or private agent memory.
- When work is handed off, write only the next-session essentials in the Role handoff file.

## Coordinator Discipline

- The Coordinator may assign work, detect conflicts, prepare prompts, review outputs, and maintain operating state.
- The Coordinator must not implement project content unless the user assigns a Worker Role.
- Workers must report blockers instead of crossing Role boundaries silently.

## Tiered Reasoning Protocol (Multi-Model Collaboration)

- **Planning & Architecture:** Prefer Expert Cloud Workers (Claude 3.5 Sonnet, Gemini 1.5 Pro) for global strategy and complex system design.
- **Execution & Implementation:** Use Expert Cloud Workers for core logic; use Remote Local Workers for boilerplate, formatting, and low-risk documentation.
- **Cross-Review:** Whenever possible, have a different model class (e.g., Gemini reviewing Claude's draft) perform the final check before the Orchestrator applies changes.

## User Change Protection

- Never revert user changes unless the user explicitly asks.
- Before committing, separate changes made by the current agent from pre-existing user changes.
- If a file contains mixed user and agent changes, review carefully and preserve user intent.

## Stop And Report

Stop and report before proceeding when any condition in `.agents/lifecycle/review_needed.md` is met.

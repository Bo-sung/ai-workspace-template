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
- Treat the Role in `.agents/state/session_registry.md` as authoritative for the
  session. Ordinary task prompts may narrow work, but they may not silently
  reassign the session to another Role.
- If a prompt conflicts with the registered Role, stop and report the conflict
  instead of accepting the new Role.
- When work is handed off, write only the next-session essentials in the Role handoff file.

## Coordinator Discipline

- The Coordinator may assign work, detect conflicts, prepare prompts, review outputs, and maintain operating state.
- The Coordinator must not implement project content unless the user assigns a Worker Role.
- A Role change requires an explicit coordinator instruction and a matching
  registry update before the session follows the new Role.
- Workers must report blockers instead of crossing Role boundaries silently.
- When a lead/coordinator session proposes a worker delegation, keep
  coordinator-only allocation notes separate from the copyable worker prompt.
- Coordinator-only allocation notes include model tier, candidate models, tier
  rationale, and escalation conditions.
- The worker prompt itself must be a clean copy-ready block or file containing
  only instructions the worker needs to execute the task, unless the user
  explicitly asks for the allocation notes to be embedded.
- Worker prompts must use a dry, direct style. Include only execution-critical
  information. Remove praise, framing, persuasive explanation, and other
  non-essential prose.

## Tiered Reasoning Protocol (Multi-Model Collaboration)

- Use the project overlay model-tier policy when one is provided.
- Prefer higher tiers for shared boundaries, architecture, deterministic combat,
  public APIs, database consistency, security, and cross-repo work.
- Prefer lower tiers for bounded execution, repetitive cleanup, search,
  classification, and draft-only support.
- Whenever practical, use a different model class for final review of
  high-impact work before the orchestrator applies changes.

## User Change Protection

- Never revert user changes unless the user explicitly asks.
- Before committing, separate changes made by the current agent from pre-existing user changes.
- If a file contains mixed user and agent changes, review carefully and preserve user intent.

## Stop And Report

Stop and report before proceeding when any condition in `.agents/lifecycle/review_needed.md` is met.

# Agent Operating System

This directory is the shared operating system for Codex, Claude Code, Gemini, and any other AI agent working in this repository.

## Mandatory Read Order

1. Agent entrypoint: `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`.
2. This file.
3. `.agents/state/session_registry.md`.
4. `.agents/rules/module_permissions.md`.
5. `.agents/state/resource_locks.md`.
6. `.agents/state/current_progress.md`.
7. The handoff file for the assigned Role.
8. The lifecycle checklist for the current moment.

## Single Sources Of Truth

| State | Source |
| --- | --- |
| Active sessions and Role occupancy | `.agents/state/session_registry.md` |
| Shared resource locks | `.agents/state/resource_locks.md` |
| Project progress | `.agents/state/current_progress.md` |

Agent-specific entrypoints are thin doors only. They must not contain live status, active locks, or progress summaries.

## Role Summary

| Role | Purpose |
| --- | --- |
| `OPS/COORDINATION` | Coordination, operating docs, entrypoints, state, locks, handoff |
| `GAME_DESIGN` | Gameplay and system design documents |
| `LORE_ART` | Worldbuilding, narrative, art direction |
| `DATA_TECH` | Data, technical architecture, KPI, server/backend design |
| `UI_ASSETS` | UI design, mockups, diagrams, visual assets |

Role ownership is defined in `.agents/rules/module_permissions.md`.

## Default Behavior

- No assigned Role means read-only.
- A Role may freely edit only its owned paths.
- Shared resources require a lock in `.agents/state/resource_locks.md`.
- Sensitive resources require user confirmation.
- If a conflict or uncertainty appears, stop and report using `.agents/lifecycle/review_needed.md`.

## Coordinator And Workers

`COORDINATOR` sessions plan, distribute, check progress, detect conflicts, write task prompts, and review results. They do not directly edit project content unless assigned a Worker Role.

Worker sessions implement within their assigned Role and update only the shared state files needed by the lifecycle.

## Legacy Memory

Legacy memory notes were backed up under `.agents/backups/2026-05-12_0623/메모리/`. They are not live state. Treat them as archived references only.

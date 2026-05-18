# Agent Operating System

This directory is the reusable operating system for Codex, Claude Code, Gemini,
and any other AI agent working in a local project workspace.

The tracked files under `.agents/` should remain portable across projects. Put
project-specific paths, repository lists, roles, handoff notes, and temporary
cache data in the local overlay described below instead of hardcoding them into
the base rules.

## Mandatory Read Order

1. Agent entrypoint: `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`.
2. This file.
3. `.agents/rules/document_policy.md`.
4. `.agents/rules/module_permissions.md`.
5. `.agents/rules/domain_policy.md`.
6. `.agents/rules/commit_policy.md`.
7. Optional local overlay files under `.agents/project/`, if present.
8. `.agents/state/session_registry.md`.
9. `.agents/state/resource_locks.md`.
10. `.agents/state/current_progress.md`.
11. The handoff file for the assigned Role, if one exists.
12. The lifecycle checklist for the current moment.

If a required state or overlay file is missing, do not invent its contents.
Proceed with the safest default: read-only until the user assigns or approves a
Role and scope.

## Reusable Base Vs Local Overlay

| Area | Location | Git policy |
| --- | --- | --- |
| Portable agent rules | `.agents/rules/*.md` | Tracked |
| Portable lifecycle checklists | `.agents/lifecycle/*.md` | Tracked |
| Portable templates | `.agents/templates/*.md` | Tracked |
| Live coordination state | `.agents/state/*.md` | Project-specific; may be tracked only when this repository is intentionally used as the project control repo |
| Role handoff notes | `.agents/handoff/*.md` | Project-specific; keep concise |
| Local project overlay | `.agents/project/**` | Ignored by default |
| Generated or temporary cache | `.agents/cache/**` | Ignored by default |

Use `.agents/templates/project_overlay.md` as the starting point for a new
project overlay. The overlay is where a project can define:

- Project name and current scope.
- Canonical project roots and nested Git repositories.
- Role-to-path ownership for that project.
- Shared files that require locks.
- Domain-specific constraints such as Unity, backend, data, art, or document
  rules.
- Project-specific validation commands.

## Single Sources Of Truth

| State | Source |
| --- | --- |
| Active sessions and Role occupancy | `.agents/state/session_registry.md` |
| Shared resource locks | `.agents/state/resource_locks.md` |
| Project progress | `.agents/state/current_progress.md` |
| Project-specific static context | `.agents/project/**` |

Agent-specific entrypoints are thin doors only. They must not contain live
status, active locks, or progress summaries.

## Role Summary

The base system defines role naming conventions and semantics only. Concrete
owned paths belong in the project overlay or in
`.agents/rules/module_permissions.md` when this repository is intentionally
serving as a project-specific control repo.

Namespace implementation roles by work area so prompts stay unambiguous:
`PLAN_*`, `SERVER_*`, `CLIENT_*`, `SHARED_*`, `QA_*`, and `BUILD_*`.

| Role | Purpose |
| --- | --- |
| `OPS_COORDINATION` | Coordination, operating docs, entrypoints, state, locks, handoff |
| `INFRA_TOOLS` | Agent tooling, local automation, shared scripts, hooks |
| `PLAN_GAME_DESIGN` | Gameplay and system design documents |
| `PLAN_LORE_ART` | Worldbuilding, narrative, art direction, visual tone |
| `PLAN_DATA_TECH` | Data, technical architecture, KPI, server/backend design docs |
| `PLAN_UI_ASSETS` | UI design, mockups, diagrams, visual planning assets |
| `SERVER_*` | Server runtime implementation split by API/domain/data/validation |
| `CLIENT_*` | Client runtime implementation split by app/battle/network |
| `SHARED_*` | Shared libraries and contracts used by multiple runtimes |
| `QA_*` | Tests, fixtures, validation, and reproducibility checks |
| `BUILD_*` | Solution, package, CI, and build infrastructure |

## Default Behavior

- No assigned Role means read-only unless the user explicitly approves the
  current task scope.
- The registered Role is stable for the lifetime of the session. Ordinary task
  prompts may assign work, but they do not change the session Role.
- A Role may freely edit only its owned paths.
- Shared resources require a lock in `.agents/state/resource_locks.md`.
- Sensitive resources require user confirmation.
- If an incoming prompt conflicts with the registered Role, stop and report the
  conflict instead of silently switching roles.
- If a conflict or uncertainty appears, stop and report using
  `.agents/lifecycle/review_needed.md`.

## Coordinator And Workers

`COORDINATOR` sessions plan, distribute, check progress, detect conflicts, write
task prompts, and review results. They do not directly edit project content
unless assigned a Worker Role or explicitly approved by the user.

Worker sessions implement within their assigned Role and update only the shared
state files needed by the lifecycle.

## Legacy Memory

Legacy memory and imported notes are archived references only. They are not live
state. To make an archived note actionable, integrate only the needed next step
into the current project state or handoff file.

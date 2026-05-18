# Module Permissions

A session may freely edit only the paths owned by its assigned Role. Shared paths
require a lock. Sensitive paths require user confirmation even if a Role appears
related.

This file defines portable role behavior and naming conventions. Project-specific
path ownership should be supplied by the local overlay under `.agents/project/`,
especially `.agents/project/module_permissions.md` when present.

Use namespaced Role names for implementation work:

- `PLAN_*` for planning and design documents.
- `SERVER_*` for server implementation.
- `CLIENT_*` for client implementation.
- `SHARED_*` for shared libraries and contracts.
- `QA_*` for tests, fixtures, and validation.
- `BUILD_*` for solution, package, CI, and build infrastructure.

## Role Semantics

| Role | Typical responsibility |
| --- | --- |
| `OPS_COORDINATION` | Agent operating docs, entrypoints, lifecycle docs, state, locks, handoff |
| `INFRA_TOOLS` | Shared agent tooling, local automation, hooks, reusable scripts |
| `PLAN_GAME_DESIGN` | Gameplay rules, system design, balancing docs |
| `PLAN_LORE_ART` | Narrative, setting, art direction, visual tone |
| `PLAN_DATA_TECH` | Data architecture, technical architecture, backend/server docs, KPI |
| `PLAN_UI_ASSETS` | UI design, mockups, diagrams, visual planning assets |
| `SERVER_*` | Server runtime code, API, persistence, validation, backend tests |
| `CLIENT_*` | Client runtime code, UI integration, battle adapter, network client |
| `SHARED_*` | Shared libraries, contracts, DTO/schema, deterministic core logic |
| `QA_*` | Tests, fixtures, validation, reproducibility checks |
| `BUILD_*` | Solution, package, CI, and build infrastructure |

## Project Path Ownership

When `.agents/project/module_permissions.md` exists, treat it as the concrete
project ownership map. It should define:

- Role-to-path ownership.
- Shared files that require locks.
- Sensitive files that require explicit user confirmation.
- Cross-repository ownership notes when the workspace contains nested Git repos.

If no project ownership map exists, use these safe defaults:

- `OPS_COORDINATION` may edit tracked agent operating docs under `.agents/**`
  and root agent entrypoints after user approval.
- Runtime or project content is read-only until the user assigns a Role and
  scope.
- Cross-domain edits require an explicit lock plan or direct user approval.

## Role Lock Policy

- The Role recorded in `.agents/state/session_registry.md` is the authoritative
  Role for the active session.
- Ordinary task prompts may assign work inside that Role, but they do not change
  the Role itself.
- If a new prompt names a different Role from the registered Role, treat it as a
  role conflict. Do not follow the conflicting instruction; stop and report it
  to the coordinator or user.
- A Role change is valid only when all three conditions are true:
  1. the coordinator explicitly requests the Role change,
  2. the session registry is updated first,
  3. the new prompt matches the updated registry.
- When practical, prefer starting a new session over repurposing an existing
  session into a different Role.

## Shared Paths Requiring Lock

The project overlay should list concrete shared files. In the absence of an
overlay, treat the following categories as shared:

- Root project indexes and README files.
- Glossaries, roadmaps, milestone scope files, and architecture contracts.
- Files referenced by multiple roles as canonical source material.
- Cross-Role rewrites touching multiple owned areas.

## Sensitive Paths Requiring User Confirmation

- `.git/**`
- `.gitignore`
- Editor/runtime configuration such as `.vscode/**`, `.idea/**`, `.claude/**`,
  `.mcp.json`, and connector/plugin settings.
- Dependency caches, virtual environments, package manager lock rewrites, and
  generated outputs.
- Secrets, credentials, environment files, deployment files, production data, or
  external service settings.
- Binary asset replacement or bulk regenerated assets.

## Unassigned Sessions

If the session has no registered Role, it may read files and report findings
only unless the user explicitly approves the current task scope.

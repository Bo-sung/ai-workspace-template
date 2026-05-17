# Module Permissions

A session may freely edit only the paths owned by its assigned Role. Shared paths
require a lock. Sensitive paths require user confirmation even if a Role appears
related.

This file defines portable role behavior. Project-specific path ownership should
be supplied by the local overlay under `.agents/project/`, especially
`.agents/project/module_permissions.md` when present.

## Role Semantics

| Role | Typical responsibility |
| --- | --- |
| `OPS/COORDINATION` | Agent operating docs, entrypoints, lifecycle docs, state, locks, handoff |
| `INFRA` | Shared agent tooling, local automation, hooks, reusable scripts |
| `GAME_DESIGN` | Gameplay rules, system design, balancing docs |
| `LORE_ART` | Narrative, setting, art direction, visual tone |
| `DATA_TECH` | Data architecture, technical architecture, backend/server docs, KPI |
| `UI_ASSETS` | UI design, mockups, diagrams, visual assets |
| `CLIENT` | Client runtime code and client-specific assets |
| `SERVER` | Server runtime code, API, persistence, backend tests |

## Project Path Ownership

When `.agents/project/module_permissions.md` exists, treat it as the concrete
project ownership map. It should define:

- Role-to-path ownership.
- Shared files that require locks.
- Sensitive files that require explicit user confirmation.
- Cross-repository ownership notes when the workspace contains nested Git repos.

If no project ownership map exists, use these safe defaults:

- `OPS/COORDINATION` may edit tracked agent operating docs under `.agents/**`
  and root agent entrypoints after user approval.
- Runtime or project content is read-only until the user assigns a Role and
  scope.
- Cross-domain edits require an explicit lock plan or direct user approval.

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

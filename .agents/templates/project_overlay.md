# Project Overlay Template

Copy this template into `.agents/project/README.md` for each local project, then
fill in only the information that is specific to that project. The
`.agents/project/` folder is ignored by default so the reusable agent OS can move
between projects without carrying stale context.

## Project

- Name:
- Current phase:
- Primary workspace root:
- Notes:

## Repositories

| Name | Path | Purpose | Main branch | Development branch |
| --- | --- | --- | --- | --- |
| agent-os | `<absolute-or-workspace-relative-path>` | Reusable agent rules and tooling | `main` | `develop` |
| plan | `<path>` | Planning/design docs | `main` | `develop` |
| client | `<path>` | Client runtime | `main` | `develop` |
| server | `<path>` | Server runtime | `main` | `develop` |

## Roles And Owned Paths

| Role | Owned paths |
| --- | --- |
| `OPS_COORDINATION` |  |
| `INFRA_TOOLS` |  |
| `PLAN_GAME_DESIGN` |  |
| `PLAN_LORE_ART` |  |
| `PLAN_DATA_TECH` |  |
| `PLAN_UI_ASSETS` |  |
| `SHARED_BATTLE_CORE` |  |
| `SHARED_API_CONTRACT` |  |
| `SERVER_API` |  |
| `SERVER_DOMAIN` |  |
| `SERVER_DATA` |  |
| `SERVER_BATTLE_VALIDATION` |  |
| `CLIENT_APP` |  |
| `CLIENT_BATTLE_ADAPTER` |  |
| `CLIENT_NETWORK` |  |
| `QA_TEST` |  |
| `BUILD_INFRA` |  |

## Shared Paths Requiring Locks

- Add shared paths here.

## Sensitive Paths Requiring User Confirmation

- Add sensitive paths here.

## Domain Rules

- Add project-specific domain rules here.

## Validation Commands

| Scope | Command |
| --- | --- |
| Agent docs | `rg "<term>" .agents` |
| Client |  |
| Server |  |
| Planning docs |  |

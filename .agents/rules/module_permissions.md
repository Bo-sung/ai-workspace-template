# Module Permissions

A session may freely edit only the paths owned by its assigned Role. Shared paths require a lock. Sensitive paths require user confirmation even if a Role appears related.

> **Path note:** All project content lives under `Project/FrontierBastion_plan/`. The earlier versions of this file referenced these paths as if rooted at the repository root (e.g. `시스템/...`). All references below use the current layout.

## Roles And Owned Paths

| Role | Owned paths |
| --- | --- |
| `OPS/COORDINATION` | `.agents/**`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `Project/FrontierBastion_plan/PROJECT_QUICK_REFERENCE.md` |
| `INFRA` | `.shared-ai-tools/**` (worker CLI tooling, workers.yaml, prompts, docs). Does **not** include modifying `.shared-ai-tools/venvs/**` package contents — dependency changes require user confirmation. |
| `GAME_DESIGN` | `Project/FrontierBastion_plan/시스템/**` (excluding the DATA_TECH and UI_ASSETS paths listed below) |
| `LORE_ART` | `Project/FrontierBastion_plan/01_프로젝트_개요.md`, `Project/FrontierBastion_plan/02_세계관_및_설정.md`, `Project/FrontierBastion_plan/04_메카_및_적대_세력.md`, `Project/FrontierBastion_plan/05_비주얼_및_톤_가이드.md`, `Project/FrontierBastion_plan/Frontier_Bastion_기획서_원본.md` |
| `DATA_TECH` | `Project/FrontierBastion_plan/시스템/데이터 테이블.md`, `Project/FrontierBastion_plan/시스템/데이터 아키텍처.md`, `Project/FrontierBastion_plan/시스템/서버 아키텍처.md`, `Project/FrontierBastion_plan/시스템/기술 요구사항.md`, `Project/FrontierBastion_plan/시스템/KPI 지표.md` |
| `UI_ASSETS` | `Project/FrontierBastion_plan/시스템/UI 설계.md`, `Project/FrontierBastion_plan/assets/ui/**`, `Project/FrontierBastion_plan/assets/diagrams/**`, `Project/FrontierBastion_plan/assets/maps/**` |

`03_핵심_게임플레이.md` is co-owned by `GAME_DESIGN` and `LORE_ART`; treat it as a shared file requiring a lock.

## Shared Paths Requiring Lock

- `README.md` (repo root)
- `Project/FrontierBastion_plan/README.md`
- `Project/FrontierBastion_plan/프로젝트 목표.md`
- `Project/FrontierBastion_plan/용어 사전.md`
- `Project/FrontierBastion_plan/03_핵심_게임플레이.md`
- `Project/FrontierBastion_plan/시스템/개발 로드맵.md`
- `Project/FrontierBastion_plan/시스템/Phase 1 구현 범위.md`
- Cross-Role rewrites touching multiple owned areas
- Any file used as a canonical index, glossary, roadmap, or project-wide contract

## Sensitive Paths Requiring User Confirmation

- `.git/**`
- `.gitignore`
- `.claude/**`
- `.obsidian/**`
- `.vscode/**`
- `.trash/**`
- `.mcp.json` (repo root) — changes Claude Code runtime behavior on restart
- `.shared-ai-tools/venvs/**` (Python package contents — dependency changes only with user approval)
- Generated outputs or bulk regenerated assets
- Secrets, credentials, environment files, deployment files, or external service settings

## Unassigned Sessions

If the session has no registered Role, it may read files and report findings only.

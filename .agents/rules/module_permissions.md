# Module Permissions

A session may freely edit only the paths owned by its assigned Role. Shared paths require a lock. Sensitive paths require user confirmation even if a Role appears related.

## Roles And Owned Paths

| Role | Owned paths |
| --- | --- |
| `OPS/COORDINATION` | `.agents/**`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `PROJECT_QUICK_REFERENCE.md` |
| `GAME_DESIGN` | `시스템/게임 개요.md`, `시스템/게임 모드.md`, `시스템/핵심 컨텐츠.md`, `시스템/전투 메카닉.md`, `시스템/스테이지 시스템.md`, `시스템/적 시스템.md`, `시스템/스탯 시스템.md`, `시스템/스킬 시스템.md`, `시스템/영웅 시스템.md`, `시스템/영웅/**`, `시스템/영지 시스템.md`, `시스템/영지/**`, `시스템/장비 시스템.md`, `시스템/재화 시스템.md`, `시스템/재화 시스템_상세.md`, `시스템/진행 시스템.md`, `시스템/소셜 시스템.md`, `시스템/수익화 모델.md` |
| `LORE_ART` | `세계관 기획서.md`, `세계관/**`, `아트 방향성 기획서.md` |
| `DATA_TECH` | `시스템/데이터 테이블.md`, `시스템/데이터 아키텍처.md`, `시스템/서버 아키텍처.md`, `시스템/기술 요구사항.md`, `시스템/KPI 지표.md` |
| `UI_ASSETS` | `시스템/UI 설계.md`, `assets/ui/**`, `assets/diagrams/**`, `assets/maps/**` |

## Shared Paths Requiring Lock

- `README.md`
- `프로젝트 목표.md`
- `용어 사전.md`
- `시스템/개발 로드맵.md`
- Cross-Role rewrites touching multiple owned areas
- Any file used as a canonical index, glossary, roadmap, or project-wide contract

## Sensitive Paths Requiring User Confirmation

- `.git/**`
- `.gitignore`
- `.claude/**`
- `.obsidian/**`
- `.vscode/**`
- `.trash/**`
- Generated outputs or bulk regenerated assets
- Secrets, credentials, environment files, deployment files, or external service settings

## Unassigned Sessions

If the session has no registered Role, it may read files and report findings only.

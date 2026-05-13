# Project Quick Reference

## Repository

- Project root: `H:\Git\FantasyTowerDeffence_docs`
- Git root: `H:\Git\FantasyTowerDeffence_docs`
- Current branch at setup: `master`
- Remote: `origin git@github.com:Bo-sung/FantasyDeffence_Docs.git`
- Standard Git form: `git -C H:\Git\FantasyTowerDeffence_docs <command>`

## Start Here

1. Read your agent entrypoint: `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`.
2. Read `.agents/README.md`.
3. Read `.agents/state/session_registry.md`.
4. Read `.agents/rules/module_permissions.md`.
5. Read `.agents/state/resource_locks.md`.
6. Read `.agents/state/current_progress.md`.
7. Read only the handoff file for your Role.

## Single Sources Of Truth

- Active sessions and Role occupancy: `.agents/state/session_registry.md`
- Shared resource locks: `.agents/state/resource_locks.md`
- Project progress: `.agents/state/current_progress.md`

Do not duplicate current state in agent entrypoints, local agent memory, or ad hoc report files.

## Roles

- `OPS/COORDINATION`: agent operating documents, entrypoints, session state, locks, progress, handoff.
- `GAME_DESIGN`: gameplay and system design documents under `시스템/`.
- `LORE_ART`: worldbuilding, story, art direction, and narrative-facing terminology.
- `DATA_TECH`: data tables, technical architecture, server architecture, KPI, technical requirements.
- `UI_ASSETS`: UI design docs, UI mockups, diagrams, and visual assets.

Shared root documents such as `README.md`, `프로젝트 목표.md`, `용어 사전.md`, and `시스템/개발 로드맵.md` require a lock or user confirmation before editing.

## Legacy State Backup

Legacy memory notes formerly under `메모리/` were moved to `.agents/backups/2026-05-12_0623/메모리/`.

Those files are archival inputs only. They are not current progress, active session state, or active handoff until intentionally integrated into `.agents/state/current_progress.md` or a Role handoff.

## Sensitive Or Confirm-Before-Edit Areas

- `.git/**`
- `.claude/**`
- `.obsidian/**`
- `.vscode/**`
- `.trash/**`
- `.gitignore`
- Binary assets under `assets/**` when replacing or regenerating them
- Any generated files, deployment settings, secrets, credentials, or external environment configuration

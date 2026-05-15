# GAME_DESIGN Handoff

## Current State

- Role free. Next session to claim should register in `.agents/state/session_registry.md` before any edit.
- **Phase A 완료** (2026-05-16): SF 용어 매핑 확정 + Hub 5개 파일 적용 완료. 매핑 표는 `Project/FrontierBastion_plan/용어 사전.md` §SF 리테마 용어 매핑 참조.
- All system documents live under `Project/FrontierBastion_plan/시스템/`. The earlier `.agents/rules/module_permissions.md` rooted them at the repo root — that has been corrected on 2026-05-15.

## Active Mandate: SF Re-theme

The `시스템/` document set was migrated from the legacy `FantasyTowerDeffence_docs` repo. Combat structure (공방형 라인 디펜스, 부대 카드, Phase 1 스코프) is canonical and must be preserved. Terminology and flavor are still fantasy and must be re-skinned to match `Project/FrontierBastion_plan/Frontier_Bastion_기획서_원본.md` (SF 우주 변경 개척, 총독/파일럿/메카/식민지/침식체).

### Phase A — ✅ 완료 (2026-05-16)

용어 사전 매핑 확정 + Hub 5개 파일(전투 코어, 부대 카드 시스템, 파일럿 시스템, 핵심 컨텐츠, 스테이지 시스템) 적용 완료.

### Phase B — 다음 작업 (이전 Phase A 계획 유지) Suggested mappings to validate:
   - 영웅 → 파일럿 (Pilot)
   - 영지 → 식민지 / 전초기지 (Colony / Outpost)
   - 마나 → 에너지 / 지령 포인트 (Energy / Command Points) — pick one and stay consistent
   - 소환 유닛 → 산업 프레임 유닛 / 보조 유닛
   - 보스 → 침식체 변종 / 모선 (Variant / Mothership)
   - 적 군집 → 침식체 군집 (Husk Swarm)
   - MAG / RES → SF-flavored stat pair (e.g. 에너지 출력 / 차폐) — decide with DATA_TECH input
2. **Apply mapping to the first wave** of system docs (these are the player-facing core):
   - `시스템/게임 개요.md` — game name placeholder, theme, target audience line
   - `시스템/전투 코어.md`, `시스템/전투 메카닉.md` — stat names, mana terminology
   - `시스템/부대 카드 시스템.md` — pilot + frame unit pairing
   - `시스템/영웅 시스템.md` (rename concept to "파일럿 시스템" — decide whether to rename the file or just retitle inside)
   - `시스템/영지 시스템.md` (same — "식민지 시스템")
3. **Do not** rename file paths until the user confirms — file renames cascade through every cross-link in the doc set. Retitle inside the file first; queue the path rename as a separate task.

### Phase B — Propagation

After Phase A lands and the glossary is stable:

- `시스템/스킬 시스템.md`, `시스템/스탯 시스템.md`, `시스템/적 시스템.md`, `시스템/스테이지 시스템.md`
- `시스템/장비 시스템.md`, `시스템/재화 시스템.md`, `시스템/재화 시스템_상세.md`, `시스템/진행 시스템.md`
- `시스템/소셜 시스템.md`, `시스템/수익화 모델.md`
- `시스템/영웅/**`, `시스템/영지/**` subfolders

### Shared files (require a lock)

- `Project/FrontierBastion_plan/용어 사전.md`
- `Project/FrontierBastion_plan/03_핵심_게임플레이.md` (co-owned with LORE_ART)
- `Project/FrontierBastion_plan/시스템/Phase 1 구현 범위.md` (keep scope numbers stable — terminology only)
- `Project/FrontierBastion_plan/시스템/개발 로드맵.md`

### Out of scope for this Role

- Renaming files (queue as separate user-confirmed task).
- Changing Phase 1 scope, system counts, or mechanic numbers.
- Worldbuilding overview docs `01_…05_` — those belong to LORE_ART.
- Data table column names — coordinate with DATA_TECH before changing stat identifiers.

## Working Tips

- Read `.agents/rules/module_permissions.md` and `.agents/state/resource_locks.md` before each edit.
- Use the Tiered Reasoning Protocol (`.agents/rules/collaboration.md`) — bring an Expert Cloud Worker for any non-trivial mechanic reinterpretation; reserve local edits for terminology swaps and link fixes.
- Update `.agents/state/current_progress.md` at the end of each working block, not just at session end.

## Last Updated

2026-05-16T19:30:00+09:00 by `claude-20260516-1700-game-design-sf-retheme` (GAME_DESIGN).

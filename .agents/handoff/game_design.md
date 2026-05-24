# GAME_DESIGN Handoff

## Current State

- Role free. Next session to claim should register in `.agents/state/session_registry.md` before any edit.
- **Phase A 완료** (2026-05-16): SF 용어 매핑 확정 + Hub 5개 파일 적용 완료.
- **Phase B 완료** (2026-05-17): 21개 시스템 문서 SF 용어 전환 완료. 게임 개요, 전투 메카닉, 스탯/스킬/적/장비/재화/진행/게임모드 + 영웅·영지 서브폴더 전체. commit: `7eab547`
- **Glossary v2 normalized** (2026-05-17): 용어 사전 v2 SF 재정렬 완료. commit: `478d3ae`
- All system documents live under `Project/FrontierBastion_plan/시스템/`. The earlier `.agents/rules/module_permissions.md` rooted them at the repo root — that has been corrected on 2026-05-15.

## Active Mandate: SF Re-theme

The `시스템/` document set was migrated from the legacy `FantasyTowerDeffence_docs` repo. Combat structure (공방형 라인 디펜스, 부대 카드, Phase 1 스코프) is canonical and must be preserved. Terminology and flavor are still fantasy and must be re-skinned to match `Project/FrontierBastion_plan/Frontier_Bastion_기획서_원본.md` (SF 우주 변경 개척, 총독/파일럿/메카/식민지/침식체).

### Phase A — ✅ 완료 (2026-05-16)

용어 사전 매핑 확정 + Hub 5개 파일(전투 코어, 부대 카드 시스템, 파일럿 시스템, 핵심 컨텐츠, 스테이지 시스템) 적용 완료.

### Phase B — ✅ 완료 (2026-05-17)

21개 파일 SF 용어 전환 완료. 의도적 잔류: 마법사(역할명), 마법체(종족 분류 race=magic DATA_TECH 협의 필요), 파일명 내 `영웅`(링크 경로).

### Phase C — 다음 작업 후보 Suggested mappings to validate:
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

2026-05-17T02:00:00+09:00 by `claude-20260517-0000-game-design-sf-retheme-phaseB` (GAME_DESIGN).

## Combat Geometry / Projectile Addendum (2026-05-24)

- Phase 1 전장은 `지상 2 + 공중 1`로 고정한다.
- 지상 1라인과 지상 2라인의 기본 간격은 약 `200`이며, 이 값은 **클라 배치용 간격**이자 **코어 거리 계산용 간격**이다.
- 공중 라인은 지상 라인보다 훨씬 위에 둔다. 클라이언트는 가독성을 위해 라인 1/2/공중을 비틀린 이등변 삼각형 형태로 그릴 수 있지만, 이 렌더링은 시각화 전용이다.
- 같은 x 좌표라도 라인 간 물리 거리가 존재하므로, 근접 유닛의 타라인 공격이 막히는 이유는 "사거리가 닿지 않음"으로 설명한다.
- 원거리 공격은 투사체 기반이다. 근접은 즉시 판정, 원거리는 투사체 판정으로 분리한다.
- 교차 타격은 모든 원거리 유닛에 자동 허용하지 않는다. 유닛/스킬의 타겟 정책과 사거리를 동시에 만족해야 한다.
- 투사체가 교차 라인으로 이동하는 경우, 투사체는 **대상 라인**에 귀속된 것으로 취급한다.

### Follow-up

1. 전투 코어 문서의 거리/판정 규칙을 변경할 때는 `SHARED_BATTLE_CORE`와 동기화한다.
2. 시각화 배치나 라인 표현을 바꿀 때는 `스테이지 시스템.md`와 `전투 코어.md`의 용어를 먼저 맞춘다.
3. projectile speed, miss behavior, target snapshot 방식은 아직 확정하지 말고 `결정 필요`로 유지한다.
4. Phase 1 scope 숫자나 라인 수는 바꾸지 않는다.

# DATA_TECH Handoff

## Current State

- Role free. SF Re-theme DATA_TECH 1차 완료 (2026-05-17, commit `905dad5`).

## 완료된 작업

- `데이터 테이블.md`: 섹션 헤더·컬럼 설명 SF 전환 + **식별자 결정 사항 섹션** 추가
- `데이터 아키텍처.md`: 게임 타이틀 Frontier Bastion으로 변경, 영지→식민지 설명 전환
- `서버 아키텍처.md`: 게임 타이틀, Manor/Hero 모듈 한국어 레이블 전환
- `KPI 지표.md`: 영웅→파일럿, 은화→크레딧 전환

## 식별자 결정 사항 (동결 — Phase 1 착수 전 재검토)

| 식별자 | 결정 |
|--------|------|
| `hero_id`, `config_hero`, `user_hero` | 유지 (코드 미존재) |
| `manor_*` 테이블 접두사 | 유지 (GAME_DESIGN 협의 필요) |
| `base_mag`, `base_res`, `growth_mag`, `growth_res` | 유지, 설명에 빔 출력/차폐 병기 |
| `race` 컬럼 | 유지, SF 대안(bio_class/unit_type) GAME_DESIGN 협의 대기 |
| `CUR_SILVER`, `CUR_MANA`, `cost_silver` | 식별자 유지, 표시값(크레딧·레어메탈)만 변경 완료 |
| `damage_type: magical`, `stat_type: mag` | 유지 (구현 시 결정) |

## 미결 사항

- `race` SF 대안 확정 → GAME_DESIGN과 협의
- `hero`/`manor` 접두사 rename 로드맵 → Phase 1 코드 작성 전 확정
- `PROJECT_QUICK_REFERENCE.md`에 기존 미커밋 변경사항 있음 (OPS 소유 — 건드리지 않음)

## Next Session Notes

- Data tables, data architecture, technical requirements, server architecture, and KPI documents are owned by this Role.
- Any migration, production data, or secret-related work requires user confirmation.

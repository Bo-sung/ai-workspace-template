# BattleCore Handoff

## Current State

- Repo exists: `H:\Git\Portpolio\FrontierBastion\Project\FrontierBastion_battlecore`
- Role owner: `SHARED_BATTLE_CORE`
- Build-sensitive owner: `BUILD_INFRA`
- Branch model: Git Flow
- Branches: `main`, `develop`
- Current branch after setup: `develop`
- Initial commit: `ebc93d7` (`chore: scaffold BattleSim.Core repo`)

## Projectile Combat Addendum (2026-05-24)

### Decision Summary

- Phase 1 ranged combat should be **projectile-based**, not hitscan.
- Melee stays as immediate contact resolution.
- If a ranged attack crosses lanes, the projectile is spawned and simulated on the **target lane**.
- The lane model must keep 1D progress, but each lane also needs world start/end coordinates so projectile travel can be simulated deterministically.
- The two ground lanes should have a default world separation of about 200 so same-progress cross-lane distance is non-zero even when `x` aligns.

### Why This Matters

- Current `BattleSim.Core` ranged resolution subtracts HP on the fire tick.
- That makes ranged combat feel instantaneous and prevents visible travel time across lanes.
- The new line model is intended to support parallel ground lanes plus one air lane, so cross-lane projectile travel needs to be explicit in the core rather than implied by distance only.

### Required Core Changes

| Area | Required change |
| --- | --- |
| `LaneDefinition` | Add lane start/end world coordinates while keeping 1D progress |
| Combat resolution | Replace direct ranged HP subtraction with projectile spawn events |
| Projectile runtime model | Add projectile state: `source lane`, `projectile lane`, `source progress`, `target lane`, `target entity`, `damage snapshot`, `owner`, `ttl`, `speed` |
| Targeting rules | Same-lane melee stays immediate; ranged and cross-lane shots resolve by projectile arrival |
| Distance model | Include lane separation in cross-lane distance so melee-range units cannot cross-hit by default |
| Determinism | Snapshot damage/effects at fire time; bump `config_version` and refresh replay fixtures |

### Open Details For Core

- Exact miss behavior if the target becomes invalid before projectile arrival.
- Whether the projectile should resolve against a fire-time target snapshot or a live target position on the target lane.
- Exact collision radius / arrival threshold for projectile hit confirmation.

### Lock / Validation Impact

- `SHARED_BATTLE_CORE` lock is required.
- `SERVER_BATTLE_VALIDATION` golden fixtures will change.
- Client mirror work will be needed for projectile spawn / impact visuals and lane-aware rendering.

## Battle Support Upgrade Addendum (2026-06-01)

### Decision Summary

- Phase 1 has **no base defense weapons**, **no wall weapons**, and **no tower weapons**.
- The new combat support loop is a **stage-only temporary effect**, not a permanent meta upgrade.
- Support upgrades are purchased during the current stage battle by spending battle energy.
- Support upgrade tracks:
  - battle energy regen increase
  - battle energy max storage increase
  - pilot combat bonus for the current stage battle
- Each track can be upgraded up to **5 levels**.
- While a support upgrade is in progress, battle energy regeneration stops.
- The player is expected to survive the upgrade window by relying on stored battle energy and pilot direct deploy actions.

### Core Interpretation

- This is not a colony-level permanent stat increase.
- The effect must be treated as a **transient battle modifier** bound to the current stage battle.
- The modifier expires when the stage battle ends.
- If the core needs to serialize this state, it should live in battle runtime state or battle snapshot data, not in permanent account progression.

### Why This Matters

- The old tower-defense style interpretation is no longer valid for Phase 1 combat.
- Core logic and validation should not assume persistent base defense weapon upgrades.
- Client and server replay / validation need to agree on the same temporary support state so the battle remains deterministic.

### Required Core Changes

| Area | Required change |
| --- | --- |
| Battle state | Add a transient stage-battle support modifier state |
| Battle energy | Support upgrades pause regeneration while active |
| Pilot bonus | Apply only for the current stage battle, then clear on battle end |
| Persistence | Do not store as permanent colony progression |
| Validation | Include the support modifier in deterministic replay / golden fixtures if it affects outcomes |

### Open Details For Core

- Exact serialization shape for the transient support modifier.
- Whether the current support level is selected up front or can be progressed mid-battle via commands.
- Whether pilot combat bonus applies to direct deploy only or to linked drone squad stats as well.

### Lock / Validation Impact

- `SHARED_BATTLE_CORE` lock is required if the modifier enters core state or replay contracts.
- `SERVER_BATTLE_VALIDATION` fixtures may change if support state affects damage, regen, or deploy cadence.
- Client HUD must display the support level and the regen pause state clearly.

## API Skeleton Cleanup (sonnet-20260518-shared-battle-core-api-cleanup)

작성일: 2026-05-18 / Role: SHARED_BATTLE_CORE

### 변경한 타입 목록

| 파일 | 변경 내용 |
|---|---|
| `Config/LaneType.cs` (신규) | `enum LaneType { Ground=1, Air=2 }` |
| `State/OwnerSide.cs` (신규) | `enum OwnerSide { Player=1, Enemy=2 }` |
| `Config/LaneDefinition.cs` | `string LaneType` → `LaneType LaneType` |
| `State/BattleState.cs` (`BattleEntity`) | `string OwnerSide` → `OwnerSide OwnerSide` |
| `Config/BattleConfigSnapshot.cs` | `Slots` 프로퍼티 제거; `Lanes` 방어 복사 적용; 생성자 파라미터에서 `slots` 제거 |
| `State/BattleInitialState.cs` | `SlotDefinition[] Slots` 추가; 방어 복사; 생성자 파라미터에 `slots` 추가 |
| `FixedPoint/Fp.cs` | `ToString()` 음수 소수 버그 수정 |
| `tests/.../SimulatorTests.cs` | `MinimalConfig()`에서 slots 제거; `MinimalInitialState()` 헬퍼 추가; `LaneType.Ground` enum 사용; nullable pragma 추가 |
| `tests/.../FpTests.cs` | `ToStringNegativeFractional()` 테스트 케이스 추가 |

### 책임 경계 정리 결과

- `BattleConfigSnapshot`: 스테이지 레벨 고정 파라미터 전용. 에너지 경제, 파일럿 타이밍, 기지 HP, 최대 틱, 레인 정의.
- `BattleInitialState`: 전투별 플레이어 특정 데이터. 스테이지 ID, RNG 시드, **슬롯/덱 선택** (플레이어가 선택한 파일럿/드론/비용 스냅샷).
- `SlotDefinition`은 `Config` 네임스페이스에 그대로 유지하되, 프로퍼티는 `BattleInitialState`에서 보유. `BattleInitialState`가 `using BattleSim.Core.Config`를 참조함.

### Immutable/Read-Only 처리 방식

- `BattleConfigSnapshot.Lanes`: 생성자에서 `(LaneDefinition[])lanes.Clone()` 방어 복사.
- `BattleInitialState.Slots`: 생성자에서 `(SlotDefinition[])slots.Clone()` 방어 복사.
- `BattleState.Slots`, `BattleState.Lanes`, `LaneState.Entities`: `IReadOnlyList<T>` 유지 (기존).
- `SlotDefinition`, `LaneDefinition` 자체: `sealed` + `private set` 유지 — 원소 프로퍼티 변경 불가.

### Enum화한 항목

| 이전 | 이후 | 위치 |
|---|---|---|
| `string LaneType` ("ground"\|"air") | `LaneType LaneType` (Ground=1, Air=2) | `LaneDefinition` |
| `string OwnerSide` ("player"\|"enemy") | `OwnerSide OwnerSide` (Player=1, Enemy=2) | `BattleEntity` |

API/DB 문자열 인코딩은 Core 밖에서 처리.

### Fp.ToString() 수정

- 버그: `Fp.FromRaw(-5000).ToString()` → `"0.5000"` (부호 누락)
- 수정: absolute raw 기반으로 whole/frac 분리 후 부호 별도 적용
- 수정 후: `"-0.5000"` (올바름)
- 테스트 추가: `ToStringNegativeFractional()` — `-0.5000`, `-1.5000`, `0.5000`, `1.0000` 4개 케이스 검증

### Nullable 경고 처리

- CS8625 2건: `SpawnDroneSquad(0, 0, null)`과 `RecallPilot(0, 0, null)` — 둘 다 의도적 null 검증 테스트.
- 처리 방식: `#pragma warning disable/restore CS8625` + 인라인 주석으로 의도 명시 (PD-A 참조).
- Core 프로젝트 (`netstandard2.1`)에 nullable context 미도입 유지 — csproj 변경 금지 제약 준수.

### 테스트 결과

```
Fp tests passed.
RNG tests passed.
Simulator skeleton tests passed.
BattleSim.Core all checks passed.
```

빌드: 경고 0개, 오류 0개.

### 남은 PendingDecision

| ID | 항목 | 상태 |
|---|---|---|
| PD-A | `RecallPilot` lane_id 필수 여부 | 미결. `null` 허용 상태 유지 + pragma 문서화 |
| PD-B | `SelectLane` 독립 command 여부 | 미결 |
| PD-C | `ActivateSkill` Phase 1 포함 여부 | 미결 |
| PD-D | DeckSnapshot 저장 방식 | 미결 |
| PD-E | StageSnapshot 저장 방식 | 미결 |

### 다음 구현 작업 전 코디네이터 결정 필요

1. **RecallPilot.laneId (PD-A)** — 필수로 결정되면 `BattleCommand.RecallPilot` 파라미터 validation 추가, pragma 제거, `BattleCommand.LaneId`를 nullable/non-nullable로 확정.
2. **LaneType 추가값** — "ground"/"air" 외에 다른 레인 타입이 확정되면 `Config/LaneType.cs` 추가.
3. **Unity TargetFramework 확정** — Core csproj `netstandard2.1` 유지 여부. 확정되면 nullable context 도입 가능 여부 재검토.

## Structure

```text
BattleSim.Core.sln
Directory.Build.props
src/BattleSim.Core/
tests/BattleSim.Core.Tests/
fixtures/configs/
fixtures/input_logs/
fixtures/expected_results/
fixtures/seeds/
docs/
```

## Decisions Recorded

- BattleSim.Core is a separate repo, not nested under server or client.
- Target Framework is `.NET Standard 2.1` candidate only; final value is pending Unity compatibility confirmation.
- Package/versioning is not selected.
- Server/client reference style is not selected.
- Public API is intentionally minimal after scaffold: `BattleCoreDefaults` only.

## Validation

- `dotnet build BattleSim.Core.sln` passed with 0 warnings and 0 errors.
- `dotnet run --project tests\BattleSim.Core.Tests\BattleSim.Core.Tests.csproj --no-build` passed.

## Next Session Notes

- Expand command model, config model, fixed-point math, RNG, result model only after taking the shared BattleSim.Core lock.
- Choose deterministic RNG algorithm before gameplay logic depends on randomness.
- Choose package/versioning and server/client reference strategy before integration work.
- Activate persistent commit hook for this nested repo only after explicit user approval; the initial commit used the agent hook through one-shot `git -c core.hooksPath=...`.

---

## Fixed-Point / RNG 정책 후보 (sonnet-20260518-shared-battle-core-fp-rng-review)

작성일: 2026-05-18 / Role: SHARED_BATTLE_CORE / 읽기·보고 전용

### 추천안 요약

| 항목 | 추천 | 비고 |
|---|---|---|
| FixedPoint 노출 방식 | `Fp` readonly struct | 컴파일 타임 타입 안전, 힙 할당 없음 |
| 위치/거리 scale | 별도 정수 단위 (int milliunits) | fp10000 통일 시 의미 혼용 위험 |
| RNG 알고리즘 | Xoshiro256** | Unity 내부 채택, BigCrush 통과, 명세 공개 |
| 나눗셈 반올림 | 절삭 통일 (반올림은 명시적 메서드) | 암묵적 혼용 금지 |
| RNG 인스턴스 수 | 단일 (Phase 1) | 복수는 Phase 2 검토 |

### 구현 착수 전 필수 결정

- **FP-1**: Fp struct vs FpMath static — 결정 시 `src/BattleSim.Core/FixedPoint/` 구현 착수 가능
- **RNG-1**: 알고리즘 확정 — 결정 시 `src/BattleSim.Core/Rng/` 구현 착수 가능

### 오버플로우 경계 (확인됨)

- 일반 게임 수치 범위에서 `Fp * Fp` (`long * long / Scale`) 안전
- 위치 × 배율 혼합 계산은 별도 scale 분리로 회피 권장

자세한 내용: 채팅 세션 보고서 참조 (비교표, 구현 스케치, 테스트 항목 포함).

---

## Input Log & Replay Data Model 후보 (sonnet-20260518-shared-battle-core-input-replay-model)

작성일: 2026-05-18 / Role: SHARED_BATTLE_CORE / 검토 대상: SHARED_API_CONTRACT, QA_TEST
읽기·보고 전용. 파일 생성/편집 없음.

### 핵심 결론

- command_type 확정 후보: `spawn_drone_squad`, `deploy_pilot`, `recall_pilot` (3종)
- command_type 미결정: `activate_skill` (스킬 시스템 선행), `select_lane` (UI 흐름 선행)
- **DB 갭**: `battle_attempt.deck_hash`만으로는 full replay 덱 재구성 불가 → DeckSnapshot 별도 캡처 필요
- **DB 갭**: entry 시점 stage snapshot 미저장 → full replay 시 config_stage 버전 관리 또는 별도 테이블 필요
- B-lite 최소 필드: input_log 5컬럼 (tick, slot_index, command_type, lane_id, client_sequence) + envelope 6필드
- Full replay 추가 필드: DeckSnapshot, StageSnapshot, target_id, target_option

### 미결정 항목 요약

| ID | 항목 | 블로킹 |
|---|---|---|
| PD-A | recall_pilot 시 lane_id nullable 여부 | B-lite 검증 로직 |
| PD-B | select_lane 독립 command 여부 | command_type 최종 목록 |
| PD-C | activate_skill Phase 1 포함 여부 | command_type + target_option 스키마 |
| PD-D | DeckSnapshot 저장 방식 | Full replay + QA fixture 스키마 |
| PD-E | StageSnapshot 저장 방식 | Full replay |
| PD-F | target_option JSONB 스키마 | activate_skill 확정 후 |
| PD-G | battle_input_log 보관 기간 | 운영 정책 |

### API/DB 변경 필요 항목

- `battle_attempt`: deck_snapshot 컬럼 추가 또는 별도 테이블 (Full replay용)
- config_stage 버전 관리 방식 또는 battle_stage_snapshot 테이블 (Full replay용)
- `battle_input_log.lane_id`: nullable 허용 여부 결정 (recall_pilot 케이스)

자세한 내용: 채팅 세션 보고서 참조.

---

## API 초안 (sonnet-20260518-shared-battle-core-api-draft)

작성일: 2026-05-18 / Role: SHARED_BATTLE_CORE / 검토 대상: SHARED_API_CONTRACT, QA_TEST
읽기·보고 전용 세션 산출물. 파일 생성/편집 없음. 구현 착수 전 검토용.

---

### 1. API 설계 원칙

1. **Pure library** — Unity API (`MonoBehaviour`, `Time.deltaTime`, `UnityEngine.Random`), ASP.NET, DB 접근 금지. `.NET Standard 2.1` 범위 내 BCL만 의존.
2. **Deterministic** — 동일한 `BattleConfigSnapshot` + `BattleInitialState` + `BattleCommand[]` 시퀀스는 항상 동일한 `BattleResult`를 산출. 부동소수점 금지.
3. **Fixed-point** — 전투 판정에 영향을 주는 모든 수치는 scale 10000의 `long` 기반. 1.0 = 10000, 중간 계산 오버플로우는 `long` 산술로 방지.
4. **Tick-driven** — `AdvanceTick()` 1회 호출 = 50ms 진행. 호출 측(Unity/서버)이 tick 루프를 소유하고 Core는 한 tick만 처리.
5. **Command injection** — 플레이어 입력(`BattleCommand`)은 Core 내부에서 생성하지 않고 외부(클라이언트 UI/리플레이 로더)에서 주입. Core는 수동적인 상태 머신.
6. **Immutable snapshot** — `BattleConfigSnapshot`, `BattleInitialState`, `BattleResult`는 생성 후 변경 불가. `GetState()`는 불변 스냅샷을 반환.
7. **Replay-friendly** — `BattleReplayEnvelope`는 서버 B-lite 제출과 full deterministic replay 양쪽에 동일하게 사용. Core는 envelope을 파싱/검증하지 않으며, 파싱은 서버 `BattleValidation` 모듈의 책임.

---

### 2. C# Pseudo-code

```csharp
namespace BattleSim.Core
{
    // ──────────────────────────────────────────────────────────────
    // 이미 존재하는 상수 (BattleCoreDefaults.cs)
    // ──────────────────────────────────────────────────────────────
    public static class BattleCoreDefaults
    {
        public const int TickRate         = 20;       // TPS
        public const int TickMilliseconds = 50;       // ms per tick
        public const int FixedPointScale  = 10000;    // 1.0 = 10000
        public const int DeckSlotCount    = 5;        // 신규 제안
        public const string ValidationMode = "b_lite"; // 신규 제안
    }

    // ──────────────────────────────────────────────────────────────
    // BattleConfigSnapshot
    //   서버가 config_version 기준으로 발급. 전투 중 변경 불가.
    // ──────────────────────────────────────────────────────────────
    public sealed class BattleConfigSnapshot
    {
        public string ConfigVersion { get; init; }

        // 에너지 계열 (fp10000)
        public long InitialEnergy      { get; init; }
        public long MaxEnergy          { get; init; }
        public long EnergyRegenPerTick { get; init; }

        // 파일럿 출격 계열 (tick 단위; 기획 초 값을 서버가 변환해 전달)
        public int PilotDeployCooldownTick      { get; init; }
        public int PilotReturnCooldownTick      { get; init; }
        public int PilotKnockoutDroneResumeTick { get; init; }

        // 스테이지/라인 계열
        public long PlayerBaseInitialHp { get; init; } // fp10000
        public long EnemyBaseInitialHp  { get; init; } // fp10000
        public int  MaxBattleTick       { get; init; }

        // 슬롯별 드론 부대 비용 (length == DeckSlotCount)
        public long[] SlotEnergyCost   { get; init; }
        public int[]  SlotCooldownTick { get; init; }

        // ... 나머지 Config 테이블 필드는 스키마 확정 시 추가 ...
    }

    // ──────────────────────────────────────────────────────────────
    // BattleInitialState
    //   서버 battle_attempt 발급 응답에서 클라이언트가 조합.
    //   서버 full replay 시에도 동일 구조로 재구성.
    // ──────────────────────────────────────────────────────────────
    public sealed class BattleInitialState
    {
        public long   BattleAttemptId { get; init; }
        public string StageId         { get; init; }
        public string DeckHash        { get; init; }
        public long   RngSeed         { get; init; }

        public SlotDefinition[] Slots { get; init; } // length == DeckSlotCount
        public LaneDefinition[] Lanes { get; init; }
    }

    public sealed class SlotDefinition
    {
        public int    SlotIndex    { get; init; }
        public string PilotId     { get; init; }
        public string DroneSquadId { get; init; }
    }

    public sealed class LaneDefinition
    {
        public string LaneId   { get; init; }
        public string LaneType { get; init; } // "ground" | "air"
    }

    // ──────────────────────────────────────────────────────────────
    // BattleState
    //   GetState()가 반환하는 불변 스냅샷. 내부 가변 상태는 비공개.
    // ──────────────────────────────────────────────────────────────
    public sealed class BattleState
    {
        public int  CurrentTick    { get; init; }
        public long PlayerBaseHp   { get; init; } // fp10000
        public long EnemyBaseHp    { get; init; } // fp10000
        public long PlayerEnergy   { get; init; } // fp10000
        public bool IsTerminated   { get; init; }
        public BattleTerminationReason TerminationReason { get; init; }

        public IReadOnlyList<SlotState>   Slots { get; init; }
        public IReadOnlyList<LaneState>   Lanes { get; init; }
    }

    public enum BattleTerminationReason { None, PlayerBaseDestroyed, EnemyBaseDestroyed, TimeOut }

    public sealed class SlotState
    {
        public int  SlotIndex         { get; init; }
        public bool IsPilotDeployed   { get; init; }
        public bool IsPilotKnockedOut { get; init; }
        public int  DroneCooldownTick { get; init; }
        public int  PilotCooldownTick { get; init; }
    }

    public sealed class LaneState
    {
        public string LaneId { get; init; }
        public IReadOnlyList<BattleEntity> Entities { get; init; }
    }

    public sealed class BattleEntity
    {
        public string EntityId  { get; init; }
        public string OwnerSide { get; init; } // "player" | "enemy"
        public long   Hp        { get; init; } // fp10000
        // 위치 단위: PendingDecision (PD-03)
        public long   Position  { get; init; }
    }

    // ──────────────────────────────────────────────────────────────
    // CommandType  (최종 목록 PendingDecision PD-02)
    // ──────────────────────────────────────────────────────────────
    public enum CommandType
    {
        SpawnDroneSquad, // 확정 후보
        DeployPilot,     // 확정 후보
        RecallPilot,     // 확정 후보
        ActivateSkill,   // 스킬 시스템 확정 후 결정
        SelectLane,      // UI 흐름 확정 후 결정
    }

    // ──────────────────────────────────────────────────────────────
    // BattleCommand
    //   클라이언트 UI 또는 리플레이 로더가 주입하는 단일 명령.
    // ──────────────────────────────────────────────────────────────
    public sealed record BattleCommand(
        int         Tick,
        int         SlotIndex,
        string      LaneId,
        CommandType CommandType,
        string?     TargetId,
        string?     TargetOption,  // JSON 직렬화 문자열 (DB JSONB 대응)
        int         ClientSequence
    );

    // ──────────────────────────────────────────────────────────────
    // BattleInputLogEntry
    //   DB battle_input_log 행 C# 미러. string CommandType (DB VARCHAR 대응).
    // ──────────────────────────────────────────────────────────────
    public sealed record BattleInputLogEntry(
        int     Tick,
        int     SlotIndex,
        string  LaneId,
        string  CommandType,   // DB VARCHAR(30) 직접 대응
        string? TargetId,
        string? TargetOption,
        int     ClientSequence
    );

    // ──────────────────────────────────────────────────────────────
    // BattleResult
    //   DB battle_result 행과 1:1. "rejected"는 서버 전용이므로 미포함.
    // ──────────────────────────────────────────────────────────────
    public sealed record BattleResult(
        BattleOutcome Outcome,
        int           ClearTimeTick,
        long          PlayerBaseHpRatio, // fp10000
        long          EnemyBaseHpRatio,  // fp10000
        int           Stars              // 산출 공식 PendingDecision PD-07
    );

    public enum BattleOutcome { Victory, Defeat, Timeout }

    // ──────────────────────────────────────────────────────────────
    // BattleReplayEnvelope
    //   POST /api/battle/stage/clear body의 Core 쪽 표현.
    //   B-lite 및 future full replay 공용.
    //   JSON 키 명명 규칙 PendingDecision PD-06.
    // ──────────────────────────────────────────────────────────────
    public sealed class BattleReplayEnvelope
    {
        public string               ConfigVersion   { get; init; }
        public long                 RngSeed         { get; init; }
        public string               DeckHash        { get; init; }
        public string               StageId         { get; init; }
        public long                 BattleAttemptId { get; init; }
        public BattleInputLogEntry[] InputLog       { get; init; }
        public BattleResult         ResultClaim     { get; init; }
    }

    // ──────────────────────────────────────────────────────────────
    // IBattleRng  (알고리즘 PendingDecision PD-01)
    // ──────────────────────────────────────────────────────────────
    public interface IBattleRng
    {
        void Initialize(long seed);
        int  NextInt(int minInclusive, int maxExclusive);
        long NextLong(long minInclusive, long maxExclusive);
        // 후보: LCG / Xoshiro256** / PCG32
    }

    // ──────────────────────────────────────────────────────────────
    // BattleSimulator  (핵심 public surface)
    // ──────────────────────────────────────────────────────────────
    public sealed class BattleSimulator
    {
        public BattleSimulator(BattleConfigSnapshot config, BattleInitialState initial) { }

        public int  CurrentTick    { get; }
        public bool IsTerminated   { get; }

        // 이번 tick에 적용할 명령 주입 (Command.Tick == CurrentTick 이어야 함)
        public void SubmitCommand(BattleCommand command) { }

        // 1 tick 진행 (50ms). SubmitCommand 후 호출. 내부적으로 CurrentTick++.
        public void AdvanceTick() { }

        // 현재 상태 불변 스냅샷
        public BattleState GetState() { }

        // IsTerminated == true 일 때만 유효. 그 전 호출 시 InvalidOperationException.
        public BattleResult GetResult() { }

        // BattleReplayEnvelope 조립용 / 서버 검증 비교용
        public IReadOnlyList<BattleInputLogEntry> GetInputLog() { }
    }
}
```

---

### 3. 타입별 책임 표

| 타입 | 책임 | 생성자 | 소비자 |
|---|---|---|---|
| `BattleCoreDefaults` | Phase 1 상수 단일 출처 | — (static) | server, client, test |
| `BattleConfigSnapshot` | config_version 고정 수치 스냅샷. 전투 중 불변. | **server** | BattleSimulator, client |
| `BattleInitialState` | 전투 시작 조건(시드, 덱, 스테이지). 한 번만 주입. | **client** (서버 응답 조합) | BattleSimulator |
| `BattleState` | 특정 tick 시뮬레이션 상태 불변 스냅샷 | BattleSimulator 내부 | client (UI), server (replay 검증) |
| `BattleCommand` | 단일 플레이어 입력. enum CommandType 사용. | **client UI** or **replay loader** | BattleSimulator.SubmitCommand |
| `BattleInputLogEntry` | DB battle_input_log 행 mirror. string CommandType. | BattleSimulator 내부 | client (envelope 조립), server (B-lite) |
| `BattleResult` | 전투 최종 결과. 터미널 tick 상태에서 산출. | BattleSimulator 내부 | client (UI, ResultClaim), server (검증 기준) |
| `BattleReplayEnvelope` | B-lite 제출 및 future full replay 공용 컨테이너. | **client** (전투 종료 시 조립) | server BattleValidation 모듈 |
| `IBattleRng` | deterministic RNG 추상화. 구현 알고리즘 교체 가능. | Core 내부 | BattleSimulator (내부 only) |

---

### 4. Phase 1 확정값 반영 방식

| 확정 항목 | 반영 위치 | 방식 |
|---|---|---|
| TickRate = 20 TPS | `BattleCoreDefaults.TickRate` | 이미 존재 |
| TickMilliseconds = 50 | `BattleCoreDefaults.TickMilliseconds` | 이미 존재 |
| FixedPointScale = 10000 | `BattleCoreDefaults.FixedPointScale` | 이미 존재 |
| DeckSlotCount = 5 | `BattleCoreDefaults.DeckSlotCount` | 신규 제안 |
| ValidationMode = "b_lite" | `BattleCoreDefaults.ValidationMode` | 신규 제안 |
| 중간 계산 `long` | 모든 fp10000 수치 필드 타입 | `long`으로 선언 |
| 파일럿 직접 출격 에너지 미소모 | `BattleConfigSnapshot`에 파일럿 에너지 비용 필드 없음 | Config 구성으로 암시적 반영 |
| 격추 후 재출격 불가 | `SlotState.IsPilotKnockedOut` flag | AdvanceTick 내부 판정 |
| 시간 초과 승패 = HP 비율 비교 | `BattleResult.PlayerBaseHpRatio`, `EnemyBaseHpRatio` | `BattleOutcome.Timeout` + 비율 필드 |
| B-lite 검증 (Phase 1) | `BattleReplayEnvelope` 구조 | full replay 시에도 동일 envelope 재사용 가능하도록 설계 |

**기획 초 값 → tick 변환 규칙**: Config 테이블에 `pilot_deploy_cooldown_sec` 저장 → 서버가 `BattleConfigSnapshot` 조립 시 `tick = (int)(sec * TickRate)` 변환 → Core 내부는 tick 단위만 사용.

---

### 5. PendingDecision 목록

| ID | 항목 | 후보 | 블로킹 여부 |
|---|---|---|---|
| PD-01 | **RNG 알고리즘** | LCG / Xoshiro256** / PCG32 | **구현 블로킹** |
| PD-02 | **CommandType 최종 목록** | SpawnDroneSquad·DeployPilot·RecallPilot 확정 / ActivateSkill·SelectLane 논의 필요 | API contract 블로킹 |
| PD-03 | **위치/거리 fixed-point scale 통일** | A안: fp10000 동일 / B안: 별도 물리 단위 | **구현 블로킹** |
| PD-04 | **FixedPoint 타입 노출 방식** | A안: `long` raw / B안: `Fp` struct wrapper | API 안정성 |
| PD-05 | **Target Framework 최종값** | `.NET Standard 2.1` 후보 | 빌드 인프라 |
| PD-06 | **BattleReplayEnvelope JSON 키 명명** | snake_case vs PascalCase | API contract 블로킹 |
| PD-07 | **Stars 산출 공식** | 클리어 시간 / 피해 비율 / 고정 3성 등 | 기획 미확정 |
| PD-08 | **SelectLane 독립 command 여부** | A안: lane_id 포함 (현재 초안) / B안: SelectLane 별도 | CommandType 목록 연동 |
| PD-09 | **deterministic replay validation 범위** | B-lite only / 랭킹 차등 / 전체 | Phase 2+ 계획 |

---

### 6. Server / Client / API Contract 영향

**Server `BattleValidation` 모듈**
- `POST /api/battle/stage/clear` body → `BattleReplayEnvelope` 역직렬화 (PD-06 JSON 키 명명 연동)
- B-lite: `BattleAttemptId` 조회 → `DeckHash`/`ConfigVersion`/`RngSeed` 일치 → `InputLog` 유효성(tick 순서, slot 범위 0~4, command_type allowlist) → `ResultClaim` 범위 검증
- future full replay: `new BattleSimulator(config, initial)` → InputLog 순으로 SubmitCommand + AdvanceTick → GetResult()와 ResultClaim 비교

**Client `BattleAdapter` 모듈**
- `new BattleSimulator(config, initial)` → 매 tick마다 SubmitCommand → AdvanceTick → GetState() 렌더링
- Unity UI 이벤트 → BattleCommand 생성 → SubmitCommand (Core가 내부적으로 InputLogEntry 기록)
- IsTerminated 감지 → GetResult() + GetInputLog()로 BattleReplayEnvelope 조립 → clear API 호출

**API Contract (SHARED_API_CONTRACT 협의 필요)**
- `POST /api/battle/stage/enter` 응답 → 클라이언트가 BattleInitialState 조립
- `POST /api/battle/stage/clear` 요청 body = BattleReplayEnvelope 직렬화
- `BattleResult` 수치(fp10000 long)의 JSON 표현: int64 그대로 vs 정규화 float 선택 필요

**QA_TEST / fixtures**
- `fixtures/configs/` — BattleConfigSnapshot JSON (ConfigVersion별)
- `fixtures/input_logs/` — BattleInputLogEntry[] JSON
- `fixtures/expected_results/` — BattleResult JSON (동일 seed + config + log → 동일 result)
- `fixtures/seeds/` — BattleInitialState JSON (smoke test용)

---

### 7. Lock / 승인 필요 항목

**구현 단계 shared lock 대상**

| 리소스 | 사유 |
|---|---|
| `Project/FrontierBastion_battlecore/src/BattleSim.Core/**` | 공개 API 파일 신규 생성. server/client 양쪽 의존 |
| `Project/FrontierBastion_battlecore/fixtures/**` | QA_TEST와 동시 작업 시 충돌 가능 |
| `*.sln`, `*.csproj`, `Directory.Build.props` | Target Framework/패키지 변경 시 BUILD_INFRA 협의 필요 |

**코디네이터 질문 목록**

1. **RNG 알고리즘 결정 일정** — PD-01. 구현 착수 전 필수.
2. **CommandType 최종 목록 트랙** — PD-02. 스킬/타겟팅 담당 Role 확정 후 SHARED_API_CONTRACT와 동시 갱신.
3. **FixedPoint 타입 노출 방식** — PD-04. `Fp` struct 공개 시 server/client 양쪽 참조 방식(NuGet vs project reference)과 함께 결정.
4. **BattleReplayEnvelope JSON 키 명명** — PD-06. server DTO ↔ DB 컬럼명 ↔ C# 속성명 3방향 영향. API contract 확정 전 server/client 착수 불가.
5. **위치/거리 scale 결정 주체** — PD-03. 게임 디자인과 기술 양쪽 관여. 어느 Role이 주도?
6. **BattleCoreDefaults 신규 상수 추가 여부** — `DeckSlotCount`, `ValidationMode`. BUILD_INFRA 관점 ok 확인 필요.

**구현 착수 전 우선 결정 권장 항목**: PD-01(RNG) · PD-04(Fp 타입) · PD-06(JSON 키 명명) — 이 3개가 Core public API 타입 시그니처를 잠그는 데 직접 영향.

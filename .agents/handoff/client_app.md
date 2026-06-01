# CLIENT_APP Handoff

## Current State

- Role owner: `CLIENT_APP`
- Related plan docs already updated:
  - `Project/FrontierBastion_plan/시스템/전투 코어.md`
  - `Project/FrontierBastion_plan/시스템/전투 메카닉.md`
  - `Project/FrontierBastion_plan/시스템/스테이지 시스템.md`
  - `Project/FrontierBastion_plan/용어 사전.md`
- Related core handoff: `.agents/handoff/battlecore.md`

## Visual Layout Decision

- Phase 1 battlefield uses `지상 2 + 공중 1`.
- Client rendering should not collapse the two ground lanes onto the same y-position.
- Use a **skewed isosceles triangle projection** for readability:
  - line 1: upper ground lane
  - line 2: lower ground lane
  - air lane: much higher than both ground lanes
- Ground lane spacing starts at about `200`.
- The projection is visualization only. Core lane identity and combat rules remain authoritative.

## Combat Presentation Rules

- Melee attacks remain immediate on the source lane.
- Ranged attacks are projectile-based.
- Cross-lane projectile visuals should be spawned on the **target lane** path, matching the core rule.
- The client should show travel time, impact, and lane-specific arrival, even if the battle core resolves the actual hit deterministically.
- Projectile and impact effects should use world-space / `SpriteRenderer` style rendering, not large uGUI images for combat actors.

## Battle Support Upgrade Presentation (2026-06-01)

- Phase 1 has no base defense weapons, wall weapons, or tower weapons to render.
- The new battle support loop is a **current-stage temporary effect**, not a permanent colony upgrade.
- Only one support upgrade may run at a time.
- Time is specified at 20 TPS, so the client should display durations in seconds while keeping tick-based timing aligned with the core.
- The HUD should present support upgrades as battle-state information tied to the current run.
- Sync the latest `BattleSim.Core.dll` from support-upgrade commit `21db43e`.
- Mirror the new public API:
  - `BattleSupportTrack`
  - `BattleSideSupportState`
  - `BattleCommand.StartSupportUpgrade`
  - `BattleCommandType.StartSupportUpgrade`
  - `BattleEventType.SupportUpgradeStarted` / `SupportUpgradeCompleted`
  - `BattleEvent.SupportTrack` / `SupportLevel`
  - `BattleSideState.SupportState`
- The client should visibly show:
  - whether a resource upgrade is active
  - whether a pilot upgrade is active
  - the current support level
  - the remaining time for the active upgrade
  - whether battle energy regeneration is paused
  - whether pilot summoning is blocked
  - that the effect ends when the current stage battle ends
- Add UI commands for starting Resource/Pilot support upgrades.
- Prevalidate `DeployPilot` while Pilot upgrade is active so the player gets immediate feedback.
- Use `RecentEvents` for visual/UI feedback, especially `SupportUpgradeStarted` and `SupportUpgradeCompleted`.
- Do not infer support timing from energy deltas alone; use `SupportState` and `RecentEvents`.
- If support upgrades affect pilot combat bonuses, the client should reflect the bonus only inside the active battle and clear it on battle end.
- Do not present the support upgrade as a persistent base-building or tower-defense layer.

## Required Follow-up

1. Update any stage battle view / lane layout code to use distinct world positions for each lane.
2. Mirror projectile lane assignment from the core contract so cross-lane shots do not visually spawn on the wrong path.
3. Keep the client in sync with `BattleSim.Core` contract changes if projectile state fields are added or renamed.
4. Render support upgrade state in the battle HUD and clear it when the stage ends.
5. If the data contract changes, treat it as a shared-core dependency and coordinate with `SHARED_BATTLE_CORE`.

## Risks / Notes

- The old "two lanes overlapping visually" approach will confuse projectile and lane separation.
- Any future change to lane spacing must stay in sync with the core distance model.
- If the projectile snapshot / miss rule changes later, the client effect timing may need another pass.

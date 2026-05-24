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

## Required Follow-up

1. Update any stage battle view / lane layout code to use distinct world positions for each lane.
2. Mirror projectile lane assignment from the core contract so cross-lane shots do not visually spawn on the wrong path.
3. Keep the client in sync with `BattleSim.Core` contract changes if projectile state fields are added or renamed.
4. If the data contract changes, treat it as a shared-core dependency and coordinate with `SHARED_BATTLE_CORE`.

## Risks / Notes

- The old "two lanes overlapping visually" approach will confuse projectile and lane separation.
- Any future change to lane spacing must stay in sync with the core distance model.
- If the projectile snapshot / miss rule changes later, the client effect timing may need another pass.

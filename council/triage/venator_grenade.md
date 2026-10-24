# venator_grenade: triage of changes since CLEANBASE

Confidence: calculated, unvalidated (no sandbox results; no council/evidence/venator.json).

## What changed (silent, no changes line)
| # | Change | Verdict |
|---|---|---|
| 1 | Battle Vest moved ahead of Cultist Sacrifice (Vest 6.4k -> 4.0k, Cultist 4.8k -> 6.4k); gun 4.8k 4.8k -> 6.4k | MISTAKE |
Nothing else differs (items, notes, boxes, ability order identical).

## Section N comparison (council/triage/calc/venator_paths.txt)
Kit: grenade 35 + 1.0x EBaseWeaponDamageIncrease, Gutshot 60 + 0.7x, so the weapon-damage % (gun invest bonus 15% at 2.4k, 46% at 4.8k) is the build's ability damage. Battle Vest: +18% weapon damage, +7% fire rate (only above 65% HP), 18% bullet resist. Cultist: gun 4.8k (+31% invest bonus), +10% (+0.8/boon) weapon damage, +50 (+4/boon) HP, +1 charge, range/radius +12%, 170% bonus souls on an NPC (buff 160s, cooldown 270s).

| Window | V0 clean (Cultist first) | V1 current (Vest first) |
|---|---|---|
| 4.0k-4.8k (800 souls) | grenade 58, Gutshot 76, gun x1.23 | grenade 76 (58 under 65% HP), Gutshot 89, gun x1.51, 18% bullet resist: **V1 better** |
| 4.8k-6.4k (1,600 souls) | grenade 106, Gutshot 110, gun x1.71, +86 HP, Cultist farming/buff live | grenade 76 (58), Gutshot 89, gun x1.51 (x1.23 under 65% HP), +22% EHP vs bullets: **V0 better on damage and farm** |
| from 6.4k | identical | identical |
V2 (Extra Health before Cultist: gun 4.8k at 5.6k) and V3 (Vest before Monster Rounds) are dominated by V0 or V1 in each window.
Verdict: V0 has +39% grenade damage (+83% under 65% HP) for twice as long as V1's lead, plus earlier farming. That is a grenade build's main job, and the 4.8k default holds with no waiver. Restored V0.

Item roles (J): Battle Vest = damage (conditional) + bullet resist + regen, and stays in the build either way. Cultist = gun spike + farming + charge + ability range. The decision weighs both items over the whole window.

## Corrected progression (council/work/venator_grenade.js)
Early: High-Velocity Rounds, Close Quarters, Monster Rounds, Cultist Sacrifice, Battle Vest, Extra Health, Fortitude. Mid/Late/Counters/rich unchanged. Ability order unchanged: 1123141322443423.
Spikes: gun 4.8k @4.8k, health 4.8k @9.6k. walk1 FLAGS none, CHECK12 none, abtimeline gate PASS.

## Open mechanics questions, shown both ways
- Unlock vs ability-point queue: model A and model A strict give identical tiers at every checkpoint. Model B puts grenade T3 at 3.9k (vs 6.0k). Verdict is the same in all.
- 1-charge counting (F7): if 2+ charges are needed (Kieran's reading), Cultist's +1 charge, Extra Charge, Rapid Recharge and Recharging Rush act on the trap (2 charges from unlock) only. If 1-charge abilities count, they also act on the grenade (1 charge from T3), and Cultist at 4.8k gives the grenade a 2nd charge from T3 (6.0k A / 3.9k B) instead of from 6.4k. That only widens V0's lead. Mid items are valid under both readings.

## Model-only
That the invest bonus feeds EBaseWeaponDamageIncrease (INFERRED: both are weapon-damage %), whether Cultist's stats come from the buff, Cultist soul value, 100%-hit gun numbers, and resist as EHP. Scenario: council/sandbox/scenarios/venator_grenade_cultist_vs_vest.json (not run).

## Depends on item data that could change
Cultist (BaseAttackDamagePercent 10 + 0.8/boon, BonusSoulsPct 170, cooldown 270, duration 160), Battle Vest (18/7/18, 65% threshold), the WeaponMod invest table (4.8k = 46), grenade/Gutshot scaling, grenade T3 charge.

## Gate: PASSES, 0 blocking
UNRESOLVED (present before this proposal): THRESH_ITEM_NO_THRESHOLD_LINE Recharging Rush @19.2k. The proposal reason has the "Threshold:" line (200 in 3.5s needed vs ~1134 from the gun at 100% hits, 5.3 body hits). It enters `changes` only on apply, so it resolves on apply. RT_ITEMS is the export round-trip, which the gate ignores.

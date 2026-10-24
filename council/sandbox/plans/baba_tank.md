# baba_tank sandbox plan (Rizuhble's Iron Granny Baba)
Hero enum `Baba` (UNVERIFIED: internal id hero_baba exists in game data; Enum.TryParse falls back to Haze silently, check the setup log). Abilities (cast keys 1-4): 1=Threadsap, 2=Granny Long Legs, 3=Baba's Brew, 4=Feed The Birds.

Final 12 used in scenarios: Radiant Regeneration, Healing Booster, Healbane, Reactive Barrier, Torment Pulse, Fortitude, Spirit Snatch, Rapid Recharge, Superior Duration, Unstoppable, Boundless Spirit, Escalating Exposure

## Uncertain slots and substitutes
- Healbane: swap with Healing Booster, Extra Regen, Spirit Shielding and none. Why uncertain: Early slot sold; is anti-heal needed vs a build sustain item?
- Torment Pulse: swap with Healing Rite, Reactive Barrier, Fortitude and none. Why uncertain: Mid aura on tank; check with 5 enemies at close range

## Economy
Tanky melee-ish; Extra Regen first. Melee heavy via Granny Long Legs ground pound (75 +0.6 spirit).

## Early game checkpoints (cumulative souls with component refunds, from core order)
- 8k (8000 souls): Extra Charge, Spirit Strike, Radiant Regeneration, Healing Booster, Healbane
- 12k (9600 souls): Extra Charge, Spirit Strike, Radiant Regeneration, Healing Booster, Healbane, Reactive Barrier
- 20k (19200 souls): Extra Charge, Radiant Regeneration, Healing Booster, Healbane, Reactive Barrier, Torment Pulse, Fortitude, Spirit Snatch, Extra Spirit
- 30k (27200 souls): Radiant Regeneration, Healing Booster, Healbane, Reactive Barrier, Torment Pulse, Fortitude, Spirit Snatch, Rapid Recharge, Mystic Vulnerability, Superior Duration, Improved Spirit
- full (43200 souls): Radiant Regeneration, Healing Booster, Healbane, Reactive Barrier, Torment Pulse, Fortitude, Spirit Snatch, Rapid Recharge, Superior Duration, Unstoppable, Boundless Spirit, Escalating Exposure
Check at each: cooldowns back before next pass, health, damage, ammo (reload frequency), spike present. `baba_tank_early.txt`

## Rotation (per pass, 2 passes per block; fetch 350 before each)
- `cast 1 0.5`: Threadsap
- `cast 2 0.6`: Granny Long Legs (resists, melee lifesteal)
- `cast melee 1.2`: heavy melee pound (slow 50%)
- `cast 3 0.6`: Brew
- `cast melee 1.2`: heavy
- `cast 4 6.8`: ult channel
- `hold k s` = press-and-hold ability key (PLANNED op; scripts currently emit `cast k s`, which only presses 0.35s, so charge/perfect-window timings are NOT valid until hold exists).

## Conditions
- Accuracy sections: 100 x1, 50 x3 (counterbalanced order), 40 x1; plus 5 enemies at close range with accuracy 50 (shoot one), body/head mix `#@ headpct 25` for gun builds. Report if winner changes.
- Incoming gun+spirit damage on player: `hurtme 150` per pass now; planned `#@ incoming gun 40 spirit 20` per second.
- Enemy resist: swap file 1 has a resist section (bullet 20 / spirit 15) for shred/amp items.
- Stacks/charges: run rotation from 0 stacks, after 1 pass (1), after 3 passes (max) where kit stacks (see rotation).
- CC: `baba_tank_cc.txt` applies none/stun 1.5/slow/silence (`#@ cc`), with and without Unstoppable (stun cancels ult).

## Healing attribution (TEST_MATRIX section)
Heal sources from game data:
- kit: Granny Long Legs T3: +50% melee lifesteal
- kit: Torment Pulse (damage only)
- kit: Healing Booster/Tempo; Radiant/Mystic Regen; Fortitude
- item: Radiant Regeneration (HealingPerCast, Regeneration)
- item: Healing Booster (HealAmpCastPercent, HealAmpRegenPercent, BonusHealthRegen)
- item: Healbane (HealOnKill)
- regen: base regen, any Mystic/Radiant Regeneration and Fortitude out-of-combat only (do not count mid-fight).
Blocks (`baba_tank_heal.txt`): full, noheal_items, minus_Radiant Regeneration, minus_Healing Booster, minus_Healbane, only_Radiant Regeneration, only_Healing Booster, only_Healbane, cand_Extra Regen, cand_Healing Rite at HP 25/50/80% (2 reps at 25%, 1 at 50/80%).
Marginal effect of a slot item = full - minus_<item>, and only_<item> - noheal_items (baseline: kit + regen only). Never use raw hps. Needs per-source heal logging in the csv; else removal isolation above.

## Scenario files
- `/mnt/user-data/outputs/dwpkg2/scenarios/baba_tank_swap1.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/baba_tank_swap2.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/baba_tank_heal.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/baba_tank_early.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/baba_tank_cc.txt`

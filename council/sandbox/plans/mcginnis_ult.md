# mcginnis_ult sandbox plan (Rizuhble's Bombing Run McGinnis)
Hero enum `Forge` (UNVERIFIED: internal id hero_forge exists in game data; Enum.TryParse falls back to Haze silently, check the setup log). Abilities (cast keys 1-4): 1=Mini Turret, 2=Medicinal Specter, 3=Spectral Wall, 4=Heavy Barrage.

Final 12 used in scenarios: Enduring Speed, Stamina Mastery, Superior Cooldown, Escalating Exposure, Unstoppable, Boundless Spirit, Lightning Scroll, Superior Duration, Greater Expansion, Infuser, Diviner's Kevlar, Refresher

## Uncertain slots and substitutes
- Infuser: swap with Vampiric Burst, Healing Booster, Leech and none. Why uncertain: Late lifesteal imbue; barrage hits ~6/s so it could be great or a wasted T3. Imbue target: Heavy Barrage.
- Mystic Slow: swap with Slowing Hex, Mystic Vulnerability, Superior Duration and none. Why uncertain: Counter-sit mid slot sold for a counter; does a slow beat amp/duration for the barrage?

## Economy
Turrets and Barrage clear waves from range; Mini Turret does 50% to non-heroes so farm is average. Monster Rounds is the farm item (sold late). No Cultist needed unless lane lost (Extra Regen box).

## Early game checkpoints (cumulative souls with component refunds, from core order)
- 8k (8000 souls): Monster Rounds, Extra Spirit, Extra Stamina, Mystic Expansion, Compress Cooldown, Duration Extender, Enduring Speed
- 12k (12000 souls): Monster Rounds, Extra Spirit, Mystic Expansion, Compress Cooldown, Duration Extender, Enduring Speed, Stamina Mastery, Mystic Slow
- 20k (19200 souls): Monster Rounds, Mystic Expansion, Duration Extender, Enduring Speed, Stamina Mastery, Mystic Slow, Improved Spirit, Mystic Vulnerability, Superior Cooldown, Debuff Reducer, Spirit Lifesteal
- 30k (28800 souls): Monster Rounds, Mystic Expansion, Duration Extender, Enduring Speed, Stamina Mastery, Mystic Slow, Improved Spirit, Superior Cooldown, Spirit Lifesteal, Escalating Exposure, Unstoppable
- full (60000 souls): Monster Rounds, Enduring Speed, Stamina Mastery, Superior Cooldown, Escalating Exposure, Unstoppable, Boundless Spirit, Lightning Scroll, Superior Duration, Greater Expansion, Infuser, Diviner's Kevlar, Refresher
Check at each: cooldowns back before next pass, health, damage, ammo (reload frequency), spike present. `mcginnis_ult_early.txt`

## Rotation (per pass, 2 passes per block; fetch 350 before each)
- `cast 3 0.6`: wall first: T1 amp +20% damage on hit enemies, so it must land before the rockets
- `cast 1 0.5`: turret
- `cast 2 0.5`: specter (self regen)
- `cast 4 8.5`: Heavy Barrage 8s channel, you are slowed; stand still on target
- `fire 1.5`
- `hold k s` = press-and-hold ability key (PLANNED op; scripts currently emit `cast k s`, which only presses 0.35s, so charge/perfect-window timings are NOT valid until hold exists).

## Conditions
- Accuracy sections: 100 x1, 50 x3 (counterbalanced order), 40 x1; plus 5 enemies at close range with accuracy 50 (shoot one), body/head mix `#@ headpct 25` for gun builds. Report if winner changes.
- Incoming gun+spirit damage on player: `hurtme 150` per pass now; planned `#@ incoming gun 40 spirit 20` per second.
- Enemy resist: swap file 1 has a resist section (bullet 20 / spirit 15) for shred/amp items.
- Stacks/charges: run rotation from 0 stacks, after 1 pass (1), after 3 passes (max) where kit stacks (see rotation).
- CC: `mcginnis_ult_cc.txt` applies none/stun 1.5/slow/silence (`#@ cc`), with and without Unstoppable (channel cancel on stun/silence).

## Healing attribution (TEST_MATRIX section)
Heal sources from game data:
- kit: Medicinal Specter: 25 (+0.3x spirit) regen/s to allies incl. self, 6.5s; T3 +2% max HP regen and +3m radius
- item: Infuser (AbilityLifestealPercentHero, AbilityLifestealPercentHeroPassive)
- regen: base regen, any Mystic/Radiant Regeneration and Fortitude out-of-combat only (do not count mid-fight).
Blocks (`mcginnis_ult_heal.txt`): full, noheal_items, minus_Infuser, only_Infuser, cand_Vampiric Burst, cand_Healing Booster, cand_Leech at HP 25/50/80% (2 reps at 25%, 1 at 50/80%).
Marginal effect of a slot item = full - minus_<item>, and only_<item> - noheal_items (baseline: kit + regen only). Never use raw hps. Needs per-source heal logging in the csv; else removal isolation above.

## Scenario files
- `/mnt/user-data/outputs/dwpkg2/scenarios/mcginnis_ult_swap1.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/mcginnis_ult_swap2.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/mcginnis_ult_heal.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/mcginnis_ult_early.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/mcginnis_ult_cc.txt`

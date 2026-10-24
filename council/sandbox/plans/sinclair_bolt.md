# sinclair_bolt sandbox plan (Rizuhble's Abracadabolt Sinclair)
Hero enum `Magician` (UNVERIFIED: internal id hero_magician exists in game data; Enum.TryParse falls back to Haze silently, check the setup log). Abilities (cast keys 1-4): 1=Vexing Bolt, 2=Spectral Assistant, 3=Rabbit Hex, 4=Audience Participation.

Final 12 used in scenarios: Trophy Collector, Veil Walker, Rapid Recharge, Superior Duration, Tankbuster, Enchanter's Emblem, Greater Expansion, Diviner's Kevlar, Boundless Spirit, Vortex Web, Superior Cooldown, Spirit Burn

## Uncertain slots and substitutes
- Rapid Recharge: swap with Compress Cooldown, Extra Stamina, Superior Cooldown and none. Why uncertain: Mid cd item: stamina vs cd.
- Trophy Collector: swap with Sprint Boots, Enduring Speed, Veil Walker and none. Why uncertain: Build note: assists; economy item. Compare with farm.

## Economy
Caster farming via bolt+assistant on waves; Trophy Collector passive souls. Check 8k: Extra Spirit+Extra Charge+Mystic Burst.

## Early game checkpoints (cumulative souls with component refunds, from core order)
- 8k (6400 souls): Extra Charge, Mystic Burst, Improved Spirit, Duration Extender, Trophy Collector
- 12k (12000 souls): Mystic Burst, Improved Spirit, Duration Extender, Trophy Collector, Veil Walker, Rapid Recharge
- 20k (18400 souls): Improved Spirit, Trophy Collector, Veil Walker, Rapid Recharge, Mystic Expansion, Superior Duration, Tankbuster, Enchanter's Emblem
- 30k (28800 souls): Improved Spirit, Trophy Collector, Veil Walker, Rapid Recharge, Superior Duration, Tankbuster, Enchanter's Emblem, Greater Expansion, Compress Cooldown, Diviner's Kevlar
- full (48000 souls): Trophy Collector, Veil Walker, Rapid Recharge, Superior Duration, Tankbuster, Enchanter's Emblem, Greater Expansion, Diviner's Kevlar, Boundless Spirit, Vortex Web, Superior Cooldown, Spirit Burn
Check at each: cooldowns back before next pass, health, damage, ammo (reload frequency), spike present. `sinclair_bolt_early.txt`

## Rotation (per pass, 2 passes per block; fetch 350 before each)
- `cast 2 0.5`: Assistant first: it also fires Bolt copies (T3 +damage) and attacks whenever you fire
- `cast 3 0.5`: Rabbit Hex (damage amp +15%)
- `cast 1 0.5`: Bolt (damage rises with travel time: far target, up to 2s)
- `fire 2`: assistant fires with you
- `cast 4 0.1`: skip ult
- `hold k s` = press-and-hold ability key (PLANNED op; scripts currently emit `cast k s`, which only presses 0.35s, so charge/perfect-window timings are NOT valid until hold exists).

## Conditions
- Accuracy sections: 100 x1, 50 x3 (counterbalanced order), 40 x1; plus 5 enemies at close range with accuracy 50 (shoot one), body/head mix `#@ headpct 25` for gun builds. Report if winner changes.
- Incoming gun+spirit damage on player: `hurtme 150` per pass now; planned `#@ incoming gun 40 spirit 20` per second.
- Enemy resist: swap file 1 has a resist section (bullet 20 / spirit 15) for shred/amp items.
- Stacks/charges: run rotation from 0 stacks, after 1 pass (1), after 3 passes (max) where kit stacks (see rotation).
- CC: `sinclair_bolt_cc.txt` applies none/stun 1.5/slow/silence (`#@ cc`), with and without Unstoppable (stun).

## Healing attribution (TEST_MATRIX section)
Heal sources from game data:
- kit: none in kit
- item: Veil Walker (HealOnVeil)
- regen: base regen, any Mystic/Radiant Regeneration and Fortitude out-of-combat only (do not count mid-fight).
Blocks (`sinclair_bolt_heal.txt`): full, noheal_items, minus_Veil Walker, only_Veil Walker at HP 25/50/80% (2 reps at 25%, 1 at 50/80%).
Marginal effect of a slot item = full - minus_<item>, and only_<item> - noheal_items (baseline: kit + regen only). Never use raw hps. Needs per-source heal logging in the csv; else removal isolation above.

## Scenario files
- `/mnt/user-data/outputs/dwpkg2/scenarios/sinclair_bolt_swap1.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/sinclair_bolt_swap2.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/sinclair_bolt_heal.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/sinclair_bolt_early.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/sinclair_bolt_cc.txt`

# sinclair sandbox plan (Rizuhble's Rabbit Punch Sinclair)
Hero enum `Magician` (UNVERIFIED: internal id hero_magician exists in game data; Enum.TryParse falls back to Haze silently, check the setup log). Abilities (cast keys 1-4): 1=Vexing Bolt, 2=Spectral Assistant, 3=Rabbit Hex, 4=Audience Participation.

Final 12 used in scenarios: Cultist Sacrifice, Fortitude, Reactive Barrier, Enduring Speed, Shadow Weave, Superior Duration, Point Blank, Hollow Point, Crushing Fists, Arctic Blast, Alchemical Fire, Colossus

## Uncertain slots and substitutes
- Cultist Sacrifice: swap with Extra Regen, Healing Rite and none. Why uncertain: Needed? Melee Sinclair farms with punch; build has Cultist by 8:00.
- Hollow Point: swap with Hunter's Aura, Point Blank, Close Quarters and none. Why uncertain: Build names Hunter's Aura swap.

## Economy
Melee: farms OK with Stalker but Sinclair has weak clear; Cultist ~8:00 eats big camp. Check 8k: Monster Rounds+Extra Health+Stalker+Grit.

## Early game checkpoints (cumulative souls with component refunds, from core order)
- 8k (6400 souls): Extra Health, Stalker, Grit, Cultist Sacrifice
- 12k (11200 souls): Stalker, Cultist Sacrifice, Fortitude, Reactive Barrier, Melee Charge
- 20k (19200 souls): Stalker, Cultist Sacrifice, Fortitude, Reactive Barrier, Melee Charge, Enduring Speed, Shadow Weave, Superior Duration
- 30k (27200 souls): Stalker, Cultist Sacrifice, Fortitude, Reactive Barrier, Melee Charge, Enduring Speed, Shadow Weave, Superior Duration, Cold Front, Point Blank, Hollow Point
- full (45600 souls): Stalker, Cultist Sacrifice, Fortitude, Reactive Barrier, Enduring Speed, Shadow Weave, Superior Duration, Point Blank, Hollow Point, Crushing Fists, Arctic Blast, Alchemical Fire, Colossus
Check at each: cooldowns back before next pass, health, damage, ammo (reload frequency), spike present. `sinclair_early.txt`

## Rotation (per pass, 2 passes per block; fetch 350 before each)
- `cast 3 0.5`: Rabbit Hex first: rabbits take +15% damage, 2s duration, 0.9s detonation delay - melee INSIDE the window
- `cast melee 1.2`: heavy punch
- `cast melee 1.2`: heavy punch
- `cast 1 0.5`: Bolt
- `cast 2 0.5`: Assistant (reloads weapon; attacks when you fire)
- `fire 1.5`
- Note: Audience Participation copies enemy ult only after enemy casts: skipped.
- `hold k s` = press-and-hold ability key (PLANNED op; scripts currently emit `cast k s`, which only presses 0.35s, so charge/perfect-window timings are NOT valid until hold exists).

## Conditions
- Accuracy sections: 100 x1, 50 x3 (counterbalanced order), 40 x1; plus 5 enemies at close range with accuracy 50 (shoot one), body/head mix `#@ headpct 25` for gun builds. Report if winner changes.
- Incoming gun+spirit damage on player: `hurtme 150` per pass now; planned `#@ incoming gun 40 spirit 20` per second.
- Enemy resist: swap file 1 has a resist section (bullet 20 / spirit 15) for shred/amp items.
- Stacks/charges: run rotation from 0 stacks, after 1 pass (1), after 3 passes (max) where kit stacks (see rotation).
- CC: `sinclair_cc.txt` applies none/stun 1.5/slow/silence (`#@ cc`), with and without Unstoppable (stun before punch).

## Healing attribution (TEST_MATRIX section)
Heal sources from game data:
- kit: none in kit; Melee: Lifestrike swap, Restorative
- regen: base regen, any Mystic/Radiant Regeneration and Fortitude out-of-combat only (do not count mid-fight).
Blocks (`sinclair_heal.txt`): full, noheal_items, cand_Extra Regen, cand_Healing Rite at HP 25/50/80% (2 reps at 25%, 1 at 50/80%).
Marginal effect of a slot item = full - minus_<item>, and only_<item> - noheal_items (baseline: kit + regen only). Never use raw hps. Needs per-source heal logging in the csv; else removal isolation above.

## Scenario files
- `/mnt/user-data/outputs/dwpkg2/scenarios/sinclair_swap1.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/sinclair_swap2.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/sinclair_heal.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/sinclair_early.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/sinclair_cc.txt`

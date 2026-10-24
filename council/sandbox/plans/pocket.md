# pocket sandbox plan (Rizuhble's Pocket Sized War Crimes)
Hero enum `Synth` (UNVERIFIED: internal id hero_synth exists in game data; Enum.TryParse falls back to Haze silently, check the setup log). Abilities (cast keys 1-4): 1=Barrage, 2=Flying Cloak, 3=Enchanter's Satchel, 4=Affliction.

Final 12 used in scenarios: Battle Vest, Cultist Sacrifice, Swift Striker, Tankbuster, Majestic Leap, Superior Cooldown, Dispel Magic, Spirit Burn, Superior Duration, Greater Expansion, Ethereal Shift, Diviner's Kevlar

## Uncertain slots and substitutes
- Restorative Shot: swap with Healing Booster, Extra Regen, Melee Lifesteal and none. Why uncertain: Shotgun hero: bought first, sold for Kevlar. Does it still pay at low HP?
- Battle Vest: swap with Extra Health, Grit, Reactive Barrier and none. Why uncertain: Early armor; sold in rich box. Pocket is squishy.

## Economy
Pocket farms badly: Cultist Sacrifice ~8:00 (in build) + Majestic Leap/Warp Stone. Plan: 8k Restorative Shot+Monster Rounds+Battle Vest+Mystic Burst (7.2k) then Cultist before 8:00; check clear speed with Affliction/Barrage on waves.

## Early game checkpoints (cumulative souls with component refunds, from core order)
- 8k (8000 souls): Restorative Shot, Battle Vest, Mystic Burst, Cultist Sacrifice, Swift Striker
- 12k (12000 souls): Restorative Shot, Battle Vest, Cultist Sacrifice, Swift Striker, Compress Cooldown, Tankbuster
- 20k (17600 souls): Restorative Shot, Battle Vest, Cultist Sacrifice, Swift Striker, Tankbuster, Majestic Leap, Mystic Expansion, Superior Cooldown
- 30k (28800 souls): Restorative Shot, Battle Vest, Cultist Sacrifice, Swift Striker, Tankbuster, Majestic Leap, Mystic Expansion, Superior Cooldown, Dispel Magic, Duration Extender, Spirit Burn
- full (45600 souls): Restorative Shot, Battle Vest, Cultist Sacrifice, Swift Striker, Tankbuster, Majestic Leap, Superior Cooldown, Dispel Magic, Spirit Burn, Superior Duration, Greater Expansion, Ethereal Shift, Diviner's Kevlar
Check at each: cooldowns back before next pass, health, damage, ammo (reload frequency), spike present. `pocket_early.txt`

## Rotation (per pass, 2 passes per block; fetch 350 before each)
- `cast 4 0.8`: Affliction first: DOT on all in 9m (no item procs, non-lethal); T3 blocks enemy healing
- `cast 1 2.2`: Barrage channel 2s: hit heroes stack damage amp 6%/stack (15s) - before gun
- `fire 1.5`: shotgun close
- `cast 2 0.4`: Flying Cloak (T2 +weapon damage 6s) then teleport
- `cast 3 1.6`: Enchanter's Satchel: escape, damage on end
- `fire 1`
- `hold k s` = press-and-hold ability key (PLANNED op; scripts currently emit `cast k s`, which only presses 0.35s, so charge/perfect-window timings are NOT valid until hold exists).

## Conditions
- Accuracy sections: 100 x1, 50 x3 (counterbalanced order), 40 x1; plus 5 enemies at close range with accuracy 50 (shoot one), body/head mix `#@ headpct 25` for gun builds. Report if winner changes.
- Incoming gun+spirit damage on player: `hurtme 150` per pass now; planned `#@ incoming gun 40 spirit 20` per second.
- Enemy resist: swap file 1 has a resist section (bullet 20 / spirit 15) for shred/amp items.
- Stacks/charges: run rotation from 0 stacks, after 1 pass (1), after 3 passes (max) where kit stacks (see rotation).
- CC: `pocket_cc.txt` applies none/stun 1.5/slow/silence (`#@ cc`), with and without Unstoppable (stuns cancel Barrage and ult (Affliction channel 0.6)).

## Healing attribution (TEST_MATRIX section)
Heal sources from game data:
- kit: none in kit (Affliction removes enemy healing)
- kit: Restorative Shot (heals on hit), Cultist hp regen
- regen: base regen, any Mystic/Radiant Regeneration and Fortitude out-of-combat only (do not count mid-fight).
Blocks (`pocket_heal.txt`): full, noheal_items, cand_Restorative Shot, cand_Healing Booster, cand_Extra Regen at HP 25/50/80% (2 reps at 25%, 1 at 50/80%).
Marginal effect of a slot item = full - minus_<item>, and only_<item> - noheal_items (baseline: kit + regen only). Never use raw hps. Needs per-source heal logging in the csv; else removal isolation above.

## Scenario files
- `/mnt/user-data/outputs/dwpkg2/scenarios/pocket_swap1.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/pocket_swap2.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/pocket_heal.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/pocket_early.txt`
- `/mnt/user-data/outputs/dwpkg2/scenarios/pocket_cc.txt`
